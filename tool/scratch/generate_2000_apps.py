"""
정확히 2,000개의 국내/글로벌 추천인 지원 앱 및 서비스 초대형 데이터셋 빌더
"""

import json
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 기존 1000개 데이터셋 로드
sample_json_path = os.path.join(project_root, "context", "sample_apps.json")
with open(sample_json_path, "r", encoding="utf-8") as f:
    existing_data = json.load(f)

existing_apps = existing_data.get("apps", [])
existing_referrals = existing_data.get("referrals", [])
seen_ids = set(a["id"] for a in existing_apps)

all_apps = list(existing_apps)
all_referrals = list(existing_referrals)

print(f"기존 앱 수: {len(all_apps)}개")

# 2,000개까지 확장을 위한 추가 도메인/업종별 데이터
NEW_SECTORS = [
    # (카테고리, 한글업종, 영문업종, 혜택설명)
    ("생활/서비스", "지역화폐", "LocalPay", "첫 충전 시 10% 추가 인센티브 캐시백"),
    ("음식배달", "공공배달", "PublicDelivery", "신규 가입 5,000원 할인 쿠폰 및 배달비 지원"),
    ("쇼핑/이커머스", "전통시장", "MarketOnline", "온누리상품권 10% 할인 결제 지원"),
    ("생활/서비스", "무인스터디", "UnmannedStudy", "첫 100시간 충전 시 10시간 무료"),
    ("생활/서비스", "셀프빨래방", "Laundromat", "코인 충전 시 20% 추가 보너스 적립"),
    ("생활/서비스", "실내골프", "IndoorGolf", "스크린 타석 1회 무료 체험권"),
    ("생활/서비스", "복싱체육관", "BoxingGym", "첫 등록 시 글러브 및 핸드랩 증정"),
    ("생활/서비스", "크로스핏", "CrossfitBox", "일일 드랍인 무료 체험권"),
    ("생활/서비스", "요가스튜디오", "YogaStudio", "첫 달 수강 시 요가매트 증정"),
    ("생활/서비스", "무인프린트", "PrintCafe", "첫 복사/출력 1,000원 무료 충전"),
    ("생활/서비스", "셀프스튜디오", "SelfPhoto", "네컷사진 무료 1회 촬영권"),
    ("생활/서비스", "보드게임카페", "BoardGame", "평일 음료 주문 시 1시간 무료 이용"),
    ("생활/서비스", "만화카페", "MangaCafe", "첫 방문 2시간+음료 패키지 30% 할인"),
    ("생활/서비스", "방탈출카페", "EscapeRoom", "첫 테마 예약 5,000원 할인 쿠폰"),
    ("생활/서비스", "VR체험관", "VRPark", "자유이용권 첫 구매 20% 할인"),
    ("생활/서비스", "키즈카페", "KidsCafe", "보호자 무료 음료권 및 아이 1시간 추가"),
    ("생활/서비스", "원데이도예", "CeramicClass", "물레 도예 체험 10,000원 할인"),
    ("생활/서비스", "가죽공방", "LeatherCraft", "카드지갑 원데이 클래스 15% 할인"),
    ("생활/서비스", "향수공방", "PerfumeLab", "나만의 향수 만들기 50ml 할인 바우처"),
    ("생활/서비스", "베이킹스튜디오", "BakingStudio", "케이크/마카롱 클래스 10,000원 쿠폰"),
    ("쇼핑/이커머스", "중고도서", "UsedBook", "첫 중고서적 판매 시 매입가 10% 보너스"),
    ("쇼핑/이커머스", "빈티지샵", "VintageShop", "빈티지 의류 첫 구매 5,000원 할인"),
    ("쇼핑/이커머스", "악기쇼핑몰", "MusicStore", "기타/건반 첫 구매 튜너 무료 증정"),
    ("쇼핑/이커머스", "피규어샵", "FigureShop", "애니메이션 피규어 첫 주문 5% 적립"),
    ("쇼핑/이커머스", "보드게임샵", "BoardGameShop", "인기 보드게임 웰컴 3,000원 할인"),
    ("가상자산/재테크", "웹3노드", "Web3Node", "노드 참여 검증자 보상 10% 부스트"),
    ("가상자산/재테크", "탈중앙렌딩", "DeFiLending", "담보 대출 첫 이용 수수료 캐시백"),
    ("가상자산/재테크", "코인스테이킹", "CryptoStaking", "연 8% 특별 스테이킹 이자 혜택"),
    ("가상자산/재테크", "게임파이", "GameFi", "P2E 캐릭터 첫 민팅 가스비 지원"),
    ("교육/어학", "코딩캠프", "CodingBootcamp", "국비지원 부트캠프 첫 상담 스타벅스"),
    ("교육/어학", "디자인스쿨", "DesignSchool", "UX/UI 포트폴리오 무료 첨삭"),
    ("교육/어학", "원어민회화", "NativeTalk", "원어민 1:1 화상영어 첫 달 30%"),
    ("교육/어학", "자격증패스", "CertPass", "기사/기능사 합격 패키지 3만원 할인"),
    ("앱테크", "영수증리뷰", "ReceiptReview", "플레이스 영수증 인증 건당 100원"),
    ("앱테크", "출석앱테크", "DailyCheck", "연속 30일 출석 시 네이버페이 5,000원"),
    ("앱테크", "미션리워드", "MissionReward", "일일 퀘스트 완료 시 문화상품권 교환"),
    ("소셜/데이팅", "취향커뮤니티", "TasteClub", "와인/독서 모임 첫 가입 1만원 쿠폰"),
    ("소셜/데이팅", "러닝크루", "RunningCrew", "마라톤 크루 첫 참가 스포츠 타월"),
    ("소셜/데이팅", "동네모임", "LocalMeet", "동네 친구 만들기 환영 웰컴 포인트"),
    ("여행/숙박", "펜션예약", "PensionStay", "풀빌라/독채 펜션 첫 예약 2만원 할인"),
    ("여행/숙박", "글램핑", "Glamping", "불멍/바베큐 세트 무료 제공 바우처"),
    ("여행/숙박", "게스트하우스", "Guesthouse", "제주/부산 게하 첫 예약 조식 무료"),
    ("여행/숙박", "렌터카비교", "RentCarCompare", "제주도 렌터카 첫 예약 20% 추가 할인"),
    ("음식배달", "반찬배송", "SideDish", "가정식 집반찬 정기배송 첫 주 50%"),
    ("음식배달", "샐러드정기배송", "SaladDaily", "새벽 샐러드 배송 첫 달 보냉백 무료"),
    ("음식배달", "도시락구독", "LunchBox", "직장인 점심 도시락 첫 주 무료 배송"),
    ("패션/뷰티", "맞춤정장", "TailorSuit", "맞춤 셔츠 1장 무료 맞춤 제작권"),
    ("패션/뷰티", "가발패션", "WigFashion", "자연모 가발 첫 구매 20% 할인"),
    ("패션/뷰티", "안경온라인", "GlassesMall", "블루라이트 차단 안경 첫 구매 1만원 할인"),
    ("패션/뷰티", "타투디자인", "TattooDesign", "타투 도안 상담 및 첫 시술 10% 지원")
]

