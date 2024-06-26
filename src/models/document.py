from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, JSON, ForeignKey
from marshmallow_sqlalchemy.fields import Nested
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
    user: Mapped['User'] = relationship('User', back_populates='documents')

class DocumentSchema(ma.Schema):
    # Custom field validation
    org_name = fields.String(required=True)
    document_type = fields.String(required=True)
    document_number = fields.String(required=True, validate=validate.Length(min=1))
    date = fields.String(required=True)
    content = fields.Dict(required=True)

    template = fields.Nested('TemplateSchema', exclude=('documents',))
    user = fields.Nested('UserSchema', exclude=('documents',))

    class Meta:
        fields = ('id', 'org_name', 'email', 'org_name', 'is_admin', 'documents')