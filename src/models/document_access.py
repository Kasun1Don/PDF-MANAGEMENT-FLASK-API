import uuid
from datetime import datetime, timedelta
from init import db, ma
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from marshmallow import fields, validate


class DocumentAccess(db.Model):
    __tablename__ = 'document_accesses'
    
    id: Mapped[int] = mapped_column(primary_key=True)

    share_link: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    # three days to access from access link creation date
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now() + timedelta(days=3), nullable=False)
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    signed: Mapped[bool] = mapped_column(Boolean(), default=False)
    access_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    views: Mapped[int] = mapped_column(default=0)
    
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey('documents.id', ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    document: Mapped['Document'] = relationship('Document', back_populates='document_accesses')
    user: Mapped['User'] = relationship('User', back_populates='document_accesses')

class DocumentAccessSchema(ma.Schema):
    # Custom field validation
    share_link = fields.UUID(dump_only=True)
    purpose = fields.String(required=True)
    signed = fields.Boolean(dump_only=True)
    views = fields.Integer(dump_only=True)
    # access_time = fields.DateTime(required=False)
    document_id = fields.Integer(required=True)

    document = fields.Nested('DocumentSchema', only=['id', 'document_type', 'document_number', 'content'], exclude=('document_accesses',))
    user = fields.Nested('UserSchema', only=['username', 'email'], exclude=('document_accesses',))

    class Meta:
        fields = ('document_id', 'share_link', 'expires_at', 
                  'purpose', 'access_time', 'signed', 'views', 'documents')


class DocumentAccessViewSchema(ma.Schema):
    document_id = fields.Int()
    share_link = fields.UUID()
    views = fields.Int()
    purpose = fields.String()

    class Meta:
        fields = ('views', 'document_id', 'share_link', 'purpose')