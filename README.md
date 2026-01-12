# PERSO Auto Tester

🤖 PERSO AI 더빙 서비스 자동화 QA 테스트 시스템

## 🎯 기능

- 🔐 로그인 자동화
- 📤 영상 업로드 자동화  
- 🌏 번역 프로세스 검증
- 📡 실시간 로그 스트리밍
- 📸 자동 스크린샷 캡처

---

## 🚀 빠른 시작

### 1. 설치
```bash
# 저장소 클론
git clone https://github.com/Griotold/perso-auto-tester.git
cd perso-auto-tester

# 의존성 설치
pdm install

# Playwright 브라우저 설치
pdm run playwright install chromium
```

### 2. 환경변수 설정

`.env` 파일 생성:
```bash
cp .env.example .env
```

`.env` 파일 수정:
```env
PERSO_EMAIL=your-email@eastsoft.com
PERSO_PASSWORD=your-password
VIDEO_FILE_PATH=./test_videos/sample.mp4
HEADLESS=true
```

### 3. 실행

#### 개발자 모드 (크롬 브라우저 보기)
```bash
# 로그인 테스트
pdm run test:login

# 업로드 + 번역 테스트
pdm run test:upload
```

#### 웹 UI 모드 (QA/상사용)
```bash
# 개발 서버
pdm run dev

# 접속
http://localhost:8000
```

---

## 📖 사용 방법

### 개발자 (디버깅)

실제 크롬 브라우저를 보면서 테스트:
```bash
pdm run test:login
```

![개발자 모드](https://via.placeholder.com/600x300?text=Chrome+Browser+Opens)

### QA 팀 / 상사 (웹 UI)

브라우저에서 버튼 클릭:
```bash
pdm run dev
```

접속: http://localhost:8000

![웹 UI](https://via.placeholder.com/600x400?text=Web+UI+Screenshot)

---

## 🏗️ 프로젝트 구조
```
perso-auto-tester/
├── api/
│   ├── main.py              # FastAPI 메인
│   └── routers/
│       ├── pages.py         # HTML 페이지
│       └── test.py          # WebSocket 테스트 API
├── tasks/
│   ├── test_login.py        # 로그인 테스트
│   └── test_upload.py       # 업로드 + 번역 테스트
├── utils/
│   ├── config.py            # 환경 설정
│   ├── login.py             # 로그인 공통 함수
│   └── popup_handler.py     # 팝업 처리
├── test_videos/
│   └── sample.mp4           # 테스트용 영상
├── scripts/
│   └── README.md            # 개발자 가이드
├── Dockerfile               # 도커 이미지
└── .env                     # 환경변수 (gitignore)
```

---

## 🔧 개발자 가이드

자세한 개발 가이드는 [scripts/README.md](scripts/README.md) 참고

---

## 🌊 DigitalOcean 배포

### 자동 배포

`main` 브랜치에 push하면 자동 배포:
```bash
git push origin main
```

### 환경변수 설정

DigitalOcean App Platform에서 설정:
```
PERSO_EMAIL=your-email@eastsoft.com
PERSO_PASSWORD=your-password
VIDEO_FILE_PATH=/app/test_videos/sample.mp4
HEADLESS=true
PERSO_URL=https://perso.ai/ko/workspace/vt
```

---

## 📝 API 문서

서버 실행 후 접속:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🤝 기여

이슈 및 PR 환영합니다!

---

## 📄 라이선스

MIT
