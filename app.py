"""
클라우드 배포 및 로컬 실행을 위한 메인 진입점 (app.py)
"""

import os
import sys

# tool/260929_v1.0 경로 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
tool_dir = os.path.join(current_dir, "tool", "260929_v1.0")
if tool_dir not in sys.path:
    sys.path.insert(0, tool_dir)

from server import run

if __name__ == "__main__":
    env_port = os.environ.get("PORT")
    if env_port:
        port = int(env_port)
    elif len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
    run(port)
