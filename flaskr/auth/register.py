from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

from flaskr import db

blueprint = Blueprint('register', __name__, url_prefix='/auth')


@blueprint.route('/register')
def new():
    return render_template('auth/register.html')


@blueprint.route('/register', methods=['POST'])
def create():
    username = request.form['username']
    password = request.form['password']

    error = _validate_form(username, password)
    if error is not None:
        flash(error)
        return render_template('auth/register.html')

    db.create_user(username, password)

    return redirect(url_for('login.new'))


def _validate_form(username, password):
    if not username:
        return 'Username is required.'
    if not password:
        return 'Password is required.'
    if db.get_user('username', username) is not None:
        return 'User {} is already registered.'.format(username)
