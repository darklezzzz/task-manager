# Задание 4. Управление задачами и конфликтами Git

SQLite tasks; CRUD, комбинированная фильтрация, статистика. Реальный учебный конфликт задокументирован в CONFLICT_REPORT.md.

## Установка и запуск

Нужны Python 3.11+ и uv. Проект является самостоятельным Git-репозиторием;
его можно скопировать отдельно от учебного workspace. Внутри этого workspace
для команд пакетов используйте `uv run --all-packages <команда>`, либо сначала
из корня выполните `uv sync --all-packages`, затем запускайте команды из `.venv/bin/`.
После отдельного клонирования:

```sh
uv sync --locked
uv run task-manager --help
uv run pytest -v
uv run ruff check .
```

Все команды ниже выполняются из корня отдельного проекта с новой базой `.data/application.db`.
Команды с идентификатором 1 предполагают пустую базу. Повторная регистрация ID — ошибка.
Вывод — UTF-8 / JSON; неверные аргументы завершаются с кодом 2.

```sh
uv run task-manager create 'Написать тесты' Анна --priority high
uv run task-manager list --assignee Анна --priority high --status todo
uv run task-manager update 1 '{"status":"done"}'
uv run task-manager statistics
```

## Архитектура и алгоритм

Проверка полей → транзакция SQLite → CRUD → фильтры → агрегирование по статусам.

Код в `src/`, автоматизированные проверки в `tests/`, воспроизводимая демонстрация —
`examples/demo.py`, результаты — `examples/`. Запуск: `uv run python examples/demo.py`.
Она использует временное хранилище и обновляет только демонстрационные результаты.

## Связь с управлением конфигурацией

Идентификация, история и проверяемые состояния описаны в [SCMP.md](SCMP.md).
История версий: [CHANGELOG.md](CHANGELOG.md). Учебный отчёт: [REPORT.md](REPORT.md).
Git-доказательства: `git log --graph --oneline --all`, `git branch`, `git tag`.

## Ограничения

Нет сетевой совместной работы, авторизации и уведомлений. Дата — плановая дата задачи, формат YYYY-MM-DD.

## GitHub

[darklezzzz/task-manager](https://github.com/darklezzzz/task-manager).
