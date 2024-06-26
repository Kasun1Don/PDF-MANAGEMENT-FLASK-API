from init import app
from marshmallow.exceptions import ValidationError
from blueprints.cards_bp import cards_bp
from blueprints.users_bp import users_bp
from blueprints.cli_bp import db_commands
@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()

print(app.url_map)


#handles any error object (captures 404 & 405)
@app.errorhandler(405)
@app.errorhandler(404)
def not_found(err): 
    return {'error': 'Not Found'}, 404


# marshmallow exceptions library validation error:
@app.errorhandler(ValidationError)
def invalid_request(err):
    return {'error': vars(err)['messages']}, 400

@app.errorhandler(KeyError)
def missing_key(err):
    return {'error': f"missing field: {str(err)}"}, 400