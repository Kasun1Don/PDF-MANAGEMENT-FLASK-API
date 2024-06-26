from typing import List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, JSON, ForeignKey
from marshmallow import fields, validate

class Document(db.Model):
    __tablename__ = 'documents'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    org_name: Mapped[str] = mapped_column(String(100), nullable=False)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)
    document_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    date: Mapped[str] = mapped_column(String(10), nullable=False)
    content: Mapped[dict] = mapped_column(JSON, nullable=False)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey('templates.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    template: Mapped['Template'] = relationship('Template', back_populates='documents')
    users: Mapped['User'] = relationship('User', back_populates='documents')
    document_accesses: Mapped[list['DocumentAccess']] = relationship('DocumentAccess', back_populates='document')
    signatures: Mapped[list['Signature']] = relationship('Signature', back_populates='document')
    
class DocumentSchema(ma.Schema):
    # Custom field validation
    org_name = fields.String(required=True)
    document_type = fields.String(required=True)
    document_number = fields.String(required=True, validate=validate.Length(min=1))
    date = fields.String(required=True)
    content = fields.Dict(required=True)

    template = fields.Nested('TemplateSchema', exclude=('documents',))
    user = fields.Nested('UserSchema', only=['username', 'email', 'org_name'],exclude=('documents',))

    class Meta:
        fields = ('id', 'org_name', 'document_type', 'document_number', 'date', 'content', 'template', 'user')
