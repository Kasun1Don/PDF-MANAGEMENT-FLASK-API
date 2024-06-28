
from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from init import db
from models.template import Template, TemplateSchema
from auth import admin_only

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
    
    # Check if the template with the same name already exists
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


