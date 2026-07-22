from app import app

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

from config import Config

from core.database import load_data, save_data
from core.utils import (
    hash_password,
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

import shutil
import zipfile
from datetime import datetime


# ===========================
# LOGIN
# ===========================

@app.route("/", methods=["GET", "POST"])
def login():

    if session.get("username"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        password = request.form.get("password", "").strip()

        data = load_data()

        normal_password = data["settings"].get(
            "normal_password",
            Config.NORMAL_PASSWORD
        )

        if password != normal_password:
            return render_template(
                "login.html",
                error="Password Salah!"
            )

        if "admin" not in data["users"]:
            data["users"]["admin"] = {
                "joined": datetime.now().isoformat(),
                "password_hash": hash_password(password)
            }
            save_data(data)

        session["username"] = "admin"

        return redirect(url_for("dashboard"))

    return render_template("login.html")


# ===========================
# LOGOUT
# ===========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

# ===========================
# DASHBOARD
# ===========================

@app.route("/dashboard")
def dashboard():

    if not session.get("username"):
        return redirect(url_for("login"))

    data = load_data()

    username = session["username"]

    user_servers = {}

    changed = False

    for name, server in data["servers"].items():

        if server.get("owner") != username:
            continue

        pid = server.get("pid")

        if pid and not is_process_alive(pid):
            server["status"] = "stopped"
            server["pid"] = None
            changed = True

        user_servers[name] = server

    if changed:
        save_data(data)

    running = sum(
        1
        for server in user_servers.values()
        if server.get("status") == "running"
    )

    return render_template(
        "dashboard.html",
        servers=user_servers,
        running=running,
        total=len(user_servers),
        username=username,
        site_name=data["settings"].get(
            "site_name",
            "REYCLOUD VPS MINI"
        ),
        theme_color=data["settings"].get(
            "theme_color",
            "#00ff41"
        )
    )


# ===========================
# API STATS
# ===========================

@app.route("/api/stats")
def api_stats():

    if not session.get("username"):
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    return jsonify(system_stats())


# ===========================
# API PING
# ===========================

@app.route("/api/ping")
def ping():

    return jsonify({
        "success": True,
        "message": "pong"
    })

# ===========================
# CREATE SERVER
# ===========================

@app.route("/server/create", methods=["POST"])
def create_server():

    if not session.get("username"):
        return redirect(url_for("login"))

    data = load_data()

    name = request.form.get("name", "").strip().replace(" ", "-")
    runtime = request.form.get("runtime", "python")

    if not name:
        return redirect(url_for("dashboard"))

    if name in data["servers"]:
        return redirect(url_for("dashboard"))

    data["servers"][name] = {
        "name": name,
        "owner": session["username"],
        "runtime": runtime,
        "status": "stopped",
        "pid": None,
        "port": 8080,
        "main_file": "",
        "main_command": "",
        "created": datetime.now().isoformat()
    }

    save_data(data)

    (Config.SERVERS_DIR / name / "extracted").mkdir(
        parents=True,
        exist_ok=True
    )

    return redirect(url_for("server_detail", name=name))


# ===========================
# DELETE SERVER
# ===========================

@app.route("/server/delete/<name>", methods=["POST"])
def delete_server(name):

    if not session.get("username"):
        return redirect(url_for("login"))

    data = load_data()

    server = data["servers"].get(name)

    if not server:
        return redirect(url_for("dashboard"))

    if server["owner"] != session["username"]:
        return "Access Denied", 403

    stop_process(name)

    shutil.rmtree(
        Config.SERVERS_DIR / name,
        ignore_errors=True
    )

    del data["servers"][name]

    save_data(data)

    return redirect(url_for("dashboard"))


# ===========================
# SERVER DETAIL
# ===========================

@app.route("/server/<name>")
def server_detail(name):

    if not session.get("username"):
        return redirect(url_for("login"))

    data = load_data()

    server = data["servers"].get(name)

    if not server:
        return "Server Not Found", 404

    if server["owner"] != session["username"]:
        return "Access Denied", 403

    if server.get("pid") and not is_process_alive(server["pid"]):
        server["status"] = "stopped"
        server["pid"] = None
        save_data(data)

    files = list_files(
        Config.SERVERS_DIR / name / "extracted"
    )

    return render_template(
        "server.html",
        server_name=name,
        config=server,
        files=files

      # ===========================
# UPLOAD FILE / ZIP
# ===========================

@app.route("/server/<name>/upload", methods=["POST"])
def upload_file(name):

    if not session.get("username"):
        return jsonify({"success": False}), 401

    data = load_data()

    server = data["servers"].get(name)

    if not server:
        return jsonify({
            "success": False,
            "error": "Server tidak ditemukan."
        }), 404

    if server["owner"] != session["username"]:
        return jsonify({
            "success": False,
            "error": "Access denied."
        }), 403

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "Tidak ada file."
        })

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "Nama file kosong."
        })

    extract_dir = Config.SERVERS_DIR / name / "extracted"
    extract_dir.mkdir(parents=True, exist_ok=True)

    upload_path = Config.SERVERS_DIR / name / file.filename

    file.save(upload_path)

    extracted = []

    if file.filename.lower().endswith(".zip"):

        try:

            with zipfile.ZipFile(upload_path, "r") as z:

                z.extractall(extract_dir)

                extracted = [
                    f.filename
                    for f in z.infolist()
                    if not f.is_dir()
                ]

            upload_path.unlink(missing_ok=True)

        except Exception as e:

            upload_path.unlink(missing_ok=True)

            return jsonify({
                "success": False,
                "error": str(e)
            })

    else:

        destination = extract_dir / file.filename

        shutil.move(
            str(upload_path),
            str(destination)
        )

        extracted.append(file.filename)

    return jsonify({
        "success": True,
        "files": extracted
    })


