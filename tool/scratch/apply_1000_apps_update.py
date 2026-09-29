"""
1,000개 앱 데이터셋 주입, 틴더/골드스푼 퀵칩 및 소셜 탭 추가, 고성능 페이지네이션 적용
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

    # 1. SEED_DATA 교체
    start_idx = content.find("const SEED_DATA = {")
    end_idx = content.find(end_marker, start_idx)
    if start_idx != -1 and end_idx != -1:
        content = content[:start_idx] + f"const SEED_DATA = {seed_json_str};" + content[end_idx + 1:]
    else:
        print(f"Warning: could not find SEED_DATA in {target_file}")

    # 2. 로컬스토리지 캐시 키 v5 갱신
    content = content.replace("referral_data_store_v4", "referral_data_store_v5")
    content = content.replace("< 150", "< 800")
    content = content.replace("< 80", "< 800")

    # 3. 퀵 검색 태그에 틴더, 골드스푼 추가
    old_chips = '<button onclick="quickSearch(\'토스\')"'
    new_chips = '<button onclick="quickSearch(\'틴더\')" class="px-2.5 py-1 bg-rose-50 hover:bg-rose-100 border border-rose-200 rounded-lg transition font-bold text-rose-600"><i class="fa-solid fa-fire mr-1 text-rose-500"></i>틴더</button>\n        <button onclick="quickSearch(\'골드스푼\')" class="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 border border-amber-200 rounded-lg transition font-bold text-amber-700"><i class="fa-solid fa-crown mr-1 text-amber-500"></i>골드스푼</button>\n        <button onclick="quickSearch(\'토스\')"'
    if old_chips in content and "quickSearch('틴더')" not in content:
        content = content.replace(old_chips, new_chips, 1)

    # 4. 카테고리 필터 탭에 소셜/데이팅 추가
    old_tabs = '<button onclick="filterCategory(\'패션/뷰티\')"'
    new_tabs = '<button onclick="filterCategory(\'소셜/데이팅\')" class="category-tab px-3 py-1.5 rounded-full font-semibold bg-white border border-slate-200 text-slate-600 hover:bg-slate-100 transition" data-category="소셜/데이팅">소셜/데이팅</button>\n      <button onclick="filterCategory(\'패션/뷰티\')"'
    if old_tabs in content and "data-category=\"소셜/데이팅\"" not in content:
        content = content.replace(old_tabs, new_tabs, 1)

    # 5. 그리드 렌더링 성능 최적화: 36개 단위 더보기(Pagination) 로직 적용
    old_render = """    function renderAppsGrid(apps) {
      const container = document.getElementById('appsGrid');
      container.innerHTML = '';"""

    new_render = """    let gridDisplayLimit = 36;
    let currentRenderedApps = [];

    function renderAppsGrid(apps) {
      currentRenderedApps = apps;
      const container = document.getElementById('appsGrid');
      container.innerHTML = '';
      
      const displayed = currentSearchQuery ? apps : apps.slice(0, gridDisplayLimit);"""

    if old_render in content:
        content = content.replace(old_render, new_render, 1)

    # 더보기 버튼 추가
    old_end = """        container.appendChild(card);
      });
    }"""

    new_end = """        container.appendChild(card);
      });

      // 1000개 대규모 앱을 위한 더보기 버튼
      if (!currentSearchQuery && apps.length > gridDisplayLimit) {
        const remaining = apps.length - gridDisplayLimit;
        const moreContainer = document.createElement('div');
        moreContainer.className = "col-span-full py-6 text-center";
        moreContainer.innerHTML = `
          <button onclick="loadMoreApps()" class="px-8 py-3.5 bg-white hover:bg-indigo-50 border-2 border-indigo-200 hover:border-indigo-500 rounded-2xl text-indigo-700 font-extrabold text-sm shadow-md transition transform active:scale-95 flex items-center justify-center space-x-2 mx-auto">
            <i class="fa-solid fa-angles-down"></i>
            <span>서비스 더보기 (+36개 / 남은 ${remaining}개)</span>
          </button>
        `;
        container.appendChild(moreContainer);
      }
    }

    function loadMoreApps() {
      gridDisplayLimit += 36;
      renderAppsGrid(currentRenderedApps);
    }"""

    if old_end in content:
        content = content.replace(old_end, new_end, 1)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[완료] {target_file} 1,000개 앱 및 틴더/골드스푼 기능 탑재 성공!")
