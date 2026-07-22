import os
import shutil

try:
    import psutil
    PSUTIL = True
except ImportError:
    psutil = None
    PSUTIL = False


def cpu_usage():
    if PSUTIL:
        return psutil.cpu_percent(interval=0.1)
    return 0


def ram_usage():
    if PSUTIL:
        return psutil.virtual_memory().percent

    try:
        with open("/proc/meminfo") as f:
            mem = {}
            for line in f:
                key, value = line.split(":")
                mem[key] = int(value.strip().split()[0])

        total = mem["MemTotal"]
        available = mem["MemAvailable"]

        used = total - available

        return round((used / total) * 100, 1)

    except Exception:
        return 0


def disk_usage():
    try:
        total, used, free = shutil.disk_usage("/")
        return round((used / total) * 100, 1)
    except Exception:
        return 0


def system_stats():
    return {
        "cpu": cpu_usage(),
        "ram": ram_usage(),
        "disk": disk_usage()
    }
