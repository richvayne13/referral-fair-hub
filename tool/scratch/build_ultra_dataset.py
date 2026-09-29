"""
200개 규모의 국내/해외 전 분야 추천인(레퍼럴) 앱 및 사이트 울트라 데이터셋 빌더
"""

import json
import os

ULTRA_APPS = [
    # ==========================================
    # 1. 금융 / 핀테크 / 인터넷은행 / 증권 / 송금 (25개)
    # ==========================================
    {"id": "toss", "name_ko": "토스", "name_en": "Toss", "aliases": ["토스뱅크", "토스증권", "ㅌㅅ"], "category": "금융/핀테크", "desc": "친구 초대 시 둘 다 최대 5,000원 랜덤 포인트", "url": "https://toss.im", "color": "#0064FF"},
    {"id": "kakaobank", "name_ko": "카카오뱅크", "name_en": "KakaoBank", "aliases": ["카뱅", "카카오", "ㅋㅂ"], "category": "금융/핀테크", "desc": "모임통장 및 26주적금 개설 시 캐시백", "url": "https://www.kakaobank.com", "color": "#FEE500"},
    {"id": "kbank", "name_ko": "케이뱅크", "name_en": "K-Bank", "aliases": ["케이", "케뱅", "ㅋㅇㅂㅋ"], "category": "금융/핀테크", "desc": "행운상자 열고 최대 10만원 현금 당첨", "url": "https://www.kbanknow.com", "color": "#00186B"},
    {"id": "shinhan_sol", "name_ko": "신한 SOL", "name_en": "Shinhan SOL", "aliases": ["신한은행", "신한쏠", "쏠", "ㅅㅎ"], "category": "금융/핀테크", "desc": "신규 계좌 개설 시 마이신한포인트 지급", "url": "https://www.shinhan.com", "color": "#0046FF"},
    {"id": "kb_star", "name_ko": "KB스타뱅킹", "name_en": "KB Star", "aliases": ["국민은행", "스타뱅킹", "ㄱㅁ"], "category": "금융/핀테크", "desc": "스타뱅킹 가입 시 스타프렌즈 적립금", "url": "https://www.kbstar.com", "color": "#FFBC00"},
    {"id": "naverpay", "name_ko": "네이버페이", "name_en": "Naver Pay", "aliases": ["네페", "ㄴㅇㅂ"], "category": "금융/핀테크", "desc": "초대 링크 가입 시 네이버페이 5,000P", "url": "https://pay.naver.com", "color": "#03C75A"},
    {"id": "kakaopay", "name_ko": "카카오페이", "name_en": "Kakao Pay", "aliases": ["카페", "카카오머니"], "category": "금융/핀테크", "desc": "친구 초대 시 페이머니 최대 5,000원 증정", "url": "https://www.kakaopay.com", "color": "#FFEB00"},
    {"id": "monimo", "name_ko": "모니모", "name_en": "Monimo", "aliases": ["삼성모니모", "삼성금융", "ㅁㄴㅁ"], "category": "금융/핀테크", "desc": "가입 시 젤리 및 스페셜 젤리(최대 3만원) 지급", "url": "https://www.monimo.com", "color": "#1428A0"},
    {"id": "finda", "name_ko": "핀다", "name_en": "Finda", "aliases": ["대출비교", "ㅍㄷ"], "category": "금융/핀테크", "desc": "친구 초대 시 스타벅스 기프티콘 및 현금 리워드", "url": "https://www.finda.co.kr", "color": "#1B64DA"},
    {"id": "banksalad", "name_ko": "뱅크샐러드", "name_en": "Banksalad", "aliases": ["뱅샐", "유전자검사"], "category": "금융/핀테크", "desc": "무료 유전자 검사권 및 자산관리 리워드", "url": "https://banksalad.com", "color": "#00D084"},
    {"id": "miraeasset", "name_ko": "미래에셋증권", "name_en": "Mirae Asset", "aliases": ["미래에셋", "ㅁㄹㅇㅅ"], "category": "금융/핀테크", "desc": "비대면 계좌 개설 시 미국 소수점 주식 증정", "url": "https://securities.miraeasset.com", "color": "#F37321"},
    {"id": "kiwoom", "name_ko": "키움증권", "name_en": "Kiwoom", "aliases": ["영웅문", "ㅋㅇㅈㄱ"], "category": "금융/핀테크", "desc": "국내/해외주식 첫 거래 시 현금 4만원", "url": "https://www.kiwoom.com", "color": "#7B1FA2"},
    {"id": "namu", "name_ko": "나무증권", "name_en": "Namu", "aliases": ["NH투자증권", "나무"], "category": "금융/핀테크", "desc": "신규 계좌 개설 시 투자지원금 달러 지급", "url": "https://www.mynamu.com", "color": "#00A05B"},
    {"id": "koreainvestment", "name_ko": "한국투자증권", "name_en": "Korea Investment", "aliases": ["한투", "미니스탁"], "category": "금융/핀테크", "desc": "미니스탁 해외주식 무료 지급 및 수수료 혜택", "url": "https://www.truefriend.com", "color": "#003876"},
    {"id": "toss_securities", "name_ko": "토스증권", "name_en": "Toss Securities", "aliases": ["토증", "토스주식"], "category": "금융/핀테크", "desc": "주식 계좌 개설 시 랜덤 인기 미국주식 1주", "url": "https://tossinvest.com", "color": "#0064FF"},
    {"id": "signalplanner", "name_ko": "시그널플래너", "name_en": "Signal Planner", "aliases": ["보험비교", "해빗팩토리"], "category": "금융/핀테크", "desc": "내 보험 분석 시 스타벅스 커피 즉시 증정", "url": "https://signalplanner.co.kr", "color": "#0055FF"},
    {"id": "wise", "name_ko": "와이즈 송금", "name_en": "Wise", "aliases": ["트랜스퍼와이즈", "해외송금", "ㅇㅇㅈ"], "category": "금융/핀테크", "desc": "첫 해외 송금 시 최대 80만원 수수료 무료 쿠폰", "url": "https://wise.com", "color": "#9FE870"},
    {"id": "wirebarley", "name_ko": "와이어바알리", "name_en": "WireBarley", "aliases": ["외화송금", "ㅇㅇㅇㅂㅇㄹ"], "category": "금융/핀테크", "desc": "가입 시 10,000원 상당 송금 할인 쿠폰팩", "url": "https://www.wirebarley.com", "color": "#0052FF"},
    {"id": "hanapass", "name_ko": "하나패스", "name_en": "HanaPass", "aliases": ["하나송금", "해외송금"], "category": "금융/핀테크", "desc": "친구 초대 시 모바일 상품권 및 수수료 면제", "url": "https://www.hanapass.com", "color": "#00907F"},
    {"id": "payco", "name_ko": "페이코", "name_en": "PAYCO", "aliases": ["NHN페이코", "ㅍㅇㅋ"], "category": "금융/핀테크", "desc": "가입 시 페이코 포인트 5,000P + 웰컴 쿠폰팩", "url": "https://www.payco.com", "color": "#FA2828"},
    {"id": "ssgpay", "name_ko": "SSG페이", "name_en": "SSGPAY", "aliases": ["쓱페이", "ㅅㅍㅇ"], "category": "금융/핀테크", "desc": "첫 결제 시 쓱머니 추가 적립 및 청구할인", "url": "https://www.ssgpay.com", "color": "#FF5252"},
    {"id": "lpay", "name_ko": "엘포인트", "name_en": "L.POINT", "aliases": ["엘페이", "롯데포인트"], "category": "금융/핀테크", "desc": "친구 초대 시 1,000P 즉시 적립 + 룰렛 이벤트", "url": "https://www.lpoint.com", "color": "#007AFF"},
    {"id": "chabun", "name_ko": "차이", "name_en": "CHAI", "aliases": ["차이카드", "ㅊㅇ"], "category": "금융/핀테크", "desc": "초대장 가입 시 번개 부스트 캐시백 혜택", "url": "https://chai.finance", "color": "#FF4500"},
    {"id": "qfund", "name_ko": "피플펀드", "name_en": "PeopleFund", "aliases": ["P2P투자", "온투업"], "category": "금융/핀테크", "desc": "투자 지원금 10,000원 즉시 지급", "url": "https://www.peoplefund.co.kr", "color": "#1E3A8A"},
    {"id": "fount", "name_ko": "파운트", "name_en": "Fount", "aliases": ["로보어드바이저", "AI투자"], "category": "금융/핀테크", "desc": "AI 자산관리 시작 시 투자 지원금 증정", "url": "https://fount.co", "color": "#3B82F6"},

    # ==========================================
    # 2. 쇼핑 / 종합몰 / 해외직구 / 리셀 (25개)
    # ==========================================
    {"id": "coupang", "name_ko": "쿠팡", "name_en": "Coupang", "aliases": ["로켓배송", "로켓와우", "ㅋㅍ"], "category": "쇼핑/이커머스", "desc": "로켓와우 첫 달 무료 체험 및 5천원 캐시백", "url": "https://www.coupang.com", "color": "#E30613"},
    {"id": "aliexpress", "name_ko": "알리익스프레스", "name_en": "AliExpress", "aliases": ["알리", "알리익스", "ㅇㄹ"], "category": "쇼핑/이커머스", "desc": "신규 가입 시 100원 딜 및 웰컴 쿠폰팩 4종", "url": "https://ko.aliexpress.com", "color": "#FF4747"},
    {"id": "temu", "name_ko": "테무", "name_en": "Temu", "aliases": ["티무", "ㅌㅁ"], "category": "쇼핑/이커머스", "desc": "10만원 상당 쿠폰팩 및 무료 선물 혜택", "url": "https://www.temu.com", "color": "#FB7701"},
    {"id": "kurly", "name_ko": "컬리", "name_en": "Kurly", "aliases": ["마켓컬리", "ㅋㄹ"], "category": "쇼핑/이커머스", "desc": "친구 초대 시 첫 주문 완료 후 적립금 5,000원", "url": "https://www.kurly.com", "color": "#5F0080"},
    {"id": "oasis", "name_ko": "오아시스마켓", "name_en": "Oasis Market", "aliases": ["오아시스", "새벽배송"], "category": "쇼핑/이커머스", "desc": "첫 구매 완료 후 추천인과 친구 둘 다 10,000원", "url": "https://www.oasis.co.kr", "color": "#28A745"},
    {"id": "karrot", "name_ko": "당근", "name_en": "Karrot", "aliases": ["당근마켓", "ㄷㄱ"], "category": "쇼핑/이커머스", "desc": "동네 인증 및 친구 초대 시 당근머니 지급", "url": "https://www.daangn.com", "color": "#FF6F0F"},
    {"id": "bungae", "name_ko": "번개장터", "name_en": "Bungaejangter", "aliases": ["번장", "번개페이"], "category": "쇼핑/이커머스", "desc": "초대 코드 입력 시 번개포인트 2,000P 지급", "url": "https://m.bunjang.co.kr", "color": "#FF0000"},
    {"id": "joonggonara", "name_ko": "중고나라", "name_en": "Joonggonara", "aliases": ["중나"], "category": "쇼핑/이커머스", "desc": "안전결제 첫 결제 수수료 무료 쿠폰 증정", "url": "https://web.joongna.com", "color": "#00A862"},
    {"id": "ohouse", "name_ko": "오늘의집", "name_en": "Ohouse", "aliases": ["오하우스", "ㅇㄴㅇㅈ"], "category": "쇼핑/이커머스", "desc": "친구 초대 코드 입력 시 5,000원 즉시 할인", "url": "https://ohou.se", "color": "#35C5F0"},
    {"id": "kream", "name_ko": "크림", "name_en": "KREAM", "aliases": ["크림스니커즈", "한정판", "ㅋㄹ"], "category": "쇼핑/이커머스", "desc": "회원가입 시 2,000 포인트 즉시 적립", "url": "https://kream.co.kr", "color": "#222222"},
    {"id": "soldout", "name_ko": "솔드아웃", "name_en": "SoldOut", "aliases": ["무신사솔드아웃"], "category": "쇼핑/이커머스", "desc": "추천코드 입력 가입 시 3,000P 즉시 적립", "url": "https://www.soldout.co.kr", "color": "#000000"},
    {"id": "iherb", "name_ko": "아이허브", "name_en": "iHerb", "aliases": ["영양제직구", "ㅇㅇㅎㅂ"], "category": "쇼핑/이커머스", "desc": "추천인 코드 입력 시 전 품목 5% 상시 할인 + 첫 구매 20%", "url": "https://kr.iherb.com", "color": "#458500"},
    {"id": "elevenst", "name_ko": "11번가", "name_en": "11st", "aliases": ["십일번가", "우주패스"], "category": "쇼핑/이커머스", "desc": "우주패스 첫 달 100원 및 SK pay 포인트", "url": "https://www.11st.co.kr", "color": "#FA2828"},
    {"id": "gmarket", "name_ko": "G마켓", "name_en": "Gmarket", "aliases": ["지마켓", "스마일클럽"], "category": "쇼핑/이커머스", "desc": "신세계 유니버스 클럽 가입 시 캐시백", "url": "https://www.gmarket.co.kr", "color": "#00B050"},
    {"id": "auction", "name_ko": "옥션", "name_en": "Auction", "aliases": ["스마일페이", "ㅇㅅ"], "category": "쇼핑/이커머스", "desc": "첫 구매 쿠폰팩 및 스마일캐시 리워드", "url": "https://www.auction.co.kr", "color": "#E60012"},
    {"id": "ssg", "name_ko": "SSG닷컴", "name_en": "SSG.COM", "aliases": ["쓱닷컴", "이마트몰"], "category": "쇼핑/이커머스", "desc": "첫 주문 1만원 할인 쿠폰 및 쓱머니", "url": "https://www.ssg.com", "color": "#FA5252"},
    {"id": "rakuten", "name_ko": "라쿠텐 리베이츠", "name_en": "Rakuten", "aliases": ["라쿠텐", "캐시백"], "category": "쇼핑/이커머스", "desc": "첫 쇼핑 시 5,000원 추가 캐시백 보너스", "url": "https://www.rebates.kr", "color": "#BF0000"},
    {"id": "topcashback", "name_ko": "탑캐시백", "name_en": "TopCashback", "aliases": ["미국캐시백", "해외직구"], "category": "쇼핑/이커머스", "desc": "친구 초대 링크 가입 시 $10 웰컴 보너스", "url": "https://www.topcashback.com", "color": "#008752"},
    {"id": "qoo10", "name_ko": "큐텐", "name_en": "Qoo10", "aliases": ["큐텐재팬", "직구몰"], "category": "쇼핑/이커머스", "desc": "장바구니 웰컴 할인 쿠폰팩 즉시 발급", "url": "https://www.qoo10.com", "color": "#FF2B54"},
    {"id": "yes24", "name_ko": "예스24", "name_en": "YES24", "aliases": ["도서예스24", "티켓예스24"], "category": "쇼핑/이커머스", "desc": "신규 가입 시 도서상품권 2,000원 지급", "url": "https://www.yes24.com", "color": "#1956CE"},
    {"id": "aladin", "name_ko": "알라딘", "name_en": "Aladin", "aliases": ["알라딘중고샵", "ㅇㄹㄷ"], "category": "쇼핑/이커머스", "desc": "전자책/종이책 2,000원 할인쿠폰 + 마일리지", "url": "https://www.aladin.co.kr", "color": "#2067B2"},
    {"id": "interpark", "name_ko": "인터파크", "name_en": "Interpark", "aliases": ["인터파크티켓", "투어"], "category": "쇼핑/이커머스", "desc": "신규 회원 투어/티켓 할인 쿠폰팩", "url": "https://www.interpark.com", "color": "#E61E28"},
    {"id": "musinsa_boutique", "name_ko": "무신사 뷰티", "name_en": "Musinsa Beauty", "aliases": ["무뷰", "화장품"], "category": "쇼핑/이커머스", "desc": "뷰티 첫 구매 20% 쿠폰 및 추천 마일리지", "url": "https://www.musinsa.com/beauty", "color": "#111111"},
    {"id": "wemakeprice", "name_ko": "위메프", "name_en": "Wemakeprice", "aliases": ["특가쇼핑", "ㅇㅁㅍ"], "category": "쇼핑/이커머스", "desc": "신규 첫 구매 5,000원 할인 쿠폰", "url": "https://front.wemakeprice.com", "color": "#FA2828"},
    {"id": "tmon", "name_ko": "티몬", "name_en": "TMON", "aliases": ["티켓몬스터", "ㅌㅁ"], "category": "쇼핑/이커머스", "desc": "첫 결제 특가 딜 및 적립금", "url": "https://www.tmon.co.kr", "color": "#FA5900"},

    # ==========================================
    # 3. 배달 / 음식 / 외식 / 밀키트 (15개)
    # ==========================================
    {"id": "baemin", "name_ko": "배달의민족", "name_en": "Baemin", "aliases": ["배민", "배민원", "ㅂㅁ"], "category": "음식배달", "desc": "첫 주문 시 1만원 상당 웰컴 쿠폰팩 증정", "url": "https://baemin.com", "color": "#2AC1BC"},
    {"id": "coupangeats", "name_ko": "쿠팡이츠", "name_en": "Coupang Eats", "aliases": ["쿠이", "쿠팡배달"], "category": "음식배달", "desc": "와우회원 무제한 무료배달 및 5천원 할인", "url": "https://www.coupangeats.com", "color": "#00A5FF"},
    {"id": "yogiyo", "name_ko": "요기요", "name_en": "Yogiyo", "aliases": ["요기패스", "ㅇㄱㅇ"], "category": "음식배달", "desc": "첫 주문 시 최대 1만원 즉시 할인", "url": "https://www.yogiyo.co.kr", "color": "#FA0050"},
    {"id": "ddangyo", "name_ko": "땡겨요", "name_en": "Ddangyo", "aliases": ["신한배달", "ㄸㄱㅇ"], "category": "음식배달", "desc": "신규 가입 첫 주문 시 5,000원 쿠폰 2장 지급", "url": "https://www.ddangyo.com", "color": "#FF5900"},
    {"id": "catchtable", "name_ko": "캐치테이블", "name_en": "Catchtable", "aliases": ["식당예약", "ㅋㅊㅌㅇㅂ"], "category": "음식배달", "desc": "오마카세/파인다이닝 예약 시 5,000원 할인", "url": "https://app.catchtable.co.kr", "color": "#FF2B2B"},
    {"id": "tabling", "name_ko": "테이블링", "name_en": "Tabling", "aliases": ["원격줄서기", "ㅌㅇㅂㄹ"], "category": "음식배달", "desc": "테이블링 페이 충전 시 즉시 3,000원 페이백", "url": "https://www.tabling.co.kr", "color": "#1C1C1E"},
    {"id": "starbucks", "name_ko": "스타벅스", "name_en": "Starbucks", "aliases": ["스벅", "사이렌오더"], "category": "음식배달", "desc": "e-카드 최초 등록 시 무료 음료 e-쿠폰 증정", "url": "https://www.starbucks.co.kr", "color": "#006241"},
    {"id": "marketit", "name_ko": "마켓잇", "name_en": "Marketit", "aliases": ["맛집협찬", "ㅁㅋㅇ"], "category": "음식배달", "desc": "외식/맛집 협찬 포인트 친구 초대 5,000P", "url": "https://marketit.asia", "color": "#3B82F6"},
    {"id": "cookat", "name_ko": "쿠캣", "name_en": "Cookat", "aliases": ["쿠캣마켓", "간편식"], "category": "음식배달", "desc": "친구 초대 시 5,000원 적립금 즉시 지급", "url": "https://cookatmarket.com", "color": "#FF4B2B"},
    {"id": "rankingdak", "name_ko": "랭킹닭컴", "name_en": "Rankingdak", "aliases": ["닭가슴살", "ㄹㅋㄷㅋ"], "category": "음식배달", "desc": "추천인 가입 시 닭가슴살 특가 + 1,000P 지급", "url": "https://www.rankingdak.com", "color": "#E63946"},
    {"id": "wingeat", "name_ko": "윙잇", "name_en": "Wingeat", "aliases": ["밀키트", "식단관리"], "category": "음식배달", "desc": "추천코드 가입 후 첫 구매 시 적립금 3,000원", "url": "https://www.wingeat.com", "color": "#3B82F6"},
    {"id": "fresheasy", "name_ko": "프레시지", "name_en": "Fresheasy", "aliases": ["밀키트1위", "ㅍㄹㅅㅈ"], "category": "음식배달", "desc": "가입 즉시 1만원 쿠폰팩 및 100원 딜", "url": "https://fresheasy.co.kr", "color": "#2EC4B6"},
    {"id": "dietshin", "name_ko": "다이어트신", "name_en": "Dietshin", "aliases": ["다신샵", "다이어트식단"], "category": "음식배달", "desc": "신규 가입 시 5,000원 할인권 + 닭가슴살 특가", "url": "https://dshop.dietshin.com", "color": "#FF6B6B"},
    {"id": "barobul", "name_ko": "불스원몰", "name_en": "Bullsone", "aliases": ["차량용품", "불스원"], "category": "음식배달", "desc": "신규 가입 3,000P 및 와이퍼 특가", "url": "https://bullsonemall.com", "color": "#C92A2A"},
    {"id": "ediya", "name_ko": "이디야멤버스", "name_en": "Ediya", "aliases": ["이디야커피", "ㅇㄷㅇ"], "category": "음식배달", "desc": "스탬프 적립 및 무료 아메리카노 교환권", "url": "https://www.ediya.com", "color": "#0C2340"},

    # ==========================================
    # 4. 패션 / 뷰티 / 명품 / 렌즈 (18개)
    # ==========================================
    {"id": "musinsa", "name_ko": "무신사", "name_en": "Musinsa", "aliases": ["무탠다드", "ㅁㅅㅅ"], "category": "패션/뷰티", "desc": "친구 초대 시 둘 다 적립금 1,000원 + 첫 구매 쿠폰", "url": "https://www.musinsa.com", "color": "#000000"},
    {"id": "oliveyoung", "name_ko": "올리브영", "name_en": "Olive Young", "aliases": ["올영", "올리브", "ㅇㄹㅂㅇ"], "category": "패션/뷰티", "desc": "신규 가입 시 4천원 할인 쿠폰 및 올영세일 적립금", "url": "https://www.oliveyoung.co.kr", "color": "#94C11F"},
    {"id": "ably", "name_ko": "에이블리", "name_en": "Ably", "aliases": ["에블", "ㅇㅇㅂㄹ"], "category": "패션/뷰티", "desc": "신규 가입 시 5,000원 쿠폰팩 즉시 발급", "url": "https://m.a-bly.com", "color": "#FF4975"},
    {"id": "zigzag", "name_ko": "지그재그", "name_en": "Zigzag", "aliases": ["직잭", "ㅈㄱㅈㄱ"], "category": "패션/뷰티", "desc": "첫 구매 20% 할인 쿠폰 및 직진배송 무료배송", "url": "https://zigzag.kr", "color": "#FF2D78"},
    {"id": "29cm", "name_ko": "29CM", "name_en": "29CM", "aliases": ["이십구센티", "29씨엠"], "category": "패션/뷰티", "desc": "첫 결제 15% 할인 쿠폰 및 추천 마일리지 5,000P", "url": "https://www.29cm.co.kr", "color": "#000000"},
    {"id": "wconcept", "name_ko": "W컨셉", "name_en": "W Concept", "aliases": ["더블유컨셉", "ㄷㅂㅇㅋㅅ"], "category": "패션/뷰티", "desc": "디자이너 브랜드 10% 쿠폰 및 5,000원 할인권", "url": "https://www.wconcept.co.kr", "color": "#111111"},
    {"id": "brandi", "name_ko": "브랜디", "name_en": "Brandi", "aliases": ["하루배송", "ㅂㄹㄷ"], "category": "패션/뷰티", "desc": "전 상품 무료배송 및 친구 초대 1,000P 즉시 지급", "url": "https://www.brandi.co.kr", "color": "#FF2553"},
    {"id": "hiver", "name_ko": "하이버", "name_en": "Hiver", "aliases": ["남성쇼핑", "ㅎㅇㅂ"], "category": "패션/뷰티", "desc": "남자 쇼핑앱 첫 구매 1만원 쿠폰팩", "url": "https://www.hiver.co.kr", "color": "#1D1D1F"},
    {"id": "queenit", "name_ko": "퀸잇", "name_en": "Queenit", "aliases": ["4050패션", "ㅋㅇ"], "category": "패션/뷰티", "desc": "가입 즉시 백화점 브랜드 10만원 쿠폰팩 지급", "url": "https://www.queenit.kr", "color": "#E91E63"},
    {"id": "trenbe", "name_ko": "트렌비", "name_en": "Trenbe", "aliases": ["명품쇼핑", "ㅌㄹㅂ"], "category": "패션/뷰티", "desc": "명품 구매 시 5만원 웰컴 쿠폰팩 즉시 발급", "url": "https://www.trenbe.com", "color": "#333333"},
    {"id": "balaan", "name_ko": "발란", "name_en": "Balaan", "aliases": ["명품발란", "ㅂㄹ"], "category": "패션/뷰티", "desc": "첫 명품 쇼핑 웰컴 할인 바우처 및 포인트", "url": "https://www.balaan.co.kr", "color": "#000000"},
    {"id": "mustit", "name_ko": "머스트잇", "name_en": "MustIt", "aliases": ["명품머스트잇", "ㅁㅅƮㅇ"], "category": "패션/뷰티", "desc": "친구 초대 시 3,000P 즉시 적립 + 10% 쿠폰", "url": "https://mustit.co.kr", "color": "#1E1E1E"},
    {"id": "glowpick", "name_ko": "글로우픽", "name_en": "Glowpick", "aliases": ["화장품리뷰", "ㄱㄹㅇㅍ"], "category": "패션/뷰티", "desc": "화장품 리뷰 작성 시 포인트 및 뷰티박스 증정", "url": "https://www.glowpick.com", "color": "#FF385C"},
    {"id": "hwahae", "name_ko": "화해", "name_en": "Hwahae", "aliases": ["성분분석", "화장품성분", "ㅎㅎ"], "category": "패션/뷰티", "desc": "가입 시 10,000원 쿠폰팩 및 무료 체험단", "url": "https://www.hwahae.co.kr", "color": "#00B894"},
    {"id": "lensme", "name_ko": "렌즈미", "name_en": "LensMe", "aliases": ["컬러렌즈", "콘택트렌즈"], "category": "패션/뷰티", "desc": "앱 가입 시 렌즈 3,000원 할인 쿠폰 즉시 발급", "url": "https://www.lens-me.com", "color": "#E84393"},
    {"id": "olens", "name_ko": "오렌즈", "name_en": "Olens", "aliases": ["컬러렌즈1위", "ㅇㄹㅈ"], "category": "패션/뷰티", "desc": "신규 가입 15% 할인 쿠폰 및 샘플 증정", "url": "https://o-lens.com", "color": "#2D3436"},
    {"id": "stylenanda", "name_ko": "스타일난다", "name_en": "3CE", "aliases": ["쓰리씨이", "3CE"], "category": "패션/뷰티", "desc": "신규 가입 시 5,000원 쿠폰 및 3CE 립스틱 적립", "url": "https://stylenanda.com", "color": "#D63031"},
    {"id": "kolonmall", "name_ko": "코오롱몰", "name_en": "KolonMall", "aliases": ["코오롱스포츠", "ㅋㅇㄹ"], "category": "패션/뷰티", "desc": "신규 가입 2만원 할인 쿠폰 및 OLO 포인트", "url": "https://www.kolonmall.com", "color": "#0984E3"},

    # ==========================================
    # 5. 앱테크 / 리워드 / 만보기 / 영수증 / 설문 (20개)
    # ==========================================
    {"id": "tiktok_lite", "name_ko": "틱톡 라이트", "name_en": "TikTok Lite", "aliases": ["틱톡", "틱라", "ㅌㅌ"], "category": "앱테크", "desc": "친구 초대 출석 시 최대 3만원 상당 현금 포인트 지급", "url": "https://lite.tiktok.com", "color": "#FE2C55"},
    {"id": "cashwalk", "name_ko": "캐시워크", "name_en": "Cashwalk", "aliases": ["캐워크", "만보기", "ㅋㅅㅇㅋ"], "category": "앱테크", "desc": "추천인 코드 입력 시 1,000캐시 즉시 지급", "url": "https://cashwalk.com", "color": "#FFD000"},
    {"id": "cashdoc", "name_ko": "캐시닥", "name_en": "Cashdoc", "aliases": ["용돈퀴즈", "ㅋㅅㄷ"], "category": "앱테크", "desc": "가입 시 1,000캐시 + 매일 병원 리뷰 퀴즈", "url": "https://cashdoc.me", "color": "#00B894"},
    {"id": "challengers", "name_ko": "챌린저스", "name_en": "Challengers", "aliases": ["미라클모닝", "습관형성"], "category": "앱테크", "desc": "추천코드 입력 시 100% 환급 챌린지 상금 지원", "url": "https://chlngers.com", "color": "#F03E3E"},
    {"id": "balosodeuk", "name_ko": "발로소득", "name_en": "Balosodeuk", "aliases": ["일상지원금", "ㅂㄹㅅㄷ"], "category": "앱테크", "desc": "친구 초대 시 일상지원금 1,000코인 즉시 충전", "url": "https://balosodeuk.com", "color": "#3B82F6"},
    {"id": "timespread", "name_ko": "타임스프레드", "name_en": "Timespread", "aliases": ["폰잠금", "시간표"], "category": "앱테크", "desc": "잠금화면 열 때마다 캐시 적립 + 1,000캐시", "url": "https://timespread.co.kr", "color": "#6C5CE7"},
    {"id": "moneywalk", "name_ko": "머니워크", "name_en": "Moneywalk", "aliases": ["건강만보기", "ㅁㄴㅇㅋ"], "category": "앱테크", "desc": "5천보만 걸어도 매일 포인트 + 친구 추천 1,000P", "url": "https://moneywalk.com", "color": "#10B981"},
    {"id": "okcashbag", "name_ko": "OK캐쉬백", "name_en": "OK Cashbag", "aliases": ["오케이캐쉬백", "ㅇㅋㅇㅋㅅㅂ"], "category": "앱테크", "desc": "오락(O락) 출석체크 및 친구 초대 1,000P", "url": "https://www.okcashbag.com", "color": "#ED1C24"},
    {"id": "panelnow", "name_ko": "패널나우", "name_en": "PanelNow", "aliases": ["설문조사", "ㅍㄴㄴㅇ"], "category": "앱테크", "desc": "가입 시 300P 즉시 적립 + 2,000P부터 현금 교환", "url": "https://www.panelnow.co.kr", "color": "#FF7675"},
    {"id": "embrain", "name_ko": "엠브레인 패널파워", "name_en": "Embrain Panel Power", "aliases": ["패널파워", "엠브레인"], "category": "앱테크", "desc": "가입 후 일주일 간 2,500원 적립 보장", "url": "https://www.panel.co.kr", "color": "#0984E3"},
    {"id": "surveylink", "name_ko": "서베이링크", "name_en": "SurveyLink", "aliases": ["서베이", "ㅅㅂㅇㄹㅋ"], "category": "앱테크", "desc": "신규 가입 시 1,000P 및 모바일 영화관람권 추첨", "url": "https://www.surveylink.co.kr", "color": "#E17055"},
    {"id": "yafit", "name_ko": "야핏무브", "name_en": "Yafit Move", "aliases": ["자전거만보기", "ㅇㅍㅁㅂ"], "category": "앱테크", "desc": "걸음 및 라이딩으로 마일리지 적립 + 친구 초대 1,000M", "url": "https://yafit.co.kr", "color": "#FDCB6E"},
    {"id": "cashfi", "name_ko": "캐시파이", "name_en": "CashFi", "aliases": ["와이파이앱테크", "ㅋㅅㅍㅇ"], "category": "앱테크", "desc": "Wi-Fi 쓸 때마다 캐시 적립 + 친구 초대 500P", "url": "https://cashfi.io", "color": "#00CEC9"},
    {"id": "receipt_snap", "name_ko": "스냅카우", "name_en": "SnapCow", "aliases": ["영수증적립", "영수증앱테크"], "category": "앱테크", "desc": "영수증 사진만 찍으면 장당 50원 현금 적립", "url": "https://snapcow.io", "color": "#6C5CE7"},
    {"id": "cliptocash", "name_ko": "짤", "name_en": "ZZAL", "aliases": ["짤포인트", "문상적립"], "category": "앱테크", "desc": "문화상품권 및 구글 기프트카드 1분 교환", "url": "https://zzal.co.kr", "color": "#FAB1A0"},
    {"id": "hpoint", "name_ko": "H.Point", "name_en": "H.Point", "aliases": ["현대백화점포인트", "ㅎㅍㅇㅌ"], "category": "앱테크", "desc": "가입 시 1,000P 및 출석 룰렛 보너스", "url": "https://www.h-point.co.kr", "color": "#2D3436"},
    {"id": "cjone", "name_ko": "CJ ONE", "name_en": "CJ ONE", "aliases": ["씨제이원", "올리브영포인트"], "category": "앱테크", "desc": "원워크(ONE워킹) 만보기 및 매일 룰렛 적립", "url": "https://www.cjone.com", "color": "#E84118"},
    {"id": "happyball", "name_ko": "해피포인트", "name_en": "Happy Point", "aliases": ["파리바게뜨", "배스킨라빈스"], "category": "앱테크", "desc": "신규 가입 시 파리바게뜨 2,000원 쿠폰 증정", "url": "https://www.happypointcard.com", "color": "#E84393"},
    {"id": "donamoo", "name_ko": "돈나무", "name_en": "Donamoo", "aliases": ["미션앱테크", "ㄷㄴㅁ"], "category": "앱테크", "desc": "퀴즈 및 클릭 미션으로 하루 3,000원 용돈 벌기", "url": "https://donamoo.kr", "color": "#27AE60"},
    {"id": "bebegrow", "name_ko": "크라우드웍스", "name_en": "Crowdworks", "aliases": ["데이터라벨링", "재택알바"], "category": "앱테크", "desc": "AI 데이터 라벨링 부업 첫 미션 완료 시 보너스", "url": "https://www.crowdworks.kr", "color": "#2980B9"},

    # ==========================================
    # 6. 가상자산 / 암호화폐 / 글로벌 거래소 / Web3 (18개)
    # ==========================================
    {"id": "upbit", "name_ko": "업비트", "name_en": "Upbit", "aliases": ["비트코인", "두나무", "ㅇㅂㅌ"], "category": "가상자산/재테크", "desc": "케이뱅크 실명계좌 연동 및 첫 거래 이벤트", "url": "https://upbit.com", "color": "#093687"},
    {"id": "bithumb", "name_ko": "빗썸", "name_en": "Bithumb", "aliases": ["빗섬", "ㅂㅅ"], "category": "가상자산/재테크", "desc": "신규 가입 시 2만원 상당 웰컴 가상자산 지급", "url": "https://www.bithumb.com", "color": "#F37321"},
    {"id": "coinone", "name_ko": "코인원", "name_en": "Coinone", "aliases": ["코인", "ㅋㅇㅇ"], "category": "가상자산/재테크", "desc": "거래 수수료 평생 20% 페이백 혜택", "url": "https://coinone.co.kr", "color": "#1F53FF"},
    {"id": "korbit", "name_ko": "코빗", "name_en": "Korbit", "aliases": ["신한코빗", "ㅋㅂ"], "category": "가상자산/재테크", "desc": "추천코드 입력 가입 시 10,000원 상당 비트코인", "url": "https://korbit.co.kr", "color": "#1B2A4A"},
    {"id": "gopax", "name_ko": "고팍스", "name_en": "GOPAX", "aliases": ["전북은행고팍스", "ㄱㅍㅅ"], "category": "가상자산/재테크", "desc": "계좌 등록 및 첫 거래 시 5,000원 상당 원화 지급", "url": "https://www.gopax.co.kr", "color": "#1E88E5"},
    {"id": "binance", "name_ko": "바이낸스", "name_en": "Binance", "aliases": ["해외거래소", "바낸", "ㅂㅇㄴㅅ"], "category": "가상자산/재테크", "desc": "레퍼럴 가입 시 거래 수수료 최대 20% 평생 할인", "url": "https://www.binance.com", "color": "#F3BA2F"},
    {"id": "bybit", "name_ko": "바이비트", "name_en": "Bybit", "aliases": ["선물거래", "ㅂㅇㅂƮ"], "category": "가상자산/재테크", "desc": "수수료 20% 할인 및 최대 $30,000 증정금 이벤트", "url": "https://www.bybit.com", "color": "#FB923C"},
    {"id": "bitget", "name_ko": "비트겟", "name_en": "Bitget", "aliases": ["카피트레이딩", "ㅂƮㄱ"], "category": "가상자산/재테크", "desc": "수수료 평생 50% 할인 + 신규 가입 $1,000 리워드", "url": "https://www.bitget.com", "color": "#00F0FF"},
    {"id": "okx", "name_ko": "OKX", "name_en": "OKX", "aliases": ["오케이엑스", "ㅇㅋㅇㅅ"], "category": "가상자산/재테크", "desc": "미스터리 박스 열고 최대 $10,000 코인 당첨", "url": "https://www.okx.com", "color": "#000000"},
    {"id": "gateio", "name_ko": "게이트아이오", "name_en": "Gate.io", "aliases": ["게이트", "ㄱㅇƮㅇㅇㅇ"], "category": "가상자산/재테크", "desc": "상장 초기 신규 알트코인 에어드랍 및 20% 수수료 할인", "url": "https://www.gate.io", "color": "#2196F3"},
    {"id": "mexc", "name_ko": "MEXC", "name_en": "MEXC", "aliases": ["멕시", "한국어지원거래소"], "category": "가상자산/재테크", "desc": "선물 거래 수수료 10% 할인 + 1,000 USDT 증정금", "url": "https://www.mexc.com", "color": "#00B894"},
    {"id": "bingx", "name_ko": "빙엑스", "name_en": "BingX", "aliases": ["빙스", "카피트레이딩"], "category": "가상자산/재테크", "desc": "모의투자 및 수수료 25% 페이백 바우처", "url": "https://bingx.com", "color": "#0052FF"},
    {"id": "kucoin", "name_ko": "쿠코인", "name_en": "KuCoin", "aliases": ["쿠코", "해외거래소"], "category": "가상자산/재테크", "desc": "신규 트레이더 $500 웰컴 보너스 팩", "url": "https://www.kucoin.com", "color": "#24AE8F"},
    {"id": "htx", "name_ko": "후오비", "name_en": "HTX", "aliases": ["에이치티엑스", "후오비코리아"], "category": "가상자산/재테크", "desc": "신규 가입 시 미스터리 박스 및 수수료 감면", "url": "https://www.htx.com", "color": "#1257FF"},
    {"id": "tradingview", "name_ko": "트레이딩뷰", "name_en": "TradingView", "aliases": ["차트분석", "트뷰", "ㅌㅂ"], "category": "가상자산/재테크", "desc": "친구 초대 시 둘 다 $15 차트 구독 크레딧 증정", "url": "https://kr.tradingview.com", "color": "#131722"},
    {"id": "metamask", "name_ko": "메타마스크", "name_en": "MetaMask", "aliases": ["이더리움지갑", "Web3지갑"], "category": "가상자산/재테크", "desc": "포트폴리오 스왑 수수료 캐시백 이벤트", "url": "https://metamask.io", "color": "#E2761B"},
    {"id": "burrito", "name_ko": "부리또월렛", "name_en": "Burrito Wallet", "aliases": ["빗썸지갑", "ㅂㄹㄸ"], "category": "가상자산/재테크", "desc": "친구 초대 시 코인 에어드랍 및 룰렛 티켓", "url": "https://www.burritowallet.com", "color": "#FFC107"},
    {"id": "dcent", "name_ko": "디센트", "name_en": "D'CENT", "aliases": ["콜드월렛", "하드웨어지갑"], "category": "가상자산/재테크", "desc": "지문인증 콜드월렛 구매 시 특별 할인 링크", "url": "https://dcentwallet.com", "color": "#0A0A0A"},

    # ==========================================
    # 7. 여행 / 숙박 / 모빌리티 / 킥보드 / 렌터카 (18개)
    # ==========================================
    {"id": "yanolja", "name_ko": "야놀자", "name_en": "Yanolja", "aliases": ["숙박", "여행", "ㅇㄴㅈ"], "category": "여행/숙박", "desc": "친구 초대 시 코인 2,000P 및 5만원 쿠폰팩", "url": "https://www.yanolja.com", "color": "#FF0055"},
    {"id": "goodchoice", "name_ko": "여기어때", "name_en": "Good Choice", "aliases": ["여기", "숙소", "ㅇㄱㅇㄸ"], "category": "여행/숙박", "desc": "신규 가입 총 15만원 쿠폰팩 + 친구 추천 포인트", "url": "https://www.goodchoice.kr", "color": "#F7323F"},
    {"id": "myrealtrip", "name_ko": "마이리얼트립", "name_en": "MyRealTrip", "aliases": ["마리트", "해외투어"], "category": "여행/숙박", "desc": "초대 링크 가입 시 즉시 사용 가능한 5,000원 쿠폰", "url": "https://www.myrealtrip.com", "color": "#51ABF3"},
    {"id": "agoda", "name_ko": "아고다", "name_en": "Agoda", "aliases": ["호텔예약", "ㅇㄱㄷ"], "category": "여행/숙박", "desc": "초대 시 전 세계 호텔 10% 추가 할인 쿠폰", "url": "https://www.agoda.com", "color": "#008577"},
    {"id": "tripcom", "name_ko": "트립닷컴", "name_en": "Trip.com", "aliases": ["항공권특가", "ㅌㄹㄷㅋ"], "category": "여행/숙박", "desc": "항공권/호텔 예약 시 트립코인 리워드 및 할인", "url": "https://kr.trip.com", "color": "#2681FF"},
    {"id": "klook", "name_ko": "클룩", "name_en": "Klook", "aliases": ["입장권", "투어패스", "ㅋㄹ"], "category": "여행/숙박", "desc": "친구 초대 링크 가입 시 3,500원 할인 쿠폰", "url": "https://www.klook.com", "color": "#FF5B00"},
    {"id": "airbnb", "name_ko": "에어비앤비", "name_en": "Airbnb", "aliases": ["숙소공유", "ㅇㅇㅂㅇㅂ"], "category": "여행/숙박", "desc": "첫 여행 완료 후 호스트 및 게스트 여행 크레딧", "url": "https://www.airbnb.co.kr", "color": "#FF5A5F"},
    {"id": "socar", "name_ko": "쏘카", "name_en": "Socar", "aliases": ["카셰어링", "렌터카", "ㅆㅋ"], "category": "여행/숙박", "desc": "친구 추천 시 1만원 할인 쿠폰 + 크레딧", "url": "https://www.socar.kr", "color": "#00A8FF"},
    {"id": "greencar", "name_ko": "그린카", "name_en": "Greencar", "aliases": ["롯데렌탈", "ㄱㄹㅋ"], "category": "여행/숙박", "desc": "추천인 가입 시 1만원 무료 이용권 즉시 지급", "url": "https://www.greencar.co.kr", "color": "#00C300"},
    {"id": "tmoney_go", "name_ko": "티머니GO", "name_en": "Tmoney GO", "aliases": ["티머니고", "고속버스"], "category": "여행/숙박", "desc": "고속/시외버스 및 따릉이 이용 시 마일리지 적립", "url": "https://tmoneygo.tmoney.co.kr", "color": "#003478"},
    {"id": "kakaot", "name_ko": "카카오 T", "name_en": "Kakao T", "aliases": ["카카오택시", "카카오바이크"], "category": "여행/숙박", "desc": "첫 택시/대리/바이크 이용 시 5,000원 쿠폰", "url": "https://www.kakaomobility.com", "color": "#FFCD00"},
    {"id": "ut", "name_ko": "우티", "name_en": "UT Taxi", "aliases": ["우버택시", "티맵택시"], "category": "여행/숙박", "desc": "신규 가입 첫 탑승 50% 할인 (최대 1만원)", "url": "https://www.ut.taxi", "color": "#000000"},
    {"id": "i_m", "name_ko": "아이엠택시", "name_en": "i.M Taxi", "aliases": ["대형택시", "아이엠"], "category": "여행/숙박", "desc": "가입 즉시 5,000원 할인권 2장 발급", "url": "https://www.imtaxi.co.kr", "color": "#1A1A1A"},
    {"id": "tada", "name_ko": "타다", "name_en": "TADA", "aliases": ["타다넥스트", "ㅌㄷ"], "category": "여행/숙박", "desc": "첫 탑승 시 5,000원 할인 쿠폰 즉시 증정", "url": "https://tada.live", "color": "#1C2541"},
    {"id": "kickgoing", "name_ko": "킥고잉", "name_en": "Kickgoing", "aliases": ["전동킥보드", "ㅋㄱㅇ"], "category": "여행/숙박", "desc": "친구 초대 가입 시 1,500원 무료 라이딩 쿠폰", "url": "https://kickgoing.io", "color": "#3B82F6"},
    {"id": "swing", "name_ko": "스윙", "name_en": "SWING", "aliases": ["스윙킥보드", "전동자전거"], "category": "여행/숙박", "desc": "첫 탑승 무료 쿠폰 + 친구 초대 1,000포인트", "url": "https://swingmobility.com", "color": "#000000"},
    {"id": "gongyu", "name_ko": "지쿠터", "name_en": "Gcooter", "aliases": ["지쿠", "ㅈㅋ"], "category": "여행/숙박", "desc": "친구 초대 시 2,000원 라이딩 할인권 지급", "url": "https://gcooter.com", "color": "#00C853"},
    {"id": "bookingcom", "name_ko": "부킹닷컴", "name_en": "Booking.com", "aliases": ["해외호텔", "ㅂㅋㄷㅋ"], "category": "여행/숙박", "desc": "지니어스 회원 등급 10~15% 할인 리워드", "url": "https://www.booking.com", "color": "#003580"},

    # ==========================================
    # 8. 교육 / 어학 / 토익 / AI회화 (12개)
    # ==========================================
    {"id": "speak", "name_ko": "스픽", "name_en": "Speak", "aliases": ["AI영어회화", "ㅅㅍ"], "category": "교육/어학", "desc": "초대 링크 가입 시 연간 구독권 20,000원 즉시 할인", "url": "https://www.usespeak.com", "color": "#2563EB"},
    {"id": "duolingo", "name_ko": "듀오링고", "name_en": "Duolingo", "aliases": ["외국어학습", "ㄷㅇㄹㄱ"], "category": "교육/어학", "desc": "친구 초대 시 듀오링고 슈퍼(Super) 1주일 무료", "url": "https://ko.duolingo.com", "color": "#58CC02"},
    {"id": "ringles", "name_ko": "링글", "name_en": "Ringle", "aliases": ["아이비리그영어", "ㄹㄱ"], "category": "교육/어학", "desc": "추천인 가입 시 50,000원 상당 무료 수업 크레딧", "url": "https://www.ringleplus.com", "color": "#1E293B"},
    {"id": "cake", "name_ko": "케이크", "name_en": "Cake", "aliases": ["영어회화앱", "ㅋㅇㅋ"], "category": "교육/어학", "desc": "친구 초대 시 케이크 플러스 7일 무료 이용권", "url": "https://mycake.me", "color": "#FF2E93"},
    {"id": "santatoeic", "name_ko": "산타토익", "name_en": "Santa TOEIC", "aliases": ["AI토익", "ㅅㅌㅌㅇ"], "category": "교육/어학", "desc": "AI 토익 예측 진단 점수 무료 제공 + 수강권 할인", "url": "https://www.aitoteic.com", "color": "#FF4B4B"},
    {"id": "yanadoo", "name_ko": "야나두", "name_en": "Yanadoo", "aliases": ["영어야나두", "ㅇㄴㄷ"], "category": "교육/어학", "desc": "첫 수강 시 50,000원 수강지원금 바우처", "url": "https://www.yanadoo.co.kr", "color": "#FFD600"},
    {"id": "siwon", "name_ko": "시원스쿨", "name_en": "Siwon School", "aliases": ["기초영어", "ㅅㅇㅅㅋ"], "category": "교육/어학", "desc": "신규 가입 시 기초 강의 무료 수강권", "url": "https://www.siwonstudy.com", "color": "#0984E3"},
    {"id": "class101", "name_ko": "클래스101", "name_en": "Class101", "aliases": ["취미강의", "ㅋㄹㅅ101"], "category": "교육/어학", "desc": "구독 첫 달 1,000원 딜 + 친구 초대 5,000원 쿠폰", "url": "https://class101.net", "color": "#FF5600"},
    {"id": "inflearn", "name_ko": "인프런", "name_en": "Inflearn", "aliases": ["코딩강의", "ㅇㅍㄹ"], "category": "교육/어학", "desc": "신규 가입 시 IT/프로그래밍 10% 웰컴 쿠폰", "url": "https://www.inflearn.com", "color": "#00C471"},
    {"id": "fastcampus", "name_ko": "패스트캠퍼스", "name_en": "Fast Campus", "aliases": ["직무교육", "ㅍㅅƮㅋㅍㅅ"], "category": "교육/어학", "desc": "신규 회원 가입 시 3만원 할인 쿠폰팩", "url": "https://fastcampus.co.kr", "color": "#E8344E"},
    {"id": "cambly", "name_ko": "캠블리", "name_en": "Cambly", "aliases": ["원어민화상영어", "ㅋㅂㄹ"], "category": "교육/어학", "desc": "추천코드 입력 시 15분 무료 수업권 증정", "url": "https://www.cambly.com", "color": "#FFC800"},
    {"id": "realclass", "name_ko": "리얼클래스", "name_en": "RealClass", "aliases": ["미드영어", "ㄹㅇㅋㄹㅅ"], "category": "교육/어학", "desc": "아이패드 패키지 친구 추천 5만원 추가 할인", "url": "https://realclass.co.kr", "color": "#111111"},

    # ==========================================
    # 9. 생활 / 세탁 / 청소 / 차량 / 이사 (15개)
    # ==========================================
    {"id": "laundrygo", "name_ko": "런드리고", "name_en": "Laundrygo", "aliases": ["비대면세탁", "ㄹㄷㄹㄱ"], "category": "생활/서비스", "desc": "친구 초대 시 5,000포인트 즉시 지급", "url": "https://www.laundrygo.com", "color": "#0052FF"},
    {"id": "setak_special", "name_ko": "세탁특공대", "name_en": "Setak Special", "aliases": ["세특", "ㅅㅌㅌㄱㄷ"], "category": "생활/서비스", "desc": "친구 초대 코드 입력 시 5,000원 할인 쿠폰", "url": "https://getwash.co.kr", "color": "#00D1FF"},
    {"id": "miso", "name_ko": "미소", "name_en": "Miso", "aliases": ["가사도우미", "홈클리닝", "ㅁㅅ"], "category": "생활/서비스", "desc": "첫 가사청소 10,000원 할인 쿠폰 증정", "url": "https://miso.kr", "color": "#3B82F6"},
    {"id": "cheongso_lab", "name_ko": "청소연구소", "name_en": "Cheongso Lab", "aliases": ["집청소", "ㅊㅅㅇㄱㅅ"], "category": "생활/서비스", "desc": "친구 초대 시 5,000원 할인 쿠폰 즉시 발급", "url": "https://www.cleaninglab.co.kr", "color": "#2ECC71"},
    {"id": "michael", "name_ko": "마이클", "name_en": "Michael", "aliases": ["차량관리", "엔진오일", "ㅁㅇㅋ"], "category": "생활/서비스", "desc": "엔진오일/타이어 교환 시 15,000원 할인 쿠폰", "url": "https://www.macarong.net", "color": "#FF5722"},
    {"id": "heydealer", "name_ko": "헤이딜러", "name_en": "Heydealer", "aliases": ["내차팔기", "중고차", "ㅎㅇㄷㄹ"], "category": "생활/서비스", "desc": "견적 신청 시 주유 상품권 및 진단 리워드", "url": "https://www.heydealer.com", "color": "#2C3E50"},
    {"id": "kcar", "name_ko": "케이카", "name_en": "K Car", "aliases": ["직영중고차", "ㅋㅇㅋ"], "category": "생활/서비스", "desc": "홈서비스 배송비 무료 쿠폰 및 보증금 지원", "url": "https://www.kcar.com", "color": "#E74C3C"},
    {"id": "soomgo", "name_ko": "숨고", "name_en": "Soomgo", "aliases": ["전문가매칭", "ㅅㄱ"], "category": "생활/서비스", "desc": "신규 가입 시 견적 요청 무료 캐시 증정", "url": "https://soomgo.com", "color": "#00C7AE"},
    {"id": "kmong", "name_ko": "크몽", "name_en": "Kmong", "aliases": ["외주프리랜서", "ㅋㅁ"], "category": "생활/서비스", "desc": "신규 가입 10,000원 쿠폰팩 즉시 지급", "url": "https://kmong.com", "color": "#FFD400"},
    {"id": "zigbang", "name_ko": "직방", "name_en": "Zigbang", "aliases": ["원룸구하기", "ㅈㅂ"], "category": "생활/서비스", "desc": "첫 이사/중개 시 중개보수 할인 지원", "url": "https://www.zigbang.com", "color": "#FA8231"},
    {"id": "dabang", "name_ko": "다방", "name_en": "Dabang", "aliases": ["부동산원룸", "ㄷㅂ"], "category": "생활/서비스", "desc": "방 구하기 챌린지 월세 지원금 추첨", "url": "https://www.dabangapp.com", "color": "#3867D6"},
    {"id": "jimssam", "name_ko": "짐싸", "name_en": "Zimssa", "aliases": ["원룸이사", "용달이사", "ㅈㅆ"], "category": "생활/서비스", "desc": "이사 예약 시 5,000원 할인 쿠폰", "url": "https://www.zimssa.com", "color": "#20BF6B"},
    {"id": "modoo_cleanup", "name_ko": "모두의청소", "name_en": "Modoo Cleanup", "aliases": ["입주청소", "이사청소"], "category": "생활/서비스", "desc": "입주/이사 청소 예약 시 10,000원 할인", "url": "https://www.modoo-clean.co.kr", "color": "#4B7BEC"},
    {"id": "fitpet", "name_ko": "핏펫", "name_en": "Fitpet", "aliases": ["반려동물", "강아지병원", "ㅍㅍ"], "category": "생활/서비스", "desc": "친구 초대 가입 시 5,000P 즉시 지급", "url": "https://www.fitpetmall.com", "color": "#FC5C65"},
    {"id": "aboutpet", "name_ko": "어바웃펫", "name_en": "AboutPet", "aliases": ["반려동물용품", "고양이간식"], "category": "생활/서비스", "desc": "신규 가입 1만원 쿠폰팩 + 100원 딜", "url": "https://aboutpet.co.kr", "color": "#FD9644"},

    # ==========================================
    # 10. AI / 생산성 / IT / 클라우드 (15개)
    # ==========================================
    {"id": "notion", "name_ko": "노션", "name_en": "Notion", "aliases": ["노트앱", "생산성", "ㄴㅅ"], "category": "라이프스타일", "desc": "추천인 링크 가입 시 $10 크레딧 지급", "url": "https://www.notion.so", "color": "#000000"},
    {"id": "canva", "name_ko": "캔바", "name_en": "Canva", "aliases": ["디자인", "카드뉴스", "ㅋㅂ"], "category": "라이프스타일", "desc": "친구 초대 시 Canva Pro 프리미엄 요소 무료 이용권", "url": "https://www.canva.com", "color": "#00C4CC"},
    {"id": "gamma", "name_ko": "감마 AI", "name_en": "Gamma AI", "aliases": ["PPT제작", "AI발표자료", "ㄱㅁ"], "category": "라이프스타일", "desc": "추천 링크 가입 시 200 크레딧 무료 증정", "url": "https://gamma.app", "color": "#8B5CF6"},
    {"id": "typecast", "name_ko": "타입캐스트", "name_en": "Typecast", "aliases": ["AI성우", "음성합성", "ㅌㅇㅋㅅƮ"], "category": "라이프스타일", "desc": "가입 시 10분 무료 다운로드 캐시 즉시 증정", "url": "https://typecast.ai", "color": "#6366F1"},
    {"id": "liner", "name_ko": "라이너 AI", "name_en": "Liner AI", "aliases": ["AI검색", "하이라이트", "ㄹㅇㄴ"], "category": "라이프스타일", "desc": "초대 가입 시 Liner Pro 1개월 무료 체험권", "url": "https://getliner.com", "color": "#3B82F6"},
    {"id": "vrew", "name_ko": "브루", "name_en": "Vrew", "aliases": ["자동자막", "영상편집", "ㅂㄹ"], "category": "라이프스타일", "desc": "AI 음성인식 자막 생성 무료 코인 증정", "url": "https://vrew.voyagerx.com", "color": "#10B981"},
    {"id": "moyo", "name_ko": "모요", "name_en": "Moyo", "aliases": ["알뜰폰비교", "모두의요금제", "ㅁㅇ"], "category": "라이프스타일", "desc": "알뜰폰 개통 시 네이버페이 3만원 + 스타벅스", "url": "https://www.moyo.plan", "color": "#2563EB"},
    {"id": "toss_mobile", "name_ko": "토스모바일", "name_en": "Toss Mobile", "aliases": ["토스알뜰폰", "ㅌㅅㅁㅂㅇ"], "category": "라이프스타일", "desc": "요금제 가입 시 토스포인트 캐시백 혜택", "url": "https://toss.im/mobile", "color": "#0064FF"},
    {"id": "freet", "name_ko": "프리티", "name_en": "FreeT", "aliases": ["프리텔레콤", "알뜰폰", "ㅍㄹƮ"], "category": "라이프스타일", "desc": "셀프개통 시 신세계 상품권 1만원", "url": "https://www.freet.co.kr", "color": "#E91E63"},
    {"id": "apple", "name_ko": "애플", "name_en": "Apple", "aliases": ["아이폰", "맥북", "ㅇㅍ"], "category": "라이프스타일", "desc": "학생 교육 할인 및 기기 구매 시 액세서리 쿠폰", "url": "https://www.apple.com/kr", "color": "#1C1C1E"},
    {"id": "choco", "name_ko": "초코", "name_en": "Choco", "aliases": ["초콜릿", "초코앱", "ㅊㅋ"], "category": "라이프스타일", "desc": "가입 시 웰컴 초콜릿 포인트 3,000P 지급", "url": "https://choco.example.com", "color": "#8B5A2B"},
    {"id": "setapp", "name_ko": "세트앱", "name_en": "Setapp", "aliases": ["맥앱구독", "ㅅƮㅇ"], "category": "라이프스타일", "desc": "맥용 유료 앱 무제한 구독 1개월 무료", "url": "https://setapp.com", "color": "#2D3436"},
    {"id": "nordvpn", "name_ko": "노드VPN", "name_en": "NordVPN", "aliases": ["VPN우회", "ㄴㄷvpn"], "category": "라이프스타일", "desc": "친구 초대 시 3개월 무료 이용권 추가 증정", "url": "https://nordvpn.com", "color": "#4A90E2"},
    {"id": "surfshark", "name_ko": "서프샤크", "name_en": "Surfshark", "aliases": ["무제한VPN", "ㅅㅍㅅㅋ"], "category": "라이프스타일", "desc": "친구 초대 시 최대 24개월 무료 이용 혜택", "url": "https://surfshark.com", "color": "#18B092"},
    {"id": "chatgpt_plus", "name_ko": "ChatGPT", "name_en": "ChatGPT", "aliases": ["챗GPT", "OpenAI", "ㅊgpt"], "category": "라이프스타일", "desc": "Plus 멤버십 친구 초대 무료 패스 증정", "url": "https://chatgpt.com", "color": "#10A37F"},

    # ==========================================
    # 11. 건강 / 피트니스 / 다이어트 (10개)
    # ==========================================
    {"id": "quat", "name_ko": "콰트", "name_en": "QUAT", "aliases": ["홈트레이닝", "ㅋㅌ"], "category": "생활/서비스", "desc": "홈트 무료 체험권 및 스마트 덤벨 할인권", "url": "https://quat.life", "color": "#FF4B4B"},
    {"id": "planfit", "name_ko": "플랜핏", "name_en": "Planfit", "aliases": ["헬스루틴", "ㅍㄹㅍ"], "category": "생활/서비스", "desc": "AI 운동 루틴 추천 + 코칭 1개월 무료권", "url": "https://planfit.ai", "color": "#2563EB"},
    {"id": "noom", "name_ko": "눔", "name_en": "Noom", "aliases": ["식단다이어트", "ㄴ"], "category": "생활/서비스", "desc": "1:1 AI 건강 코칭 2주 무료 체험권", "url": "https://www.noom.com", "color": "#E8505B"},
    {"id": "burnfit", "name_ko": "번핏", "name_en": "BurnFit", "aliases": ["운동일지", "ㅂㅍ"], "category": "생활/서비스", "desc": "운동 일지 무제한 클라우드 백업 프로 이용권", "url": "https://burnfit.io", "color": "#111111"},
    {"id": "gymboxx", "name_ko": "짐박스", "name_en": "Gymboxx", "aliases": ["헬스장패스", "ㅈㅂㅅ"], "category": "생활/서비스", "desc": "회원가입 시 일일 무료 입장권 증정", "url": "https://gymboxx.co.kr", "color": "#F39C12"},
    {"id": "inbody", "name_ko": "인바디", "name_en": "InBody", "aliases": ["체성분검사", "ㅇㅂㄷ"], "category": "생활/서비스", "desc": "가정용 다이얼 체중계 연동 포인트 적립", "url": "https://www.inbody.com", "color": "#C0392B"},
    {"id": "habitnow", "name_ko": "해빗나우", "name_en": "HabitNow", "aliases": ["습관트래커", "ㅎㅂㄴㅇ"], "category": "생활/서비스", "desc": "루틴 생성 시 프리미엄 테마 무료 언락", "url": "https://habitnow.app", "color": "#8E44AD"},
    {"id": "sleeptown", "name_ko": "슬립타운", "name_en": "SleepTown", "aliases": ["수면관리", "ㅅㄹㅌㅇ"], "category": "생활/서비스", "desc": "규칙적인 수면 시 건물 건설 리워드", "url": "https://sleeptown.seekrtech.com", "color": "#2C3E50"},
    {"id": "glowfit", "name_ko": "글로우핏", "name_en": "Glowfit", "aliases": ["필라테스예약", "ㄱㄹㅇㅍ"], "category": "생활/서비스", "desc": "필라테스/요가 첫 1회 체험권 1만원", "url": "https://glowfit.kr", "color": "#E91E63"},
    {"id": "dietnote", "name_ko": "밀당다이어트", "name_en": "Mealdang", "aliases": ["밀당식단", "ㅁㄷ"], "category": "생활/서비스", "desc": "다이어트 도시락 10팩 패키지 30% 할인", "url": "https://mealdang.com", "color": "#27AE60"},

    # ==========================================
    # 12. 도서 / 웹툰 / OTT / 엔터테인먼트 (10개)
    # ==========================================
    {"id": "ridi", "name_ko": "리디", "name_en": "Ridi", "aliases": ["리디북스", "웹툰", "ㄹㄷ"], "category": "도서/구독", "desc": "친구 초대 시 리디캐시 포인트 즉시 지급", "url": "https://ridibooks.com", "color": "#1F8CE6"},
    {"id": "millie", "name_ko": "밀리의서재", "name_en": "Millie", "aliases": ["밀리", "전자책", "ㅁㄹㅇㅅㅈ"], "category": "도서/구독", "desc": "첫 달 무료 구독 및 친구 초대 1개월 추가 연장", "url": "https://www.millie.co.kr", "color": "#FFEB00"},
    {"id": "welaaa", "name_ko": "윌라 오디오북", "name_en": "Welaaa", "aliases": ["윌라", "오디오북", "ㅇㄹ"], "category": "도서/구독", "desc": "친구 초대 시 1개월 무료 체험 쿠폰 추가 지급", "url": "https://www.welaaa.com", "color": "#FF4500"},
    {"id": "kakaopage", "name_ko": "카카오페이지", "name_en": "KakaoPage", "aliases": ["웹소설", "카카페", "ㅋㅋㅇㅍㅇㅈ"], "category": "도서/구독", "desc": "친구 초대 시 최대 5,000캐시 뽑기권 지급", "url": "https://page.kakao.com", "color": "#FEE500"},
    {"id": "series", "name_ko": "네이버 시리즈", "name_en": "Naver Series", "aliases": ["쿠키", "시리즈", "ㅅㄹㅈ"], "category": "도서/구독", "desc": "쿠키 충전 및 친구 초대 무료 쿠키 지급", "url": "https://series.naver.com", "color": "#03C75A"},
    {"id": "watcha", "name_ko": "왓챠", "name_en": "Watcha", "aliases": ["왓챠피디아", "영화추천", "ㅇㅊ"], "category": "도서/구독", "desc": "친구 초대 시 2주 프리미엄 무료 이용권 증정", "url": "https://watcha.com", "color": "#FF0558"},
    {"id": "wavve", "name_ko": "웨이브", "name_en": "Wavve", "aliases": ["공중파드라마", "ㅇㅇㅂ"], "category": "도서/구독", "desc": "첫 달 100원 및 친구 초대 코인 적립", "url": "https://www.wavve.com", "color": "#1353FF"},
    {"id": "tving", "name_ko": "티빙", "name_en": "Tving", "aliases": ["tvN다시보기", "ㅌㅂ"], "category": "도서/구독", "desc": "연간 이용권 25% 할인 + 캐시백 혜택", "url": "https://www.tving.com", "color": "#FF153C"},
    {"id": "spoqa", "name_ko": "도도포인트", "name_en": "Dodo Point", "aliases": ["카페적립", "ㄷㄷㅍㅇㅌ"], "category": "도서/구독", "desc": "동네 단골 카페 10회 적립 시 무료 커피", "url": "https://www.dodopoint.com", "color": "#E67E22"},
    {"id": "spoon", "name_ko": "스푼라디오", "name_en": "Spoon Radio", "aliases": ["오디오라이브", "ㅅㅍㄹㄷㅇ"], "category": "도서/구독", "desc": "가입 시 10스푼 코인 무료 충전", "url": "https://www.spooncast.net", "color": "#FF4500"}
]

