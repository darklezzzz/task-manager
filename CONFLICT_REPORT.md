# Контролируемый конфликт Git

Две ветки созданы от общего состояния main. В обеих изменена одна и та же область
учебного файла examples/team_commands.txt.

- feature-filter: `40597898dd88fca19df0be2a068facc84119cbcf`
- feature-statistics: `1480fc8003f9bdad0ac6de41d55ebd0a0b881790`
- Итоговый merge commit с двумя родителями: `007a7d81c3ad0459b0f673e44e988d576908bb8f`

## Результат попытки слияния

```text
Auto-merging examples/team_commands.txt
CONFLICT (content): Merge conflict in examples/team_commands.txt
Automatic merge failed; fix conflicts and then commit the result.
UU examples/team_commands.txt
```

## Реальные маркеры конфликта до разрешения

```text
task-manager list
<<<<<<< HEAD
task-manager list --assignee Анна --priority high --status todo
=======
task-manager statistics
>>>>>>> feature-statistics
```

## Разрешение

Оставлены команды фильтрации и статистики. Маркеры удалены, файл добавлен в индекс,
выполнен git commit. Обе функции проверяются tests/test_tasks.py, включая
`test_statistics_after_merge` и `test_filter`.

```sh
git show --format=fuller 007a7d81c3ad0459b0f673e44e988d576908bb8f
git log --graph --oneline --all
uv run pytest -v
```
