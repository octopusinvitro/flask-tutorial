from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr import db

blueprint = Blueprint('login', __name__, url_prefix='/auth')


@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None

    if user_id is not None:
        g.user = db.get_user('id', user_id)


@blueprint.route('/login')
def new():
    return render_template('auth/login.html')


@blueprint.route('/login', methods=['POST'])
def create():
    username = request.form['username']
    password = request.form['password']

    user = db.get_user('username', username)

    error = _validate_form(user, password)
    if error is not None:
        flash(error)
        return render_template('auth/login.html')

    session.clear()
    session['user_id'] = user['id']

    return redirect(url_for('index'))


@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def _validate_form(user, password):
    if user is None:
        return 'Incorrect username. Not registered?'
    if not db.is_same_password(user, password):
        return 'Incorrect password.'
