"""
스마트 한글 초성 및 별칭(Aliases) 다국어 검색 엔진 (search_engine.py)
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
            aliases = app.get("aliases", [])
            app_copy["aliases_chosung"] = [extract_chosung(a) for a in aliases]
            self.apps.append(app_copy)

    def search(self, query: str, limit: int = 12) -> List[Dict[str, Any]]:
        q = query.strip().lower()
        if not q:
            return self.apps[:limit]

        results = []
        for app in self.apps:
            score = 0
            name_ko = app.get("name_ko", "").lower()
            name_en = app.get("name_en", "").lower()
            chosung = app.get("chosung_ko", "")
            aliases = [a.lower() for a in app.get("aliases", [])]
            aliases_chosung = app.get("aliases_chosung", [])

            # 1. 한글/영문 접두사 및 완전 일치
            if name_ko == q or name_en == q:
                score += 200
            elif name_ko.startswith(q) or name_en.startswith(q):
                score += 120
            elif q in name_ko or q in name_en:
                score += 60

            # 2. 별칭(Aliases) 일치 (예: '배민' -> 배달의민족, '카뱅' -> 카카오뱅크)
            for alias in aliases:
                if alias == q:
                    score += 180
                elif alias.startswith(q):
                    score += 100
                elif q in alias:
                    score += 50

            # 3. 한글 초성 검색 일치 (예: 'ㅊㅋ' -> 초코, 'ㅂㅁ' -> 배민, 'ㅌㅅ' -> 토스)
            if chosung == q:
                score += 150
            elif chosung.startswith(q):
                score += 90
            elif q in chosung:
                score += 40

            for ac in aliases_chosung:
                if ac == q:
                    score += 140
                elif ac.startswith(q):
                    score += 80

            # 4. 카테고리 매칭
            if q in app.get("category", "").lower():
                score += 30

            if score > 0:
                results.append((score, app))

        results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in results[:limit]]
