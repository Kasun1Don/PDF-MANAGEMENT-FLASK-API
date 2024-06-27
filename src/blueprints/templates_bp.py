from datetime import timedelta
from flask import Blueprint, request, abort
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, jwt_required
from init import db, bcrypt
from models.template import Template, TemplateSchema


templates_bp = Blueprint("templates", __name__, url_prefix="/templates")


# Route to get all templates
@templates_bp.route("/", methods=["GET"])
@jwt_required()
def get_templates():
    templates = db.session.query(Template).all()
    return TemplateSchema(many=True).dump(templates), 200


# Route to create a new template (admin only)
@templates_bp.route("/create", methods=["POST"])
@jwt_required()
def create_template():
    template_schema = TemplateSchema()

    # params = TemplateSchema(only=["name", "structure"]).load(
    #     request.json, unknown="exclude")

    # new_template = Template(
    #     name=params["name"],
    #     structure=params["structure"])

    # Validate and deserialize input into a dictionary
    template_data = template_schema.load(request.json)
    # Create a new Template instance using the deserialized data
    new_template = Template(**template_data)

    db.session.add(new_template)
    db.session.commit()
    return template_schema.dump(new_template), 201


# creator can update a template (need make creator_id or more complex)

# creator can delete a template (need make creator_id or more complex)
