from functools import wraps
from flask_login import current_user
from flask import abort
from app.models.enums import UserRole


def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.role not in allowed_roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator