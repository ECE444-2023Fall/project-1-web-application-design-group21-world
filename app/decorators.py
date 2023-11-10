from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.role not in roles:
                abort(403)  # Forbidden
            return func(*args, **kwargs)
        return decorated_view
    return wrapper
