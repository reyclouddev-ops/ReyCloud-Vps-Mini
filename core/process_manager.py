import os
import signal
import subprocess

try:
    import psutil
    PSUTIL = True
except Exception:
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
            p = psutil.Process(pid)
            p.kill()
        except Exception:
            pass
        return

    try:
        os.kill(pid, signal.SIGKILL)
    except Exception:
        pass


def start_process(command, cwd=None, env=None, logfile=None):
    log = open(logfile, "a") if logfile else subprocess.DEVNULL

    proc = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=log,
        stderr=log,
        env=env,
        preexec_fn=os.setsid if os.name != "nt" else None
    )

    RUNNING_PROCESSES[proc.pid] = {
        "proc": proc,
        "log": log
    }

    return proc


def stop_process(pid):
    if pid not in RUNNING_PROCESSES:
        kill_process(pid)
        return

    entry = RUNNING_PROCESSES[pid]

    try:
        entry["proc"].terminate()
    except Exception:
        pass

    try:
        entry["log"].close()
    except Exception:
        pass

    RUNNING_PROCESSES.pop(pid, None)
