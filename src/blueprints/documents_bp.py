from flask import Blueprint, request
from models.document import Document, DocumentSchema
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from auth import authorize_owner

documents_bp = Blueprint('documents', __name__, url_prefix="/documents")

# create documents
@documents_bp.route('/', methods=['POST'])
@jwt_required()
def create_document():
    # retrieve the ID of the current authenticated user to retrieve their org name
    user_id = get_jwt_identity()
    current_user = db.session.get(User, user_id)
    
    # validate and deserialize input
    document_schema = DocumentSchema(only=["document_type", "content", "template_id"])
    params = document_schema.load(request.json, unknown='exclude')
    
    new_document = Document(
        org_name=current_user.org_name,
        document_type=params["document_type"],
        content=params["content"],
        template_id=params["template_id"],
        user_id=user_id
    )
    
    db.session.add(new_document)
    db.session.commit()

    return DocumentSchema().dump(new_document)
    
    # return document_schema.dump(new_document), 201

# user can delete documents if they created it


# update document


# get all documents
@documents_bp.route("/", methods=["GET"])
@jwt_required()
def get_documents():
    documents = db.session.query(Document).all()
    return DocumentSchema(many=True).dump(documents), 200

# document creator can delete documents
@documents_bp.route('/<int:document_id>', methods=['DELETE'])
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