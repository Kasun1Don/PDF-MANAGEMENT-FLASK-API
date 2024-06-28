from datetime import timedelta
from flask import Blueprint, request
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from init import db, bcrypt

# from auth import admin_only


users_bp = Blueprint("users", __name__, url_prefix="/users")


# get a list of all users from the organization
@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    stmt = db.select(User).where(User.id == user_id)
    current_user_org = db.session.scalar(stmt).org_name
    
    users_stmt = db.select(User).where(User.org_name == current_user_org)
    users = db.session.scalars(users_stmt).all()
    return UserSchema(many=True).dump(users), 200


# user registration (orgname should be unique)
@users_bp.route("/register", methods=["POST"])
def register_user():
    params = UserSchema(only=["id", "username", "email", "password", "org_name"]).load(
        request.json, unknown="exclude"
    )

    stmt = db.select(User).filter_by(email=request.json["email"])
    user = db.session.scalar(stmt)

    if user:
        return {"error": "Email already registered"}, 400

    user = User(
        username=params["username"],
        email=params["email"],
        password=bcrypt.generate_password_hash(params["password"]).decode("utf8"),
        org_name=params["org_name"],
    )
    db.session.add(user)
    db.session.commit()

    return UserSchema().dump(user), 201


# login access token (after registration)
@users_bp.route("/login", methods=["POST"])
def login():

    params = UserSchema(only=["email", "password"]).load(
        request.json, unknown="exclude"
    )

    stmt = db.select(User).where(User.email == params["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(
        user.password, params["password"]
    ):  # check against stored password and input password

        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=4))

        return {"token": token}
    else:

        return {"error": "Invalid email or password"}, 401


# application admin can create a user (add roles permissions in future)
@users_bp.route("/create", methods=["POST"])
@jwt_required()
def create_user():
    params = UserSchema(
        only=["id", "username", "email", "password", "org_name", "is_admin"]
    ).load(request.json, unknown="exclude")

    stmt = db.select(User).filter_by(email=request.json["email"])
    user = db.session.scalar(stmt)

    if user:
        return {"error": "Email already registered"}, 400

    user = User(
        username=params["username"],
        email=params["email"],
        password=bcrypt.generate_password_hash(params["password"]).decode("utf8"),
        org_name=params["org_name"],
        is_admin=params["is_admin"],
    )
    db.session.add(user)
    db.session.commit()

    return UserSchema().dump(user), 201


# admin can delete a user (if from same organization)
@users_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
    user_to_delete = db.get_or_404(User, id)
    
    db.session.delete(user_to_delete)
    db.session.commit()
    return {"message": "User deleted successfully"}


# user can update their email, password and username
