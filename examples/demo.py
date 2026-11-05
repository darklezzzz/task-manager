import json
import tempfile
from pathlib import Path

from task_manager.core import TaskManager

with tempfile.TemporaryDirectory() as directory:
    app = TaskManager(Path(directory) / "tasks.db")
    app.create("Тестирование", "Анна", priority="high", status="done")
    app.create("Документация", "Борис", status="in_progress")
    result = {
        "tasks": app.find(),
        "filtered": app.find("Анна", "high", "done"),
        "statistics": app.statistics(),
    }
    (Path(__file__).parent / "tasks.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(result["statistics"])
