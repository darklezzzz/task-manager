import pytest
from task_manager.core import TaskManager


@pytest.fixture
def app(tmp_path):
    return TaskManager(tmp_path / "tasks.db")


def test_create_get(app):
    task = app.create("Test", "Анна")
    assert app.get(task["id"])["assignee"] == "Анна"


def test_update(app):
    task = app.create("Test", "Анна")
    assert app.update(task["id"], status="done")["status"] == "done"


def test_delete(app):
    task = app.create("Test", "Анна")
    app.delete(task["id"])
    assert app.find() == []


def test_missing(app):
    with pytest.raises(ValueError):
        app.get(999)


@pytest.mark.parametrize(
    "fields", [{"priority": "urgent"}, {"status": "bad"}, {"due": "not-date"}, {"title": ""}]
)
def test_invalid(app, fields):
    values = dict(title="Test", assignee="Анна") | fields
    with pytest.raises(ValueError):
        app.create(**values)


def test_filter(app):
    app.create("One", "Анна", priority="high")
    app.create("Two", "Борис", status="done")
    assert len(app.find(assignee="Анна", priority="high", status="todo")) == 1


def test_statistics_after_merge(app):
    assert app.statistics()["completion_percent"] == 0
    app.create("One", "Анна", status="done")
    app.create("Two", "Борис")
    assert app.statistics()["completion_percent"] == 50
    assert len(app.find(status="done")) == 1


def test_restart(app, tmp_path):
    task = app.create("Keep", "Анна")
    app.db.close()
    assert TaskManager(tmp_path / "tasks.db").get(task["id"])["title"] == "Keep"


def test_unknown_update(app):
    task = app.create("Keep", "Анна")
    with pytest.raises(ValueError):
        app.update(task["id"], unexpected=True)
