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
    """Create a document access link

    Allows authenticated users to create a unique document access link code with a specific purpose 
    (either 'Review' or 'Sign'). This access link code can be shared with anyone to access the document
    (endpoint: /access/<insert link code>).
    The link expires 3 days from creation (set as default in the document_access model).

    Returns:
        dict: the newly created document access link serialized in DocumentAccessSchema format.
    """
    params = DocumentAccessSchema(only=["document_id", "purpose"]).load(
        request.json, unknown="exclude"
    )
    if params["purpose"] not in VALID_PURPOSES:
        return {"error": "Invalid 'Purpose'. Valid options are: 'Review' or 'Sign'"}, 400

    current_user_id = get_jwt_identity()

    # check if the given document_id exists in the Documents table
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
    """Sign a document using a unique share link

    This endpoint allows a user to sign a document with a unique share link that can be created
    at /access. It verifies the share link hasn't expired and checks if the document has already been signed, 
    and if valid, creates a new signature record with digital signature, email and name. The 'signed' status of the DocumentAccess 
    record is updated accordingly.

    Returns:
        Response: a JSON response with the new signature name, email and timestamp.
    """    
    # load and validate input data using the Signature Schema defined
    params = SignatureSchema().load(request.json, unknown="exclude")

    access = db.session.query(DocumentAccess).filter_by(share_link=share_link).first()

    # check if the share link has expired
    if access.expires_at < datetime.now():
        return {"error": "share link has expired"}, 403

    # check if the document has already been signed (1 signature per document)
    existing_signature = db.session.query(exists().where(Signature.document_id == access.document_id)).scalar()
    if existing_signature:
        return {"error": "Document has already been signed"}, 400
    
    # new signature
    new_signature = Signature(
        document_id=access.document_id,
        signature_data=params["signature_data"],
        signer_name=params.get("signer_name"),
        signer_email=params.get("signer_email"),
    )
    db.session.add(new_signature)
    # update the default 'false' status of the DocumentAccess record
    access.signed = True
    db.session.commit()
    return SignatureSchema().dump(new_signature), 201


# access a document through unique link for signing or viewing/visiting
@documents_accesses_bp.route("/<uuid:share_link>", methods=["GET"])
def access_document(share_link):
    """Access a document using a unique share link (anyone can access).

    This endpoint allows a user to access a document using the unique share link generated.
    It updates the access time and increments the view counter for the document access record.

    Returns:
        Response: A JSON response with the updated document access data.
    """    
    # checks if the share_link exists in the DocumentsAccess table.
    access = db.session.query(DocumentAccess).filter_by(share_link=share_link).first()

    # updates the access time to now
    access.access_time = datetime.now()
    access.visits += 1  # increment document view counter
    db.session.commit()
    return DocumentAccessSchema().dump(access), 200
# raises Attribute error when access link doesn't exist
@documents_accesses_bp.errorhandler(AttributeError)
def handle_attribute_error(e):
    return {"error": "please create a document access link first"}, 500


# all unsigned access links ordered by expiry date (created by current user)
@documents_accesses_bp.route("/unsigned", methods=["GET"])
@jwt_required()
def get_unsigned_access_links():
    """ Retrieve all unsigned document access links created by the current user.

    This endpoint allows a user to get a list of their unsigned document access links, 
    when the 'purpose' was set to 'Sign' the document. The links are ordered by the expiration date in ascending order. 

    Returns:
        Response: A JSON response with the unsigned document access links.
    """    
    current_user_id = get_jwt_identity()

    unsigned_links = (
        db.session.query(DocumentAccess)
        .filter_by(user_id=current_user_id, purpose="Sign", signed=False)
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


# link visits, sorted by number of link visits (for links created by current user)
@documents_accesses_bp.route("/visits", methods=["GET"])
@jwt_required()
def get_visits():
    """Sorts the access links by number of visits (Access links created by the current user)

    This endpoint allows a user to see their most viewed links and or if a link was viewed at all. 
    The DocumentAccess model has a field for visits which increases with each visit.

    Returns:
         Response: A JSON response with all the document access links, sorted by visits.
    """    
    current_user_id = get_jwt_identity()
    # query the DocumentAccess table to retrieve ALL DocumentAccess instances created by the current user_id, ordered by the number of visits in descending order
    document_accesses = (
        db.session.query(DocumentAccess)
        .filter_by(user_id=current_user_id)
        .order_by(desc(DocumentAccess.visits))
        .all()
    )
    return DocumentAccessVisitSchema(many=True).dump(document_accesses), 200
