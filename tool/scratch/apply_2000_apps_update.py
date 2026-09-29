"""
2,000개 앱 데이터셋을 index.html에 주입하고 캐시 키를 v6로 갱신
"""

import json
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
json_path = os.path.join(project_root, "context", "sample_apps.json")
result_html_path = os.path.join(project_root, "result", "260929_v1.0", "index.html")
root_html_path = os.path.join(project_root, "index.html")

with open(json_path, "r", encoding="utf-8") as f:
    seed_json_str = f.read()

end_marker = ';\n\n    // 로컬 데이터 스토어 관리'

for target_file in [result_html_path, root_html_path]:
    if not os.path.exists(target_file):
        continue

    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    start_idx = content.find("const SEED_DATA = {")
    end_idx = content.find(end_marker, start_idx)

    if start_idx != -1 and end_idx != -1:
        content = content[:start_idx] + f"const SEED_DATA = {seed_json_str};" + content[end_idx + 1:]
        content = content.replace("referral_data_store_v5", "referral_data_store_v6")
        content = content.replace("< 800", "< 1500")

        with open(target_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[완료] {target_file} 2,000개 앱 데이터 갱신 성공!")
    else:
        print(f"[오류] {target_file}에서 SEED_DATA 마커를 찾지 못했습니다.")