# ===========================
# SAVE SERVER SETTINGS
# ===========================

@app.route("/server/<name>/settings", methods=["POST"])
def save_server_settings(name):

    if not session.get("username"):
        return jsonify({"success": False}), 401

    data = load_data()

    server = data["servers"].get(name)

    if not server:
        return jsonify({
            "success": False
        }), 404

    if server["owner"] != session["username"]:
        return jsonify({
            "success": False
        }), 403

    payload = request.get_json()

    server["main_file"] = payload.get(
        "main_file",
        server.get("main_file", "")
    )

    server["main_command"] = payload.get(
        "main_command",
        server.get("main_command", "")
    )

    server["port"] = int(
        payload.get(
            "port",
            server.get("port", 8080)
        )
    )

    data["servers"][name] = server

    save_data(data)

    return jsonify({
        "success": True
    })

# ==========================
# LOGS
# ==========================

@app.route("/server/<name>/logs")
def server_logs(name):
    data = load_data()

    if name not in data["servers"]:
        return jsonify({
            "success": False,
            "message": "Server tidak ditemukan"
        }), 404

    log_file = Config.SERVERS_DIR / name / "logs.txt"

    if not log_file.exists():
        return jsonify({
            "success": True,
            "logs": ""
        })

    try:
        logs = log_file.read_text(errors="ignore")
    except Exception:
        logs = ""

    return jsonify({
        "success": True,
        "logs": logs
    })


@app.route("/server/<name>/logs/clear", methods=["POST"])
def clear_logs(name):
    data = load_data()

    if name not in data["servers"]:
        return jsonify({
            "success": False
        }), 404

    log_file = Config.SERVERS_DIR / name / "logs.txt"

    log_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.write_text("")

    return jsonify({
        "success": True
    })

# ==========================
# SERVER STATUS
# ==========================

@app.route("/server/<name>/status")
def server_status(name):

    data = load_data()


    if name not in data["servers"]:
        return jsonify({
            "success": False,
            "message": "Server tidak ditemukan"
        }), 404



    server_path = Config.SERVERS_DIR / name


    status_file = server_path / "status.txt"


    status = "offline"


    if status_file.exists():

        try:
            status = status_file.read_text().strip()

        except:
            status = "unknown"



    return jsonify({
        "success": True,
        "server": name,
        "status": status
    })




# ==========================
# START SERVER
# ==========================

@app.route("/server/<name>/start", methods=["POST"])
def start_server(name):

    data = load_data()


    if name not in data["servers"]:
        return jsonify({
            "success": False,
            "message":"Server tidak ditemukan"
        }),404



    server_path = Config.SERVERS_DIR / name

    server_path.mkdir(
        parents=True,
        exist_ok=True
    )


    status_file = server_path / "status.txt"


    status_file.write_text(
        "running"
    )


    log_file = server_path / "logs.txt"


    with open(log_file,"a") as f:
        f.write(
            "\n[SERVER] Server started"
        )


    return jsonify({
        "success":True,
        "message":"Server berhasil dinyalakan"
    })





# ==========================
# STOP SERVER
# ==========================

@app.route("/server/<name>/stop", methods=["POST"])
def stop_server(name):

    data = load_data()


    if name not in data["servers"]:
        return jsonify({
            "success":False,
            "message":"Server tidak ditemukan"
        }),404



    server_path = Config.SERVERS_DIR / name


    status_file = server_path / "status.txt"


    status_file.write_text(
        "offline"
    )



    with open(server_path / "logs.txt","a") as f:
        f.write(
            "\n[SERVER] Server stopped"
        )


    return jsonify({
        "success":True,
        "message":"Server dimatikan"
    })





# ==========================
# RESTART SERVER
# ==========================

@app.route("/server/<name>/restart", methods=["POST"])
def restart_server(name):

    data = load_data()


    if name not in data["servers"]:
        return jsonify({
            "success":False,
            "message":"Server tidak ditemukan"
        }),404



    server_path = Config.SERVERS_DIR / name


    status_file = server_path / "status.txt"


    status_file.write_text(
        "restarting"
    )


    with open(server_path / "logs.txt","a") as f:
        f.write(
            "\n[SERVER] Server restarting"
        )


    status_file.write_text(
        "running"
    )


    return jsonify({
        "success":True,
        "message":"Server berhasil restart"
    })
