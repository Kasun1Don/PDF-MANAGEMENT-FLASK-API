from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from marshmallow import fields, validate
from marshmallow.validate import Regexp

class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    org_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)

    documents: Mapped[list['Document']] = relationship('Document', back_populates='users')
    document_accesses: Mapped[list['DocumentAccess']] = relationship('DocumentAccess', back_populates='user', cascade='all, delete')

class UserSchema(ma.Schema):
    # Custom field validation
    email = fields.Email(required=True)
    username = fields.String(required=True, validate=validate.Length(min=1, error='username must have more than one character'))
    password = fields.String(required=True, validate=Regexp('^[a-z0-9_-]{3,16}$', 
        error='Password must be 3-16 characters long and can only contain lowercase letters, numbers, hyphens, and underscores'), load_only=True)
    org_name = fields.String(required=True, validate=validate.Length(min=1,  error='your organization name is required'))
    is_admin = fields.Boolean(required=True)

    document_accesses = fields.Nested('DocumentAccessSchema', many=True, dump_only=True)

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'org_name', 'is_admin')
