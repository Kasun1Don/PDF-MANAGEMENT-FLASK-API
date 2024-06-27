from flask import Blueprint, request
from models.document import Document, DocumentSchema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
# from auth import authorize_owner

document_accesses_bp = Blueprint("access", __name__, url_prefix="/access")

# create document access link




# update when document was accessed by whoever it's sent to