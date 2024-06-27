
from datetime import datetime
from flask import Blueprint, request
from models.document_access import DocumentAccess, DocumentAccessSchema
from models.document import Document
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db

# from auth import authorize_owner

documents_accesses_bp = Blueprint("access", __name__, url_prefix="/access")

VALID_PURPOSES = ["Review", "Sign"]


# create document access link
@documents_accesses_bp.route("/", methods=["POST"])
@jwt_required()
def create_access():
    params = DocumentAccessSchema(only=['document_id', 'purpose']).load(request.json, unknown='exclude')

    if params['purpose'] not in VALID_PURPOSES:
        return {"error": "Invalid purpose. Valid options are: 'Review' or 'Sign'"}, 400

    current_user_id = get_jwt_identity()

    db.get_or_404(Document, params['document_id'])

    new_access = DocumentAccess(
        document_id=params["document_id"],
        user_id=current_user_id,
        purpose=params["purpose"],
    )
    db.session.add(new_access)
    db.session.commit()
    return DocumentAccessSchema().dump(new_access), 201


# update 'access_time' when document access link is accessed by whoever it's sent to
@documents_accesses_bp.route('/<uuid:share_link>', methods=['GET'])
def access_document(share_link):
    # Check if the share_link exists
    access = db.session.query(DocumentAccess).filter_by(share_link=share_link).first()
    
    # Update the access time
    access.access_time = datetime.now()
    db.session.commit()
    return DocumentAccessSchema().dump(access), 200
    # return {'message': 'Access time updated'}, 200


# all unsigned access links by expiry date (for current user)

# all signed access links (for current user)

# how many views for links (for current user) <maybe +1> for each visit