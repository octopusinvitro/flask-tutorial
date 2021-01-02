from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr import db

blueprint = Blueprint('blog', __name__)


@blueprint.route('/')
def index():
    return render_template('blog/index.html', posts=db.get_posts())


@blueprint.route('/create')
@login_required
def new():
    return render_template('blog/create.html')


@blueprint.route('/create', methods=['POST'])
@login_required
def create():
    title = request.form['title']
    body = request.form['body']

    error = _validate_form(title)
    if error is not None:
        flash(error)
        return render_template('blog/create.html')

    db.create_post(title, body, g.user['id'])
    return redirect(url_for('blog.index'))


@blueprint.route('/<int:id>/update')
@login_required
def edit(id):
    post = db.get_post(id)
    abort_if_missing_or_forbidden(post)
    return render_template('blog/update.html', post=post)


@blueprint.route('/<int:id>/update', methods=['POST'])
@login_required
def update(id):
    post = db.get_post(id)
    abort_if_missing_or_forbidden(post)

    title = request.form['title']
    body = request.form['body']

    error = _validate_form(title)
    if error is not None:
        flash(error)
        return render_template('blog/update.html', post=post)

    db.update_post(title, body, id)
    return redirect(url_for('blog.index'))


@blueprint.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = db.get_post(id)
    abort_if_missing_or_forbidden(post)

    db.delete_post(id)
    return redirect(url_for('blog.index'))


def abort_if_missing_or_forbidden(post, check_author=True):
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)


def _validate_form(title):
    if not title:
        return 'Title is required.'
