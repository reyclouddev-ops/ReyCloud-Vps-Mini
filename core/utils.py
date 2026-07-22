import hashlib
from pathlib import Path


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_run_command(runtime, main_file):
    ext = Path(main_file).suffix.lower()

    if runtime == "node" or ext in (".js", ".mjs", ".ts"):
        return ["node", main_file]

    elif runtime == "static":
        return [
            "python",
            "-m",
            "http.server",
            "8080"
        ]

    return [
        "python",
        "-u",
        main_file
    ]


def list_files(directory, base=""):
    result = []

    directory = Path(directory)

    if not directory.exists():
        return result

    try:
        entries = sorted(
            directory.iterdir(),
            key=lambda x: (x.is_file(), x.name.lower())
        )

        for entry in entries:

            rel = f"{base}/{entry.name}" if base else entry.name

            if entry.is_dir():

                result.append({
                    "name": entry.name,
                    "path": rel,
                    "type": "dir",
                    "size": 0
                })

                result.extend(
                    list_files(entry, rel)
                )

            else:

                result.append({
                    "name": entry.name,
                    "path": rel,
                    "type": "file",
                    "size": entry.stat().st_size
                })

    except Exception:
        pass

    return result


def format_size(size):

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    i = 0

    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1

    return f"{size:.2f} {units[i]}"
