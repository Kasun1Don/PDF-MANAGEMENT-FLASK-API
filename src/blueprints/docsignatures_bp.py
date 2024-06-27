from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import desc
from models.docsignature import Signature, SignatureSchema
from init import db

signatures_bp = Blueprint("signatures", __name__, url_prefix="/signatures")

# Route to list all signed documents from latest to oldest
@signatures_bp.route("/", methods=["GET"])
@jwt_required()
def list_signed_documents():
    signatures = db.session.query(Signature).order_by(desc(Signature.timestamp)).all()
    return jsonify(SignatureSchema(many=True).dump(signatures)), 200