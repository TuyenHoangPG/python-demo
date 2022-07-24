"""Flask app initialization via factory pattern."""
from http.client import INTERNAL_SERVER_ERROR
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from shared.configs import get_config
from shared.constants.message import ERROR
from shared.utils.response import error_server_error


cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    from api.v1 import api_v1

    app.register_blueprint(api_v1)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.errorhandler(INTERNAL_SERVER_ERROR)
    def handle_server_error(e):
        print(e)
        return error_server_error(ERROR["SERVER_ERROR"])

    return app
