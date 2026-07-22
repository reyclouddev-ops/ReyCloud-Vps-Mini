import threading
import time
import urllib.request
import os


def ping():

    try:

        url = os.environ.get("RENDER_EXTERNAL_URL")

        if url:
            target = f"{url}/api/ping"

        else:
            port = os.environ.get("PORT", "5000")
            target = f"http://127.0.0.1:{port}/api/ping"

        req = urllib.request.Request(
            target,
            headers={
                "User-Agent": "ReyCloud-KeepAlive"
            }
        )

        urllib.request.urlopen(req, timeout=10)

    except Exception:
        pass


def keep_alive():

    while True:

        ping()

        time.sleep(240)


def start_keep_alive():

    threading.Thread(
        target=keep_alive,
        daemon=True
    ).start()
