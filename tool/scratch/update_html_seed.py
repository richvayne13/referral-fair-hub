"""
index.html 파일의 SEED_DATA를 context/sample_apps.json의 94개 앱 최신 데이터로 자동 교체
"""

import json
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

json_path = os.path.join(project_root, "context", "sample_apps.json")
result_html_path = os.path.join(project_root, "result", "260929_v1.0", "index.html")
root_html_path = os.path.join(project_root, "index.html")

with open(json_path, "r", encoding="utf-8") as f:
    seed_json_str = f.read()

# SEED_DATA 블록 교체 패턴
seed_pattern = re.compile(r'const SEED_DATA = \{.*?\n    \};', re.DOTALL)
replacement = f"const SEED_DATA = {seed_json_str};"

for target_file in [result_html_path, root_html_path]:
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # also update version key in localStorage so existing browsers reset to the new 94 apps!
        content = content.replace("referral_data_store_v2", "referral_data_store_v3")
        content = content.replace("< 20", "< 80")

        new_content, count = seed_pattern.subn(replacement, content, count=1)
        if count == 0:
            print(f"[경고] {target_file}에서 SEED_DATA 패턴을 찾지 못했습니다.")
        else:
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[성공] {target_file} 94개 앱 데이터로 갱신 완료!")
