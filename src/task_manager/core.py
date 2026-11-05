"""SQLite-backed team task management."""

import sqlite3
from datetime import date
from pathlib import Path

STATUSES = ("todo", "in_progress", "done")
PRIORITIES = ("low", "normal", "high")


class TaskManager:
    def __init__(self, database):
        Path(database).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(database)
        self.db.row_factory = sqlite3.Row
        self.db.execute("""CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY, title TEXT NOT NULL, assignee TEXT NOT NULL,
            priority TEXT NOT NULL, status TEXT NOT NULL, date TEXT NOT NULL)""")

    def _validate(self, title, assignee, priority, status, due):
        if not title.strip() or not assignee.strip():
            raise ValueError("Название и исполнитель обязательны")
        if priority not in PRIORITIES or status not in STATUSES:
            raise ValueError("Неверный приоритет или статус")
        try:
            date.fromisoformat(due)
        except (ValueError, TypeError) as exc:
            raise ValueError("Дата должна иметь формат YYYY-MM-DD") from exc

    def create(self, title, assignee, priority="normal", status="todo", due=None):
        due = due or date.today().isoformat()
        self._validate(title, assignee, priority, status, due)
        with self.db:
            cur = self.db.execute(
                "INSERT INTO tasks(title,assignee,priority,status,date) VALUES(?,?,?,?,?)",
                (title, assignee, priority, status, due),
            )
        return self.get(cur.lastrowid)

    def get(self, ident):
        row = self.db.execute("SELECT * FROM tasks WHERE id=?", (ident,)).fetchone()
        if row is None:
            raise ValueError("Задача не найдена")
        return dict(row)

    def update(self, ident, **fields):
        item = self.get(ident)
        if not fields or fields.keys() - {"title", "assignee", "priority", "status", "date"}:
            raise ValueError("Неизвестные или пустые поля обновления")
        item.update(fields)
        self._validate(
            item["title"], item["assignee"], item["priority"], item["status"], item["date"]
        )
        with self.db:
            self.db.execute(
                "UPDATE tasks SET title=?,assignee=?,priority=?,status=?,date=? WHERE id=?",
                tuple(item[k] for k in ("title", "assignee", "priority", "status", "date"))
                + (ident,),
            )
        return self.get(ident)

    def delete(self, ident):
        self.get(ident)
        with self.db:
            self.db.execute("DELETE FROM tasks WHERE id=?", (ident,))

    def find(self, assignee=None, priority=None, status=None):
        clauses, values = [], []
        for key, value in [("assignee", assignee), ("priority", priority), ("status", status)]:
            if value is not None:
                clauses.append(key + "=?")
                values.append(value)
        query = "SELECT * FROM tasks" + (" WHERE " + " AND ".join(clauses) if clauses else "")
        return [dict(r) for r in self.db.execute(query + " ORDER BY id", values)]

    def statistics(self):
        counts = {s: 0 for s in STATUSES}
        counts.update(dict(self.db.execute("SELECT status,COUNT(*) FROM tasks GROUP BY status")))
        total = sum(counts.values())
        return dict(
            counts, total=total, completion_percent=100 * counts["done"] / total if total else 0
        )
