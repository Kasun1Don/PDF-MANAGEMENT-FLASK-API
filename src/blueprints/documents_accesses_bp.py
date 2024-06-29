from datetime import datetime
from init import db
from models.document_access import (DocumentAccess, DocumentAccessSchema, DocumentAccessVisitSchema)
from models.docsignature import Signature, SignatureSchema
from models.document import Document
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request
from sqlalchemy import desc, exists


documents_accesses_bp = Blueprint("access", __name__, url_prefix="/access")

# document access link "purpose" field options:
VALID_PURPOSES = ["Review", "Sign"]

# create document access link
@documents_accesses_bp.route("/", methods=["POST"])
@jwt_required()
def create_access():
    params = DocumentAccessSchema(only=["document_id", "purpose"]).load(
        request.json, unknown="exclude"
    )

    if params["purpose"] not in VALID_PURPOSES:
        return {"error": "Invalid 'Purpose'. Valid options are: 'Review' or 'Sign'"}, 400

    current_user_id = get_jwt_identity()

    db.get_or_404(Document, params["document_id"])

    new_access = DocumentAccess(
        document_id=params["document_id"],
        user_id=current_user_id,
        purpose=params["purpose"],
    )
    db.session.add(new_access)
    db.session.commit()
    return DocumentAccessSchema(only=['document_id', 'share_link', 'expires_at', 'purpose']).dump(new_access), 201

# document signing link
@documents_accesses_bp.route("/<uuid:share_link>/sign", methods=["POST"])
def sign_document(share_link):
    params = SignatureSchema().load(request.json, unknown="exclude")

    # Find the DocumentAccess by share_link
    access = db.session.query(DocumentAccess).filter_by(share_link=share_link).first()

    # check if the share link has expired
    if access.expires_at < datetime.now():
        return {"error": "share link has expired"}, 403

    # check if the document has already been signed (1 signature per document)
    existing_signature = db.session.query(exists().where(Signature.document_id == access.document_id)).scalar()
    if existing_signature:
        return {"error": "Document has already been signed"}, 400
    
    # Create a new signature
    new_signature = Signature(
        document_id=access.document_id,
        signature_data=params["signature_data"],
        signer_name=params.get("signer_name"),
        signer_email=params.get("signer_email"),
    )

    db.session.add(new_signature)

    # Update the signed status of the DocumentAccess record
    access.signed = True

    db.session.commit()

    return SignatureSchema().dump(new_signature), 201


# update 'access_time' when document access link is accessed
@documents_accesses_bp.route("/<uuid:share_link>", methods=["GET"])
def access_document(share_link):
    # Check if the share_link exists
    access = db.session.query(DocumentAccess).filter_by(share_link=share_link).first()

    # Update the access time
    access.access_time = datetime.now()
    access.visits += 1  # increment document view counter
    db.session.commit()
    return DocumentAccessSchema().dump(access), 200
    # return {'message': 'Access time updated'}, 200
@documents_accesses_bp.errorhandler(AttributeError)
def handle_attribute_error(e):
    return {"error": "please create a document access link first"}, 500


# all unsigned access links by ordered by expiry date (created by current user)
@documents_accesses_bp.route("/unsigned", methods=["GET"])
@jwt_required()
def get_unsigned_access_links():
    current_user_id = get_jwt_identity()
    unsigned_links = (
        db.session.query(DocumentAccess)
        .filter_by(user_id=current_user_id, purpose="Sign", signed=False)  # Add filter for signed=False
        .order_by(DocumentAccess.expires_at)
        .all()
    )
    return DocumentAccessSchema(many=True, exclude=["document"]).dump(unsigned_links), 200



# all signed access links (created by current user)
@documents_accesses_bp.route("/signed", methods=["GET"])
@jwt_required()
def get_signed_access_links():
    current_user_id = get_jwt_identity()
    signed_links = (
        db.session.query(DocumentAccess)
        .filter_by(user_id=current_user_id, signed=True)
        .all()
    )
    return DocumentAccessSchema(many=True).dump(signed_links), 200


# link visits sorted by number of link visits (for links created by current user)
@documents_accesses_bp.route("/visits", methods=["GET"])
@jwt_required()
def get_visits():
    current_user_id = get_jwt_identity()

    # Query and order by visits
    document_accesses = (
        db.session.query(DocumentAccess)
        .filter_by(user_id=current_user_id)
        .order_by(desc(DocumentAccess.visits))
        .all()
    )
    return DocumentAccessVisitSchema(many=True).dump(document_accesses), 200