KOREAN_REGIONS = [
    "서울 강남", "서울 서초", "서울 송파", "서울 마포", "서울 영등포", "서울 용산", "서울 성동", "서울 광진", "서울 동대문", "서울 종로",
    "경기 분당", "경기 판교", "경기 일산", "경기 수원", "경기 화성", "경기 용인", "경기 평택", "경기 부천", "경기 남양주", "경기 하남",
    "인천 송도", "인천 청라", "인천 부평", "인천 구월",
    "부산 해운대", "부산 서면", "부산 센텀", "부산 남포", "부산 광안리",
    "대구 수성", "대구 동성로", "대구 달서",
    "대전 둔산", "대전 유성",
    "광주 상무", "광주 수완",
    "울산 삼산", "세종 보람", "창원 상남", "제주 노형", "제주 서귀포", "원주 무실", "천안 불당", "전주 효자", "포항 양덕"
]

region_idx = 0
sector_idx = 0

while len(all_apps) < 2000:
    region = KOREAN_REGIONS[region_idx % len(KOREAN_REGIONS)]
    cat, sub_ko, sub_en, desc = NEW_SECTORS[sector_idx % len(NEW_SECTORS)]

    app_id = f"app_{len(all_apps)+1}_{sub_en.lower()}_{region_idx}"
    if app_id in seen_ids:
        app_id = f"{app_id}_{len(all_apps)}"
    seen_ids.add(app_id)

    app_name_ko = f"{region} {sub_ko}"
    app_name_en = f"{sub_en} {region.replace(' ', '')}"

    all_apps.append({
        "id": app_id,
        "name_ko": app_name_ko,
        "name_en": app_name_en,
        "aliases": [app_name_ko, sub_ko, region.split()[1] if ' ' in region else region],
        "category": cat,
        "description": f"{app_name_ko} 가입 및 추천 시 {desc}",
        "app_url": f"https://www.{app_id}.com",
        "icon_color": "#4f46e5"
    })

    all_referrals.append({
        "id": f"ref_{app_id}_1",
        "app_id": app_id,
        "code": f"REF-{len(all_apps):04d}-VIP",
        "nickname": f"{region.split()[1]}매니아",
        "copy_count": 1
    })

    sector_idx += 1
    if sector_idx % len(NEW_SECTORS) == 0:
        region_idx += 1

all_apps = all_apps[:2000]
all_referrals = all_referrals[:2000]

print(f"★ 최종 생성 완료: 정확히 앱 {len(all_apps)}개, 추천코드 {len(all_referrals)}개!")

# 저장
with open(sample_json_path, "w", encoding="utf-8") as f:
    json.dump({"apps": all_apps, "referrals": all_referrals}, f, ensure_ascii=False, indent=2)

runtime_path = os.path.join(project_root, "context", "runtime_data.json")
with open(runtime_path, "w", encoding="utf-8") as f:
    json.dump({"apps": all_apps, "referrals": all_referrals}, f, ensure_ascii=False, indent=2)

print("context/sample_apps.json 및 runtime_data.json 2,000개 저장 완료!")
