"""
정확한 인덱스 기반으로 201개 울트라 앱 SEED_DATA 교체
"""

import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))

json_path = os.path.join(project_root, "context", "sample_apps.json")
result_html_path = os.path.join(project_root, "result", "260929_v1.0", "index.html")
root_html_path = os.path.join(project_root, "index.html")

with open(json_path, "r", encoding="utf-8") as f:
    seed_json_str = f.read()

new_seed_decl = f"const SEED_DATA = {seed_json_str};"
end_marker = ';\n\n    // 로컬 데이터 스토어 관리'

for target_file in [result_html_path, root_html_path]:
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()

        start_idx = content.find("const SEED_DATA = {")
        end_idx = content.find(end_marker, start_idx)

        if start_idx != -1 and end_idx != -1:
            new_content = content[:start_idx] + new_seed_decl + content[end_idx + 1:]
            new_content = new_content.replace("referral_data_store_v3", "referral_data_store_v4")
            new_content = new_content.replace("referral_data_store_v2", "referral_data_store_v4")
            new_content = new_content.replace("< 80", "< 150")

            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[성공] {target_file} 201개 앱 데이터로 갱신 완료!")
        else:
            print(f"[오류] {target_file}에서 마커를 찾지 못했습니다.")
