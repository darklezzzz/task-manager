"""Command line interface; run --help for available operations."""

import argparse
import json
import sqlite3

from .core import TaskManager


def main():
    parser = argparse.ArgumentParser(description="task-manager")
    parser.add_argument("--database", default=".data/application.db")
    commands = parser.add_subparsers(dest="command", required=True)
    sub = commands.add_parser("create")
    sub.add_argument("title")
    sub.add_argument("assignee")
    sub.add_argument("--priority", default="normal")
    sub.add_argument("--status", default="todo")
    sub.add_argument("--date")
    sub = commands.add_parser("get")
    sub.add_argument("id", type=int)
    sub = commands.add_parser("update")
    sub.add_argument("id", type=int)
    sub.add_argument("fields")
    sub = commands.add_parser("delete")
    sub.add_argument("id", type=int)
    sub = commands.add_parser("list")
    sub.add_argument("--assignee")
    sub.add_argument("--priority")
    sub.add_argument("--status")
    sub = commands.add_parser("statistics")
    args = parser.parse_args()
    try:
        app = TaskManager(args.database)
        if args.command == "create":
            result = app.create(args.title, args.assignee, args.priority, args.status, args.date)
        if args.command == "get":
            result = app.get(args.id)
        if args.command == "update":
            result = app.update(args.id, **json.loads(args.fields))
        if args.command == "delete":
            result = app.delete(args.id)
        if args.command == "list":
            result = app.find(args.assignee, args.priority, args.status)
        if args.command == "statistics":
            result = app.statistics()
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if not isinstance(result, str)
            else result
        )
        if isinstance(result, dict) and result.get("passed") is False:
            return 1
        return 0
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(2, f"Ошибка: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
