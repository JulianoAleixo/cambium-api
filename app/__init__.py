from flask import Flask

from app.config.settings import Config
from app.routes.exchange import exchange_bp
from app.routes.frankfurter import frankfurter_bp
from app.routes.health import health_bp


def create_app(config: Config = None) -> Flask:
    app = Flask(__name__)

    if config is None:
        config = Config()

    app.config.from_object(config)

    app.register_blueprint(health_bp)
    app.register_blueprint(frankfurter_bp)
    app.register_blueprint(exchange_bp)

    return app
