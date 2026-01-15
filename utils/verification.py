"""테스트 검증 유틸리티"""
import time
from utils.video_processing import wait_for_video_processing

def verify_login_success(page, log):
    """로그인 성공 여부 검증
    
    프로필 드롭다운 → 로그아웃 버튼 확인
    
    Args:
        page: Playwright page
        log: 로그 함수
        
    Returns:
        bool: 검증 성공 여부
        
    Raises:
        Exception: 검증 실패 시
    """
    log("🔍 로그인 성공 여부 확인 중...")
    time.sleep(2)  # 화면 안정화
    
    # 1. 프로필 버튼 찾기
    log("  🔍 프로필 버튼 검색 중...")
    try:
        profile_button = page.locator('text=Plan').first
        if not profile_button.is_visible(timeout=3000):
            raise Exception("프로필 버튼을 찾을 수 없음")
        log("  ✅ 프로필 버튼 발견!")
    except Exception as e:
        log(f"  ❌ 프로필 버튼 검색 실패: {e}")
        raise
    
    # 2. 드롭다운 열기
    log("  👆 프로필 드롭다운 클릭...")
    profile_button.click()
    time.sleep(2)  # 드롭다운 애니메이션 대기
    
    # 3. 로그아웃 버튼 확인
    log("  🔍 로그아웃 버튼 검색 중...")
    try:
        logout_button = page.locator('text=로그아웃').first
        if not logout_button.is_visible(timeout=3000):
            raise Exception("로그아웃 버튼을 찾을 수 없음")
        log("  ✅ 로그아웃 버튼 발견!")
    except Exception as e:
        log(f"  ❌ 로그아웃 버튼 검색 실패: {e}")
        raise
    
    log("✅ 로그인 성공 확인 완료!")
    return True

def verify_upload_success(page, log):
    """업로드 성공 여부 검증
    
    번역 설정 모달 확인
    
    Args:
        page: Playwright page
        log: 로그 함수
        
    Returns:
        bool: 검증 성공 여부
        
    Raises:
        Exception: 검증 실패 시
    """
    log("🔍 업로드 성공 여부 확인 중...")
    
    # 번역 설정 모달 확인
    try:
        # 방법 1: "번역 언어" 텍스트
        modal = page.locator('text=번역 언어').first
        if modal.is_visible(timeout=3000):
            log("  ✅ 번역 설정 모달 발견!")
            return True
    except:
        pass
    
    # 방법 2: "Auto Detect"
    try:
        modal = page.locator('text=Auto Detect').first
        if modal.is_visible(timeout=2000):
            log("  ✅ 번역 설정 모달 발견!")
            return True
    except:
        pass
    
    log("  ❌ 번역 설정 모달 없음")
    raise Exception("번역 설정 모달을 찾을 수 없음")

def verify_translate_success(page, log):
    """번역 성공 여부 검증
    
    비디오 처리가 완료될 때까지 대기하고 성공 확인
    
    Args:
        page: Playwright page
        log: 로그 함수
        
    Raises:
        Exception: 검증 실패 시
    """
    log("🔍 번역 성공 여부 확인 중...")
    
    # 비디오 처리 완료 대기
    wait_for_video_processing(page, "sample", log)
    
    log("✅ 번역 성공 확인 완료!")