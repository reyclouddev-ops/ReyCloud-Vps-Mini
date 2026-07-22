import json
import hashlib
from config import Config


def load_data():
    if Config.DATA_FILE.exists():
        try:
            return json.loads(Config.DATA_FILE.read_text())
        except Exception:
            pass

    return {
        "servers": {},
        "users": {},
        "settings": {
            "maintenance": False,
            "maintenance_msg": "System under maintenance.",
            "theme_color": "#00ff41",
            "normal_password": Config.NORMAL_PASSWORD,
            "site_name": "REYCLOUD VPS MINI",
            "auto_restart_interval": 300
        }
    }


def save_data(data):
    Config.DATA_FILE.write_text(
        json.dumps(data, indent=2, default=str)
    )


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_settings():
    return load_data().get("settings", {})


def get_theme_color():
    return get_settings().get("theme_color", "#00ff41")


def get_site_name():
    return get_settings().get(
        "site_name",
        "REYCLOUD VPS MINI"
    )
