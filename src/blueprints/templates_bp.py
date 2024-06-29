
from init import db
from models.template import Template, TemplateSchema
from models.document import Document
from auth import admin_only
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

templates_bp = Blueprint("templates", __name__, url_prefix="/templates")


# get all document templates
@templates_bp.route("/", methods=["GET"])
@jwt_required()
def get_templates():
    templates = db.session.query(Template).all()
    # returns all available templates serialized in Template Schema format
    return TemplateSchema(many=True).dump(templates), 200


# admins can create new templates (must be unique name)
@templates_bp.route("/", methods=["POST"])
@admin_only
def create_template():
    """create a new document template

    This route allows admins to create a new template by providing the template's unique name and structure.

    Checks if a template with the same name already exists and, if not, creates and saves the new template 
    to the database.

    >The `structure` field is expected to be a JSON object defining the fields of the template.

    Returns:
        dict: the newly created template serialized in TemplateSchema format, or an error message if the 
        template name already exists.
    """    
    params = TemplateSchema(only=["name", "structure"]).load(request.json, unknown="exclude")
    
    # check if a template with the same name already exists in the database
    # looks for the first match in the Templates table's "name" column
    existing_template = db.session.query(Template).filter_by(name=params["name"]).first()
    
    if existing_template:
        return {"error": "Template with this name already exists"}, 400
    
    new_template = Template(
        name=params["name"],
        structure=params["structure"]
    )
    db.session.add(new_template)
    db.session.commit()
    
    return TemplateSchema().dump(new_template), 201

# delete a template if it's not being used
@templates_bp.route("/<int:id>", methods=["DELETE"])
@admin_only
def delete_template(id):
    template = db.get_or_404(Template, id)

    # ensures referential integrity by preventing deletion, if the template is in use (if the template is used once or more).
    documents_using_template = db.session.query(Document).filter_by(template_id=id).count()
    if documents_using_template > 0:
        return {"error": "Cannot delete template. It's being used by one or more documents."}, 400

    db.session.delete(template)
    db.session.commit()
    return {"message": "Template deleted successfully"}, 200