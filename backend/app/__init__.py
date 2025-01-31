from pathlib import Path
from app.core.logging import setup_logging

# 确保上传目录存在
UPLOAD_DIR = Path(__file__).parent.parent / 'uploads'
UPLOAD_DIR.mkdir(exist_ok=True)

setup_logging() 