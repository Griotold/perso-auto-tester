"""
api/routers/test.py

테스트 실행 WebSocket 라우터.
클라이언트와 WebSocket 연결을 맺고, 테스트(로그인/업로드/번역)를 실행하면서
실시간으로 로그를 스트리밍하고 결과를 반환합니다.

엔드포인트: /test/ws/{test_type}
- test_type: "login" | "upload" | "translate"
"""
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from functools import partial
from typing import Callable, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pathlib import Path
import sys

# 프로젝트 루트 추가
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tasks.test_login import test_login_sync
from tasks.test_upload import test_upload_sync
from tasks.test_translate import test_translate_sync
from utils.teams_notifier import send_teams_notification

logger = logging.getLogger("perso-auto-tester")
router = APIRouter()


def _run_test(
    test_func: Callable,
    log_callback: Callable,
    log_collector: List[str],
) -> dict:
    """테스트 함수 실행 wrapper (log_collector 전달용)"""
    return test_func(log_callback=log_callback, log_collector=log_collector)

@router.websocket("/ws/{test_type}")
async def websocket_test(websocket: WebSocket, test_type: str):
    """WebSocket으로 테스트 실행 및 로그 스트리밍"""
    await websocket.accept()
    logger.info(f"WebSocket connected: {test_type}")

    # 테스트 함수 매핑
    test_functions = {
        "login": test_login_sync,
        "upload": test_upload_sync,
        "translate": test_translate_sync,
    }

    if test_type not in test_functions:
        await websocket.send_json({
            "type": "result",
            "success": False,
            "message": "지원하지 않는 테스트 타입입니다"
        })
        return

    try:
        # 로그 전송 함수
        async def send_log(msg: str):
            try:
                await websocket.send_json({"type": "log", "message": msg})
            except Exception:
                pass

        # 로그 수집 리스트
        log_collector: List[str] = []

        # 별도 스레드에서 동기 함수 실행
        executor = ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_event_loop()

        test_func = test_functions[test_type]
        start_time = datetime.now()

        result = await loop.run_in_executor(
            executor,
            partial(_run_test, test_func, send_log, log_collector),
        )

        end_time = datetime.now()

        # 결과 전송
        await websocket.send_json({
            "type": "result",
            "success": result["success"],
            "message": result["message"],
            "screenshot": result.get("screenshot")
        })

        # Teams 알림 전송
        await send_teams_notification(
            test_type=test_type,
            success=result["success"],
            message=result["message"],
            start_time=start_time,
            end_time=end_time,
            screenshot_filename=result.get("screenshot"),
            logs=log_collector,
        )

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        try:
            await websocket.send_json({
                "type": "result",
                "success": False,
                "message": f"테스트 실행 중 에러: {str(e)}"
            })
        except Exception:
            pass