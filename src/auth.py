from init import db
from models.user import User
from flask import abort, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

# admin only login
def admin_only(fn):
    @wraps(fn) # preserves the original function's metadata
    @jwt_required()
    def inner(*args, **kwargs):
        user_id = get_jwt_identity()
        stmt = db.select(User).where(User.id == user_id, User.is_admin)
        user = db.session.scalar(stmt)
        if user:
            return fn(*args, **kwargs)
        else:
            return {'error': "You must be an admin to access this resource"}, 403
    return inner()


# ensure that the JWT use is the owner of the document (for Document deletion)
def authorize_owner(document):
    user_id = get_jwt_identity()
    if user_id != document.user_id:
        abort(make_response(jsonify(error = "You must be document owner"), 403))

