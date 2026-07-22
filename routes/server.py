from flask import (
    Blueprint,
    request,
    jsonify,
    redirect,
    url_for,
    session
)

from models.database import load_data, save_data
from core.process_manager import (
    start_process,
    stop_process
)

server = Blueprint("server", __name__)


@server.route("/server/create", methods=["POST"])
def create_server():

    if "username" not in session:
        return redirect(url_for("auth.login"))

    data = load_data()

    name = request.form.get("name", "").strip()

    runtime = request.form.get("runtime", "python")

    if not name:
        return redirect(url_for("dashboard.dashboard"))

    if name in data["servers"]:
        return redirect(url_for("dashboard.dashboard"))

    data["servers"][name] = {
        "owner": session["username"],
        "runtime": runtime,
        "status": "stopped",
        "main_file": "",
        "main_command": "",
        "pid": None,
        "port": 8080
    }

    save_data(data)

    return redirect(url_for("dashboard.dashboard"))


@server.route("/server/start/<name>", methods=["POST"])
def start(name):

    ok = start_process(name)

    return jsonify({
        "success": ok
    })


@server.route("/server/stop/<name>", methods=["POST"])
def stop(name):

    ok = stop_process(name)

    return jsonify({
        "success": ok
    })


@server.route("/server/delete/<name>", methods=["POST"])
def delete(name):

    data = load_data()

    if name in data["servers"]:
        del data["servers"][name]
        save_data(data)

    return jsonify({
        "success": True
    })
