from datetime import datetime
from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.template import Template
from models.document import Document
from models.document_access import DocumentAccess
from models.signature import Signature


db_commands = Blueprint('db', __name__)

@db_commands.cli.command("create")
def db_create():
    db.drop_all()
    db.create_all()
    print("Created tables")

    users = [
        User(
            username="alice",
            email="admin@example.com",
            password=bcrypt.generate_password_hash("password").decode('utf8'),
            org_name="OrgA",
            is_admin=True
        ),
        User(
            username="bob",
            email="bob@example.com",
            password=bcrypt.generate_password_hash("password").decode('utf8'),
            org_name="OrgA",
            is_admin=False
        ),
        User(
            username="charlie",
            email="charlie@example.com",
            password=bcrypt.generate_password_hash("password").decode('utf8'),
            org_name="OrgB",
            is_admin=True
        )
    ]
    db.session.add_all(users)
    db.session.commit()

    # Creating sample templates
    templates = [
        Template(
            name="Invoice Template",
            structure={"fields": ["date", "total_amount", "item_list"]}
        ),
        Template(
            name="Legal Document Template",
            structure={"fields": ["title", "content", "signatures"]}
        )
    ]
    db.session.add_all(templates)
    db.session.commit()

    # Creating sample documents
    documents = [
        Document(
            org_name="OrgA",
            document_type="Invoice",
            document_number="2be167bc-ed6e-4893-879e-130c15fd8823",
            date="2024-05-01",
            content={"date": "2024-05-01", "total_amount": 1000, "item_list": ["Item1", "Item2"]},
            template_id=1,
            user_id=1

        ),
        Document(
            org_name="OrgB",
            document_type="Legal",
            document_number="bbf75963-fd2f-4317-b3e2-070eeb1ed4ca",
            date="2024-06-01",
            content={"title": "Agreement", "content": "This is a legal document.", "signatures": []},
            template_id=2,
            user_id=1
        )
    ]
    db.session.add_all(documents)
    db.session.commit()

    # Creating sample document accesses
    document_accesses = [
        DocumentAccess(
            document_id=1,
            user_id=3,
            share_link="http://example.com/share/INV001",
            expires_at=datetime(2024, 6, 1),
            purpose="Review",
            signed=False
        ),
        DocumentAccess(
            document_id=2,
            user_id=2,
            share_link="http://example.com/share/LD001",
            expires_at=datetime(2024, 7, 1),
            purpose="Sign",
            signed=False
        )
    ]
    db.session.add_all(document_accesses)
    db.session.commit()

    # Creating sample signatures
    signatures = [
        Signature(
            document_id=1,
            timestamp=datetime(2024, 6, 1),
            signature_data="Signature1",
            signer_name="Charlie",
            signer_email="charlie@example.com"
        )
    ]
    db.session.add_all(signatures)
    db.session.commit()

    print("Seeded database")

