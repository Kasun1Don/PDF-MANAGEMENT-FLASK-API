from datetime import timedelta
from flask import Blueprint, request
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, jwt_required
from init import db, bcrypt
from auth import admin_only



users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/login', methods=['POST']) # change default GET to POST
def login():
    
    params = UserSchema(only=['username','email', 'password']).load(request.json, unknown='exclude')
   
    stmt = db.select(User).where(User.email == params['email'])
    user = db.session.scalar(stmt) 
    if user and bcrypt.check_password_hash(user.password, params['password']): #check against stored password and input password

        # Generate the JWT with unique identifier (using attribute from User object)
        token = create_access_token(identity=user.id, expires_delta=timedelta(hours=4))
        # Return the JWT
        return {'token': token}
    else:
        # error handling(user not found, wrong username or wrong password)
        return {'error': 'Invalid email or password'}, 401 #don't say exactly which


# setup the user
@users_bp.route('/', methods=['POST'])
@admin_only
def create_user():
     # create a new user
     params = UserSchema(only=['email', 'password', 'name', 'is_admin']).load(request.json)
     print(params)
     return params




# #register a new user

# @app.route("/register", methods=["POST"])
# def auth_register():
#     #The request data will be loaded in a user_schema converted to JSON. request needs to be imported from
#     user_fields = user_schema.load(request.json)
#    # find the user by email address
#     stmt = db.select(User).filter_by(email=request.json['email'])
#     user = db.session.scalar(stmt)

#     if user:
#         # return an abort message to inform the user. That will end the request
#         return abort(400, description="Email already registered")
#     # Create the user object
#     user = User()
#     #Add the email attribute
#     user.email = user_fields["email"]
#     #Add the password attribute hashed by bcrypt
#     user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
#     #Add it to the database and commit the changes
#     db.session.add(user)
#     db.session.commit()
#     #create a variable that sets an expiry date
#     expiry = timedelta(days=1)
#     #create the access token
#     access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
#     # return the user email and the access token
#     return jsonify({"user":user.email, "token": access_token })


