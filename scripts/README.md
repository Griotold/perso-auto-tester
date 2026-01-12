# 개발자 가이드

## 🔧 디버깅 모드 (크롬 브라우저 보면서 테스트)

개발자가 실제 브라우저 동작을 확인하면서 디버깅할 수 있습니다.

### 로그인 테스트
```bash
pdm run test:login
```

### 업로드 + 번역 테스트
```bash
pdm run test:upload
```

**특징:**
- ✅ 실제 크롬 브라우저 창이 뜹니다
- ✅ 천천히 동작 (slow_mo=500)
- ✅ DevTools 사용 가능
- ✅ 스크린샷 자동 저장 (`/tmp/screenshots/`)
- ✅ 터미널에 상세 로그 출력

---

## 🌐 웹 UI 모드 (QA/상사용)

웹 브라우저에서 버튼 클릭으로 테스트 실행 (headless)

### 개발 서버 실행
```bash
pdm run dev
```

접속: http://localhost:8000

**특징:**
- ✅ 웹 UI에서 버튼 클릭
- ✅ 실시간 로그 스트리밍
- ✅ 스크린샷 자동 표시
- ✅ Headless 모드 (백그라운드 실행)

---

## 🚀 프로덕션 배포

### DigitalOcean App Platform
```bash
git push origin main
```

자동으로 배포됨

### 환경변수 설정 (DO)
```
PERSO_EMAIL=your-email@eastsoft.com
PERSO_PASSWORD=your-password
VIDEO_FILE_PATH=/app/test_videos/sample.mp4
HEADLESS=true
```

---

## 📸 스크린샷 확인

로컬 개발 시 스크린샷은 여기에 저장됩니다:
```
/tmp/screenshots/login_success.png
/tmp/screenshots/login_error.png
```

웹 UI에서 자동으로 표시됩니다.

---

## 🐛 트러블슈팅

### 크롬이 안 뜰 때
```bash
# Playwright 재설치
pdm run playwright install chromium
pdm run playwright install-deps
```

### 환경변수 확인
```bash
# .env 파일 확인
cat .env

# HEADLESS 값 확인
echo $HEADLESS
```

### 로그 확인
```bash
# 서버 로그
pdm run dev

# 직접 실행 로그
pdm run test:login
```
