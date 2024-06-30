from init import db
from models.docsignature import Signature, SignatureSchema
from datetime import timedelta, datetime
from flask_jwt_extended import jwt_required
from flask import Blueprint
from sqlalchemy import desc


signatures_bp = Blueprint("signatures", __name__, url_prefix="/signatures")


# get all documents signed in the last 24 hours
@signatures_bp.route("/", methods=["GET"])
@jwt_required()
def list_signed_documents():
    """Retrieve all signed documents within the last 24 hours.

    This endpoint allows a user to get a list of all documents that have been signed within the last 24 hours.
    The results are ordered by the timestamp in descending order.

    Returns:
        Response: A JSON response with the signed documents from the last 24 hours.
    """
    # calculate the timestamp for 24 hours ago from the current time
    last_24_hours = datetime.now() - timedelta(hours=24)
    # query the Signatures table, filtering by timestamp greater than or equal to 'last_24_hours', descending order
    signatures = (db.session.query(Signature)
        .filter(Signature.timestamp >= last_24_hours)
        .order_by(desc(Signature.timestamp)).all())
    return SignatureSchema(many=True).dump(signatures), 200


# Route to find the signature for a specific document id
@signatures_bp.route("/document/<int:document_id>", methods=["GET"])
@jwt_required()
def get_signature_from_documents(document_id):
    """Get all signature details for a specific document.

    This endpoint allows a user to get the signature details associated with a specific document, 
    identified by its document_id. The results are ordered by the timestamp in descending order.

    Returns:
        Response: A JSON response with the signature for the specified document.
    """    
    signature = (
        db.session.query(Signature)
        .filter_by(document_id=document_id)
        .order_by(desc(Signature.timestamp)).first()
    )
    return SignatureSchema(only=["timestamp", "signature_data", "signer_name", "signer_email"]
            ).dump(signature), 200
