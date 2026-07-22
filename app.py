from flask import Flask

from config import Config

app = Flask(__name__)

app.config["SECRET_KEY"] = Config.SECRET_KEY

Config.SERVERS_DIR.mkdir(exist_ok=True)
