# 260929 데이터 사전 (Data Dictionary) - 공정 추천인 플랫폼

본 문서는 공정 추천인 플랫폼(추천인.com)의 원천 데이터 구조 및 엔티티 스펙을 정의합니다.

---

## 1. 앱/서비스 마스터 (Apps)
각 서비스 및 앱의 기본 정보와 검색 인덱싱용 필드를 포함합니다.

| 필드명 | 타입 | 영문 명칭 | 제약조건 | 설명 / 예시 |
| :--- | :--- | :--- | :--- | :--- |
| `id` | string | App ID | PK, Unique | 앱 고유 식별자 (예: `choco`, `toss`, `apple`, `kream`) |
| `name_ko` | string | Name (Korean) | Not Null | 한글 서비스명 (예: "초코", "토스", "애플", "크림") |
| `name_en` | string | Name (English) | Not Null | 영문 서비스명 (예: "Choco", "Toss", "Apple", "KREAM") |
| `chosung` | string | Chosung Index | Generated | 검색용 한글 초성 (예: "ㅊㅋ", "ㅌㅅ", "ㅇㅍ", "ㅋㄹ") |
| `category` | string | Category | Not Null | 카테고리 (예: "금융/핀테크", "쇼핑/이커머스", "라이프스타일", "가상자산") |
| `description` | string | Description | Optional | 추천인 혜택 요약 (예: "가입 시 5,000원 적립금 즉시 지급") |
| `app_url` | string | App URL | Optional | 앱스토어 또는 웹 가입 바로가기 URL |
| `icon_color` | string | Icon Color | Optional | UI 표시용 뱃지 색상 (Hex 코드) |

---

## 2. 추천인 코드 대기열 (Referral Code Queue)
사용자들이 등록한 추천인 코드와 공정 분배 상태를 관리하는 핵심 모델입니다.

| 필드명 | 타입 | 영문 명칭 | 제약조건 | 설명 / 예시 |
| :--- | :--- | :--- | :--- | :--- |
| `id` | string | Code ID | PK, Unique | 추천인 코드 항목 고유 ID (예: `ref_choco_001`) |
| `app_id` | string | App ID | FK (Apps.id) | 대상 앱 식별자 |
| `code` | string | Referral Code | Not Null | 실제 추천인 코드 또는 추천 링크 (예: `CHOCO-7788`, `TOSS9981`) |
| `nickname` | string | Registrant Nick | Not Null | 등록자 닉네임 (익명 처리 지원, 예: "민트초코", "테크러버") |
| `created_at` | datetime | Created At | ISO-8601 | 최초 큐 진입 일시 |
| `last_copied_at` | datetime | Last Copied At | Nullable | 마지막으로 복사된 일시 |
| `copy_count` | integer | Copy Count | Default: 0 | 누적 복사 횟수 |
| `status` | string | Queue Status | Enum | 현재 상태 (`ACTIVE`: 대기 중, `COOLDOWN`: 복사 후 쿨다운 중) |
| `cooldown_until` | datetime | Cooldown Until | Nullable | 쿨다운 해제 예정 일시 (복사 시각 + 10분) |
| `queue_order` | integer | Queue Order | Auto-sort | 현재 대기열 순번 (1 = 최우선 노출 순위) |

---

## 3. 복사 이벤트 로그 (Copy Event Logs)
복사 이력 추적 및 매크로 어뷰징 방지용 로그 모델입니다.

| 필드명 | 타입 | 영문 명칭 | 제약조건 | 설명 / 예시 |
| :--- | :--- | :--- | :--- | :--- |
| `log_id` | string | Log ID | PK, Unique | 이벤트 로그 ID |
| `code_id` | string | Code ID | FK | 복사된 추천인 코드 ID |
| `app_id` | string | App ID | FK | 대상 앱 ID |
| `client_ip_hash`| string | IP Hash | Masked | 복사 요청자 IP의 단방향 해시값 (개인정보 보호) |
| `timestamp` | datetime | Timestamp | ISO-8601 | 복사 발생 일시 |
