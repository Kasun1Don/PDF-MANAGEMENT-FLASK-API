from os import environ
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')

# don't sort JSON response keys alphabetically
app.json.sort_keys = False

# configuration settings
db = SQLAlchemy(model_class=Base)
db.init_app(app)

ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)