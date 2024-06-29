import uuid
from datetime import datetime, timedelta
from init import db, ma
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from marshmallow import fields


class DocumentAccess(db.Model):
    __tablename__ = 'document_accesses'
    
    id: Mapped[int] = mapped_column(primary_key=True)

    share_link: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    # access links expire after 3 days
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now() + timedelta(days=3), nullable=False)
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    signed: Mapped[bool] = mapped_column(Boolean(), default=False)
    access_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    visits: Mapped[int] = mapped_column(default=0)
    
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey('documents.id', ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    document: Mapped['Document'] = relationship('Document', back_populates='document_accesses')
    user: Mapped['User'] = relationship('User', back_populates='document_accesses')

class DocumentAccessSchema(ma.Schema):
    share_link = fields.UUID(dump_only=True)
    purpose = fields.String(required=True)
    signed = fields.Boolean(dump_only=True)
    visits = fields.Integer(dump_only=True)
    document_id = fields.Integer(required=True)

    document = fields.Nested('DocumentSchema', only=['id', 'document_type', 'document_number', 'content'], exclude=('document_accesses',))
    user = fields.Nested('UserSchema', only=['username', 'email'], exclude=('document_accesses',))

    class Meta:
        fields = ('document_id', 'share_link', 'expires_at', 
                  'purpose', 'access_time', 'signed', 'visits', 'document','document_access', 'documents')

    # alternate schema for link visits/views
class DocumentAccessVisitSchema(ma.Schema):
    share_link = fields.UUID(dump_only=True)
    purpose = fields.String(required=True)
    signed = fields.Boolean(dump_only=True)
    visits = fields.Integer(dump_only=True)
    document_id = fields.Integer(required=True)

    document = fields.Nested('DocumentSchema', only=['document_type'])

    class Meta:
        fields = ('visits', 'document_id', 'share_link', 'purpose', 'document')