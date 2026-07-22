from flask import Flask

from config import Config

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

# Buat folder servers jika belum ada
Config.SERVERS_DIR.mkdir(exist_ok=True)

# Jalankan background service
from core.keep_alive import start_keep_alive
from core.auto_restart import start_auto_restart

start_keep_alive()
start_auto_restart()

# Load semua routes
import routes

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=Config.PORT,
        debug=False
    )
