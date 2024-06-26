from typing import List
from init import db, ma
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON
from marshmallow import fields, validate


class Template(db.Model):
    __tablename__ = 'templates'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    structure: Mapped[dict] = mapped_column(JSON, nullable=False)

    documents: Mapped[list['Document']] = relationship('Document', back_populates='template')


class TemplateSchema(ma.Schema):
    # Custom field validation
    name = fields.String(required=True)
    structure = fields.Dict(required=True)

    documents = fields.Nested('DocumentSchema', many=True, exclude=('template',))

    class Meta:
        fields = ('id', 'name', 'structure', 'documents')