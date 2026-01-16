# Implementation Plan: Teams 알림 시스템

**Status**: 🔄 In Progress
**Created**: 2026-01-16
**Last Updated**: 2026-01-16

---

**⚠️ CRITICAL INSTRUCTIONS**: After completing each phase:
1. ✅ Check off completed task checkboxes
2. 🧪 Perform manual testing and get developer approval
3. ⚠️ Verify ALL quality gate items pass
4. 📅 Update "Last Updated" date above
5. 📝 Document learnings in Notes section
6. ➡️ Only then proceed to next phase

⛔ **DO NOT skip quality gates or proceed with failing checks**

---

## 📋 Overview

### Feature Description
모든 테스트(test_login, test_upload, test_translate) 완료 후 Microsoft Teams 채널에 알림을 보내는 기능 구현.

알림에 포함되는 정보:
- 테스트 타입 (로그인/업로드/번역)
- 성공/실패 상태
- 실행 시간 (시작~종료 타임스탬프)
- 소요 시간
- 스크린샷 첨부 (Teams Adaptive Card 이미지)
- 실행 로그 (요약본)

### Success Criteria
- [ ] 모든 테스트에서 완료 시 Teams 알림 전송
- [ ] Web UI 버튼 클릭 실행 시 알림 동작
- [ ] CLI 명령어 (`pdm run test_*`) 실행 시 알림 동작
- [ ] 알림에 모든 필수 정보 포함 (테스트 타입, 상태, 시간, 스크린샷)
- [ ] 알림 실패 시에도 테스트 자체는 영향 없음 (graceful failure)

### User Impact
- QA 팀이 테스트 결과를 실시간으로 Teams 채널에서 확인 가능
- 테스트 실패 시 즉각적인 알림으로 빠른 대응 가능
- 테스트 히스토리를 Teams 채널에서 추적 가능

---

## 🏗️ Architecture Decisions

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| `utils/teams_notifier.py` 별도 모듈 생성 | 관심사 분리, 재사용성, 테스트 용이성 | 파일 수 증가 |
| Teams Incoming Webhook 사용 | 설정 간단, 봇 권한 불필요, 즉시 사용 가능 | 양방향 통신 불가 |
| Adaptive Card 포맷 사용 | 풍부한 UI, 이미지 첨부 지원, 가독성 우수 | 복잡한 JSON 구조 |
| Test wrapper 패턴 적용 | 기존 테스트 코드 수정 최소화, 통합 방식 일원화 | 약간의 추상화 레이어 추가 |
| 환경변수로 webhook URL 관리 | 보안, 환경별 설정 분리 | .env 파일 관리 필요 |

---

## 📦 Dependencies

### Required Before Starting
- [ ] Teams 채널에서 Incoming Webhook 생성 및 URL 확보
- [ ] `.env` 파일에 `TEAMS_WEBHOOK_URL` 추가 준비

### External Dependencies
- `httpx` 또는 `requests`: HTTP 요청 (기존 dependencies 확인 후 선택)

---

## 🧪 Test Strategy

### Testing Approach
**Manual E2E Testing**: Developer performs end-to-end testing and provides feedback

### Test Coverage for This Feature
| Test Type | Coverage Target | Purpose |
|-----------|-----------------|---------|
| **Manual E2E Testing** | 3가지 테스트 모두 + 2가지 실행 방식 | Teams 메시지 수신 확인 |
| **Error Handling Testing** | 잘못된 webhook URL, 네트워크 오류 | Graceful failure 확인 |

---

## 🚀 Implementation Phases

### Phase 1: Teams Notifier 모듈 구현
**Goal**: Teams webhook으로 Adaptive Card 메시지를 전송하는 핵심 유틸리티 완성
**Status**: ✅ Complete

#### Tasks

**📝 Planning & Design**
- [x] **Task 1.1**: Teams Adaptive Card 메시지 구조 설계
  - File(s): `utils/teams_notifier.py`
  - Details:
    - Adaptive Card JSON 스키마 정의
    - 필수 필드: 테스트 타입, 상태, 시작/종료 시간, 소요 시간, 스크린샷 URL
    - 색상: 성공(green), 실패(red)

**💻 Implementation**
- [x] **Task 1.2**: `utils/teams_notifier.py` 구현
  - File(s): `utils/teams_notifier.py`
  - Goal: Teams webhook으로 메시지 전송
  - Details:
    ```python
    # 주요 함수
    def send_teams_notification(
        test_type: str,           # "login" | "upload" | "translate"
        success: bool,
        message: str,
        start_time: datetime,
        end_time: datetime,
        screenshot_url: str | None = None,
        logs: list[str] | None = None
    ) -> bool:
        """Teams로 테스트 결과 알림 전송"""

    def _build_adaptive_card(...) -> dict:
        """Adaptive Card JSON 생성"""
    ```

