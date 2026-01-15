from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


@router.get("/", response_class=HTMLResponse)
async def index():
    """메인 페이지"""
    html_path = TEMPLATES_DIR / "index.html"
    return html_path.read_text(encoding="utf-8")