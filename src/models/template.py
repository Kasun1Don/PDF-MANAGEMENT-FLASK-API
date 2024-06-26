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
    
    name = fields.String(required=True, validate=validate.Length(min=1,  error='template name is required'))
    structure = fields.Dict(required=True)
    
    documents = fields.Nested('DocumentSchema', many=True, exclude=('template',))

    class Meta:
        fields = ('id', 'name', 'structure')



