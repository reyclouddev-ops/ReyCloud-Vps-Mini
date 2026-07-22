from app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    send_file,
    abort
)

import os
import io
import json
import shutil
import zipfile
from datetime import datetime
from functools import wraps
from pathlib import Path

from config import Config

from core.database import (
    load_data,
    save_data,
    hash_password,
    get_settings,
    get_theme_color,
    get_site_name
)

from core.process_manager import (
    RUNNING_PROCESSES,
    is_process_alive,
    kill_process,
    start_process,
    stop_process
)

# =====================================
# PATH
# =====================================

BASE_DIR = Config.BASE_DIR
SERVERS_DIR = Config.SERVERS_DIR

# =====================================
# TEMPLATE
# =====================================

@app.context_processor
def inject_theme():
    return {
        "theme_color": get_theme_color()
    }

# =====================================
# LOGIN REQUIRED
# =====================================

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if not session.get("username"):
            return redirect(url_for("login"))

        settings = get_settings()

        if settings.get("maintenance"):
            return render_template(
                "maintenance.html",
                message=settings.get("maintenance_msg"),
                site_name=get_site_name(),
                theme_color=get_theme_color()
            )

        return func(*args, **kwargs)

    return wrapper

# =====================================
# ROUTES
# =====================================

# Login
# Dashboard
# Create Server
# Delete Server
# Upload File
# Start Server
# Stop Server
# Logs
# Settings
# API

# Semua route akan dipindahkan bertahap ke sini.
