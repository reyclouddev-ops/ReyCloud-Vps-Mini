import os
from pathlib import Path

class Config:
    # ==========================
    # APP
    # ==========================
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        os.urandom(24).hex()
    )

    PORT = int(os.getenv("PORT", 5000))

    DEBUG = False

    # ==========================
    # PROJECT PATH
    # ==========================
    BASE_DIR = Path(__file__).parent

    DATA_FILE = BASE_DIR / "data.json"

    SERVERS_DIR = BASE_DIR / "servers"

    TEMPLATES_DIR = BASE_DIR / "templates"

    STATIC_DIR = BASE_DIR / "static"

    # ==========================
    # LOGIN
    # ==========================
    DEFAULT_PASSWORD = os.getenv(
        "NORMAL_PASSWORD",
        "Rey190327"
    )

    # ==========================
    # PANEL
    # ==========================
    DEFAULT_PORT = 8080

    AUTO_RESTART_INTERVAL = 300

    LOG_LIMIT = 1024 * 1024

    MAX_LOG_LINES = 200

    # ==========================
    # WEBSITE
    # ==========================
    SITE_NAME = "ReyCloud VPS Mini"

    THEME_COLOR = "#00ff41"

    MAINTENANCE = False

    MAINTENANCE_MESSAGE = "System under maintenance."
