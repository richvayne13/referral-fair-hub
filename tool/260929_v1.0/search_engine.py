"""
스마트 한글 초성 및 다국어 검색 엔진 (search_engine.py)
"""

from typing import List, Dict, Any

CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ',
    'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

def extract_chosung(text: str) -> str:
    """한글 음절에서 초성만 분리 추출, 영문/숫자는 소문자로 유지"""
    result = []
    for char in text:
        code = ord(char)
        if 0xAC00 <= code <= 0xD7A3:
            chosung_idx = (code - 0xAC00) // (21 * 28)
            result.append(CHOSUNG_LIST[chosung_idx])
        else:
            result.append(char.lower())
    return "".join(result)

class SearchEngine:
    def __init__(self, apps: List[Dict[str, Any]]):
        self.apps = []
        for app in apps:
            app_copy = dict(app)
            app_copy["chosung_ko"] = extract_chosung(app.get("name_ko", ""))
            app_copy["search_haystack"] = f"{app.get('name_ko', '')} {app.get('name_en', '')} {app.get('category', '')}".lower()
            self.apps.append(app_copy)

    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        검색어를 기반으로 실시간 매칭 및 관련도 순 정렬
        우선순위:
        1. 한글/영문 접두사 정확 일치
        2. 초성 정확 일치
        3. 부분 포함 일치
        """
        q = query.strip().lower()
        if not q:
            return self.apps[:limit]

        results = []
        for app in self.apps:
            score = 0
            name_ko = app.get("name_ko", "").lower()
            name_en = app.get("name_en", "").lower()
            chosung = app.get("chosung_ko", "")

            # 1. 영문 접두사 일치 (예: 'a' -> 'apple')
            if name_en.startswith(q):
                score += 100
            elif q in name_en:
                score += 50

            # 2. 한글 음절 접두사 일치 (예: '초' -> '초코')
            if name_ko.startswith(q):
                score += 100
            elif q in name_ko:
                score += 50

            # 3. 한글 초성 검색 일치 (예: 'ㅊㅋ' -> '초코')
            if chosung.startswith(q):
                score += 90
            elif q in chosung:
                score += 40

            # 4. 카테고리 또는 설명 매칭
            if q in app.get("category", "").lower():
                score += 20

            if score > 0:
                results.append((score, app))

        # 점수 내림차순 정렬
        results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in results[:limit]]
