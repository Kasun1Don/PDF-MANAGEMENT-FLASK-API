from init import db
from models.docsignature import Signature, SignatureSchema
from datetime import timedelta, datetime
from flask_jwt_extended import jwt_required
from flask import Blueprint
from sqlalchemy import desc


signatures_bp = Blueprint("signatures", __name__, url_prefix="/signatures")


# Route to list all signed documents from latest last 24 hours
@signatures_bp.route("/", methods=["GET"])
@jwt_required()
def list_signed_documents():
    last_24_hours = datetime.now() - timedelta(hours=24)
    signatures = (db.session.query(Signature)
        .filter(Signature.timestamp >= last_24_hours)
        .order_by(desc(Signature.timestamp)).all())
    
    return SignatureSchema(many=True).dump(signatures), 200


# Route to find signature(s) for a given document id
@signatures_bp.route("/document/<int:document_id>", methods=["GET"])
@jwt_required()
def get_signature_from_documents(document_id):
    signatures = (
        db.session.query(Signature)
        .filter_by(document_id=document_id)
        .order_by(desc(Signature.timestamp))
        .all()
    )
    return (
        SignatureSchema(
            many=True,
            only=["timestamp", "signature_data", "signer_name", "signer_email"],
        ).dump(signatures),
        200,
    )
