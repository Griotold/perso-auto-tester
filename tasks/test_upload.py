import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

# 프로젝트 루트 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.config import PERSO_EMAIL, HEADLESS, VIDEO_FILE_PATH
from utils.login import do_login
from utils.upload import upload_file
from utils.popup_handler import close_all_modals_and_popups
from utils.browser import create_browser_context, save_screenshot
from utils.logger import create_logger
from utils.verification import verify_upload_success

def test_upload_sync(log_callback=None):
    """파일 업로드 테스트 (번역 설정 모달 나타나는지까지)"""

    log = create_logger(log_callback)

    log(f"🚀 업로드 테스트 시작")
    log(f"📧 이메일: {PERSO_EMAIL}")
    log(f"🎬 영상 파일: {VIDEO_FILE_PATH}")
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
            
            # === STEP 3: 파일 업로드 ===
            log("\n" + "="*50)
            log("STEP 3: 파일 업로드")
            log("="*50)

            upload_file(page, log)

            # === STEP 4: 번역 설정 모달 확인 ===
            log("\n" + "="*50)
            log("STEP 4: 업로드 성공 확인 / 번역 설정 모달 확인")
            log("="*50)

            verify_upload_success(page, log)
            
            # STEP 5: 스크린샷
            log("\n" + "="*50)
            log("STEP 5: 스크린샷 저장")
            log("="*50)

            save_screenshot(page, "upload_success.png", log)
            
            log("\n" + "="*50)
            log("✅ 업로드 테스트 완료!")
            log("="*50)
            
            return {
                "success": True,
                "screenshot": "upload_success.png",
                "message": "업로드 테스트 성공!"
            }
            
        except Exception as e:
            log(f"❌ 에러 발생: {e}")
            save_screenshot(page, "upload_error.png", log)

            import traceback
            traceback.print_exc()

            return {
                "success": False,
                "screenshot": "upload_error.png",
                "message": f"업로드 실패: {str(e)}"
            }
            
        finally:
            if not HEADLESS:
                log("🏁 브라우저를 5초 후 종료합니다...")
                time.sleep(5)
            browser.close()
            log("🏁 테스트 종료")

if __name__ == "__main__":
    test_upload_sync()
