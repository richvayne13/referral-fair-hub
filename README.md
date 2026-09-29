# 추천인.com (공정 추천인 품앗이 플랫폼)

> **"특정인의 독점과 매크로 도배 없는 세상에서 가장 공정한 추천인 공유 커뮤니티"**

---

## 🌟 핵심 특징
1. **선입선출(FIFO) 회전 큐 바통터치**: 대기열에서 가장 오래 기다린 사람의 코드가 1순위로 노출되며, 복사 즉시 10분 쿨다운과 함께 대기열 맨 뒤로 자동 회전합니다.
2. **실시간 초성/다국어 검색**: `초` (음절), `a` (영문), `ㅊㅋ` (초성) 등 무엇을 검색하든 0.1초 만에 스마트 자동완성됩니다.
3. **원클릭 복사 & 딥링크**: 코드 복사와 동시에 해당 공식 앱/웹사이트로 즉시 이동할 수 있는 가입 링크를 제공합니다.
4. **투명한 대기열 공개**: 대기 중인 순번과 누적 복사 횟수를 투명하게 시각화합니다.

---

## 🚀 로컬 실행 방법 (Windows)
1. `run.bat` 파일을 더블클릭합니다.
2. 웹 브라우저가 자동으로 실행되며 `http://localhost:8080`에 접속됩니다.

---

## 🌐 무료 온라인 사이트 배포 가이드 (3분 완성)

누구나 인터넷에서 접속할 수 있는 실제 웹사이트로 배포하는 가장 쉽고 추천하는 방법입니다.

### [방법 1] Render.com 배포 (가장 추천 · 파이썬 백엔드 완벽 무료 지원)
1. 본 프로젝트를 본인의 **GitHub 저장소**에 Push합니다:
   ```bash
   git remote add origin https://github.com/<본인아이디>/<저장소이름>.git
   git branch -M main
   git push -u origin main
   ```
2. **[Render.com](https://render.com)**에 회원가입 (GitHub 계정으로 1초 로그인).
3. **[New +]** 버튼 클릭 $\rightarrow$ **[Web Service]** 선택.
4. 방금 Push한 GitHub 저장소를 선택하고 **[Connect]** 클릭.
5. 설정 입력:
   * **Name**: `fair-referral` (원하는 이름)
   * **Region**: `Singapore` (한국과 가장 가까움)
   * **Branch**: `main`
   * **Runtime**: `Python`
   * **Build Command**: 비워둠 (또는 `pip install -r requirements.txt`)
   * **Start Command**: `python app.py`
   * **Instance Type**: **Free (무료)** 선택
6. **[Deploy Web Service]** 클릭!
   * 1~2분 후 `https://fair-referral.onrender.com` 과 같은 **전 세계 어디서든 접속 가능한 무료 온라인 주소**가 생성됩니다!

---

### [방법 2] 나만의 도메인 연결 (`www.추천인.com`)
1. **가비아(Gabia)**, **후이즈**, 또는 **Cloudflare** 등에서 원하는 도메인(예: `추천인.com` 또는 `referral-fair.kr`)을 구매합니다.
2. Render 대시보드의 **Settings $\rightarrow$ Custom Domains** 메뉴로 이동합니다.
3. 구매한 도메인을 입력하고 안내되는 CNAME 레코드를 도메인 구매 사이트의 DNS 설정에 입력하면 연결 완료! (무료 SSL/HTTPS 자동 발급)