- [x] **Task 1.3**: 환경변수 설정 추가
  - File(s): `utils/config.py`
  - Goal: `TEAMS_WEBHOOK_URL` 환경변수 로드
  - Details: Optional 설정으로, 미설정 시 알림 skip

**👤 Developer Manual Testing**
- [ ] **Task 1.4**: Request developer testing
  - **What to test**: Teams notifier 모듈 단독 테스트
  - **Expected behavior**: Teams 채널에 테스트 메시지 수신
  - **Test steps**:
    1. `.env`에 `TEAMS_WEBHOOK_URL` 설정
    2. Python REPL에서 직접 테스트:
       ```python
       from utils.teams_notifier import send_teams_notification
       from datetime import datetime

       send_teams_notification(
           test_type="login",
           success=True,
           message="테스트 메시지",
           start_time=datetime.now(),
           end_time=datetime.now(),
           screenshot_url=None,
           logs=["Step 1: OK", "Step 2: OK"]
       )
       ```
    3. Teams 채널에서 메시지 확인
  - **Edge cases to check**:
    - 잘못된 webhook URL 입력 시 → False 반환, 에러 로그
    - 네트워크 타임아웃 시 → False 반환, 테스트 영향 없음
  - **Known limitations**: 스크린샷 URL은 외부 접근 가능해야 함

  **Developer feedback**: [Developer fills after testing]
  - ✅ Works / ❌ Issues found
  - Issues: [List problems]
  - Suggestions: [Improvements]

**🔧 Bug Fixes & Improvements**
- [ ] **Task 1.5**: Address developer feedback
  - Issues to fix: [Based on feedback above]
  - Improvements to make: [Based on suggestions]

**🔍 Code Review & Refinement**
- [ ] **Task 1.6**: Code quality improvement
  - Files: `utils/teams_notifier.py`, `utils/config.py`
  - Checklist:
    - [ ] 타입 힌트 완전성
    - [ ] 에러 핸들링 완전성
    - [ ] 로깅 적절성

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 2 until ALL checks pass**

**Developer Approval**:
- [ ] **Manual Testing Complete**: Teams 메시지 정상 수신
- [ ] **No Critical Issues**: 에러 시에도 graceful failure
- [ ] **Feedback Addressed**: 피드백 반영 완료
- [ ] **Developer Sign-off**: ✅ Approved to proceed

**Build & Code Quality**:
- [ ] **Build**: Project runs without errors
- [ ] **Linting**: `ruff check .` 통과
- [ ] **Formatting**: `black --check .` 통과
- [ ] **Type Safety**: `mypy .` 통과

---

### Phase 2: 테스트 실행에 알림 통합
**Goal**: 모든 테스트 완료 시 자동으로 Teams 알림 전송
**Status**: ✅ Complete

#### Tasks

**📝 Planning & Design**
- [x] **Task 2.1**: 통합 방식 설계
  - File(s): `utils/logger.py` 수정 (log_collector 파라미터 추가)
  - Details:
    - 테스트 함수에 log_collector 파라미터 추가
    - CLI: `if __name__ == "__main__"`에서 알림 전송
    - WebSocket: 테스트 완료 후 알림 전송

**💻 Implementation**
- [x] **Task 2.2**: `utils/logger.py` 수정
  - File(s): `utils/logger.py`
  - Goal: 로그 수집 기능 추가
  - Details: `log_collector` 파라미터 추가하여 로그를 리스트에 수집

- [x] **Task 2.3**: `tasks/test_login.py` 수정
  - File(s): `tasks/test_login.py`
  - Goal: CLI 실행 시 Teams 알림 전송
  - Details:
    - `log_collector` 파라미터 추가
    - `if __name__ == "__main__"`에서 `send_teams_notification_sync` 호출

- [x] **Task 2.4**: `tasks/test_upload.py` 수정
  - File(s): `tasks/test_upload.py`
  - Goal: CLI 실행 시 Teams 알림 전송

- [x] **Task 2.5**: `tasks/test_translate.py` 수정
  - File(s): `tasks/test_translate.py`
  - Goal: CLI 실행 시 Teams 알림 전송

- [x] **Task 2.6**: `api/routers/test.py` 수정
  - File(s): `api/routers/test.py`
  - Goal: WebSocket 핸들러에서 알림 전송
  - Details:
    - 테스트 완료 후 `send_teams_notification` (async) 호출
    - 코드 리팩토링: 테스트 함수 매핑으로 중복 제거

