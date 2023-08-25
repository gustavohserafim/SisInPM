import os
from flask import Flask


def create_app(test_config=None, logger_override=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if logger_override:
        # working solely with the flask logger
        app.logger.handlers = logger_override.handlers
        app.logger.setLevel(logger_override.level)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import core, auth
    app.register_blueprint(core.bp)
    app.register_blueprint(auth.bp)

    return app
