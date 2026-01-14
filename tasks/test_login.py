import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time
import asyncio

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.config import PERSO_EMAIL, HEADLESS, SCREENSHOT_DIR
from utils.browser import create_browser_context
from utils.login import do_login
from utils.popup_handler import accept_cookies, close_hubspot_iframe_popup, close_all_popups, remove_hubspot_overlay

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
            # === STEP 1: 로그인 ===
            log("\n" + "="*50)
            log("STEP 1: 로그인")
            log("="*50)

            do_login(page, log)

            # === STEP 2: 팝업/모달 닫기 ===
            log("\n" + "="*50)
            log("STEP 2: 팝업/모달 닫기")
            log("="*50)

            # 쿠키 수락
            try:
                accept_cookies(page)
            except Exception as e:
                log(f"  ⚠️ 쿠키 수락 실패: {e}")

            # HubSpot iframe 팝업
            try:
                close_hubspot_iframe_popup(page)
            except Exception as e:
                log(f"  ⚠️ HubSpot 팝업 실패: {e}")

            # HubSpot 오버레이 제거
            remove_hubspot_overlay(page, log)

            # 모든 팝업 닫기
            try:
                close_all_popups(page)
            except Exception as e:
                log(f"  ⚠️ 팝업 닫기 실패: {e}")

            # 페이지 맨 위로 스크롤
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(1)

            log("✅ 팝업/모달 정리 완료")

            # === STEP 3: 로그인 성공 확인 (프로필 드롭다운 → 로그아웃 버튼) ===
            log("\n" + "="*50)
            log("STEP 3: 로그인 성공 확인")
            log("="*50)

            log("🔍 프로필 드롭다운 찾는 중...")

            # 추가 대기 시간 (화면 완전히 로드)
            log("  ⏳ 화면 안정화 대기 중...")
            time.sleep(2)

            profile_button = None

            try:
                # === 디버깅: 페이지 전체 텍스트 확인 ===
                log("  🔍 페이지 전체 텍스트 확인 중...")
                try:
                    body_text = page.inner_text('body', timeout=3000)
                    log(f"  📄 페이지 텍스트 길이: {len(body_text)}자")

                    # 키워드 존재 확인
                    keywords = ['griotold', 'EST', 'Plan', 'Free', '로그아웃']
                    for kw in keywords:
                        if kw in body_text:
                            log(f"  ✓ '{kw}' 텍스트 발견")
                        else:
                            log(f"  ✗ '{kw}' 텍스트 없음")
                except Exception as e:
                    log(f"  ⚠️ 페이지 텍스트 확인 실패: {e}")

                # === 1차 시도: "griotold" 텍스트 (위치 제한 없음) ===
                log("  🔍 'griotold' 텍스트로 검색 중 (전체 영역)...")
                griotold_elements = page.locator('button:has-text("griotold"), div[role="button"]:has-text("griotold"), [role="button"]:has-text("griotold")').all()
                log(f"  📊 'griotold' 요소 {len(griotold_elements)}개 발견")

                for i, elem in enumerate(griotold_elements):
                    try:
                        if elem.is_visible(timeout=500):
                            box = elem.bounding_box()
                            text = elem.inner_text(timeout=500)
                            log(f"    {i+1}. '{text[:50]}' at ({box['x']:.0f}, {box['y']:.0f})")

                            # 좌측 영역 (x < 300, y < 400) - 범위 확대
                            if box and box['x'] < 300 and box['y'] < 400:
                                profile_button = elem
                                log(f"  ✅ 프로필 버튼 선택 (griotold) at ({box['x']:.0f}, {box['y']:.0f})")
                                break
                            else:
                                log(f"    ⚠️ 위치 필터링됨 (x={box['x']:.0f}, y={box['y']:.0f})")
                    except Exception as e:
                        log(f"    ⚠️ {i+1}번째 요소 처리 실패: {e}")

                # === 2차 시도: get_by_text 사용 ===
                if not profile_button:
                    log("  🔍 get_by_text로 'griotold' 검색 중...")
                    try:
                        griotold_by_text = page.get_by_text("griotold", exact=False)
                        count = griotold_by_text.count()
                        log(f"  📊 get_by_text로 {count}개 발견")

                        if count > 0:
                            for i in range(count):
                                try:
                                    elem = griotold_by_text.nth(i)
                                    if elem.is_visible(timeout=500):
                                        box = elem.bounding_box()
                                        text = elem.inner_text(timeout=500)
                                        log(f"    {i+1}. '{text[:50]}' at ({box['x']:.0f}, {box['y']:.0f})")

                                        if box and box['x'] < 300 and box['y'] < 400:
                                            profile_button = elem
                                            log(f"  ✅ 프로필 버튼 선택 (get_by_text) at ({box['x']:.0f}, {box['y']:.0f})")
                                            break
                                except Exception as e:
                                    log(f"    ⚠️ {i+1}번째 요소 처리 실패: {e}")
                    except Exception as e:
                        log(f"  ⚠️ get_by_text 실패: {e}")

                # === 3차 시도: 좌측 영역 모든 클릭 가능 요소 검색 ===
                if not profile_button:
                    log("  🔍 좌측 영역(x<300, y<400) 모든 클릭 가능 요소 검색 중...")
                    all_clickables = page.locator('button, div[role="button"], [role="button"]').all()
                    log(f"  📊 전체 클릭 가능 요소 {len(all_clickables)}개")

                    left_candidates = []
                    for elem in all_clickables:
                        try:
                            if elem.is_visible(timeout=100):
                                box = elem.bounding_box()
                                if box and box['x'] < 300 and box['y'] < 400:
                                    try:
                                        text = elem.inner_text(timeout=100).strip()
                                        if text:
                                            left_candidates.append({
                                                'elem': elem,
                                                'text': text,
                                                'x': box['x'],
                                                'y': box['y']
                                            })
                                    except:
                                        pass
                        except:
                            continue

                    log(f"  📋 좌측 영역 후보 {len(left_candidates)}개 발견:")
                    for i, cand in enumerate(left_candidates[:20]):  # 상위 20개 출력
                        log(f"    {i+1}. '{cand['text'][:50]}' at ({cand['x']:.0f}, {cand['y']:.0f})")

                    # 키워드 매칭
                    for cand in left_candidates:
                        text_lower = cand['text'].lower()
                        if any(kw in text_lower for kw in ['griotold', 'est', 'plan', 'free']):
                            profile_button = cand['elem']
                            log(f"  ✅ 프로필 버튼 선택 (키워드 매칭): '{cand['text'][:50]}' at ({cand['x']:.0f}, {cand['y']:.0f})")
                            break

                    # 키워드 매칭 실패시: 가장 위에 있는 요소 선택
                    if not profile_button and left_candidates:
                        left_candidates.sort(key=lambda c: (c['y'], c['x']))
                        best = left_candidates[0]
                        profile_button = best['elem']
                        log(f"  ⚠️ 키워드 매칭 실패, 최상단 좌측 요소 선택: '{best['text'][:50]}' at ({best['x']:.0f}, {best['y']:.0f})")

            except Exception as e:
                log(f"  ❌ 프로필 버튼 검색 중 에러: {e}")
                import traceback
                log(f"  상세: {traceback.format_exc()}")

            if not profile_button:
                log("\n" + "="*50)
                log("❌ 테스트 실패: 프로필 버튼을 찾을 수 없음")
                log("="*50)

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
                    "message": "프로필 버튼을 찾을 수 없음"
                }

            # 프로필 드롭다운 클릭
            log("  👆 프로필 드롭다운 클릭 중...")
            profile_button.click()

            # 드롭다운 애니메이션 완료 대기
            log("  ⏳ 드롭다운 메뉴 로딩 대기 중...")
            time.sleep(2)

            # 드롭다운 열린 후 스크린샷 (디버깅용)
            try:
                dropdown_screenshot = SCREENSHOT_DIR / "login_dropdown.png"
                page.screenshot(path=str(dropdown_screenshot), full_page=False)
                log(f"  📸 드롭다운 스크린샷 저장: {dropdown_screenshot.name}")
            except Exception as e:
                log(f"  ⚠️ 드롭다운 스크린샷 저장 실패: {e}")

            # "로그아웃" 버튼 확인
            log("  🔍 로그아웃 버튼 확인 중...")
            logout_found = False
            logout_button = None

            try:
                # 방법 1: text=로그아웃
                log("    🔍 방법 1: text=로그아웃")
                try:
                    logout_loc = page.locator('text=로그아웃')
                    count = logout_loc.count()
                    log(f"      📊 {count}개 발견")

                    if count > 0:
                        for i in range(count):
                            elem = logout_loc.nth(i)
                            if elem.is_visible(timeout=1000):
                                logout_button = elem
                                logout_found = True
                                log(f"      ✅ 로그아웃 버튼 발견 (text=로그아웃, {i+1}번째)")
                                break
                except Exception as e:
                    log(f"      ⚠️ 실패: {e}")

                # 방법 2: button:has-text("로그아웃")
                if not logout_found:
                    log("    🔍 방법 2: button:has-text(\"로그아웃\")")
                    try:
                        logout_button_loc = page.locator('button:has-text("로그아웃")')
                        count = logout_button_loc.count()
                        log(f"      📊 {count}개 발견")

                        if count > 0:
                            elem = logout_button_loc.first
                            if elem.is_visible(timeout=1000):
                                logout_button = elem
                                logout_found = True
                                log(f"      ✅ 로그아웃 버튼 발견 (button:has-text)")
                    except Exception as e:
                        log(f"      ⚠️ 실패: {e}")

                # 방법 3: a:has-text("로그아웃")
                if not logout_found:
                    log("    🔍 방법 3: a:has-text(\"로그아웃\")")
                    try:
                        logout_link_loc = page.locator('a:has-text("로그아웃")')
                        count = logout_link_loc.count()
                        log(f"      📊 {count}개 발견")

                        if count > 0:
                            elem = logout_link_loc.first
                            if elem.is_visible(timeout=1000):
                                logout_button = elem
                                logout_found = True
                                log(f"      ✅ 로그아웃 버튼 발견 (a:has-text)")
                    except Exception as e:
                        log(f"      ⚠️ 실패: {e}")

                # 방법 4: get_by_text로 검색
                if not logout_found:
                    log("    🔍 방법 4: get_by_text(\"로그아웃\")")
                    try:
                        logout_by_text = page.get_by_text("로그아웃", exact=False)
                        count = logout_by_text.count()
                        log(f"      📊 {count}개 발견")

                        if count > 0:
                            for i in range(count):
                                elem = logout_by_text.nth(i)
                                if elem.is_visible(timeout=500):
                                    logout_button = elem
                                    logout_found = True
                                    log(f"      ✅ 로그아웃 버튼 발견 (get_by_text, {i+1}번째)")
                                    break
                    except Exception as e:
                        log(f"      ⚠️ 실패: {e}")

                # 디버깅: 현재 보이는 모든 버튼/링크 출력
                if not logout_found:
                    log("    🔍 디버깅: 현재 보이는 모든 텍스트 요소 확인")
                    try:
                        # 모든 보이는 버튼
                        visible_buttons = page.locator('button:visible, a:visible, [role="button"]:visible').all()
                        log(f"      📋 보이는 클릭 가능 요소 {len(visible_buttons)}개:")

                        for i, btn in enumerate(visible_buttons[:15]):
                            try:
                                text = btn.inner_text(timeout=300).strip()
                                if text:
                                    log(f"        {i+1}. '{text[:50]}'")
                            except:
                                pass
                    except Exception as e:
                        log(f"      ⚠️ 버튼 목록 확인 실패: {e}")

            except Exception as e:
                log(f"  ❌ 로그아웃 버튼 검색 중 에러: {e}")
                import traceback
                log(f"  상세: {traceback.format_exc()}")

            if not logout_found:
                log("\n" + "="*50)
                log("❌ 테스트 실패: 로그아웃 버튼을 찾을 수 없음")
                log("="*50)

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
                    "message": "로그아웃 버튼을 찾을 수 없음"
                }

            log("  ✅ 로그아웃 버튼 확인 완료!")
            log("✅ 로그인 성공 확인 완료!")

            # === STEP 4: 스크린샷 저장 (드롭다운 열린 상태) ===
            log("\n" + "="*50)
            log("STEP 4: 스크린샷 저장")
            log("="*50)

            screenshot_path = SCREENSHOT_DIR / "login_success.png"
            log(f"📸 스크린샷 촬영 중 (드롭다운 열린 상태)...")
            page.screenshot(path=str(screenshot_path), full_page=False)
            log(f"✅ 스크린샷 저장 완료: {screenshot_path.name}")

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
