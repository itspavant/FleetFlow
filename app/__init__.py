from flask import Flask
from .extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    # Import ALL models so SQLAlchemy registers them
    from app import models

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.vehicles import vehicles_bp
    from app.routes.drivers import drivers_bp
    from app.routes.trips import trips_bp
    from app.routes.maintenance import maintenance_bp
    from app.routes.fuel import fuel_bp
    from app.routes.analytics import analytics_bp
    from app.routes.performance import performance_bp
    from app.routes.expenses import expenses_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(fuel_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(performance_bp)
    app.register_blueprint(expenses_bp)

    # User loader
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app