import time

def do_login(page, log):
    """PERSO AI 로그인 공통 함수

    로그인 페이지에서 workspace 페이지로 이동하고 화면이 로드될 때까지 대기합니다.
    프로필 확인 등의 검증은 수행하지 않습니다.

    Args:
        page: Playwright page 객체
        log: 로그 출력 함수 (callable)

    Returns:
        None

    Raises:
        Exception: 로그인 실패 시
    """
    from utils.config import PERSO_EMAIL, PERSO_PASSWORD

    log("📍 로그인 페이지 접속 중...")
    page.goto('https://perso.ai/ko/login', timeout=60000)
    page.wait_for_load_state('networkidle')

    log("📝 이메일 입력 중...")
    email_input = page.locator('input[type="email"], input[placeholder*="이메일"]')
    email_input.fill(PERSO_EMAIL)
    time.sleep(0.5)

    log("👆 계속 버튼 클릭...")
    continue_button = page.locator('button:has-text("계속")')
    continue_button.click()
    time.sleep(2)

    log("🔐 비밀번호 입력 중...")
    password_input = page.locator('input[type="password"]')
    password_input.fill(PERSO_PASSWORD)
    time.sleep(0.5)

    log("🚪 Enter 키로 로그인 제출...")
    password_input.press('Enter')

    log("⏳ 로그인 처리 중...")
    page.wait_for_url('**/workspace/**', timeout=15000)

    # 화면 로딩 대기
    log("⏳ 페이지 로딩 대기 중...")

    # 1. 네트워크 idle 대기
    try:
        page.wait_for_load_state('networkidle', timeout=10000)
        log("  ✓ 네트워크 로딩 완료")
    except:
        log("  ⚠️ 네트워크 타임아웃 (계속 진행)")

    # 2. 주요 UI 요소 로드 확인
    try:
        page.wait_for_selector('text=AI Dubbing', state='visible', timeout=5000)
        log("  ✓ 주요 UI 요소 로드 완료")
    except:
        log("  ⚠️ 일부 요소 로딩 지연")

    # 3. 추가 안정화
    log("  ✓ 화면 안정화 중...")
    time.sleep(2)

    log("✅ 로그인 완료!")
