from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from .config import Config
from .logging_config import setup_logging
from app.errors.handlers import register_error_handlers

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    setup_logging(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    register_error_handlers(app)

    return app