def generate_ultra_dataset():
    apps = []
    referrals = []

    for app in ULTRA_APPS:
        app_entry = {
            "id": app["id"],
            "name_ko": app["name_ko"],
            "name_en": app["name_en"],
            "aliases": app["aliases"],
            "category": app["category"],
            "description": app["desc"],
            "app_url": app["url"],
            "icon_color": app["color"]
        }
        apps.append(app_entry)

        # 각 앱별 기본 시드 추천인 코드 생성
        code_suffix = app['id'].replace('_', '').upper()[:4]
        referrals.append({
            "id": f"ref_{app['id']}_1",
            "app_id": app["id"],
            "code": f"{code_suffix}-VIP-77",
            "nickname": f"{app['name_ko']}매니아",
            "copy_count": 2
        })

    return {"apps": apps, "referrals": referrals}

if __name__ == "__main__":
    dataset = generate_ultra_dataset()
    print(f"★ 축하합니다! 총 {len(dataset['apps'])}개 울트라 앱 및 {len(dataset['referrals'])}개 추천코드 생성 완료!")

    context_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "context", "sample_apps.json"))
    runtime_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "context", "runtime_data.json"))

    with open(context_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
    with open(runtime_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print("sample_apps.json 및 runtime_data.json 파일 저장 완료!")
