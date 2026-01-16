## 2. 환경 설정 창 (1/15 ~ 1/16)

### 2.1 설계

**□ UI/UX 설계**
- 설정 페이지 와이어프레임

**□ 데이터 모델 설계**
- 설정 데이터 구조 정의
```json
  {
    "email": "string",
    "password": "string",
    "video_file_path": "string",
    "headless": "boolean"
  }
```
- JSON 파일 저장 위치: `/config/runtime_config.json`
- 설정 우선순위: **런타임 설정(JSON) > .env 기본값**
- .env는 기본값으로만 사용 (읽기 전용)

**□ API 엔드포인트 설계**
- `POST /api/config` - 설정 저장
  - Request: `{ email, password, video_file_path, headless }`
  - Response: `{ success: true, message: "설정 저장 완료" }`
- `GET /api/config` - 설정 불러오기
  - Response: `{ email, password, video_file_path, headless }`
  - 비밀번호 포함 (보안 고려 안 함)

### 2.2 백엔드 구현

**□ 설정 저장/불러오기 API**
- `POST /api/config` - 설정 저장
  - JSON 파일에 저장 (`/config/runtime_config.json`)
  - 파일 없으면 생성
- `GET /api/config` - 설정 불러오기
  - JSON 파일 우선 읽기
  - 없으면 .env 기본값 반환

**□ 환경변수 관리 로직**
- `utils/config.py` 수정
  - JSON 파일 읽기 함수 추가
  - 우선순위: JSON 설정 > .env 환경변수
  - 설정 로드 순서:
    1. `/config/runtime_config.json` 확인
    2. 있으면 JSON 값 사용
    3. 없으면 .env 기본값 사용

**□ 영상 파일 업로드 처리**
- 업로드 엔드포인트: `POST /api/upload`
- 저장 위치: `/uploads/` (gitignore 추가)
- 파일 크기 제한: 100MB
- 허용 확장자: `.mp4`, `.mov`, `.avi`
- 파일명: `uploaded_video.mp4` (고정, 덮어쓰기)

### 2.3 프론트엔드 구현

**□ 설정 페이지 UI**
- 페이지 경로: `/config` 또는 메인 페이지에 통합
- □ 이메일 입력 필드
- □ 비밀번호 입력 필드
- □ 영상 파일 선택 (파일 업로드)
- □ 대기 시간 배수 설정 (3배/4배/5배) - 제거 (자동 대기로 변경됨)
- □ Headless 모드 체크박스 (선택사항)

**□ 설정 저장/불러오기 기능**
- 페이지 로드 시 `GET /api/config` 호출하여 기존 설정 표시
- 저장 버튼 클릭 시 `POST /api/config` 호출
- 영상 파일 선택 시 `POST /api/upload` 호출

**□ 유효성 검증**
- 이메일 형식 검증
- 비밀번호 필수 입력
- 영상 파일 크기/확장자 검증

### 2.4 통합 및 테스트

**□ 테스트 실행 시 설정 적용 확인**
- 로그인 테스트에서 JSON 설정 사용 확인
- 업로드 테스트에서 업로드된 영상 사용 확인

**□ 배포 및 동작 확인**
- Digital Ocean 배포 후 설정 유지 확인
- 서버 재시작 후에도 JSON 설정 유지 확인
- Git push 후에도 JSON 설정 변경 없음 확인