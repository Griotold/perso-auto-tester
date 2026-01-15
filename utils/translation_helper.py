# utils/translation_helper.py
from utils.logger import create_logger
import time

_default_log = create_logger()

def select_language_from_dropdown(page, language_name, dropdown_index=0, log=None):
    """드롭다운에서 언어 선택
    
    Args:
        page: Playwright page 객체
        language_name: 선택할 언어 이름 (예: "Korean", "English")
        dropdown_index: 드롭다운 인덱스 (0: 첫번째, 1: 두번째)
        log: 로그 함수
    """
    log = log or _default_log
    
    log(f"🔍 {language_name} 선택을 위한 드롭다운 열기...")
    dropdown = page.locator('button[role="combobox"]').nth(dropdown_index)
    dropdown.click(force=True)
    time.sleep(2)
    
    # 검색 input에 언어 입력
    log(f"⌨️  '{language_name}' 입력 중...")
    search_input = page.locator('input[placeholder*="언어를 검색"]').first
    search_input.fill(language_name)
    time.sleep(1.5)
    
    # 언어 요소 클릭
    log(f"👆 {language_name} 선택 중...")
    elements = page.get_by_text(language_name, exact=True).all()
    
    # 마지막 요소 선택 (드롭다운 내부 요소)
    target_element = elements[-1] if len(elements) > 0 else elements[0]
    
    box = target_element.bounding_box()
    x = box['x'] + box['width'] / 2
    y = box['y'] + box['height'] / 2
    page.mouse.click(x, y)
    time.sleep(2)
    
    log(f"✅ {language_name} 선택 완료!")

def click_translate_button(page, log=None):
    """번역하기 버튼 클릭
    
    Args:
        page: Playwright page 객체
        log: 로그 함수
    """
    log = log or _default_log
    
    log("🔍 '번역하기' 버튼 찾는 중...")
    translate_button = page.locator('button:has-text("번역하기")').first
    
    log("👆 '번역하기' 버튼 클릭...")
    translate_button.click()
    time.sleep(3)
    
    log("✅ 번역하기 버튼 클릭 완료!")