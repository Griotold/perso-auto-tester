import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent

# 환경변수에서 가져오되, 상대경로면 절대경로로 변환
VIDEO_FILE_PATH = os.getenv('VIDEO_FILE_PATH', './test_videos/sample.mp4')

if not VIDEO_FILE_PATH.startswith('/'):
    # 상대경로면 프로젝트 루트 기준으로 변환
    VIDEO_FILE_PATH = str(PROJECT_ROOT / VIDEO_FILE_PATH)

# 파일 존재 여부 확인
if not Path(VIDEO_FILE_PATH).exists():
    raise FileNotFoundError(f"테스트 영상을 찾을 수 없습니다: {VIDEO_FILE_PATH}")

PERSO_EMAIL = os.getenv('PERSO_EMAIL')
PERSO_PASSWORD = os.getenv('PERSO_PASSWORD')
PERSO_URL = os.getenv('PERSO_URL', 'https://perso.ai/ko/workspace/vt')

print(f"✅ 설정 로드 완료")
print(f"📧 이메일: {PERSO_EMAIL}")
print(f"🎬 영상 파일: {VIDEO_FILE_PATH}")
