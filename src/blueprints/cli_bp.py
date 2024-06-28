from datetime import datetime
from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.template import Template
from models.document import Document
from models.document_access import DocumentAccess
from models.docsignature import Signature


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


    documents = [
        Document(
            org_name="OrgA",
            document_type="Invoice",
            document_number="123e4567-e89b-12d3-a456-426614174001",
            date="2024-05-01",
            content={"date": "2024-05-01", "total_amount": 1000, "item_list": ["Item1", "Item2"]},
            template_id=1,
            user_id=1
        ),
        Document(
            org_name="OrgB",
            document_type="Legal",
            document_number="123e4567-e89b-12d3-a456-426614174002",
            date="2024-06-01",
            content={"title": "Agreement", "content": "This is a legal document.", "signatures": []},
            template_id=2,
            user_id=1
        ),
        Document(
            org_name="OrgA",
            document_type="Invoice",
            document_number="123e4567-e89b-12d3-a456-426614174003",
            date="2024-06-15",
            content={"date": "2024-06-15", "total_amount": 1500, "item_list": ["Item3", "Item4"]},
            template_id=1,
            user_id=1
        ),
        Document(
            org_name="OrgB",
            document_type="Legal",
            document_number="123e4567-e89b-12d3-a456-426614174004",
            date="2024-07-01",
            content={"title": "Contract", "content": "This is a legal contract.", "signatures": []},
            template_id=2,
            user_id=2
        ),
        Document(
            org_name="OrgA",
            document_type="Invoice",
            document_number="123e4567-e89b-12d3-a456-426614174005",
            date="2024-07-05",
            content={"date": "2024-07-05", "total_amount": 2000, "item_list": ["Item5", "Item6"]},
            template_id=1,
            user_id=1
        ),
        Document(
            org_name="OrgB",
            document_type="Legal",
            document_number="123e4567-e89b-12d3-a456-426614174006",
            date="2024-07-10",
            content={"title": "Service Agreement", "content": "This is a service agreement.", "signatures": []},
            template_id=2,
            user_id=3
        ),
        Document(
            org_name="OrgA",
            document_type="Invoice",
            document_number="123e4567-e89b-12d3-a456-426614174007",
            date="2024-07-12",
            content={"date": "2024-07-12", "total_amount": 2500, "item_list": ["Item7", "Item8"]},
            template_id=1,
            user_id=1
        ),
        Document(
            org_name="OrgB",
            document_type="Legal",
            document_number="123e4567-e89b-12d3-a456-426614174008",
            date="2024-07-15",
            content={"title": "NDA", "content": "This is a non-disclosure agreement.", "signatures": []},
            template_id=2,
            user_id=2
        ),
        Document(
            org_name="OrgA",
            document_type="Invoice",
            document_number="123e4567-e89b-12d3-a456-426614174009",
            date="2024-07-20",
            content={"date": "2024-07-20", "total_amount": 3000, "item_list": ["Item9", "Item10"]},
            template_id=1,
            user_id=1
        ),
        Document(
            org_name="OrgB",
            document_type="Legal",
            document_number="123e4567-e89b-12d3-a456-426614174010",
            date="2024-07-25",
            content={"title": "MOU", "content": "This is a memorandum of understanding.", "signatures": []},
            template_id=2,
            user_id=1
        )
    ]

    db.session.add_all(documents)
    db.session.commit()


    document_accesses = [
        DocumentAccess(
            document_id=1,
            user_id=3,
            share_link="bbf75963-fd2f-4317-b3e2-070eeb1ed4ca",
            expires_at=datetime(2024, 6, 1),
            purpose="Review",
            signed=True
        ),
        DocumentAccess(
            document_id=2,
            user_id=2,
            share_link="2be167bc-ed6e-4893-879e-130c15fd8823",
            expires_at=datetime(2024, 7, 1),
            purpose="Sign",
            signed=True
        ),
        DocumentAccess(
            document_id=3,
            user_id=1,
            share_link="123e4567-e89b-12d3-a456-426614174011",
            expires_at=datetime(2024, 8, 1),
            purpose="Review",
            signed=False
        ),
        DocumentAccess(
            document_id=4,
            user_id=1,
            share_link="123e4567-e89b-12d3-a456-426614174012",
            expires_at=datetime(2024, 8, 5),
            purpose="Sign",
            signed=True
        )
    ]
    db.session.add_all(document_accesses)
    db.session.commit()


    signatures = [
        Signature(
            document_id=1,
            timestamp=datetime(2024, 6, 1),
            signature_data="Signature1",
            signer_name="Charlie",
            signer_email="charlie@example.com"
        ),
        Signature(
            document_id=2,
            timestamp=datetime(2024, 6, 7),
            signature_data="Signature2",
            signer_name="Charles",
            signer_email="charles@example.com"
        ),
        Signature(
            document_id=4,
            timestamp=datetime(2024, 7, 2),
            signature_data="Signature4",
            signer_name="Bob",
            signer_email="bob@example.com"
        ),
        Signature(
            document_id=5,
            timestamp=datetime(2024, 7, 6),
            signature_data="Signature5",
            signer_name="Alice",
            signer_email="alice@example.com"
        )
    ]
    db.session.add_all(signatures)
    db.session.commit()

    print("Seeded database")

