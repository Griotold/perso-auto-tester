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
from utils.popup_handler import close_all_modals_and_popups, prepare_and_check_translation_modal, handle_permission_modal, close_translation_settings_modal, close_tutorial_popup
from utils.browser import create_browser_context, save_screenshot
from utils.logger import create_logger
from utils.translation_helper import select_language_from_dropdown, click_translate_button
from utils.video_processing import verify_and_wait_for_video_processing

def test_translate_sync(log_callback=None):
    """파일 업로드 후 번역 설정을 완료하는 테스트"""

    log = create_logger(log_callback)

    log(f"🚀 번역 설정 테스트 시작")
    log(f"📧 이메일: {PERSO_EMAIL}")
    log(f"🎬 영상 파일: {VIDEO_FILE_PATH}")
    log(f"🖥️  Headless: {HEADLESS}")

    with sync_playwright() as p:
        # 브라우저 컨텍스트 생성 (utils.browser 사용, viewport 1920x1080)
        browser, context, page = create_browser_context(
            p,
            headless=HEADLESS,
            viewport_width=1920,
            viewport_height=1080
        )

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
            log("STEP 4: 번역 설정 모달 확인")
            log("="*50)

            prepare_and_check_translation_modal(page, log)

            log("✅ 번역 설정 모달 확인 완료!")

            # === STEP 5: 원본 언어 선택 (Korean) ===
            log("\n" + "="*50)
            log("STEP 5: 원본 언어 선택 (Korean)")
            log("="*50)

            select_language_from_dropdown(page, "Korean", dropdown_index=0, log=log)

            #log("✅ 원본 언어 Korean 선택 완료!")

            # === STEP 6: 번역 언어 선택 (English) ===
            log("\n" + "="*50)
            log("STEP 6: 번역 언어 선택 (English)")
            log("="*50)
            select_language_from_dropdown(page, "English", dropdown_index=1, log=log)

            # 드롭다운 닫기
            log("🔍 드롭다운 닫는 중...")
            page.mouse.click(900, 300)
            time.sleep(1)
            #log("✅ 번역 언어 English 선택 완료!")

            # === STEP 7: 번역 시작 - 번역하기 버튼 클릭 ===
            log("\n" + "="*50)
            log("STEP 7: 번역 시작 - 번역하기 버튼 클릭")
            log("="*50)
            click_translate_button(page, log)
            handle_permission_modal(page, log)
            close_translation_settings_modal(page, log)
            close_tutorial_popup(page, log)

            # === STEP 8: 번역 처리 확인 ===
            log("\n" + "="*50)
            log("STEP 8: 번역 처리 확인")
            log("="*50)

            # 페이지 전환 대기
            log("⏳ 페이지 전환 대기 중...")
            time.sleep(5)

            # 번역 처리 검증
            verify_and_wait_for_video_processing(page, "sample", log)
                        

            # === STEP 8: 스크린샷 저장 ===
            log("\n" + "="*50)
            log("STEP 8: 스크린샷 저장")
            log("="*50)

            save_screenshot(page, "translate_success.png", log)

            log("\n" + "="*50)
            log("✅ 번역 테스트 완료!")
            log("="*50)

            return {
                "success": True,
                "screenshot": "translate_success.png",
                "message": "번역 테스트가 성공적으로 완료되었습니다!"
            }

        except Exception as e:
            log(f"❌ 에러 발생: {e}")
            save_screenshot(page, "translate_error.png", log)

            import traceback
            traceback.print_exc()

            return {
                "success": False,
                "screenshot": "translate_error.png",
                "message": f"번역 테스트 실패: {str(e)}"
            }

        finally:
            if not HEADLESS:
                log("🏁 브라우저를 5초 후 종료합니다...")
                time.sleep(5)
            browser.close()
            log("🏁 테스트 종료")

if __name__ == "__main__":
    test_translate_sync()
