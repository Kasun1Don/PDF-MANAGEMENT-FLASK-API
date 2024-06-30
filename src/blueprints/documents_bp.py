from init import db
from auth import authorize_owner, admin_only
from models.document import Document, DocumentSchema
from models.user import User
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity


documents_bp = Blueprint("documents", __name__, url_prefix="/documents")


# get all documents created by the current user
@documents_bp.route("/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_documents_by_user(user_id):
    """Gets all documents for a specific user

    This route allows users to retrieve all documents associated with their user_id.
    It checks if the user exists and, if so, fetches all documents created by that user.

    Returns:
        dict: a list of documents serialized in DocumentSchema format. 
        If the user_id is not found, returns an error message.
    """
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "user_id not found"}, 404
    
    documents = db.session.query(Document).filter_by(user_id=user_id).all()
    return DocumentSchema(many=True, exclude=["template_id", "signatures", "document_accesses"]).dump(documents), 200


# get all documents for current user's organization
@documents_bp.route("/org", methods=["GET"])
@jwt_required()
def get_org_documents():
    user_id = get_jwt_identity()
    # query the User table for the user matching the JWT token identifier
    current_user = db.session.get(User, user_id)

    # query the Documents table for all documents belonging to current_user's organization
    documents = (
        db.session.query(Document).filter_by(org_name=current_user.org_name).all()
    )
    return DocumentSchema(many=True, exclude=["template_id", "signatures", "document_accesses"]).dump(documents), 200

# get a specific document by document_id
@documents_bp.route("/<int:document_id>", methods=["GET"])
@jwt_required()
def get_document(document_id):
    document = db.get_or_404(Document, document_id)
    return DocumentSchema(exclude=["template_id", "signatures", "document_accesses"]).dump(document), 200


# get ALL documents from database (Admin only)
@documents_bp.route("/", methods=["GET"])
@admin_only
def get_all_documents():
    documents = db.session.query(Document).all()
    return DocumentSchema(many=True, exclude=["template_id", "signatures", "document_accesses"]).dump(documents), 200


# create new documents 
@documents_bp.route("/", methods=["POST"])
@jwt_required()
def create_document():
    """Create a new document

    Any User can create a new document by providing the document type, content, and ID of the template they want to use. 
    The document is automatically associated with the current user's organization.

    Returns:
        dict: the newly created document serialized in DocumentSchema format.
    """    
    user_id = get_jwt_identity()
    current_user = db.session.get(User, user_id)

    # validate and deserialize input
    document_schema = DocumentSchema(only=["document_type", "content", "template_id"])
    params = document_schema.load(request.json, unknown="exclude")

    new_document = Document(
        org_name=current_user.org_name,
        document_type=params["document_type"],
        content=params["content"],
        template_id=params["template_id"],
        user_id=user_id,
    )
    db.session.add(new_document)
    db.session.commit()
    return DocumentSchema(exclude=["signatures", "document_accesses"]).dump(new_document), 201


# document creator can update a document
@documents_bp.route("/<int:document_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_document(document_id):
    """Update an existing document

    This route allows the creator of a document to update its type and content by providing 
    the document_id. Only the owner of the document can perform this action.

    Args:
        document_id (int): The ID of the document to be updated.

    Returns:
        dict: The updated document serialized in DocumentSchema format.
    """
    document = db.get_or_404(Document, document_id)

    # check if the user is the owner of the document (auth.py)
    authorize_owner(document)

    document_info = DocumentSchema(only=['document_type', 'content'], unknown="exclude").load(
        request.json)
    
    # update the relevant fields
    document.document_type=document_info.get('document_type', document.document_type)
    document.content=document_info.get('content', document.content)
    db.session.commit()
    return DocumentSchema( exclude=["template_id", "signatures", "document_accesses"]).dump(document), 200


# document creator can delete a document
@documents_bp.route("/<int:document_id>", methods=["DELETE"])
@jwt_required()
def delete_document(document_id):
    # retrieves the document by document_id
    document = db.get_or_404(Document, document_id)

    # check if the user is the owner of the document
    authorize_owner(document)

    # delete the document
    db.session.delete(document)
    db.session.commit()
    return {"message": "Document deleted successfully"}, 200