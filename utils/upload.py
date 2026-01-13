import time
from pathlib import Path

def upload_file(page, log):
    """파일 업로드 및 번역 설정 모달 확인

    Args:
        page: Playwright page 객체
        log: 로그 출력 함수 (callable)

    Returns:
        bool: 번역 설정 모달이 나타났는지 여부

    Raises:
        Exception: 파일 업로드 실패 시
    """
    from utils.config import VIDEO_FILE_PATH

    log("📁 파일 input 찾는 중...")
    file_input = page.locator('input[type="file"]').first

    if not file_input.count():
        log("❌ 파일 input을 찾을 수 없습니다")
        raise Exception("파일 input 없음")

    log(f"📤 파일 업로드 중: {Path(VIDEO_FILE_PATH).name}")
    file_input.set_input_files(VIDEO_FILE_PATH)
    log("  ✓ 파일 선택 완료")

    # 번역 설정 모달 대기
    log("⏳ 번역 설정 모달 대기 중...")
    modal_detected = False

    # 1단계: 모달 컨테이너가 먼저 나타날 때까지 대기
    try:
        page.wait_for_selector('[role="dialog"]', state='visible', timeout=15000)
        log("  ✅ 모달 컨테이너 나타남!")
        modal_detected = True

        # 추가로 1초 대기 (모달 내부 콘텐츠 로딩)
        time.sleep(1)

        # 2단계: 번역 언어 텍스트 확인
        try:
            page.wait_for_selector('text=번역 언어', timeout=5000)
            log("  ✅ 번역 설정 모달 콘텐츠 로드 완료!")
        except:
            log("  ⚠️ 번역 언어 텍스트는 못 찾았지만 모달은 열림")
    except:
        log("  ⚠️ 모달 컨테이너를 찾지 못함")

    if not modal_detected:
        log("⚠️ 15초 대기했지만 모달을 찾지 못함")

    # 안정화 대기
    time.sleep(2)

    return modal_detected
