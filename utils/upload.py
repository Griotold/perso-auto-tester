import time
from pathlib import Path
from utils.config import VIDEO_FILE_PATH

def upload_file(page, log):
    """파일 업로드 (검증 제외)
    
    Args:
        page: Playwright page
        log: 로그 함수
    """
    log("📁 파일 input 찾는 중...")
    file_input = page.locator('input[type="file"]').first
    
    if not file_input.count():
        log("❌ 파일 input을 찾을 수 없습니다")
        raise Exception("파일 input 없음")
    
    log(f"📤 파일 업로드 중: {Path(VIDEO_FILE_PATH).name}")
    file_input.set_input_files(VIDEO_FILE_PATH)
    log("  ✓ 파일 선택 완료")
    
    # 업로드 처리 대기 (서버 업로드 시간)
    log("⏳ 파일 업로드 처리 중...")
    time.sleep(3)  # 또는 적절한 대기
    
    log("✅ 파일 업로드 완료!")
    # return 없음!