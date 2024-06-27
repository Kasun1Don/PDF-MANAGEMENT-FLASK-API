from typing import List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from marshmallow import fields, validate

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
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=8), load_only=True)

    document_accesses = fields.Nested('DocumentAccessSchema', many=True, dump_only=True)

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'org_name', 'is_admin')
