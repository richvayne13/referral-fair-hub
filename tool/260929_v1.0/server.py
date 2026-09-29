"""
공정 추천인 플랫폼 HTTP REST API 서버 (server.py)
Python 표준 라이브러리(http.server) 기반 무의존성 경량 고성능 서버
"""

import json
import os
import sys
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from search_engine import SearchEngine
from queue_manager import QueueManager

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
SEED_FILE = os.path.join(PROJECT_ROOT, "context", "sample_apps.json")
RUNTIME_DATA_FILE = os.path.join(PROJECT_ROOT, "context", "runtime_data.json")
RESULT_DIR = os.path.join(PROJECT_ROOT, "result", "260929_v1.0")
INDEX_HTML = os.path.join(RESULT_DIR, "index.html")

# 매니저 및 검색엔진 인스턴스
queue_mgr = QueueManager(data_file=RUNTIME_DATA_FILE, seed_file=SEED_FILE)
search_engine = SearchEngine(queue_mgr.apps)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class ReferralRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # 콘솔 로그 간소화
        sys.stdout.write(f"[{self.log_date_time_string()}] {self.command} {self.path} - {args[0]}\n")
        sys.stdout.flush()

    def send_json(self, status_code: int, data: any):
        response_bytes = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query_params = urllib.parse.parse_qs(parsed.query)

        # 1. 메인 웹 페이지 서빙
        if path == "/" or path == "/index.html":
            if os.path.exists(INDEX_HTML):
                with open(INDEX_HTML, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "index.html not found in result directory")
            return

        # 2. 검색 API: /api/search?q=xxx
        if path == "/api/search":
            q = query_params.get("q", [""])[0]
            # 검색 엔진 갱신 (앱 추가 가능성 대비)
            results = search_engine.search(q, limit=8)
            # 대기열 정보 부가
            all_apps = queue_mgr.get_apps()
            app_map = {a["id"]: a for a in all_apps}
            enriched_results = []
            for r in results:
                info = app_map.get(r["id"], r)
                enriched_results.append(info)
            self.send_json(200, enriched_results)
            return

        # 3. 전체 앱 목록 API: /api/apps
        if path == "/api/apps":
            apps = queue_mgr.get_apps()
            self.send_json(200, apps)
            return

        # 4. 개별 앱 상세 및 대기열 조회: /api/apps/<app_id>
        if path.startswith("/api/apps/"):
            parts = path.strip("/").split("/")
            if len(parts) == 3:  # api, apps, <app_id>
                app_id = parts[2]
                detail = queue_mgr.get_app_detail(app_id)
                if detail:
                    self.send_json(200, detail)
                else:
                    self.send_json(404, {"error": "NOT_FOUND", "message": "해당 앱을 찾을 수 없습니다."})
                return

        self.send_error(404, "API Endpoint Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 요청 본문 읽기
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            body = {}

        client_ip = self.client_address[0]

        # 1. 추천인 코드 복사 & 큐 회전: /api/apps/<app_id>/copy
        if path.startswith("/api/apps/") and path.endswith("/copy"):
            parts = path.strip("/").split("/")
            if len(parts) == 4:  # api, apps, <app_id>, copy
                app_id = parts[2]
                code_id = body.get("code_id")
                result = queue_mgr.copy_referral_code(app_id, code_id, client_ip)
                status_code = 200 if result.get("success") else 429 if result.get("error") == "RATE_LIMIT" else 400
                self.send_json(status_code, result)
                return

        # 2. 신규 추천인 코드 등록: /api/apps/<app_id>/register
        if path.startswith("/api/apps/") and path.endswith("/register"):
            parts = path.strip("/").split("/")
            if len(parts) == 4:  # api, apps, <app_id>, register
                app_id = parts[2]
                code = body.get("code", "")
                nickname = body.get("nickname", "")
                result = queue_mgr.register_code(app_id, code, nickname)
                status_code = 200 if result.get("success") else 400
                self.send_json(status_code, result)
                return

        # 3. 새로운 앱 자체를 등록: /api/apps/new
        if path == "/api/apps/new":
            name_ko = body.get("name_ko", "")
            name_en = body.get("name_en", "")
            category = body.get("category", "")
            description = body.get("description", "")
            app_url = body.get("app_url", "")
            result = queue_mgr.register_new_app(name_ko, name_en, category, description, app_url)
            if result.get("success"):
                global search_engine
                search_engine = SearchEngine(queue_mgr.apps)
            status_code = 200 if result.get("success") else 400
            self.send_json(status_code, result)
            return

        self.send_error(404, "Endpoint Not Found")

def run(port: int = 8080):
    server_address = ("", port)
    httpd = ThreadedHTTPServer(server_address, ReferralRequestHandler)
    print(f"==================================================")
    print(f" 추천인.com 공정 추천인 플랫폼 서버 가동 완료!")
    print(f" 로컬 주소: http://localhost:{port}")
    print(f" 데이터 경로: {RUNTIME_DATA_FILE}")
    print(f" 웹 대시보드: {INDEX_HTML}")
    print(f"==================================================")
    httpd.serve_forever()

if __name__ == "__main__":
    env_port = os.environ.get("PORT")
    if env_port:
        port = int(env_port)
    elif len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
    run(port)
