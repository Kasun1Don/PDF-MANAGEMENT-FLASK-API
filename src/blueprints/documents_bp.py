from flask import Blueprint, request
from models.document import Document, DocumentSchema
from models.user import User
from flask_jwt_extended import jwt_required
from init import db

documents_bp = Blueprint('documents', __name__,)

@documents_bp.route('/', methods=['POST'])
@jwt_required()
def create_document(current_user):
    data = request.get_json()
    data['org_name'] = current_user.org_name  # Ensure document belongs to the user's org
    new_document = document_schema.load(data)
    db.session.add(new_document)
    db.session.commit()
    return document_schema.jsonify(new_document), 201





#user can delete documents if they created it