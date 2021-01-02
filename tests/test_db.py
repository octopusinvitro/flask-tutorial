import sqlite3

import pytest
from flask import g
from flaskr import db


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])

    assert 'Initialized' in result.output
    assert Recorder.called


def test_init_db(app):
    with app.app_context():
        db.init_db()
        database = db.get_db()
        assert database.execute('SELECT * FROM user').fetchone() is None
        assert database.execute('SELECT * FROM post').fetchone() is None


def test_get_db_saves_it_globally(app):
    with app.app_context():
        assert 'db' not in g

        database = db.get_db()

        assert 'db' in g
        assert g.db == database


def test_get_db_returns_row_objects(app):
    with app.app_context():
        database = db.get_db()
        assert database.row_factory == sqlite3.Row


def test_close_db_removes_it_from_globals(app):
    with app.app_context():
        db.close_db()
        assert 'db' not in g


def test_close_db_closes_db(app):
    with app.app_context():
        database = db.close_db()

        with pytest.raises(AttributeError) as error:
            database.execute('SELECT 1')

        assert "object has no attribute 'execute'" in str(error.value)


def test_close_db_raises_error_when_reading(app):
    with app.app_context():
        database = db.get_db()

    with pytest.raises(sqlite3.ProgrammingError) as error:
        database.execute('SELECT 1')

    assert 'closed' in str(error.value)
