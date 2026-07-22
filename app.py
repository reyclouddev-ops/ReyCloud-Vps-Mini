from flask import Flask

from config import Config

app = Flask(__name__)

app.config["SECRET_KEY"] = Config.SECRET_KEY

from routes import *

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=False
    )
