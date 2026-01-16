# utils/teams_notifier.py
"""Teams Webhook으로 테스트 결과 알림 전송"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any, List, Optional

import httpx
from pydantic import BaseModel, Field

from utils.config import APP_BASE_URL, TEAMS_WEBHOOK_URL

logger = logging.getLogger(__name__)


# =============================================================================
# MessageCard 데이터 구조
# =============================================================================


class Fact(BaseModel):
    """Teams MessageCard의 sections[].facts[] 한 줄"""

    name: str
    value: str


class Section(BaseModel):
    """Teams MessageCard의 sections[] 하나"""

    activityTitle: Optional[str] = None
    facts: List[Fact] = Field(default_factory=list)


class TeamsMessageCard(BaseModel):
    """Teams MessageCard JSON payload"""

    title: Optional[str] = None
    summary: Optional[str] = None
    themeColor: Optional[str] = None
    sections: List[Section] = Field(default_factory=list)

    def get_fact(self, name: str) -> Optional[str]:
        """sections[].facts[]에서 name이 일치하는 value 찾기"""
        for section in self.sections:
            for fact in section.facts:
                if fact.name == name:
                    return fact.value
        return None


# =============================================================================
# Teams Notifier
# =============================================================================


def _format_datetime(dt: datetime) -> str:
    """datetime을 한국 시간 형식으로 포맷"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _format_duration(start: datetime, end: datetime) -> str:
    """소요 시간을 사람이 읽기 쉬운 형식으로 포맷"""
    delta = end - start
    total_seconds = int(delta.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    if minutes > 0:
        return f"{minutes}분 {seconds}초"
    return f"{seconds}초"


def _get_test_type_korean(test_type: str) -> str:
    """테스트 타입을 한국어로 변환"""
    mapping = {
        "login": "로그인",
        "upload": "업로드",
        "translate": "번역",
    }
    return mapping.get(test_type, test_type)


def _build_message_card(
    test_type: str,
    success: bool,
    message: str,
    start_time: datetime,
    end_time: datetime,
    screenshot_url: Optional[str] = None,
    logs: Optional[List[str]] = None,
) -> dict[str, Any]:
    """Teams MessageCard JSON 생성"""
    status_emoji = "✅" if success else "❌"
    status_text = "성공" if success else "실패"
    theme_color = "00FF00" if success else "FF0000"
    test_type_kr = _get_test_type_korean(test_type)

    facts = [
        Fact(name="테스트 타입", value=test_type_kr),
        Fact(name="상태", value=f"{status_emoji} {status_text}"),
        Fact(name="시작 시간", value=_format_datetime(start_time)),
        Fact(name="종료 시간", value=_format_datetime(end_time)),
        Fact(name="소요 시간", value=_format_duration(start_time, end_time)),
    ]

    if message:
        facts.append(Fact(name="메시지", value=message))

    if screenshot_url:
        facts.append(Fact(name="스크린샷", value=f"[보기]({screenshot_url})"))

    sections = [Section(activityTitle="테스트 결과", facts=facts)]

    if logs:
        log_text = "\n".join(logs)
        sections.append(
            Section(
                activityTitle="실행 로그",
                facts=[Fact(name="로그", value=f"```\n{log_text}\n```")],
            )
        )

    card = TeamsMessageCard(
        title=f"{status_emoji} PERSO 자동화 테스트 - {test_type_kr} {status_text}",
        summary=f"{test_type_kr} 테스트 {status_text}",
        themeColor=theme_color,
        sections=sections,
    )

    return card.model_dump(exclude_none=True)


async def send_teams_notification(
    test_type: str,
    success: bool,
    message: str,
    start_time: datetime,
    end_time: datetime,
    screenshot_filename: Optional[str] = None,
    logs: Optional[List[str]] = None,
    webhook_url: Optional[str] = None,
    timeout: float = 10.0,
) -> bool:
    """Teams로 테스트 결과 알림 전송 (async)

    Args:
        test_type: 테스트 타입 ("login", "upload", "translate")
        success: 성공 여부
        message: 결과 메시지
        start_time: 테스트 시작 시간
        end_time: 테스트 종료 시간
        screenshot_filename: 스크린샷 파일명 (예: "login_success.png")
        logs: 실행 로그 목록
        webhook_url: Teams Webhook URL (기본값: 환경변수에서 로드)
        timeout: 요청 타임아웃 (초)

    Returns:
        bool: 전송 성공 여부
    """
    url = webhook_url or TEAMS_WEBHOOK_URL

    if not url:
        logger.warning("❌ TEAMS_WEBHOOK_URL이 설정되지 않았습니다. 알림을 건너뜁니다.")
        return False

    screenshot_url = None
    if screenshot_filename:
        screenshot_url = f"{APP_BASE_URL}/screenshots/{screenshot_filename}"

    card = _build_message_card(
        test_type=test_type,
        success=success,
        message=message,
        start_time=start_time,
        end_time=end_time,
        screenshot_url=screenshot_url,
        logs=logs,
    )

    async with httpx.AsyncClient(timeout=timeout, verify=False) as client:
        try:
            resp = await client.post(url, json=card)

            if resp.is_error:
                logger.error(
                    f"❌ Teams 알림 전송 실패. "
                    f"status={resp.status_code} body={resp.text[:200]}"
                )
                return False

            logger.info("✅ Teams 알림 전송 성공")
            return True

        except httpx.RequestError as exc:
            logger.error(f"❌ Teams 알림 요청 오류: {exc}")
            return False


def send_teams_notification_sync(
    test_type: str,
    success: bool,
    message: str,
    start_time: datetime,
    end_time: datetime,
    screenshot_filename: Optional[str] = None,
    logs: Optional[List[str]] = None,
    webhook_url: Optional[str] = None,
    timeout: float = 10.0,
) -> bool:
    """Teams로 테스트 결과 알림 전송 (sync wrapper for CLI)

    CLI 환경에서 호출할 때 사용합니다.
    내부적으로 asyncio.run()을 사용하여 async 함수를 호출합니다.

    Args:
        test_type: 테스트 타입 ("login", "upload", "translate")
        success: 성공 여부
        message: 결과 메시지
        start_time: 테스트 시작 시간
        end_time: 테스트 종료 시간
        screenshot_filename: 스크린샷 파일명 (예: "login_success.png")
        logs: 실행 로그 목록
        webhook_url: Teams Webhook URL (기본값: 환경변수에서 로드)
        timeout: 요청 타임아웃 (초)

    Returns:
        bool: 전송 성공 여부
    """
    return asyncio.run(
        send_teams_notification(
            test_type=test_type,
            success=success,
            message=message,
            start_time=start_time,
            end_time=end_time,
            screenshot_filename=screenshot_filename,
            logs=logs,
            webhook_url=webhook_url,
            timeout=timeout,
        )
    )
