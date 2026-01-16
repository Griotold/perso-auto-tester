import asyncio
from typing import Callable, List, Optional


def create_logger(
    log_callback: Optional[Callable] = None,
    log_collector: Optional[List[str]] = None,
):
    """테스트용 로거 생성

    Args:
        log_callback: WebSocket 등으로 로그 전송할 콜백 함수
        log_collector: 로그를 수집할 리스트 (Teams 알림용)

    Returns:
        log 함수
    """

    def log(msg: str):
        """콘솔 출력 + 콜백 전송 + 로그 수집"""
        print(msg)

        # 로그 수집 (Teams 알림용)
        if log_collector is not None:
            log_collector.append(msg)

        if log_callback:
            if asyncio.iscoroutinefunction(log_callback):
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        asyncio.create_task(log_callback(msg))
                    else:
                        asyncio.run(log_callback(msg))
                except Exception:
                    pass
            else:
                log_callback(msg)

    return log