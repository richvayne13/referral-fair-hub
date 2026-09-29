"""
85개 이상의 국내/글로벌 추천인 제도 지원 앱 및 사이트 전수 데이터셋 생성기
"""

import json
import os

APPS_DATA = [
    # --- 1. 금융 / 핀테크 / 인터넷은행 (16개) ---
    {
        "id": "toss",
        "name_ko": "토스",
        "name_en": "Toss",
        "aliases": ["토스뱅크", "토스증권", "ㅌㅅ"],
        "category": "금융/핀테크",
        "description": "친구 초대 시 둘 다 최대 5,000원 랜덤 포인트 증정",
        "app_url": "https://toss.im",
        "icon_color": "#0064FF",
        "seed_code": "TOSS-LUCKY-777",
        "seed_nick": "행운의토스"
    },
    {
        "id": "kakaobank",
        "name_ko": "카카오뱅크",
        "name_en": "KakaoBank",
        "aliases": ["카뱅", "카카오", "ㅋㅂ", "ㅋㅋㅇㅂㅋ"],
        "category": "금융/핀테크",
        "description": "모임통장 및 26주적금 개설 시 캐시백 혜택",
        "app_url": "https://www.kakaobank.com",
        "icon_color": "#FEE500",
        "seed_code": "KBANK-LION-88",
        "seed_nick": "라이언러버"
    },
    {
        "id": "kbank",
        "name_ko": "케이뱅크",
        "name_en": "K-Bank",
        "aliases": ["케이", "케뱅", "ㅋㅇㅂㅋ"],
        "category": "금융/핀테크",
        "description": "행운상자 열고 최대 10만원 현금 당첨 기회",
        "app_url": "https://www.kbanknow.com",
        "icon_color": "#00186B",
        "seed_code": "KBANK-CASH-77",
        "seed_nick": "케이왕자"
    },
    {
        "id": "shinhan_sol",
        "name_ko": "신한 SOL",
        "name_en": "Shinhan SOL",
        "aliases": ["신한은행", "신한쏠", "쏠", "ㅅㅎ"],
        "category": "금융/핀테크",
        "description": "신규 계좌 개설 시 마이신한포인트 즉시 지급",
        "app_url": "https://www.shinhan.com",
        "icon_color": "#0046FF",
        "seed_code": "SOL-PLUS-990",
        "seed_nick": "신한매니아"
    },
    {
        "id": "kb_star",
        "name_ko": "KB스타뱅킹",
        "name_en": "KB Star",
        "aliases": ["국민은행", "국민", "스타뱅킹", "ㄱㅁ"],
        "category": "금융/핀테크",
        "description": "스타뱅킹 가입 시 스타프렌즈 적립금 제공",
        "app_url": "https://www.kbstar.com",
        "icon_color": "#FFBC00",
        "seed_code": "KBSTAR-GOLD-55",
        "seed_nick": "국민골드"
    },
    {
        "id": "naverpay",
        "name_ko": "네이버페이",
        "name_en": "Naver Pay",
        "aliases": ["네페", "네이버", "ㄴㅇㅂ"],
        "category": "금융/핀테크",
        "description": "초대 링크로 가입 시 네이버페이 포인트 5,000P",
        "app_url": "https://pay.naver.com",
        "icon_color": "#03C75A",
        "seed_code": "NPAY-GREEN-77",
        "seed_nick": "초록네페"
    },
    {
        "id": "kakaopay",
        "name_ko": "카카오페이",
        "name_en": "Kakao Pay",
        "aliases": ["카페", "카카오페이머니", "ㅋㅋㅇㅍㅇ"],
        "category": "금융/핀테크",
        "description": "친구 초대 시 페이머니 최대 5,000원 즉시 증정",
        "app_url": "https://www.kakaopay.com",
        "icon_color": "#FFEB00",
        "seed_code": "KPAY-MONEY-99",
        "seed_nick": "페이마스터"
    },
    {
        "id": "monimo",
        "name_ko": "모니모",
        "name_en": "Monimo",
        "aliases": ["삼성모니모", "삼성금융", "ㅁㄴㅁ"],
        "category": "앱테크",
        "description": "가입 시 젤리 및 스페셜 젤리(최대 3만원) 지급",
        "app_url": "https://www.monimo.com",
        "icon_color": "#1428A0",
        "seed_code": "MONI-JELLY-99",
        "seed_nick": "왕젤리"
    },
    {
        "id": "finda",
        "name_ko": "핀다",
        "name_en": "Finda",
        "aliases": ["대출비교", "ㅍㄷ"],
        "category": "금융/핀테크",
        "description": "친구 초대 시 스타벅스 기프티콘 및 현금 리워드",
        "app_url": "https://www.finda.co.kr",
        "icon_color": "#1B64DA",
        "seed_code": "FINDA-LOAN-55",
        "seed_nick": "핀다추천인"
    },
    {
        "id": "banksalad",
        "name_ko": "뱅크샐러드",
        "name_en": "Banksalad",
        "aliases": ["뱅샐", "유전자검사", "ㅂㅅㄹㄷ"],
        "category": "금융/핀테크",
        "description": "무료 유전자 검사권 및 자산관리 리워드",
        "app_url": "https://banksalad.com",
        "icon_color": "#00D084",
        "seed_code": "SALAD-DNA-77",
        "seed_nick": "샐러드유전자"
    },
    {
        "id": "miraeasset",
        "name_ko": "미래에셋증권",
        "name_en": "Mirae Asset",
        "aliases": ["미래에셋", "주식", "ㅁㄹㅇㅅ"],
        "category": "금융/핀테크",
        "description": "비대면 계좌 개설 시 미국 소수점 주식 2만원 증정",
        "app_url": "https://securities.miraeasset.com",
        "icon_color": "#F37321",
        "seed_code": "MIRAE-STOCK-100",
        "seed_nick": "미국주식왕"
    },
    {
        "id": "kiwoom",
        "name_ko": "키움증권",
        "name_en": "Kiwoom",
        "aliases": ["영웅문", "키움", "ㅋㅇㅈㄱ"],
        "category": "금융/핀테크",
        "description": "국내/해외주식 첫 거래 시 현금 4만원 증정",
        "app_url": "https://www.kiwoom.com",
        "icon_color": "#7B1FA2",
        "seed_code": "KIWOOM-HERO-88",
        "seed_nick": "영웅문러버"
    },
    {
        "id": "namu",
        "name_ko": "나무증권",
        "name_en": "Namu",
        "aliases": ["NH투자증권", "나무", "ㄴㅁ"],
        "category": "금융/핀테크",
        "description": "신규 계좌 개설 시 투자지원금 달러 지급",
        "app_url": "https://www.mynamu.com",
        "icon_color": "#00A05B",
        "seed_code": "NAMU-TREE-33",
        "seed_nick": "초록나무"
    },
    {
        "id": "koreainvestment",
        "name_ko": "한국투자증권",
        "name_en": "Korea Investment",
        "aliases": ["한투", "미니스탁", "ㅎㅌ"],
        "category": "금융/핀테크",
        "description": "미니스탁 해외주식 무료 지급 및 수수료 혜택",
        "app_url": "https://www.truefriend.com",
        "icon_color": "#003876",
        "seed_code": "HANTU-MINI-99",
        "seed_nick": "한국투자"
    },
    {
        "id": "signalplanner",
        "name_ko": "시그널플래너",
        "name_en": "Signal Planner",
        "aliases": ["보험비교", "해빗팩토리", "ㅅㄱㄴ"],
        "category": "금융/핀테크",
        "description": "내 보험 분석 시 스타벅스 아메리카노 즉시 증정",
        "app_url": "https://signalplanner.co.kr",
        "icon_color": "#0055FF",
        "seed_code": "SIGNAL-COFFEE-12",
        "seed_nick": "보험분석사"
    },
    {
        "id": "toss_securities",
        "name_ko": "토스증권",
        "name_en": "Toss Securities",
        "aliases": ["토증", "토스주식", "ㅌㅈ"],
        "category": "금융/핀테크",
        "description": "주식 계좌 개설 시 랜덤 인기 미국주식 1주 지급",
        "app_url": "https://tossinvest.com",
        "icon_color": "#0064FF",
        "seed_code": "TOSS-STOCK-FREE",
        "seed_nick": "랜덤주식러"
    },

    # --- 2. 쇼핑 / 이커머스 / 해외직구 / 리셀 (15개) ---
    {
        "id": "coupang",
        "name_ko": "쿠팡",
        "name_en": "Coupang",
        "aliases": ["로켓배송", "로켓와우", "ㅋㅍ"],
        "category": "쇼핑/이커머스",
        "description": "로켓와우 첫 달 무료 체험 및 5천원 캐시백",
        "app_url": "https://www.coupang.com",
        "icon_color": "#E30613",
        "seed_code": "COUP-ROCKET-99",
        "seed_nick": "와우회원"
    },
    {
        "id": "aliexpress",
        "name_ko": "알리익스프레스",
        "name_en": "AliExpress",
        "aliases": ["알리", "알리익스", "ㅇㄹ", "ㅇㄹㅇㅅㅍㄹㅅ"],
        "category": "쇼핑/이커머스",
        "description": "신규 가입 시 100원 딜 및 웰컴 쿠폰팩 4종",
        "app_url": "https://ko.aliexpress.com",
        "icon_color": "#FF4747",
        "seed_code": "ALI-SALE-8822",
        "seed_nick": "직구고수"
    },
    {
        "id": "temu",
        "name_ko": "테무",
        "name_en": "Temu",
        "aliases": ["티무", "ㅌㅁ"],
        "category": "쇼핑/이커머스",
        "description": "신규 앱 설치 시 10만원 상당 쿠폰팩 및 무료 선물 혜택",
        "app_url": "https://www.temu.com",
        "icon_color": "#FB7701",
        "seed_code": "TEMU-GIFT-100",
        "seed_nick": "테무선물"
    },
    {
        "id": "kurly",
        "name_ko": "컬리",
        "name_en": "Kurly",
        "aliases": ["마켓컬리", "ㅋㄹ", "ㅁㅋㅋㄹ"],
        "category": "쇼핑/이커머스",
        "description": "친구 초대 시 첫 주문 완료 후 적립금 5,000원",
        "app_url": "https://www.kurly.com",
        "icon_color": "#5F0080",
        "seed_code": "KURLY-FRESH-21",
        "seed_nick": "보라컬리"
    },
    {
        "id": "oasis",
        "name_ko": "오아시스마켓",
        "name_en": "Oasis Market",
        "aliases": ["오아시스", "새벽배송", "ㅇㅇㅅㅅ"],
        "category": "쇼핑/이커머스",
        "description": "친구 초대 시 첫 구매 후 추천인과 친구 모두 10,000원",
        "app_url": "https://www.oasis.co.kr",
        "icon_color": "#28A745",
        "seed_code": "OASIS-FRESH-10K",
        "seed_nick": "유기농마켓"
    },
    {
        "id": "karrot",
        "name_ko": "당근",
        "name_en": "Karrot",
        "aliases": ["당근마켓", "ㄷㄱ", "ㄷㄱㅁㅋ"],
        "category": "쇼핑/이커머스",
        "description": "동네 인증 및 친구 초대 시 당근머니 지급",
        "app_url": "https://www.daangn.com",
        "icon_color": "#FF6F0F",
        "seed_code": "DAANGN-MANNA-33",
        "seed_nick": "따뜻한온도"
    },
    {
        "id": "bungae",
        "name_ko": "번개장터",
        "name_en": "Bungaejangter",
        "aliases": ["번장", "번개페이", "ㅂㅈ"],
        "category": "쇼핑/이커머스",
        "description": "초대 코드 입력 시 번개포인트 2,000P 지급",
        "app_url": "https://m.bunjang.co.kr",
        "icon_color": "#FF0000",
        "seed_code": "BUNGAE-FAST-99",
        "seed_nick": "번개셀러"
    },
    {
        "id": "joonggonara",
        "name_ko": "중고나라",
        "name_en": "Joonggonara",
        "aliases": ["중나", "ㅈㄱㄴㄹ"],
        "category": "쇼핑/이커머스",
        "description": "안전결제 첫 결제 수수료 무료 쿠폰 증정",
        "app_url": "https://web.joongna.com",
        "icon_color": "#00A862",
        "seed_code": "JOONGNA-SAFE-77",
        "seed_nick": "중나평화"
    },
    {
        "id": "ohouse",
        "name_ko": "오늘의집",
        "name_en": "Ohouse",
        "aliases": ["오하우스", "ㅇㄴㅇㅈ"],
        "category": "쇼핑/이커머스",
        "description": "친구 초대 코드 입력 시 5,000원 즉시 할인 쿠폰",
        "app_url": "https://ohou.se",
        "icon_color": "#35C5F0",
        "seed_code": "OHOUSE-ROOM-55",
        "seed_nick": "인테리어장인"
    },
    {
        "id": "kream",
        "name_ko": "크림",
        "name_en": "KREAM",
        "aliases": ["크림스니커즈", "한정판", "ㅋㄹ"],
        "category": "쇼핑/이커머스",
        "description": "회원가입 시 2,000 포인트 즉시 적립",
        "app_url": "https://kream.co.kr",
        "icon_color": "#222222",
        "seed_code": "KREAM-SNEAK-33",
        "seed_nick": "나이키매니아"
    },
    {
        "id": "soldout",
        "name_ko": "솔드아웃",
        "name_en": "SoldOut",
        "aliases": ["무신사솔드아웃", "ㅅㄷㅇㅇ"],
        "category": "쇼핑/이커머스",
        "description": "추천코드 입력 가입 시 3,000P 즉시 적립",
        "app_url": "https://www.soldout.co.kr",
        "icon_color": "#000000",
        "seed_code": "SOLDOUT-VIP-88",
        "seed_nick": "스니커헤드"
    },
    {
        "id": "iherb",
        "name_ko": "아이허브",
        "name_en": "iHerb",
        "aliases": ["영양제", "직구", "ㅇㅇㅎㅂ"],
        "category": "쇼핑/이커머스",
        "description": "추천인 코드 입력 시 전 품목 5% 상시 할인 + 첫 구매 20%",
        "app_url": "https://kr.iherb.com",
        "icon_color": "#458500",
        "seed_code": "IHERB-DISCOUNT-5P",
        "seed_nick": "비타민매니아"
    },
    {
        "id": "elevenst",
        "name_ko": "11번가",
        "name_en": "11st",
        "aliases": ["십일번가", "우주패스", "11ㅂㄱ"],
        "category": "쇼핑/이커머스",
        "description": "우주패스 첫 달 100원 및 SK pay 포인트 적립",
        "app_url": "https://www.11st.co.kr",
        "icon_color": "#FA2828",
        "seed_code": "11ST-PASS-77",
        "seed_nick": "우주쇼퍼"
    },
    {
        "id": "gmarket",
        "name_ko": "G마켓",
        "name_en": "Gmarket",
        "aliases": ["지마켓", "스마일클럽", "ㅈㅁㅋ"],
        "category": "쇼핑/이커머스",
        "description": "스마일클럽 가입 시 스마일캐시 35,000원 즉시 캐시백",
        "app_url": "https://www.gmarket.co.kr",
        "icon_color": "#00B050",
        "seed_code": "GMARKET-SMILE-99",
        "seed_nick": "스마일캐시"
    },
    {
        "id": "ssg",
        "name_ko": "SSG닷컴",
        "name_en": "SSG.COM",
        "aliases": ["쓱닷컴", "이마트몰", "ㅅㄱ"],
        "category": "쇼핑/이커머스",
        "description": "첫 주문 1만원 할인 쿠폰 및 쓱머니 적립",
        "app_url": "https://www.ssg.com",
        "icon_color": "#FA5252",
        "seed_code": "SSG-ROCKET-100",
        "seed_nick": "쓱배송러"
    },

    # --- 3. 음식 / 배달 / 외식 (8개) ---
    {
        "id": "baemin",
        "name_ko": "배달의민족",
        "name_en": "Baemin",
        "aliases": ["배민", "배민원", "ㅂㅁ", "ㅂㄷㅇㅁㅈ"],
        "category": "음식배달",
        "description": "첫 주문 시 1만원 상당 웰컴 쿠폰팩 증정",
        "app_url": "https://baemin.com",
        "icon_color": "#2AC1BC",
        "seed_code": "BAEMIN-YUMMY-77",
        "seed_nick": "배민VIP"
    },
    {
        "id": "coupangeats",
        "name_ko": "쿠팡이츠",
        "name_en": "Coupang Eats",
        "aliases": ["쿠이", "쿠팡배달", "ㅋㅇ", "ㅋㅍㅇㅊ"],
        "category": "음식배달",
        "description": "와우회원 무제한 무료배달 및 5천원 할인 쿠폰",
        "app_url": "https://www.coupangeats.com",
        "icon_color": "#00A5FF",
        "seed_code": "EATS-FAST-88",
        "seed_nick": "치타배달"
    },
    {
        "id": "yogiyo",
        "name_ko": "요기요",
        "name_en": "Yogiyo",
        "aliases": ["요기패스", "ㅇㄱㅇ"],
        "category": "음식배달",
        "description": "첫 주문 시 최대 1만원 즉시 할인",
        "app_url": "https://www.yogiyo.co.kr",
        "icon_color": "#FA0050",
        "seed_code": "YOGI-PASS-12",
        "seed_nick": "요기패스러버"
    },
    {
        "id": "ddangyo",
        "name_ko": "땡겨요",
        "name_en": "Ddangyo",
        "aliases": ["신한배달", "ㄸㄱㅇ"],
        "category": "음식배달",
        "description": "신규 가입 첫 주문 시 5,000원 쿠폰 2장 지급",
        "app_url": "https://www.ddangyo.com",
        "icon_color": "#FF5900",
        "seed_code": "DDANG-DISCOUNT-5K",
        "seed_nick": "땡겨요러버"
    },
    {
        "id": "catchtable",
        "name_ko": "캐치테이블",
        "name_en": "Catchtable",
        "aliases": ["식당예약", "ㅋㅊㅌㅇㅂ"],
        "category": "음식배달",
        "description": "오마카세/파인다이닝 예약 시 5,000원 할인 쿠폰",
        "app_url": "https://app.catchtable.co.kr",
        "icon_color": "#FF2B2B",
        "seed_code": "CATCH-RESERVE-77",
        "seed_nick": "미식가"
    },
    {
        "id": "tabling",
        "name_ko": "테이블링",
        "name_en": "Tabling",
        "aliases": ["원격줄서기", "ㅌㅇㅂㄹ"],
        "category": "음식배달",
        "description": "테이블링 페이 충전 시 즉시 3,000원 페이백",
        "app_url": "https://www.tabling.co.kr",
        "icon_color": "#1C1C1E",
        "seed_code": "TABLING-LINE-99",
        "seed_nick": "줄서기달인"
    },
    {
        "id": "starbucks",
        "name_ko": "스타벅스",
        "name_en": "Starbucks",
        "aliases": ["스벅", "사이렌오더", "ㅅㅂ"],
        "category": "음식배달",
        "description": "e-카드 최초 등록 시 무료 음료 e-쿠폰(BOGO) 증정",
        "app_url": "https://www.starbucks.co.kr",
        "icon_color": "#006241",
        "seed_code": "STAR-COFFEE-BOGO",
        "seed_nick": "아메리카노"
    },
    {
        "id": "marketit",
        "name_ko": "마켓잇",
        "name_en": "Marketit",
        "aliases": ["인플루언서협찬", "ㅁㅋㅇ"],
        "category": "음식배달",
        "description": "외식/맛집 협찬 포인트 친구 초대 5,000P",
        "app_url": "https://marketit.asia",
        "icon_color": "#3B82F6",
        "seed_code": "MARKET-FOOD-5K",
        "seed_nick": "맛집체험러"
    },

    # --- 4. 패션 / 뷰티 (10개) ---
    {
        "id": "musinsa",
        "name_ko": "무신사",
        "name_en": "Musinsa",
        "aliases": ["무탠다드", "ㅁㅅㅅ"],
        "category": "패션/뷰티",
        "description": "친구 초대 시 둘 다 적립금 1,000원 + 첫 구매 할인 쿠폰",
        "app_url": "https://www.musinsa.com",
        "icon_color": "#000000",
        "seed_code": "MUSINSA-OOTD-88",
        "seed_nick": "패셔니스타"
    },
    {
        "id": "oliveyoung",
        "name_ko": "올리브영",
        "name_en": "Olive Young",
        "aliases": ["올영", "올리브", "ㅇㄹㅂㅇ", "ㅇㅇ"],
        "category": "패션/뷰티",
        "description": "신규 가입 시 4천원 할인 쿠폰 및 올영세일 적립금",
        "app_url": "https://www.oliveyoung.co.kr",
        "icon_color": "#94C11F",
        "seed_code": "OLIVE-BEAUTY-77",
        "seed_nick": "올영세일"
    },
    {
        "id": "ably",
        "name_ko": "에이블리",
        "name_en": "Ably",
        "aliases": ["에블", "ㅇㅇㅂㄹ"],
        "category": "패션/뷰티",
        "description": "신규 가입 시 5,000원 쿠폰팩 즉시 발급",
        "app_url": "https://m.a-bly.com",
        "icon_color": "#FF4975",
        "seed_code": "ABLY-STYLE-99",
        "seed_nick": "에이블리짱"
    },
    {
        "id": "zigzag",
        "name_ko": "지그재그",
        "name_en": "Zigzag",
        "aliases": ["직잭", "ㅈㄱㅈㄱ"],
        "category": "패션/뷰티",
        "description": "첫 구매 20% 할인 쿠폰 및 직진배송 무료배송",
        "app_url": "https://zigzag.kr",
        "icon_color": "#FF2D78",
        "seed_code": "ZIGZAG-DIRECT-11",
        "seed_nick": "직진배송"
    },
    {
        "id": "29cm",
        "name_ko": "29CM",
        "name_en": "29CM",
        "aliases": ["이십구센티", "29씨엠", "ㅇㅅㄱ"],
        "category": "패션/뷰티",
        "description": "첫 결제 15% 할인 쿠폰 및 추천인 마일리지 5,000P",
        "app_url": "https://www.29cm.co.kr",
        "icon_color": "#000000",
        "seed_code": "29CM-SENSE-77",
        "seed_nick": "감성쇼퍼"
    },
    {
        "id": "wconcept",
        "name_ko": "W컨셉",
        "name_en": "W Concept",
        "aliases": ["더블유컨셉", "ㄷㅂㅇㅋㅅ"],
        "category": "패션/뷰티",
        "description": "디자이너 브랜드 10% 쿠폰 및 5,000원 할인권",
        "app_url": "https://www.wconcept.co.kr",
        "icon_color": "#111111",
        "seed_code": "WCONCEPT-BRAND-12",
        "seed_nick": "디자이너룩"
    },
    {
        "id": "brandi",
        "name_ko": "브랜디",
        "name_en": "Brandi",
        "aliases": ["하루배송", "ㅂㄹㄷ"],
        "category": "패션/뷰티",
        "description": "전 상품 무료배송 및 친구 초대 1,000P 즉시 지급",
        "app_url": "https://www.brandi.co.kr",
        "icon_color": "#FF2553",
        "seed_code": "BRANDI-FREE-100",
        "seed_nick": "하루배송러"
    },
    {
        "id": "hiver",
        "name_ko": "하이버",
        "name_en": "Hiver",
        "aliases": ["남성쇼핑", "ㅎㅇㅂ"],
        "category": "패션/뷰티",
        "description": "남자 쇼핑앱 첫 구매 1만원 쿠폰팩",
        "app_url": "https://www.hiver.co.kr",
        "icon_color": "#1D1D1F",
        "seed_code": "HIVER-MAN-55",
        "seed_nick": "남친룩"
    },
    {
        "id": "queenit",
        "name_ko": "퀸잇",
        "name_en": "Queenit",
        "aliases": ["4050패션", "ㅋㅇ"],
        "category": "패션/뷰티",
        "description": "가입 즉시 백화점 브랜드 10만원 쿠폰팩 지급",
        "app_url": "https://www.queenit.kr",
        "icon_color": "#E91E63",
        "seed_code": "QUEEN-STYLE-77",
        "seed_nick": "우아한퀸"
    },
    {
        "id": "trenbe",
        "name_ko": "트렌비",
        "name_en": "Trenbe",
        "aliases": ["명품쇼핑", "ㅌㄹㅂ"],
        "category": "패션/뷰티",
        "description": "명품 구매 시 5만원 웰컴 쿠폰팩 즉시 발급",
        "app_url": "https://www.trenbe.com",
        "icon_color": "#333333",
        "seed_code": "TRENBE-LUXURY-88",
        "seed_nick": "명품러버"
    },

    # --- 5. 앱테크 / 리워드 / 설문 (12개) ---
    {
        "id": "tiktok_lite",
        "name_ko": "틱톡 라이트",
        "name_en": "TikTok Lite",
        "aliases": ["틱톡", "틱라", "ㅌㅌ", "ㅌㅌㄹㅇㅌ"],
        "category": "앱테크",
        "description": "친구 초대 출석 시 최대 3만원 상당 현금 포인트 지급",
        "app_url": "https://lite.tiktok.com",
        "icon_color": "#FE2C55",
        "seed_code": "TIKTOK-CASH-77",
        "seed_nick": "매일출석"
    },
    {
        "id": "cashwalk",
        "name_ko": "캐시워크",
        "name_en": "Cashwalk",
        "aliases": ["캐워크", "만보기", "ㅋㅅㅇㅋ"],
        "category": "앱테크",
        "description": "추천인 코드 입력 시 1,000캐시 즉시 지급",
        "app_url": "https://cashwalk.com",
        "icon_color": "#FFD000",
        "seed_code": "CASH-WALK-1000",
        "seed_nick": "만보걷기"
    },
    {
        "id": "cashdoc",
        "name_ko": "캐시닥",
        "name_en": "Cashdoc",
        "aliases": ["용돈퀴즈", "ㅋㅅㄷ"],
        "category": "앱테크",
        "description": "가입 시 1,000캐시 + 매일 병원 리뷰 및 퀴즈 리워드",
        "app_url": "https://cashdoc.me",
        "icon_color": "#00B894",
        "seed_code": "CASHDOC-QUIZ-88",
        "seed_nick": "퀴즈왕"
    },
    {
        "id": "challengers",
        "name_ko": "챌린저스",
        "name_en": "Challengers",
        "aliases": ["미라클모닝", "습관형성", "ㅊㄹㅈㅅ"],
        "category": "앱테크",
        "description": "추천코드 입력 시 100% 전액 환급 챌린지 상금 지원",
        "app_url": "https://chlngers.com",
        "icon_color": "#F03E3E",
        "seed_code": "CHLNG-HABIT-99",
        "seed_nick": "미라클모닝"
    },
    {
        "id": "balosodeuk",
        "name_ko": "발로소득",
        "name_en": "Balosodeuk",
        "aliases": ["일상지원금", "ㅂㄹㅅㄷ"],
        "category": "앱테크",
        "description": "친구 초대 시 일상지원금 1,000코인 즉시 충전",
        "app_url": "https://balosodeuk.com",
        "icon_color": "#3B82F6",
        "seed_code": "BALO-COIN-1000",
        "seed_nick": "발로소득러"
    },
    {
        "id": "timespread",
        "name_ko": "타임스프레드",
        "name_en": "Timespread",
        "aliases": ["폰잠금", "시간표", "ㅌㅇㅅㅍㄹㄷ"],
        "category": "앱테크",
        "description": "잠금화면 열 때마다 캐시 적립 + 친구 초대 1,000캐시",
        "app_url": "https://timespread.co.kr",
        "icon_color": "#6C5CE7",
        "seed_code": "TIME-LOCK-55",
        "seed_nick": "폰잠금러"
    },
    {
        "id": "moneywalk",
        "name_ko": "머니워크",
        "name_en": "Moneywalk",
        "aliases": ["건강만보기", "ㅁㄴㅇㅋ"],
        "category": "앱테크",
        "description": "5,000보만 걸어도 매일 포인트 지급 + 친구 추천 1,000P",
        "app_url": "https://moneywalk.com",
        "icon_color": "#10B981",
        "seed_code": "MONEY-WALK-777",
        "seed_nick": "만보러버"
    },
    {
        "id": "okcashbag",
        "name_ko": "OK캐쉬백",
        "name_en": "OK Cashbag",
        "aliases": ["오케이캐쉬백", "ㅇㅋㅇㅋㅅㅂ"],
        "category": "앱테크",
        "description": "오락(O락) 출석체크 및 친구 초대 1,000P",
        "app_url": "https://www.okcashbag.com",
        "icon_color": "#ED1C24",
        "seed_code": "OKCASH-OROC-99",
        "seed_nick": "오케이적립"
    },
    {
        "id": "panelnow",
        "name_ko": "패널나우",
        "name_en": "PanelNow",
        "aliases": ["설문조사", "ㅍㄴㄴㅇ"],
        "category": "앱테크",
        "description": "가입 시 300P 즉시 적립 + 2,000P부터 현금 교환",
        "app_url": "https://www.panelnow.co.kr",
        "icon_color": "#FF7675",
        "seed_code": "PANEL-SURVEY-33",
        "seed_nick": "설문조사왕"
    },
    {
        "id": "embrain",
        "name_ko": "엠브레인 패널파워",
        "name_en": "Embrain Panel Power",
        "aliases": ["패널파워", "엠브레인", "ㅇㅂㄹㅇ"],
        "category": "앱테크",
        "description": "가입 후 일주일 간 2,500원 적립 보장 + 추천 적립",
        "app_url": "https://www.panel.co.kr",
        "icon_color": "#0984E3",
        "seed_code": "EMBRAIN-POWER-1",
        "seed_nick": "리서치패널"
    },
    {
        "id": "surveylink",
        "name_ko": "서베이링크",
        "name_en": "SurveyLink",
        "aliases": ["서베이", "ㅅㅂㅇㄹㅋ"],
        "category": "앱테크",
        "description": "신규 가입 시 1,000P 및 모바일 영화관람권 추첨",
        "app_url": "https://www.surveylink.co.kr",
        "icon_color": "#E17055",
        "seed_code": "SURVEY-MOVIE-77",
        "seed_nick": "서베이러"
    },
    {
        "id": "yafit",
        "name_ko": "야핏무브",
        "name_en": "Yafit Move",
        "aliases": ["자전거만보기", "ㅇㅍㅁㅂ"],
        "category": "앱테크",
        "description": "걸음 및 라이딩으로 마일리지 적립 + 친구 초대 1,000M",
        "app_url": "https://yafit.co.kr",
        "icon_color": "#FDCB6E",
        "seed_code": "YAFIT-RIDE-55",
        "seed_nick": "라이더"
    },

    # --- 6. 가상자산 / 크립토 / 거래소 (10개) ---
    {
        "id": "upbit",
        "name_ko": "업비트",
        "name_en": "Upbit",
        "aliases": ["비트코인", "두나무", "ㅇㅂㅌ"],
        "category": "가상자산/재테크",
        "description": "케이뱅크 실명계좌 연동 및 첫 거래 이벤트",
        "app_url": "https://upbit.com",
        "icon_color": "#093687",
        "seed_code": "UPBIT-COIN-777",
        "seed_nick": "코인마스터"
    },
    {
        "id": "bithumb",
        "name_ko": "빗썸",
        "name_en": "Bithumb",
        "aliases": ["빗섬", "ㅂㅅ"],
        "category": "가상자산/재테크",
        "description": "신규 가입 시 2만원 상당 웰컴 가상자산 지급",
        "app_url": "https://www.bithumb.com",
        "icon_color": "#F37321",
        "seed_code": "BITHUMB-PRO-88",
        "seed_nick": "빗썸매니아"
    },
    {
        "id": "coinone",
        "name_ko": "코인원",
        "name_en": "Coinone",
        "aliases": ["코인", "ㅋㅇㅇ"],
        "category": "가상자산/재테크",
        "description": "거래 수수료 평생 20% 페이백 혜택",
        "app_url": "https://coinone.co.kr",
        "icon_color": "#1F53FF",
        "seed_code": "COINONE-VIP-99",
        "seed_nick": "수수료페이백"
    },
    {
        "id": "korbit",
        "name_ko": "코빗",
        "name_en": "Korbit",
        "aliases": ["신한코빗", "ㅋㅂ"],
        "category": "가상자산/재테크",
        "description": "추천코드 입력 가입 시 10,000원 상당 비트코인 증정",
        "app_url": "https://korbit.co.kr",
        "icon_color": "#1B2A4A",
        "seed_code": "KORBIT-BTC-10K",
        "seed_nick": "비트코인홀더"
    },
    {
        "id": "gopax",
        "name_ko": "고팍스",
        "name_en": "GOPAX",
        "aliases": ["전북은행고팍스", "ㄱㅍㅅ"],
        "category": "가상자산/재테크",
        "description": "계좌 등록 및 첫 거래 시 5,000원 상당 원화 지급",
        "app_url": "https://www.gopax.co.kr",
        "icon_color": "#1E88E5",
        "seed_code": "GOPAX-BONUS-5K",
        "seed_nick": "고팍스러버"
    },
    {
        "id": "binance",
        "name_ko": "바이낸스",
        "name_en": "Binance",
        "aliases": ["해외거래소", "바낸", "ㅂㅇㄴㅅ"],
        "category": "가상자산/재테크",
        "description": "레퍼럴 가입 시 거래 수수료 최대 20% 평생 할인",
        "app_url": "https://www.binance.com",
        "icon_color": "#F3BA2F",
        "seed_code": "BINANCE-FEE-20P",
        "seed_nick": "바낸고수"
    },
    {
        "id": "bybit",
        "name_ko": "바이비트",
        "name_en": "Bybit",
        "aliases": ["선물거래", "ㅂㅇㅂƮ"],
        "category": "가상자산/재테크",
        "description": "수수료 20% 할인 및 최대 $30,000 증정금 이벤트",
        "app_url": "https://www.bybit.com",
        "icon_color": "#FB923C",
        "seed_code": "BYBIT-BONUS-20P",
        "seed_nick": "선물트레이더"
    },
    {
        "id": "bitget",
        "name_ko": "비트겟",
        "name_en": "Bitget",
        "aliases": ["카피트레이딩", "ㅂƮㄱ"],
        "category": "가상자산/재테크",
        "description": "수수료 평생 50% 할인 + 신규 가입 $1,000 리워드",
        "app_url": "https://www.bitget.com",
        "icon_color": "#00F0FF",
        "seed_code": "BITGET-FEE-50P",
        "seed_nick": "카피트레이더"
    },
    {
        "id": "okx",
        "name_ko": "OKX",
        "name_en": "OKX",
        "aliases": ["오케이엑스", "ㅇㅋㅇㅅ"],
        "category": "가상자산/재테크",
        "description": "미스터리 박스 열고 최대 $10,000 상당 코인 당첨",
        "app_url": "https://www.okx.com",
        "icon_color": "#000000",
        "seed_code": "OKX-BOX-10K",
        "seed_nick": "미스터리박스"
    },
    {
        "id": "gateio",
        "name_ko": "게이트아이오",
        "name_en": "Gate.io",
        "aliases": ["게이트", "ㄱㅇƮㅇㅇㅇ"],
        "category": "가상자산/재테크",
        "description": "상장 초기 신규 알트코인 에어드랍 및 20% 수수료 할인",
        "app_url": "https://www.gate.io",
        "icon_color": "#2196F3",
        "seed_code": "GATE-AIRDROP-20",
        "seed_nick": "에어드랍헌터"
    },

    # --- 7. 여행 / 숙박 / 모빌리티 (10개) ---
    {
        "id": "yanolja",
        "name_ko": "야놀자",
        "name_en": "Yanolja",
        "aliases": ["숙박", "여행", "ㅇㄴㅈ"],
        "category": "여행/숙박",
        "description": "친구 초대 시 코인 2,000P 및 5만원 쿠폰팩",
        "app_url": "https://www.yanolja.com",
        "icon_color": "#FF0055",
        "seed_code": "YANO-STAY-55",
        "seed_nick": "호캉스러버"
    },
    {
        "id": "goodchoice",
        "name_ko": "여기어때",
        "name_en": "Good Choice",
        "aliases": ["여기", "숙소", "ㅇㄱㅇㄸ"],
        "category": "여행/숙박",
        "description": "신규 가입 총 15만원 쿠폰팩 + 친구 추천 포인트",
        "app_url": "https://www.goodchoice.kr",
        "icon_color": "#F7323F",
        "seed_code": "GOOD-CHOICE-88",
        "seed_nick": "여행러버"
    },
    {
        "id": "myrealtrip",
        "name_ko": "마이리얼트립",
        "name_en": "MyRealTrip",
        "aliases": ["마리트", "해외투어", "ㅁㅇㄹㅇㅌㄹ"],
        "category": "여행/숙박",
        "description": "초대 링크 가입 시 즉시 사용 가능한 5,000원 쿠폰 지급",
        "app_url": "https://www.myrealtrip.com",
        "icon_color": "#51ABF3",
        "seed_code": "MYREAL-TOUR-5K",
        "seed_nick": "자유여행러"
    },
    {
        "id": "agoda",
        "name_ko": "아고다",
        "name_en": "Agoda",
        "aliases": ["호텔예약", "ㅇㄱㄷ"],
        "category": "여행/숙박",
        "description": "추천 초대 시 전 세계 호텔 10% 추가 할인 쿠폰",
        "app_url": "https://www.agoda.com",
        "icon_color": "#008577",
        "seed_code": "AGODA-HOTEL-10P",
        "seed_nick": "글로벌트래블"
    },
    {
        "id": "tripcom",
        "name_ko": "트립닷컴",
        "name_en": "Trip.com",
        "aliases": ["항공권", "ㅌㄹㄷㅋ"],
        "category": "여행/숙박",
        "description": "항공권/호텔 예약 시 트립코인 리워드 및 할인",
        "app_url": "https://kr.trip.com",
        "icon_color": "#2681FF",
        "seed_code": "TRIP-FLIGHT-COIN",
        "seed_nick": "항공권특가"
    },
    {
        "id": "klook",
        "name_ko": "클룩",
        "name_en": "Klook",
        "aliases": ["입장권", "투어패스", "ㅋㄹ"],
        "category": "여행/숙박",
        "description": "친구 초대 링크 가입 시 3,500원 할인 쿠폰 즉시 발급",
        "app_url": "https://www.klook.com",
        "icon_color": "#FF5B00",
        "seed_code": "KLOOK-PASS-3500",
        "seed_nick": "액티비티러버"
    },
    {
        "id": "airbnb",
        "name_ko": "에어비앤비",
        "name_en": "Airbnb",
        "aliases": ["숙소공유", "ㅇㅇㅂㅇㅂ"],
        "category": "여행/숙박",
        "description": "친구 초대 시 첫 여행 완료 후 여행 크레딧 지급",
        "app_url": "https://www.airbnb.co.kr",
        "icon_color": "#FF5A5F",
        "seed_code": "AIRBNB-STAY-CREDIT",
        "seed_nick": "감성숙소"
    },
    {
        "id": "socar",
        "name_ko": "쏘카",
        "name_en": "Socar",
        "aliases": ["카셰어링", "렌터카", "ㅆㅋ"],
        "category": "여행/숙박",
        "description": "친구 추천 시 1만원 할인 쿠폰 + 추천인 크레딧",
        "app_url": "https://www.socar.kr",
        "icon_color": "#00A8FF",
        "seed_code": "SOCAR-DRIVE-10K",
        "seed_nick": "드라이버"
    },
    {
        "id": "greencar",
        "name_ko": "그린카",
        "name_en": "Greencar",
        "aliases": ["카셰어링", "롯데렌탈", "ㄱㄹㅋ"],
        "category": "여행/숙박",
        "description": "추천인 가입 시 1만원 무료 이용권 즉시 지급",
        "app_url": "https://www.greencar.co.kr",
        "icon_color": "#00C300",
        "seed_code": "GREEN-RENT-100",
        "seed_nick": "그린드라이브"
    },
    {
        "id": "tmoney_go",
        "name_ko": "티머니GO",
        "name_en": "Tmoney GO",
        "aliases": ["티머니고", "고속버스", "ㅌㅁㄴㄱ"],
        "category": "여행/숙박",
        "description": "고속/시외버스 및 따릉이 이용 시 GO마일리지 적립",
        "app_url": "https://tmoneygo.tmoney.co.kr",
        "icon_color": "#003478",
        "seed_code": "TMONEY-GO-500",
        "seed_nick": "환승왕"
    },

    # --- 8. 도서 / 웹툰 / 콘텐츠 (6개) ---
    {
        "id": "ridi",
        "name_ko": "리디",
        "name_en": "Ridi",
        "aliases": ["리디북스", "웹툰", "ㄹㄷ"],
        "category": "도서/구독",
        "description": "친구 초대 시 리디캐시 포인트 즉시 지급",
        "app_url": "https://ridibooks.com",
        "icon_color": "#1F8CE6",
        "seed_code": "RIDI-BOOK-77",
        "seed_nick": "독서왕"
    },
    {
        "id": "millie",
        "name_ko": "밀리의서재",
        "name_en": "Millie",
        "aliases": ["밀리", "전자책", "ㅁㄹㅇㅅㅈ"],
        "category": "도서/구독",
        "description": "첫 달 무료 구독 및 친구 초대 1개월 추가 연장",
        "app_url": "https://www.millie.co.kr",
        "icon_color": "#FFEB00",
        "seed_code": "MILLIE-READ-99",
        "seed_nick": "밀리구독자"
    },
    {
        "id": "welaaa",
        "name_ko": "윌라 오디오북",
        "name_en": "Welaaa",
        "aliases": ["윌라", "오디오북", "ㅇㄹ"],
        "category": "도서/구독",
        "description": "친구 초대 시 1개월 무료 체험 쿠폰 추가 지급",
        "app_url": "https://www.welaaa.com",
        "icon_color": "#FF4500",
        "seed_code": "WELAAA-AUDIO-FREE",
        "seed_nick": "귀로듣는책"
    },
    {
        "id": "kakaopage",
        "name_ko": "카카오페이지",
        "name_en": "KakaoPage",
        "aliases": ["웹소설", "카카페", "ㅋㅋㅇㅍㅇㅈ"],
        "category": "도서/구독",
        "description": "친구 초대 시 최대 5,000캐시 뽑기권 지급",
        "app_url": "https://page.kakao.com",
        "icon_color": "#FEE500",
        "seed_code": "PAGE-CASH-LUCKY",
        "seed_nick": "웹소설매니아"
    },
    {
        "id": "series",
        "name_ko": "네이버 시리즈",
        "name_en": "Naver Series",
        "aliases": ["쿠키", "시리즈", "ㅅㄹㅈ"],
        "category": "도서/구독",
        "description": "쿠키 충전 및 친구 초대 무료 쿠키 지급",
        "app_url": "https://series.naver.com",
        "icon_color": "#03C75A",
        "seed_code": "SERIES-COOKIE-50",
        "seed_nick": "쿠키굽는사람"
    },
    {
        "id": "watcha",
        "name_ko": "왓챠",
        "name_en": "Watcha",
        "aliases": ["왓챠피디아", "영화추천", "ㅇㅊ"],
        "category": "도서/구독",
        "description": "친구 초대 시 2주 프리미엄 무료 이용권 증정",
        "app_url": "https://watcha.com",
        "icon_color": "#FF0558",
        "seed_code": "WATCHA-PREMIUM-14",
        "seed_nick": "영화광"
    },

    # --- 9. 통신 / 알뜰폰 / IT / 생산성 (8개) ---
    {
        "id": "moyo",
        "name_ko": "모요",
        "name_en": "Moyo",
        "aliases": ["알뜰폰비교", "모두의요금제", "ㅁㅇ"],
        "category": "금융/핀테크",
        "description": "알뜰폰 개통 시 네이버페이 3만원 + 스타벅스 기프티콘",
        "app_url": "https://www.moyo.plan",
        "icon_color": "#2563EB",
        "seed_code": "MOYO-PLAN-30K",
        "seed_nick": "알뜰폰박사"
    },
    {
        "id": "toss_mobile",
        "name_ko": "토스모바일",
        "name_en": "Toss Mobile",
        "aliases": ["토스알뜰폰", "ㅌㅅㅁㅂㅇ"],
        "category": "금융/핀테크",
        "description": "친구 추천으로 요금제 가입 시 토스포인트 캐시백",
        "app_url": "https://toss.im/mobile",
        "icon_color": "#0064FF",
        "seed_code": "TOSS-MOB-CASH",
        "seed_nick": "토스통신"
    },
    {
        "id": "freet",
        "name_ko": "프리티",
        "name_en": "FreeT",
        "aliases": ["프리텔레콤", "알뜰폰", "ㅍㄹƮ"],
        "category": "라이프스타일",
        "description": "친구 추천 셀프개통 시 신세계 상품권 1만원",
        "app_url": "https://www.freet.co.kr",
        "icon_color": "#E91E63",
        "seed_code": "FREET-SELF-10K",
        "seed_nick": "프리티러버"
    },
    {
        "id": "notion",
        "name_ko": "노션",
        "name_en": "Notion",
        "aliases": ["노트", "생산성", "ㄴㅅ"],
        "category": "라이프스타일",
        "description": "추천인 링크 가입 시 $10 크레딧 지급",
        "app_url": "https://www.notion.so",
        "icon_color": "#000000",
        "seed_code": "NOTION-CREDIT-10",
        "seed_nick": "생산성고수"
    },
    {
        "id": "canva",
        "name_ko": "캔바",
        "name_en": "Canva",
        "aliases": ["디자인", "카드뉴스", "ㅋㅂ"],
        "category": "라이프스타일",
        "description": "친구 초대 시 Canva Pro 프리미엄 요소 무료 이용권",
        "app_url": "https://www.canva.com",
        "icon_color": "#00C4CC",
        "seed_code": "CANVA-DESIGN-PRO",
        "seed_nick": "디자인장인"
    },
    {
        "id": "apple",
        "name_ko": "애플",
        "name_en": "Apple",
        "aliases": ["아이폰", "맥북", "ㅇㅍ"],
        "category": "쇼핑/이커머스",
        "description": "학생 교육 할인 및 기기 구매 시 액세서리 쿠폰 제공",
        "app_url": "https://www.apple.com/kr",
        "icon_color": "#1C1C1E",
        "seed_code": "APPL-KR-STUDENT-01",
        "seed_nick": "맥북에어매니아"
    },
    {
        "id": "choco",
        "name_ko": "초코",
        "name_en": "Choco",
        "aliases": ["초콜릿", "초코앱", "ㅊㅋ"],
        "category": "라이프스타일",
        "description": "가입 시 웰컴 초콜릿 포인트 3,000P 지급",
        "app_url": "https://choco.example.com",
        "icon_color": "#8B5A2B",
        "seed_code": "CHOCO-SWEET-77",
        "seed_nick": "달콤초코"
    }
]

def build_dataset():
    apps = []
    referrals = []

    for app in APPS_DATA:
        app_entry = {
            "id": app["id"],
            "name_ko": app["name_ko"],
            "name_en": app["name_en"],
            "aliases": app["aliases"],
            "category": app["category"],
            "description": app["description"],
            "app_url": app["app_url"],
            "icon_color": app["icon_color"]
        }
        apps.append(app_entry)

        # 1~2개의 기본 추천코드 대기열 생성
        ref_id = f"ref_{app['id']}_1"
        referrals.append({
            "id": ref_id,
            "app_id": app["id"],
            "code": app["seed_code"],
            "nickname": app["seed_nick"],
            "copy_count": 1
        })

    return {"apps": apps, "referrals": referrals}

if __name__ == "__main__":
    data = build_dataset()
    print(f"총 {len(data['apps'])}개 앱 및 {len(data['referrals'])}개 추천인 코드 생성 준비 완료!")

    # context/sample_apps.json 저장
    context_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "context", "sample_apps.json"))
    runtime_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "context", "runtime_data.json"))

    with open(context_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(runtime_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("sample_apps.json 및 runtime_data.json 파일 갱신 완료!")
