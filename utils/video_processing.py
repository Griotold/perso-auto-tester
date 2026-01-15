# utils/video_processing.py
from utils.logger import create_logger
from utils.browser import save_screenshot
import time

_default_log = create_logger()

# utils/video_processing.py
def wait_for_video_processing(page, video_name, log=None):
    """비디오 처리 전체 플로우
    
    Raises:
        Exception: 처리 실패 시 에러 메시지와 함께 예외 발생
    """
    log = log or _default_log
    
    # 1. workspace 확인
    if not _verify_workspace_page(page, log):
        save_screenshot(page, "translate_error.png", log)
        raise Exception("workspace 페이지로 이동하지 못함")
    
    # 2. 비디오 찾기
    video_result = _find_uploaded_video(page, video_name, log)
    if not video_result["found"]:
        log("\n" + "="*50)
        log(f"❌ 테스트 실패: {video_name} 영상을 찾을 수 없음")
        log("="*50)
        save_screenshot(page, "translate_error.png", log)
        raise Exception(f"{video_name} 영상을 찾을 수 없음")
    
    # 3. 처리 시작 확인
    if not video_result["processing_started"]:
        log("\n" + "="*50)
        log("❌ 테스트 실패: 영상 처리 중 상태를 확인할 수 없음")
        log("="*50)
        save_screenshot(page, "translate_error.png", log)
        raise Exception("영상 처리 중 상태를 확인할 수 없음")
    
    # 4. 처리 완료 대기
    processing_result = _wait_for_video_processing(page, video_name, log)
    if not processing_result["success"]:
        log("\n" + "="*50)
        log(f"❌ 테스트 실패: {processing_result['message']}")
        log("="*50)
        save_screenshot(page, "translate_error.png", log)
        raise Exception(processing_result["message"])
    
    log(f"  🎉 영상 처리 성공!")

def _verify_workspace_page(page, log):
    """workspace 페이지 확인 (private)"""
    log("🔍 홈 화면 이동 확인 중...")
    current_url = page.url
    log(f"  📍 현재 URL: {current_url}")
    
    if "/workspace" in current_url:
        log("  ✓ workspace 페이지에 있음")
        time.sleep(3)
        page.wait_for_load_state('networkidle', timeout=10000)
        log("  ✓ 페이지 로딩 완료")
        log("✅ 홈 화면으로 이동 완료!")
        return True
    else:
        log(f"  ⚠️ workspace 페이지가 아님: {current_url}")
        return False


def _find_uploaded_video(page, video_name, log):
    """업로드된 비디오 찾기 (private)"""
    log(f"\n🔍 업로드된 '{video_name}' 영상 확인 중...")
    
    processing_started = False
    video_found = False
    
    try:
        video_element = page.get_by_text(video_name).first
        
        if video_element.is_visible(timeout=5000):
            log(f"  ✓ '{video_name}' 영상 발견!")
            video_found = True
            
            processing_status_texts = ["대기 중", "영상 처리 중", "음성 추출 중", "번역 중", "음성 생성 중"]
            
            for status_text in processing_status_texts:
                try:
                    if page.get_by_text(status_text, exact=False).first.is_visible(timeout=2000):
                        log(f"  ✓ 현재 상태: {status_text}")
                        processing_started = True
                        break
                except:
                    continue
            
            if not processing_started:
                log("  ℹ️ 처리 중 텍스트를 찾을 수 없지만 영상은 존재함")
        else:
            log(f"  ⚠️ '{video_name}' 영상을 찾을 수 없음")
    except Exception as e:
        log(f"  ⚠️ 영상 확인 실패: {e}")
    
    return {
        "found": video_found,
        "processing_started": processing_started
    }


def _wait_for_video_processing(page, video_name, log):
    """비디오 처리 완료 대기 (private)"""
    log("\n⏳ 영상 처리 완료 대기 중...")
    
    processing_complete = False
    processing_failed = False
    wait_interval = 10
    elapsed = 0
    last_status_text = ""
    processing_status_texts = ["대기 중", "영상 처리 중", "음성 추출 중", "번역 중", "음성 생성 중"]
    
    while not processing_complete and not processing_failed:
        time.sleep(wait_interval)
        elapsed += wait_interval
        
        try:
            # Failed 체크
            try:
                if page.get_by_text("Failed", exact=False).first.is_visible(timeout=500):
                    log(f"  ❌ 'Failed' 감지! 영상 처리 실패")
                    processing_failed = True
                    break
            except:
                pass
            
            # 처리 상태 확인
            current_status_text = ""
            still_processing = False
            
            for status_text in processing_status_texts:
                try:
                    if page.get_by_text(status_text, exact=False).first.is_visible(timeout=500):
                        current_status_text = status_text
                        still_processing = True
                        break
                except:
                    continue
            
            # 상태 변화 로그
            if still_processing and current_status_text:
                if current_status_text != last_status_text:
                    log(f"  🔄 상태 변경: {current_status_text}")
                    last_status_text = current_status_text
                else:
                    log(f"  ⏳ {elapsed}초 경과... ({current_status_text})")
                continue
            
            # 완료 확인 (타임스탬프)
            timestamp_found = False
            try:
                if page.get_by_text("초 전").first.is_visible(timeout=500) or \
                   page.get_by_text("분 전").first.is_visible(timeout=500):
                    timestamp_found = True
            except:
                pass
            
            if timestamp_found:
                log(f"  ✅ 영상 처리 완료! (총 대기 시간: {elapsed}초)")
                processing_complete = True
                break
            else:
                log(f"  ⏳ {elapsed}초 경과... (상태 확인 중)")
        
        except Exception as e:
            log(f"  ⚠️ 처리 상태 확인 실패: {e} ({elapsed}초)")
    
    if processing_failed:
        return {"success": False, "message": "영상 처리 실패 (Failed)"}
    elif processing_complete:
        return {"success": True, "message": "영상 처리 성공"}
    else:
        return {"success": False, "message": "처리 상태를 확인할 수 없음"}