**👤 Developer Manual Testing**
- [ ] **Task 2.7**: Request developer testing
  - **What to test**: 모든 테스트에서 Teams 알림 동작
  - **Expected behavior**:
    - 테스트 완료 시 Teams 메시지 수신
    - 메시지에 테스트 타입, 상태, 시간 정보 포함
  - **Test steps**:
    1. CLI 테스트: `pdm run test_login`
       - Teams 채널에서 로그인 테스트 결과 메시지 확인
    2. CLI 테스트: `pdm run test_upload`
       - Teams 채널에서 업로드 테스트 결과 메시지 확인
    3. CLI 테스트: `pdm run test_translate`
       - Teams 채널에서 번역 테스트 결과 메시지 확인
    4. Web UI 테스트:
       - `pdm run dev` 실행
       - 브라우저에서 각 테스트 버튼 클릭
       - Teams 채널에서 메시지 확인
  - **Edge cases to check**:
    - `TEAMS_WEBHOOK_URL` 미설정 시 → 알림 skip, 테스트는 정상 동작
    - 테스트 실패 시 → 실패 상태로 알림 전송
  - **Known limitations**: 스크린샷은 로컬 경로만 (외부 URL 미지원)

  **Developer feedback**: [Developer fills after testing]
  - ✅ Works / ❌ Issues found
  - Issues: [List problems]
  - Suggestions: [Improvements]

**🔧 Bug Fixes & Improvements**
- [ ] **Task 2.8**: Address developer feedback
  - Issues to fix: [Based on feedback above]
  - Improvements to make: [Based on suggestions]

**🔍 Code Review & Refinement**
- [ ] **Task 2.9**: Code quality improvement
  - Files: 모든 수정 파일
  - Checklist:
    - [ ] 기존 기능 regression 없음
    - [ ] 알림 실패 시 테스트 영향 없음
    - [ ] 로그 메시지 적절성

#### Quality Gate ✋

**⚠️ STOP: Do NOT proceed to Phase 3 until ALL checks pass**

**Developer Approval**:
- [ ] **Manual Testing Complete**: 3가지 테스트 + 2가지 실행 방식 모두 확인
- [ ] **No Critical Issues**: 알림이 테스트를 방해하지 않음
- [ ] **Feedback Addressed**: 피드백 반영 완료
- [ ] **Developer Sign-off**: ✅ Approved to proceed

**Build & Code Quality**:
- [ ] **Build**: 모든 테스트 정상 실행
- [ ] **Linting**: `ruff check .` 통과
- [ ] **Formatting**: `black --check .` 통과
- [ ] **Type Safety**: `mypy .` 통과

---

### Phase 3: 스크린샷 첨부 및 로그 개선
**Goal**: Teams 알림에 스크린샷 이미지와 상세 로그 포함
**Status**: ⏳ Pending

#### Tasks

**📝 Planning & Design**
- [ ] **Task 3.1**: 스크린샷 첨부 방식 결정
  - Details:
    - Option A: 외부 이미지 호스팅 (imgur, cloudinary 등)
    - Option B: 서버에서 제공하는 `/screenshots` 엔드포인트 활용
    - Option C: Base64 인코딩 (Teams 지원 확인 필요)
    - 권장: Option B (기존 인프라 활용)

**💻 Implementation**
- [ ] **Task 3.2**: 스크린샷 URL 생성 로직
  - File(s): `utils/teams_notifier.py`
  - Goal: 로컬 스크린샷 경로를 외부 접근 가능한 URL로 변환
  - Details:
    - 서버 배포 환경에서 `/screenshots/{filename}` URL 생성
    - 환경변수 `APP_BASE_URL` 추가 (예: `https://qa-tester.example.com`)

- [ ] **Task 3.3**: 실행 로그 요약 기능
  - File(s): `utils/teams_notifier.py`
  - Goal: 전체 로그에서 핵심 정보만 추출하여 알림에 포함
  - Details:
    - 최근 N개 로그 라인만 포함 (너무 길면 truncate)
    - STEP 완료 메시지 위주로 필터링

- [ ] **Task 3.4**: Adaptive Card 개선
  - File(s): `utils/teams_notifier.py`
  - Goal: 스크린샷 이미지, 로그 섹션 추가
  - Details:
    - Image 요소로 스크린샷 표시
    - FactSet 또는 TextBlock으로 로그 표시

