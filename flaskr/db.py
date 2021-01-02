import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def create_user(username, password):
    db = get_db()
    db.execute(
        'INSERT INTO user (username, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()


def get_user(key, value):
    return get_db().execute('SELECT * FROM user WHERE %s = ?' % (key), (value,)).fetchone()


def is_same_password(user, password):
    return check_password_hash(user['password'], password)


def get_posts():
    return get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()


def get_post(id):
    return get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()


def create_post(title, body, author_id):
    db = get_db()
    db.execute(
        'INSERT INTO post (title, body, author_id)'
        ' VALUES (?, ?, ?)',
        (title, body, author_id)
    )
    db.commit()


def update_post(title, body, id):
    db = get_db()
    db.execute(
        'UPDATE post SET title = ?, body = ? WHERE id = ?', (title, body, id)
    )
    db.commit()


def update_post_id(author_id, id):
    db = get_db()
    db.execute('UPDATE post SET author_id = ? WHERE id = ?', (author_id, id))
    db.commit()


def delete_post(id):
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()


def get_posts_count():
    return get_db().execute('SELECT COUNT(id) FROM post').fetchone()[0]
