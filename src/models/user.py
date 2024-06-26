from typing import List
from init import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields, validate

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    org_id: Mapped[int] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    org_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)

    documents: Mapped[List['Document']] = relationship('Document', back_populates='user')


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True
        fields = ('id', 'org_id', 'username', 'email', 'org_name', 'is_admin', 'documents')

    # Custom field validation
    email = fields.Email(required=True)
    username = fields.String(required=True, validate=validate.Length(min=1))
    password_hash = fields.String(required=True, validate=validate.Length(min=8))
    documents = Nested('DocumentSchema', many=True, exclude=('user',))