import sys
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.config import PERSO_EMAIL, HEADLESS
from utils.browser import create_browser_context, save_screenshot
from utils.login import do_login
from utils.popup_handler import close_all_modals_and_popups
from utils.logger import create_logger
from utils.verification import verify_login_success
from utils.teams_notifier import send_teams_notification_sync

def test_login_sync(log_callback=None, log_collector=None):
    """로그인 테스트"""

    log = create_logger(log_callback, log_collector)

    log("🚀 로그인 테스트 시작")
    log(f"📧 이메일: {PERSO_EMAIL}")
    log(f"🖥️  Headless: {HEADLESS}")
    
    with sync_playwright() as p:
        # 브라우저 컨텍스트 생성 (utils.browser 사용)
        browser, context, page = create_browser_context(p, headless=HEADLESS)
        
        try:
            # === STEP 1: 로그인 ===
            log("\n" + "="*50)
            log("STEP 1: 로그인")
            log("="*50)

            do_login(page, log)

            # === STEP 2: 팝업/모달 닫기 ===
            log("\n" + "="*50)
            log("STEP 2: 팝업/모달 닫기")
            log("="*50)

            close_all_modals_and_popups(page, log) 

            # === STEP 3: 로그인 성공 확인 ===
            log("\n" + "="*50)
            log("STEP 3: 로그인 성공 확인")
            log("="*50)
            
            verify_login_success(page, log)

            # === STEP 4: 스크린샷 저장 (드롭다운 열린 상태) ===
            log("\n" + "="*50)
            log("STEP 4: 스크린샷 저장")
            log("="*50)

            save_screenshot(page, "login_success.png", log)

            # 드롭다운 닫기
            log("🔽 드롭다운 닫는 중...")
            page.keyboard.press('Escape')
            time.sleep(0.5)

            log("\n" + "="*50)
            log("✅ 로그인 테스트 완료!")
            log("="*50)

            return {
                "success": True,
                "screenshot": "login_success.png",
                "message": "로그인 테스트 성공!"
            }
            
        except Exception as e:
            log(f"❌ 에러 발생: {e}")
            save_screenshot(page, "login_error.png", log)

            return {
                "success": False,
                "screenshot": "login_error.png",
                "message": f"로그인 실패: {str(e)}"
            }
            
        finally:
            if not HEADLESS:
                log("🏁 브라우저를 5초 후 종료합니다...")
                time.sleep(5)
            browser.close()
            log("🏁 테스트 종료")

if __name__ == "__main__":
    logs: list[str] = []
    start_time = datetime.now()
    result = test_login_sync(log_collector=logs)
    end_time = datetime.now()

    # Teams 알림 전송
    send_teams_notification_sync(
        test_type="login",
        success=result["success"],
        message=result["message"],
        start_time=start_time,
        end_time=end_time,
        screenshot_filename=result.get("screenshot"),
        logs=logs,
    )
