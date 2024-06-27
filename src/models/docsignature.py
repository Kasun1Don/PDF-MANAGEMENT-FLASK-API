from init import db, ma
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, Text
from marshmallow import fields

class Signature(db.Model):
    __tablename__ = 'signatures'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=db.func.current_timestamp(), nullable=False)
    signature_data: Mapped[str] = mapped_column(Text, nullable=False)
    signer_name: Mapped[str] = mapped_column(String(80), nullable=True)
    signer_email: Mapped[str] = mapped_column(String(160), nullable=True)

    document_id: Mapped[int] = mapped_column(Integer, ForeignKey('documents.id'), nullable=False)

    document: Mapped['Document'] = relationship('Document', back_populates='signatures')

class SignatureSchema(ma.Schema):
    # Custom field validation
    signature_data = fields.String(required=True)
    signer_name = fields.String(required=False)
    signer_email = fields.Email(required=False)
    document_id = fields.Integer(dump_only=True)

    document = fields.Nested('DocumentSchema', exclude=('signatures',))

    class Meta:
        fields = ('id', 'document_id', 'timestamp', 'signature_data', 'signer_name', 'signer_email', 'document', 'signatures')

