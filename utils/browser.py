from utils.config import SCREENSHOT_DIR


def save_screenshot(page, filename, log=None, full_page=False):
    """스크린샷을 저장합니다.

    Args:
        page: Playwright page 객체
        filename: 저장할 파일명 (예: "login_success.png")
        log: 로그 출력 함수 (optional)
        full_page: 전체 페이지 스크린샷 여부 (default: False)

    Returns:
        str: 저장된 파일명 (성공 시), None (실패 시)
    """
    _log = log if log else print
    screenshot_path = SCREENSHOT_DIR / filename

    try:
        page.screenshot(path=str(screenshot_path), full_page=full_page)
        _log(f"📸 스크린샷 저장: {filename}")
        return filename
    except Exception as e:
        _log(f"⚠️ 스크린샷 저장 실패: {e}")
        return None


def create_browser_context(playwright, headless=True, viewport_width=1920, viewport_height=1080):
    """브라우저 컨텍스트를 생성합니다.

    Args:
        playwright: Playwright 인스턴스 (sync_playwright()의 결과)
        headless: Headless 모드 사용 여부 (default: True)
        viewport_width: 뷰포트 너비 (default: 1920)
        viewport_height: 뷰포트 높이 (default: 1080)

    Returns:
        tuple: (browser, context, page) 튜플
    """
    # 브라우저 launch 옵션 설정
    launch_options = {
        'headless': headless,
    }

    if headless:
        # Headless 모드용 추가 옵션
        launch_options['args'] = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ]
    else:
        # Non-headless 모드용 슬로우 모션
        launch_options['slow_mo'] = 500

    # 브라우저 실행
    browser = playwright.chromium.launch(**launch_options)

    # 컨텍스트 생성 (viewport 설정 포함)
    context = browser.new_context(
        viewport={'width': viewport_width, 'height': viewport_height}
    )

    # 페이지 생성
    page = context.new_page()

    return browser, context, page
