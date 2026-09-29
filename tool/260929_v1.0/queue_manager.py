"""
공정 회전 큐 및 영속성 관리 모듈 (queue_manager.py)
"""

import json
import os
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

class QueueManager:
    def __init__(self, data_file: str, seed_file: str):
        self.data_file = data_file
        self.seed_file = seed_file
        self.lock = threading.Lock()
        self.ip_last_copy_time: Dict[str, datetime] = {}
        self.load_data()

    def load_data(self):
        with self.lock:
            if os.path.exists(self.data_file):
                try:
                    with open(self.data_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        self.apps = data.get("apps", [])
                        self.referrals = data.get("referrals", [])
                        return
                except Exception as e:
                    print(f"[경고] 저장된 데이터 로드 실패, 시드 파일로 복구: {e}")

            # 시드 파일에서 초기화
            if os.path.exists(self.seed_file):
                with open(self.seed_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.apps = data.get("apps", [])
                    self.referrals = data.get("referrals", [])
                    self.save_data_unlocked()
            else:
                self.apps = []
                self.referrals = []

    def save_data_unlocked(self):
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump({
                    "apps": self.apps,
                    "referrals": self.referrals
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[오류] 데이터 저장 실패: {e}")

    def get_apps(self) -> List[Dict[str, Any]]:
        with self.lock:
            # 각 앱별 등록된 추천인 수 및 현재 1위 정보 첨부
            enriched = []
            for app in self.apps:
                app_refs = [r for r in self.referrals if r["app_id"] == app["id"]]
                item = dict(app)
                item["total_codes"] = len(app_refs)
                item["has_active"] = len(app_refs) > 0
                item["top_code"] = app_refs[0]["code"] if app_refs else None
                enriched.append(item)
            return enriched

    def get_app_detail(self, app_id: str) -> Optional[Dict[str, Any]]:
        with self.lock:
            app = next((a for a in self.apps if a["id"] == app_id), None)
            if not app:
                return None

            app_refs = [r for r in self.referrals if r["app_id"] == app_id]
            current_top = None
            waiting_list = []

            for idx, ref in enumerate(app_refs):
                ref_item = {
                    "id": ref["id"],
                    "code": ref["code"],
                    "nickname": ref["nickname"],
                    "copy_count": ref.get("copy_count", 0),
                    "created_at": ref.get("created_at"),
                    "last_copied_at": ref.get("last_copied_at"),
                    "cooldown_until": ref.get("cooldown_until"),
                    "queue_order": idx + 1,
                    "status": "CURRENT_TOP" if idx == 0 else "WAITING"
                }
                if idx == 0:
                    current_top = ref_item
                else:
                    # 대기자는 개인정보 마스킹 (예: '초코러버' -> '초코**')
                    nick = ref["nickname"]
                    masked_nick = nick[:2] + "**" if len(nick) > 2 else nick[:1] + "*"
                    masked_code = ref["code"][:4] + "****" if len(ref["code"]) > 4 else "****"
                    ref_item["masked_nickname"] = masked_nick
                    ref_item["masked_code"] = masked_code
                    waiting_list.append(ref_item)

            return {
                "app": app,
                "current_top": current_top,
                "queue_length": len(app_refs),
                "waiting_list": waiting_list
            }

    def copy_referral_code(self, app_id: str, code_id: str, client_ip: str) -> Dict[str, Any]:
        with self.lock:
            now = datetime.now()

            # 1. 어뷰징 방지: IP당 3초 내 연속 복사 차단
            if client_ip in self.ip_last_copy_time:
                diff = (now - self.ip_last_copy_time[client_ip]).total_seconds()
                if diff < 3:
                    return {
                        "success": False,
                        "error": "RATE_LIMIT",
                        "message": f"잠시 후 다시 시도해 주세요. ({int(3 - diff) + 1}초 대기)"
                    }
            self.ip_last_copy_time[client_ip] = now

            # 2. 해당 앱의 큐 추출
            app_refs = [r for r in self.referrals if r["app_id"] == app_id]
            if not app_refs:
                return {
                    "success": False,
                    "error": "NO_CODES",
                    "message": "등록된 추천인 코드가 없습니다."
                }

            top_ref = app_refs[0]
            if top_ref["id"] != code_id:
                # 이미 다른 사용자에 의해 순번이 변경되었을 경우
                return {
                    "success": True,
                    "already_rotated": True,
                    "copied_code": top_ref["code"],
                    "message": "순번이 새로 갱신되어 최우선 추천인 코드를 복사했습니다."
                }

            # 3. 큐 회전 (Baton Touch)
            # 전체 referrals 목록에서 top_ref를 찾아 맨 뒤로 이동
            self.referrals.remove(top_ref)
            top_ref["copy_count"] = top_ref.get("copy_count", 0) + 1
            top_ref["last_copied_at"] = now.isoformat()
            top_ref["cooldown_until"] = (now + timedelta(minutes=10)).isoformat()
            
            # 같은 app_id를 가진 항목들 중 가장 뒤에 배치
            # 타 앱 항목들의 순서를 교란하지 않도록 app_id 필터링 후 재조립
            other_apps_refs = [r for r in self.referrals if r["app_id"] != app_id]
            this_app_refs = [r for r in self.referrals if r["app_id"] == app_id]
            this_app_refs.append(top_ref)

            self.referrals = other_apps_refs + this_app_refs
            self.save_data_unlocked()

            next_top = this_app_refs[0] if this_app_refs else None

            return {
                "success": True,
                "copied_code": top_ref["code"],
                "registrant": top_ref["nickname"],
                "total_copies": top_ref["copy_count"],
                "next_top_nickname": next_top["nickname"] if next_top else None,
                "message": f"[{top_ref['nickname']}] 님의 추천코드가 복사되었습니다! 다음 대기자에게 순서가 양도되었습니다."
            }

    def register_code(self, app_id: str, code: str, nickname: str) -> Dict[str, Any]:
        with self.lock:
            code = code.strip().upper()
            nickname = nickname.strip()

            if not code or not nickname:
                return {"success": False, "message": "추천인 코드와 닉네임을 모두 입력해 주세요."}

            app = next((a for a in self.apps if a["id"] == app_id), None)
            if not app:
                return {"success": False, "message": "존재하지 않는 서비스입니다."}

            # 중복 코드 검사 (동일 앱 내 동일 코드 금지)
            existing = [r for r in self.referrals if r["app_id"] == app_id and r["code"] == code]
            if existing:
                return {"success": False, "message": "이미 등록되어 있는 추천인 코드입니다."}

            new_id = f"ref_{app_id}_{int(datetime.now().timestamp() * 1000)}"
            new_item = {
                "id": new_id,
                "app_id": app_id,
                "code": code,
                "nickname": nickname,
                "created_at": datetime.now().isoformat(),
                "copy_count": 0,
                "last_copied_at": None,
                "cooldown_until": None,
                "status": "ACTIVE"
            }

            self.referrals.append(new_item)
            self.save_data_unlocked()

            # 현재 몇 번째 대기 순번인지 계산
            app_queue = [r for r in self.referrals if r["app_id"] == app_id]
            assigned_order = len(app_queue)

            return {
                "success": True,
                "code_id": new_id,
                "assigned_order": assigned_order,
                "message": f"성공적으로 등록되었습니다! 현재 대기 순번: {assigned_order}순위"
            }

    def register_new_app(self, name_ko: str, name_en: str, category: str, description: str = "", app_url: str = "") -> Dict[str, Any]:
        with self.lock:
            name_ko = name_ko.strip()
            name_en = name_en.strip() or name_ko
            category = category.strip() or "기타/서비스"

            if not name_ko:
                return {"success": False, "message": "앱 이름을 입력해 주세요."}

            # 중복 체크
            if any(a["name_ko"].lower() == name_ko.lower() for a in self.apps):
                return {"success": False, "message": "이미 등록되어 있는 앱입니다."}

            import re
            slug = re.sub(r'[^a-zA-Z0-9]', '', name_en).lower()
            if not slug or any(a["id"] == slug for a in self.apps):
                slug = f"app_{int(datetime.now().timestamp())}"

            new_app = {
                "id": slug,
                "name_ko": name_ko,
                "name_en": name_en,
                "aliases": [name_ko, name_en],
                "category": category,
                "description": description or f"{name_ko} 회원가입 및 추천인 혜택",
                "app_url": app_url or "#",
                "icon_color": "#4f46e5"
            }

            self.apps.append(new_app)
            self.save_data_unlocked()

            return {
                "success": True,
                "app": new_app,
                "message": f"'{name_ko}' 앱이 성공적으로 등록되었습니다!"
            }