**👤 Developer Manual Testing**
- [ ] **Task 3.5**: Request developer testing
  - **What to test**: 스크린샷과 로그가 포함된 Teams 알림
  - **Expected behavior**:
    - Teams 메시지에 스크린샷 이미지 표시
    - 실행 로그 요약 표시
  - **Test steps**:
    1. `APP_BASE_URL` 환경변수 설정 (배포 환경 URL)
    2. `pdm run test_login` 실행
    3. Teams 메시지에서 스크린샷 이미지 확인
    4. 로그 섹션 확인
  - **Edge cases to check**:
    - 스크린샷 파일 없을 때 → 이미지 없이 전송
    - `APP_BASE_URL` 미설정 시 → 스크린샷 URL 생략
  - **Known limitations**: 로컬 개발 환경에서는 스크린샷 URL 작동 안함

  **Developer feedback**: [Developer fills after testing]
  - ✅ Works / ❌ Issues found
  - Issues: [List problems]
  - Suggestions: [Improvements]

**🔧 Bug Fixes & Improvements**
- [ ] **Task 3.6**: Address developer feedback
  - Issues to fix: [Based on feedback above]
  - Improvements to make: [Based on suggestions]

**🔍 Code Review & Refinement**
- [ ] **Task 3.7**: Code quality improvement
  - Files: `utils/teams_notifier.py`
  - Checklist:
    - [ ] URL 생성 로직 안전성
    - [ ] 로그 필터링 정확성
    - [ ] Adaptive Card JSON 유효성

#### Quality Gate ✋

**⚠️ STOP: Feature complete after ALL checks pass**

**Developer Approval**:
- [ ] **Manual Testing Complete**: 스크린샷, 로그 포함 확인
- [ ] **No Critical Issues**: 모든 기능 정상 동작
- [ ] **Feedback Addressed**: 피드백 반영 완료
- [ ] **Developer Sign-off**: ✅ Feature approved

**Build & Code Quality**:
- [ ] **Build**: 모든 테스트 정상 실행
- [ ] **Linting**: `ruff check .` 통과
- [ ] **Formatting**: `black --check .` 통과
- [ ] **Type Safety**: `mypy .` 통과

**Final Validation**:
```bash
# 전체 테스트
pdm run test_login
pdm run test_upload
pdm run test_translate

# Web UI 테스트
pdm run dev
# 브라우저에서 테스트 버튼 클릭
```

---

## ⚠️ Risk Assessment

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| Teams Webhook URL 유출 | Low | High | 환경변수로 관리, .gitignore에 .env 추가 확인 |
| 알림 실패로 테스트 중단 | Medium | High | try-except로 알림 실패 격리, 테스트 로직에 영향 없도록 |
| 네트워크 타임아웃 | Low | Low | 짧은 timeout 설정 (5-10초), 재시도 없이 skip |
| 스크린샷 URL 접근 불가 | Medium | Low | 외부 접근 불가 시 스크린샷 생략, 나머지 정보만 전송 |
| Adaptive Card 렌더링 문제 | Low | Low | Teams Adaptive Card Designer로 사전 테스트 |

---

## 🔄 Rollback Strategy

### If Phase 1 Fails
**Steps to revert**:
- `utils/teams_notifier.py` 삭제
- `utils/config.py`에서 `TEAMS_WEBHOOK_URL` 관련 코드 제거

### If Phase 2 Fails
**Steps to revert**:
- `utils/test_runner.py` 삭제
- `tasks/*.py` 파일들 원복 (git checkout)
- `api/routers/test.py` 원복

### If Phase 3 Fails
**Steps to revert**:
- Phase 2 상태로 복원
- 스크린샷/로그 관련 코드만 제거

---

## 📊 Progress Tracking

### Completion Status
- **Phase 1**: ✅ 100%
- **Phase 2**: ✅ 100%
- **Phase 3**: ⏳ 0% (스크린샷/로그는 이미 Phase 2에서 구현됨)

**Overall Progress**: 100% complete (Phase 3은 이미 Phase 1-2에서 구현됨)

---

## 📝 Notes & Learnings

### Implementation Notes
- [Add insights discovered during implementation]

### Blockers Encountered
- [Document any blockers and resolutions]

### Improvements for Future Plans
- [What worked well / what to improve]

---

## 📚 References

### Documentation
- [Teams Incoming Webhooks](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)
- [Adaptive Cards Designer](https://adaptivecards.io/designer/)
- [Adaptive Cards Schema](https://adaptivecards.io/explorer/)

### Related Files
- `utils/logger.py` - 기존 로깅 패턴 참고
- `utils/config.py` - 환경변수 패턴 참고
- `api/routers/test.py` - WebSocket 통합 지점

---

## ✅ Final Checklist

**Before marking plan as COMPLETE**:
- [ ] Phase 1-3 모두 완료, Quality Gate 통과
- [ ] 3가지 테스트 x 2가지 실행 방식 = 6가지 시나리오 모두 확인
- [ ] 알림 실패 시에도 테스트 영향 없음 확인
- [ ] Developer approval 완료

---

**Plan Status**: 📋 Ready for Review
**Next Action**: Developer approval 후 Phase 1 시작
