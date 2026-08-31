import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env")
except ImportError:
    pass

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

HOST = "0.0.0.0"
PORT = 5062
SECRET_KEY = os.environ.get("SECRET_KEY") or "ping-box-dev"
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "123456")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "").strip()
SQLITE_PATH = DATA_DIR / "data.db"
TIMEOUT = 8
