from flask import Flask
from .extensions import db, login_manager, migrate
from app.models.user import User
from app.extensions import login_manager
from app.models import user, vehicle, driver, trip
from app.models import user, vehicle, driver, trip, maintenance
from app.models import user, vehicle, driver, trip, maintenance, fuel


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    # Import models so migrations detect them
    from app.models import user, vehicle, driver

    return app