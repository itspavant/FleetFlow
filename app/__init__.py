from flask import Flask
from .extensions import db, login_manager, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    # Register blueprints (we’ll add later)
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app