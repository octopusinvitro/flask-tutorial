import os

from flask import Flask

from . import blog, db
from .auth import login, register


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(register.blueprint)
    app.register_blueprint(login.blueprint)
    app.register_blueprint(blog.blueprint)
    app.add_url_rule('/', endpoint='index')

    return app
