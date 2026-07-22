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

@app.route("/api/stats")
@login_required
def api_stats():
    return jsonify(system_stats())
