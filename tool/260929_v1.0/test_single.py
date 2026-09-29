"""
단일 케이스 기본 동작 검증 스크립트 (test_single.py)
1. 한글 초성 분해 및 다국어 자동완성 검색 알고리즘 검증
2. 선입선출(FIFO) 회전 큐 및 바통 터치 로직 검증
"""

import sys
from datetime import datetime, timedelta

# --- 1. 한글 초성 분해 엔진 ---
CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
    'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

def extract_chosung(text: str) -> str:
    """한글 음절에서 초성을 추출하고, 영문/숫자는 소문자로 유지"""
    result = []
    for char in text:
        code = ord(char)
        if 0xAC00 <= code <= 0xD7A3:  # 완성형 한글 범위
            chosung_idx = (code - 0xAC00) // (21 * 28)
            result.append(CHOSUNG_LIST[chosung_idx])
        else:
            result.append(char.lower())
    return "".join(result)

def match_query(target_text: str, query: str) -> bool:
    """영문, 부분 한글, 초성 일치 여부를 종합 판별"""
    q = query.strip().lower()
    t = target_text.lower()
    if not q:
        return False
    # 1. 일반 부분 일치 (영문, 한글 완성형)
    if q in t:
        return True
    # 2. 초성 일치 판별
    target_chosung = extract_chosung(target_text)
    if q in target_chosung:
        return True
    return False

# --- 2. 선입선출(FIFO) 회전 큐 매니저 ---
class FairQueue:
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.queue = []

    def add_code(self, code_id: str, code: str, nickname: str):
        item = {
            "id": code_id,
            "code": code,
            "nickname": nickname,
            "copy_count": 0,
            "last_copied_at": None,
            "cooldown_until": None
        }
        self.queue.append(item)
        return len(self.queue)

    def get_current_top(self):
        if not self.queue:
            return None
        return self.queue[0]

    def trigger_copy(self, code_id: str, cooldown_minutes: int = 10):
        if not self.queue:
            return None
        if self.queue[0]["id"] != code_id:
            raise ValueError(f"현재 1순위 코드가 아닙니다. (요청 ID: {code_id}, 현재 1위: {self.queue[0]['id']})")
        
        # 1. 1순위 코드 꺼내기
        current = self.queue.pop(0)
        now = datetime.now()
        current["copy_count"] += 1
        current["last_copied_at"] = now.isoformat()
        current["cooldown_until"] = (now + timedelta(minutes=cooldown_minutes)).isoformat()
        
        # 2. 큐의 맨 뒤로 회전 (바통 터치)
        self.queue.append(current)
        
        next_top = self.get_current_top()
        return current, next_top

def run_tests():
    print("========================================")
    print("1. 검색 및 한글 초성 매칭 알고리즘 검증")
    print("========================================")
    
    test_cases = [
        # (대상 텍스트, 쿼리, 예상 결과)
        ("초코", "초", True),
        ("초코", "ㅊㅋ", True),
        ("애플", "a", False),  # 영문 대상과 별도 매칭 테스트
        ("Apple", "a", True),
        ("Apple", "appl", True),
        ("크림", "ㅋㄹ", True),
        ("컬리", "ㅋㄹ", True),
        ("토스", "ㅌㅅ", True),
        ("케이뱅크", "ㅋㅇ", True),
        ("초코", "바나나", False)
    ]
    
    search_pass = True
    for target, query, expected in test_cases:
        matched = match_query(target, query)
        status = "PASS" if matched == expected else "FAIL"
        if matched != expected:
            search_pass = False
        print(f"[{status}] 대상: '{target}', 검색어: '{query}' -> 결과: {matched} (기대: {expected})")
    
    assert search_pass, "검색 알고리즘 테스트 실패!"
    print("\n>>> 검색 및 초성 분해 알고리즘 검증 완료: 100% 통과\n")
    
    print("========================================")
    print("2. 선입선출 회전 큐(FIFO Baton Touch) 검증")
    print("========================================")
    
    fq = FairQueue("choco")
    fq.add_code("ref_1", "CHOCO-USER-1", "초코러버1")
    fq.add_code("ref_2", "CHOCO-USER-2", "초코러버2")
    fq.add_code("ref_3", "CHOCO-USER-3", "초코러버3")
    
    # 1. 최초 1위 확인
    top = fq.get_current_top()
    print(f"초기 1순위: {top['nickname']} ({top['code']})")
    assert top["id"] == "ref_1", "초기 1순위가 ref_1이 아닙니다."
    
    # 2. 1순위 복사 실행 -> 회전 검증
    copied, next_top = fq.trigger_copy("ref_1")
    print(f"복사 완료: {copied['nickname']} (누적 복사 {copied['copy_count']}회, 쿨다운 설정됨)")
    print(f"승격된 새로운 1순위: {next_top['nickname']} ({next_top['code']})")
    assert next_top["id"] == "ref_2", "새 1순위가 ref_2로 승격되지 않았습니다."
    assert fq.queue[-1]["id"] == "ref_1", "이전 1위가 큐의 맨 뒤로 가지 않았습니다."
    
    # 3. 2번째 복사 실행
    copied2, next_top2 = fq.trigger_copy("ref_2")
    print(f"2차 복사 완료: {copied2['nickname']} -> 새로운 1순위: {next_top2['nickname']}")
    assert next_top2["id"] == "ref_3", "새 1순위가 ref_3이 아닙니다."
    assert fq.queue[-1]["id"] == "ref_2", "ref_2가 맨 뒤로 가지 않았습니다."
    
    # 4. 신규 유저 등록
    new_order = fq.add_code("ref_4", "CHOCO-NEW-4", "신규뉴비")
    print(f"신규 유저 등록 완료: 대기열 {new_order}순위")
    assert new_order == 4
    assert fq.queue[-1]["id"] == "ref_4"
    
    print("\n>>> 회전 큐 및 바통 터치 로직 검증 완료: 100% 통과\n")
    print("모든 기본 동작 검증(기-단계) 성공!")

if __name__ == "__main__":
    run_tests()
