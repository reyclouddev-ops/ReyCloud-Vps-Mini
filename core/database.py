import json

from config import Config


def default_data():
    return {
        "servers": {},
        "users": {},
        "settings": {
            "maintenance": Config.MAINTENANCE,
            "maintenance_msg": Config.MAINTENANCE_MESSAGE,
            "theme_color": Config.THEME_COLOR,
            "normal_password": Config.DEFAULT_PASSWORD,
            "site_name": Config.SITE_NAME,
            "auto_restart_interval": Config.AUTO_RESTART_INTERVAL
        }
    }


def load_data():
    if not Config.DATA_FILE.exists():
        return default_data()

    try:
        with open(Config.DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_data()


def save_data(data):
    with open(Config.DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
            default=str
        )
