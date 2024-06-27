from datetime import timedelta
from flask import Blueprint, request, abort
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, jwt_required
from init import db, bcrypt
# from auth import admin_only


templates_bp = Blueprint('templates', __name__, url_prefix='/templates')

