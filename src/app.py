from init import app
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from blueprints.users_bp import users_bp
from blueprints.cli_bp import db_commands
from blueprints.templates_bp import templates_bp
from blueprints.documents_bp import documents_bp
from blueprints.documents_accesses_bp import documents_accesses_bp
from blueprints.docsignatures_bp import signatures_bp


app.register_blueprint(db_commands)
app.register_blueprint(users_bp)
app.register_blueprint(templates_bp)
app.register_blueprint(documents_bp)
app.register_blueprint(documents_accesses_bp)
app.register_blueprint(signatures_bp)


@app.route("/")
def hello_world():
    return "Hello, World!"


print(app.url_map)


@app.errorhandler(405)
@app.errorhandler(404)
def not_found(err):
    return {"error": "Not Found"}, 404

# marshmallow exceptions library validation error:
@app.errorhandler(ValidationError)
def invalid_request(err):
    return {"error": vars(err)["messages"]}, 400


@app.errorhandler(KeyError)
def missing_key(err):
    return {"error": f"missing field: {str(err)}"}, 400


@app.errorhandler(BadRequest)
def handle_bad_request(err):
    return {"error": str(err.description)}, 400


@app.errorhandler(500)
def internal_server_error(err):
    return {"error": "Internal Server Error"}, 500


if __name__ == "__main__":
    app.run()
