from init import db
from models.user import User
from flask import abort, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

# admin only login
def admin_only(fn):
    @wraps(fn)
    @jwt_required()
    def inner(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()

        if not user or not user.is_admin:
            return jsonify({"error": "Admin access required"}), 403

        return fn(*args, **kwargs)
    return inner


# ensure that the JWT use is the owner of the document (for Document deletion)
def authorize_owner(document):
    user_id = get_jwt_identity()
    if user_id != document.user_id:
        abort(make_response(jsonify(error = "You must be document owner"), 403))
