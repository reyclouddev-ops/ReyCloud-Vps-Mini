from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    send_file,
    abort
)

from config import Config

from core.database import (
    load_data,
    save_data
)

from core.utils import (
    hash_password,
    get_run_command,
    list_files,
    format_size
)

from core.system import system_stats

from core.process_manager import (
    RUNNING_PROCESSES,
    is_process_alive,
    kill_process,
    start_process,
    stop_process
)

from core.auto_restart import start_auto_restart
from core.keep_alive import start_keep_alive

import io
import os
import shutil
import zipfile
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

Config.SERVERS_DIR.mkdir(exist_ok=True)

start_keep_alive()
start_auto_restart()

from core.database import (
    load_data,
    save_data
)

from core.utils import (
    hash_password,
    get_run_command,
    list_files,
    format_size
)

from core.process_manager import (
    RUNNING_PROCESSES,
    is_process_alive,
    kill_process,
    start_process,
    stop_process
)

from core.system import system_stats
from core.auto_restart import start_auto_restart
from core.keep_alive import start_keep_alive

app = Flask(__name__)

app.config["SECRET_KEY"] = Config.SECRET_KEY

start_auto_restart()

app.config["SECRET_KEY"] = Config.SECRET_KEY

start_keep_alive()

@app.route("/")
def login():
    ...

@app.route("/dashboard")
def dashboard():
    ...

@app.route("/server/create")
def create_server():
    ...

@app.route("/server/<name>/start")
def start():
    ...

@app.route("/server/<name>/stop")
def stop():
    ...

@app.route("/server/<name>/upload")
def upload():
    ...

@app.route("/server/<name>/logs")
def logs():
    ...

@app.route("/api/stats")
def api_stats():
    return jsonify(system_stats())

@app.route("/api/ping")
def ping():
    return "pong"
