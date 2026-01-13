import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time
import asyncio

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.config import PERSO_EMAIL, HEADLESS, SCREENSHOT_DIR
from utils.login import do_login
from utils.browser import create_browser_context

def test_login_sync(log_callback=None):
    """로그인 테스트 (동기 버전)"""
    
    def log(msg):
        """로그 출력 및 콜백 호출"""
        print(msg)
        if log_callback:
            if asyncio.iscoroutinefunction(log_callback):
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        asyncio.create_task(log_callback(msg))
                    else:
                        asyncio.run(log_callback(msg))
                except:
                    pass
            else:
                log_callback(msg)
    
    log(f"🚀 로그인 테스트 시작")
    log(f"📧 이메일: {PERSO_EMAIL}")
    log(f"🖥️  Headless: {HEADLESS}")
    
    with sync_playwright() as p:
        # 브라우저 컨텍스트 생성 (utils.browser 사용)
        browser, context, page = create_browser_context(p, headless=HEADLESS)
        
        try:
            # 로그인 (utils.login.do_login 사용)
            do_login(page, log)
            
            # 스크린샷 저장
            screenshot_path = SCREENSHOT_DIR / "login_success.png"
            log(f"📸 스크린샷 촬영 중...")
            page.screenshot(path=str(screenshot_path), full_page=False)
            log(f"✅ 스크린샷 저장 완료!")
            
            log("=" * 50)
            log("✅ 모든 테스트 통과!")
            log("=" * 50)
            
            return {
                "success": True,
                "screenshot": "login_success.png",
                "message": "로그인 테스트 성공!"
            }
            
        except Exception as e:
            log(f"❌ 에러 발생: {e}")
            
            # 에러 스크린샷
            try:
                error_screenshot = SCREENSHOT_DIR / "login_error.png"
                page.screenshot(path=str(error_screenshot), full_page=False)
                log(f"📸 에러 스크린샷 저장")
            except:
                pass
            
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
    test_login_sync()
