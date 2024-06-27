from flask import Blueprint, request
from models.document import Document, DocumentSchema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from auth import authorize_owner

documents_bp = Blueprint("documents", __name__, url_prefix="/documents")


# get all documents created for a given user id
@documents_bp.route("/user/<int:user_id>", methods=["GET"])
@jwt_required()
def get_documents_by_user(user_id):
    user = db.session.get(User, user_id)

    if not user:
        return {"error": "user_id not found"}, 404
    
    documents = db.session.query(Document).filter_by(user_id=user_id).all()
    return DocumentSchema(many=True, exclude=["template_id", "signatures"]).dump(documents), 200


# get all documents for current user's organization
@documents_bp.route("/org", methods=["GET"])
@jwt_required()
def get_org_documents():
    user_id = get_jwt_identity()
    current_user = db.session.get(User, user_id)

    # Retrieve documents for the current user's organization
    documents = (
        db.session.query(Document).filter_by(org_name=current_user.org_name).all()
    )
    return DocumentSchema(many=True, exclude=["template_id", "signatures"]).dump(documents), 200

# get a specific document by document_id
@documents_bp.route("/<int:document_id>", methods=["GET"])
@jwt_required()
def get_document(document_id):
    document = db.get_or_404(Document, document_id)
    return DocumentSchema(exclude=["template_id", "signatures"]).dump(document), 200


# get ALL documents from database (A)
@documents_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_documents():
    documents = db.session.query(Document).all()
    return DocumentSchema(many=True, exclude=["template_id", "signatures"]).dump(documents), 200



# create documents
@documents_bp.route("/", methods=["POST"])
@jwt_required()
def create_document():
    # retrieve the ID of the current authenticated user to retrieve their org name
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

    return DocumentSchema(exclude=["signatures"]).dump(new_document)

    # return document_schema.dump(new_document), 201



# document creator can update document
@documents_bp.route("/<int:document_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_document(document_id):
    # Retrieve the document by ID
    document = db.get_or_404(Document, document_id)

    # Check if the user is the owner of the document
    authorize_owner(document)

    document_info = DocumentSchema(only=['document_type', 'content'], unknown="exclude").load(
        request.json)
    
    # update the relevant fields
    document.document_type=document_info.get('document_type', document.document_type)
    document.content=document_info.get('content', document.content)

    db.session.commit()

    return DocumentSchema( exclude=["template_id", "signatures"]).dump(document), 200


# document creator can delete documents
@documents_bp.route("/<int:document_id>", methods=["DELETE"])
@jwt_required()
def delete_document(document_id):
    # Retrieve the document by ID
    document = db.session.get(Document, document_id)

    # If document not found, return 404
    if not document:
        return {"error": "Document not found"}, 404

    # Check if the user is the owner of the document
    authorize_owner(document)

    # Delete the document
    db.session.delete(document)
    db.session.commit()

    return {"message": "Document deleted successfully"}, 200