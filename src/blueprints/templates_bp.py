
from init import db
from models.template import Template, TemplateSchema
from models.document import Document
from auth import admin_only
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

templates_bp = Blueprint("templates", __name__, url_prefix="/templates")


# get all templates
@templates_bp.route("/", methods=["GET"])
@jwt_required()
def get_templates():
    templates = db.session.query(Template).all()
    return TemplateSchema(many=True).dump(templates), 200


# create a new template (admin only)
@templates_bp.route("/", methods=["POST"])
@admin_only
def create_template():
    params = TemplateSchema(only=["name", "structure"]).load(request.json, unknown="exclude")
    
    # Check if a template with the same name already exists in the database
    # looks for the first match in the Template table, names column
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

# delete template if not being used
@templates_bp.route("/<int:id>", methods=["DELETE"])
@admin_only
def delete_template(id):
    template = db.get_or_404(Template, id)

    # Check if there are any documents using this template
    # Ensures referential integrity by preventing deletion, if the template is in use.
    documents_using_template = db.session.query(Document).filter_by(template_id=id).count()
    if documents_using_template > 0:
        return {"error": "Cannot delete template. It's being used by one or more documents."}, 400

    db.session.delete(template)
    db.session.commit()
    return {"message": "Template deleted successfully"}, 200