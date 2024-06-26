from datetime import datetime
from typing import List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from marshmallow import fields, validate


class Signature(db.Model):
    __tablename__ = 'signatures'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey('documents.id'), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=db.func.current_timestamp())
    signature_data: Mapped[str] = mapped_column(String, nullable=False)
    signer_name: Mapped[str] = mapped_column(String, nullable=True)
    signer_email: Mapped[str] = mapped_column(String, nullable=True)

    document: Mapped['Document'] = relationship('Document', back_populates='signatures')

class SignatureSchema(ma.Schema):
        # Custom field validation
    signature_data = fields.String(required=True)
    signer_name = fields.String(required=False)
    signer_email = fields.Email(required=False)

    class Meta:
    document = fields.Nested('DocumentSchema', exclude=('signatures',))