import threading
import time
import os

from config import Config
from core.database import load_data, save_data
from core.process_manager import (
    is_process_alive,
    kill_process,
    start_process
)
from core.utils import get_run_command


def auto_restart_server(name):
    data = load_data()

    server = data["servers"].get(name)

    if not server:
        return

    pid = server.get("pid")

    if pid and is_process_alive(pid):
        kill_process(pid)

    main_file = server.get("main_file", "main.py")

    extract_dir = Config.SERVERS_DIR / name / "extracted"

    if not (extract_dir / main_file).exists():
        return

    if server.get("main_command"):
        cmd = server["main_command"].split()
    else:
        cmd = get_run_command(
            server.get("runtime", "python"),
            main_file
        )

    log_file = Config.SERVERS_DIR / name / "logs.txt"

    pid = start_process(
        name=name,
        command=cmd,
        cwd=str(extract_dir),
        env={
            **os.environ,
            "PORT": str(server.get("port", 8080))
        },
        log_file=str(log_file)
    )

    server["pid"] = pid
    server["status"] = "running"

    save_data(data)


def auto_restart_monitor():

    while True:

        try:

            data = load_data()

            interval = data["settings"].get(
                "auto_restart_interval",
                Config.AUTO_RESTART_INTERVAL
            )

            for name, server in data["servers"].items():

                pid = server.get("pid")

                if pid and not is_process_alive(pid):

                    server["status"] = "stopped"
                    server["pid"] = None

                    auto_restart_server(name)

            save_data(data)

            time.sleep(interval)

        except Exception:

            time.sleep(30)


def start_auto_restart():

    threading.Thread(
        target=auto_restart_monitor,
        daemon=True
    ).start()
