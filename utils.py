import json
import hashlib

from config import Config

def load_data():

    if Config.DATA_FILE.exists():

        try:
            return json.loads(
                Config.DATA_FILE.read_text()
            )

        except Exception:
            pass

    return {

        "servers": {},

        "users": {},

        "settings": {

            "maintenance": False,

            "maintenance_msg":
            "System Under Maintenance.",

            "theme_color": "#00ff41",

            "normal_password":
            Config.NORMAL_PASSWORD,

            "site_name":
            "REYCLOUD VPS MINI"

        }

    }


def save_data(data):

    Config.DATA_FILE.write_text(

        json.dumps(
            data,
            indent=2,
            default=str
        )

    )


def hash_password(password):

    return hashlib.sha256(

        password.encode()

    ).hexdigest()
