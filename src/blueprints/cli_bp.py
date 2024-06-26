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
    db.create_all()
    print("Created tables")

@db_commands.cli.command("seed")
def db_seed():
    # Creating sample users
    users = [
        User(
            username="alice",
            email="alice@example.com",
            password_hash=bcrypt.generate_password_hash("password").decode('utf8'),
            org_id=1,
            org_name="OrgA",
            is_admin=True
        ),
        User(
            username="bob",
            email="bob@example.com",
            password_hash=bcrypt.generate_password_hash("password").decode('utf8'),
            org_id=1,
            org_name="OrgA",
            is_admin=False
        ),
        User(
            username="charlie",
            email="charlie@example.com",
            password_hash=bcrypt.generate_password_hash("password").decode('utf8'),
            org_id=2,
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
            org_id=1,
            document_type="Invoice",
            document_number="INV001",
            date="2024-05-01",
            content={"date": "2024-05-01", "total_amount": 1000, "item_list": ["Item1", "Item2"]},
            template_id=templates[0].id,
            user_id=users[0].id
        ),
        Document(
            org_id=2,
            document_type="Legal",
            document_number="LD001",
            date="2024-06-01",
            content={"title": "Agreement", "content": "This is a legal document.", "signatures": []},
            template_id=templates[1].id,
            user_id=users[2].id
        )
    ]
    db.session.add_all(documents)
    db.session.commit()

    # Creating sample document accesses
    document_accesses = [
        DocumentAccess(
            document_id=documents[0].id,
            user_id=users[1].id,
            share_link="http://example.com/share/INV001",
            expires_at=datetime(2024, 6, 1),
            purpose="Review",
            signed=False
        ),
        DocumentAccess(
            document_id=documents[1].id,
            user_id=users[2].id,
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
            document_id=documents[1].id,
            timestamp=datetime(2024, 6, 1),
            signature_data="Signature1",
            signer_name="Charlie",
            signer_email="charlie@example.com"
        )
    ]
    db.session.add_all(signatures)
    db.session.commit()

    print("Seeded database")

@db_commands.cli.command("drop")
def db_drop():
    db.drop_all()
    print("Dropped tables")