import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        os.urandom(24).hex()
    )

    PORT = int(os.environ.get("PORT", 5000))

    NORMAL_PASSWORD = os.environ.get(
        "NORMAL_PASSWORD",
        "Rey190327"
    )

    DATA_FILE = BASE_DIR / "data.json"

    SERVERS_DIR = BASE_DIR / "servers"

    LOGS_DIR = BASE_DIR / "logs"

    UPLOADS_DIR = BASE_DIR / "uploads"

    AUTO_RESTART_INTERVAL = 300

    SERVERS_DIR.mkdir(exist_ok=True)

    LOGS_DIR.mkdir(exist_ok=True)

    UPLOADS_DIR.mkdir(exist_ok=True)
