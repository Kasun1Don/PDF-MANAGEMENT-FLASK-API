from typing import List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime
from marshmallow import fields, validate


class DocumentAccess(db.Model):
    __tablename__ = 'document_accesses'
    
    id: Mapped[int] = mapped_column(primary_key=True)

    document_id: Mapped[int] = mapped_column(Integer, ForeignKey('documents.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    share_link: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    signed: Mapped[bool] = mapped_column(Boolean, default=False)
    access_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    document: Mapped['Document'] = relationship('Document', back_populates='document_accesses')
    user: Mapped['User'] = relationship('User', back_populates='document_accesses')

class DocumentAccessSchema(ma.Schema):
    # Custom field validation
    share_link = fields.String(required=True)
    expires_at = fields.DateTime(required=True)
    purpose = fields.String(required=True)
    signed = fields.Boolean(required=True)
    access_time = fields.DateTime(required=False)

    document = fields.Nested('DocumentSchema', exclude=('document_accesses',))
    user = fields.Nested('UserSchema', only=['username', 'email'], exclude=('document_accesses',))

    class Meta:
        fields = ('id', 'document_id', 'user_id', 'share_link', 'expires_at', 
                  'purpose', 'signed', 'access_time', 'document', 'user')