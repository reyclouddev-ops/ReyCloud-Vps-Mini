import os
import signal
import subprocess

try:
    import psutil
    PSUTIL = True
except ImportError:
    psutil = None
    PSUTIL = False


RUNNING_PROCESSES = {}


def is_process_alive(pid):
    if not pid:
        return False

    if PSUTIL:
        try:
            p = psutil.Process(pid)
            return p.is_running()
        except Exception:
            return False

    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


def kill_process(pid):
    if not pid:
        return

    if PSUTIL:
        try:
            proc = psutil.Process(pid)

            for child in proc.children(recursive=True):
                try:
                    child.kill()
                except Exception:
                    pass

            proc.kill()

        except Exception:
            pass

        return

    try:
        os.kill(pid, signal.SIGKILL)
    except Exception:
        pass


def start_process(
    name,
    command,
    cwd,
    env=None,
    log_file=None
):

    if log_file:
        log = open(log_file, "a")
    else:
        log = subprocess.DEVNULL

    proc = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=log,
        stderr=log,
        env=env
    )

    RUNNING_PROCESSES[name] = {
        "proc": proc,
        "log": log
    }

    return proc.pid


def stop_process(name):

    if name not in RUNNING_PROCESSES:
        return False

    proc = RUNNING_PROCESSES[name]["proc"]

    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass

    try:
        RUNNING_PROCESSES[name]["log"].close()
    except Exception:
        pass

    del RUNNING_PROCESSES[name]

    return True
