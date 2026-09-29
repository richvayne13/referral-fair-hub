"""
통합 엔드투엔드 API 검증 스크립트 (test_integration.py)
"""

import sys
import threading
import time
import urllib.request
import json

from server import ThreadedHTTPServer, ReferralRequestHandler

TEST_PORT = 8999

def run_test_server():
    server = ThreadedHTTPServer(("127.0.0.1", TEST_PORT), ReferralRequestHandler)
    server.serve_forever()

def run_integration_tests():
    # 1. 백그라운드 서버 가동
    server_thread = threading.Thread(target=run_test_server, daemon=True)
    server_thread.start()
    time.sleep(1)

    base_url = f"http://127.0.0.1:{TEST_PORT}"

    print("========================================")
    print("통합 엔드투엔드 API 테스트 시작")
    print("========================================")

    # 1. 메인 웹 페이지 GET 테스트
    req = urllib.request.Request(f"{base_url}/")
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")
        assert "추천인.com" in html
        print("[PASS] 1. 메인 대시보드(HTML) 서빙 정상")

    # 2. 검색 API 테스트 ('초' 검색 -> '초코' 매칭)
    req = urllib.request.Request(f"{base_url}/api/search?q=%EC%B4%88")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        matched_names = [a["name_ko"] for a in data]
        assert "초코" in matched_names
        print(f"[PASS] 2. 한글 음절 검색 정상 ('초' -> {matched_names})")

    # 3. 검색 API 테스트 ('a' 검색 -> 'Apple' 매칭)
    req = urllib.request.Request(f"{base_url}/api/search?q=a")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        matched_en = [a["name_en"] for a in data]
        assert any("Apple" in name for name in matched_en)
        print(f"[PASS] 3. 영문 검색 정상 ('a' -> {matched_en})")

    # 4. 앱 상세 및 1순위 코드 조회 테스트 ('choco')
    req = urllib.request.Request(f"{base_url}/api/apps/choco")
    with urllib.request.urlopen(req) as resp:
        detail = json.loads(resp.read().decode("utf-8"))
        top = detail["current_top"]
        assert top is not None
        top_id = top["id"]
        print(f"[PASS] 4. 초코 1순위 코드 조회 정상 (1위: {top['nickname']}, 코드: {top['code']})")

    # 5. 복사 및 큐 회전(Baton Touch) 테스트
    post_data = json.dumps({"code_id": top_id}).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/api/apps/choco/copy",
        data=post_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        copy_res = json.loads(resp.read().decode("utf-8"))
        assert copy_res["success"] is True
        print(f"[PASS] 5. 추천코드 복사 및 큐 회전 성공: {copy_res['message']}")

    # 6. 복사 후 새로운 1위 확인
    req = urllib.request.Request(f"{base_url}/api/apps/choco")
    with urllib.request.urlopen(req) as resp:
        detail2 = json.loads(resp.read().decode("utf-8"))
        new_top = detail2["current_top"]
        assert new_top["id"] != top_id
        print(f"[PASS] 6. 다음 순번 대기자 1위 자동 승격 확인 (새 1위: {new_top['nickname']})")

    print("\n========================================")
    print(">>> 모든 통합 테스트 100% 통과! 배포 준비 완료.")
    print("========================================")

if __name__ == "__main__":
    run_integration_tests()
