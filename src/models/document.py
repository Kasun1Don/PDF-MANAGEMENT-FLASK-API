from typing import List
import uuid
from datetime import datetime
from init import db, ma
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from marshmallow import fields, validate

class Document(db.Model):
    __tablename__ = 'documents'
    
    id: Mapped[int] = mapped_column(primary_key=True)

    org_name: Mapped[str] = mapped_column(String(80), nullable=False)
    document_type: Mapped[str] = mapped_column(String(40), nullable=False)
    document_number: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now())
    content: Mapped[dict] = mapped_column(JSON, nullable=False)

    template_id: Mapped[int] = mapped_column(Integer, ForeignKey('templates.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="SET NULL"), nullable=True)

    template: Mapped['Template'] = relationship('Template', back_populates='documents')
    users: Mapped['User'] = relationship('User', back_populates='documents')
    document_accesses: Mapped[list['DocumentAccess']] = relationship('DocumentAccess', back_populates='document', cascade='all, delete')
    signatures: Mapped[list['Signature']] = relationship('Signature', back_populates='document', cascade='all, delete')
    
class DocumentSchema(ma.Schema):
    # Custom field validation
    org_name = fields.String(required=True, validate=validate.Length(min=1,  error='organization name is required'))
    document_type = fields.String(required=True, validate=validate.Length(min=1, error='document type/name is required'))
    content = fields.Dict(required=True)
    template_id = fields.Integer(required=True, validate=validate.Range(min=1, error='missing template_id'))

    # nested schema
    template = fields.Nested('TemplateSchema', only=['name'])
    user = fields.Nested('UserSchema', only=['username', 'email', 'org_name'],exclude=('documents',))
    document_accesses = fields.Nested('DocumentAccessSchema', many=True, dump_only=True, exclude=('documents',))
    signatures = fields.Nested('SignatureSchema',exclude=['signatures'])

    class Meta:
        fields = ('id', 'org_name', 'document_type', 'document_number', 'date', 'content', 'template_id', 'template', 'user', 'signatures', 'document_accesses')
