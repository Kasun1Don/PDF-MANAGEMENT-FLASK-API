# API for dynamically generating PDFs - QuickDoc API

GitHub repository: https://github.com/Kasun1Don/PDF-MANAGEMENT-FLASK-API

## The Problem and Solution

Documents are central to professional communication, wether it be invoices, contracts,reports and brochures. Businesses generate billions of PDFs daily. Traditional methods for generating PDFs based on real-time business data often required complex processes varying from manual data entry to custom scripting involving multiple handoffs between  different software systems. A PDF generation API addresses these challenges by providing a more automated and efficient way to create documents with real-time data. What takes hours can be done in seconds. 

Example use cases:
* Automating contract generation with pre-defined legal clauses and personalized data.
* Generating invoices with real-time product details and pricing.
* Healthcare records

An AIIM (Association for Intelligent Information Management) study on the benefits of document processing automation shows organizations can reduce document processing times by an average of 80% with automation. Much of this is attributed to a 30 - 50% reduction in the time that staff spend on document related tasks. 

With the QuickDoc API, businesses can tailor documents to their specific needs using custom templates, which combine pre-defined layouts with dynamic data fields. The API seamlessly merges data with the template, generating a complete and customized PDF document. JSON data is sent from the client to the API to fill the template fields accordingly.

Furthermore, the API enables document signatures and tracking link views for shared document links.

The endpoints offer additional business functionality, such as tracking which documents still require signatures and have not yet been signed.

#### ^https://www.ibml.com/blog/how-to-choose-the-best-document-automation-software/

## Project Tracking

The project progress was tracked using a 'GitHub Projects' Kanban board and daily standups. This proved convenient to have the project management tool in the same location as source control. The Kanban board started with "Backlog", "In progress" and "Done" columns, however due to multiple ideas for future functionality an "Extra Features" column was added.

The following are screen captures of the project progress tracking through the length of the project.

DATE: 26th June 2024

DATE: 27th June 2024

DATE: 28th June 2024



### Agile project management through Stand Ups

Here are a few examples of daily standups:


## Third party services packages and dependencies used in the project

## Benefits and drawbacks of the PostgreSQL database system

## Features, purpose and functionality of the SQLAlchemy ORM

## Entity Relationship Diagram (ERD)

The diagram below is the application's entity relationship diagram (ERD). This ERD depicts all the entities of the relational database design for this application, the relationships are depicted using crow's foot notation (refer to diagram legend). In the provided ERD, all relations have been normalised:

![ERD](/docs/API_ERD.jpeg)

### Normalisation

Normalisation prevents data redundancy, ensures data integrity, and optimizes relational database performance by reducing data anomalies and ensuring consistency across relations. This process involves 3 stages:

1. 1st Normal Form (1NF): Each table contains atomic values, and each field contains unique data.
2. 2nd Normal Form (2NF): Each non-key attribute is fully functionally dependent on the primary key. For example, in DOCUMENT_ACCESS, share_link, expires_at, and other attributes are fully dependent on the primary key id.
3. 3rd Normal Form (3NF): No transitive dependency exists. Non-key attributes depend only on the primary key. In DOCUMENTS, attributes like org_name and document_type depend directly on id.

Normalisation to 3NF ensures each non-key attribute depends only on the primary key, eliminating redundancy and ensuring data integrity. Using the `DOCUMENTS` entity to illustrate how normalisation is achieved through these stages:

### 1NF
In this form, the table has a primary key, each column has a unique name, and each cell contains only one value (atomicity). This form was the starting point of the database design for the `Documents` entity, where all the desired information fields were collated into a single table.

DOCUMENTS
id | org_name | document_type | document_number           | date       | content                             | template_id | user_id | purpose    | signed | access_time | visits | signature_data | signer_name | signer_email
---|----------|---------------|---------------------------|------------|-------------------------------------|-------------|---------|------------|--------|-------------|--------|----------------|-------------|--------------
1  | OrgA     | Invoice       | 123e4567-e89b-12d3-a456-426614174000 | 2023-07-01 | {"total": 100, "items": ["item1"]} | 1           | 1       | Review     | False  | 2023-07-01  | 3      | data1          | Alice       | alice@example.com
2  | OrgB     | Contract      | 123e4567-e89b-12d3-a456-426614174001 | 2023-07-02 | {"clauses": ["clause1"]}            | 2           | 2       | Sign       | True   | 2023-07-02  | 2      | data2          | Bob         | bob@example.com

### 2NF
Builds on 1NF by ensuring that all non-key columns are dependent on the primary key. The Documents table is split into several smaller tables based on the dependencies that exist.

* `DocumentAccess`: An DocumentAccess table is created, with the primary key of `id` to identify each access of a document. Columns like `purpose, signed, access_time, and visits are dependent on an access, hence they are part of the table.

id | document_id | user_id | share_link | expires_at | purpose | signed | access_time | visits
---|-------------|---------|------------|------------|---------|--------|-------------|-------
1  | 1           | 1       | link1      | 2023-07-05 | Review  | False  | 2023-07-01  | 3
2  | 2           | 2       | link2      | 2023-07-06 | Sign    | True   | 2023-07-02  | 2


* `Signatures`: A Signatures table is also created, with the primary key of `id` to identify each signature. Columns signature_data, signer_name, and signer_email all depend on the id.

id | document_id | timestamp  | signature_data | signer_name | signer_email
---|-------------|------------|----------------|-------------|--------------
1  | 1           | 2023-07-01 | data1          | Alice       | alice@example.com
2  | 2           | 2023-07-02 | data2          | Bob         | bob@example.com

* `Documents`: As all the non-key attributes in the original Documents table have now been split out into their own tables, `DocumentAccess` and `Signatures`, the `Documents` table now only contains the columns org_name, document_type, document_number, date, content, template_id, and user_id.

id | org_name | document_type | document_number           | date       | content                             | template_id | user_id
---|----------|---------------|---------------------------|------------|-------------------------------------|-------------|--------
1  | OrgA     | Invoice       | 123e4567-e89b-12d3-a456-426614174000 | 2023-07-01 | {"total": 100, "items": ["item1"]} | 1           | 1
2  | OrgB     | Contract      | 123e4567-e89b-12d3-a456-426614174001 | 2023-07-02 | {"clauses": ["clause1"]}            | 2           | 2

### 3NF
Builds on 2NF by ensuring that all non-key columns are only dependent on the primary key and not on any other non-key column (no transitive dependency). This further ensures data integrity and eliminates redundancy.

* `Templates`: A Templates table is created to store information about templates, eliminating transitive dependency from the Documents table.

id | name             | structure
---|------------------|-------------------------------------
1  | InvoiceTemplate  | {"layout": "invoice layout"}
2  | ContractTemplate | {"layout": "contract layout"}

* `Users`: A Users table is created to store information about users, ensuring that user information is not repeated across documents.

id | username | email              | password | org_name | is_admin
---|----------|--------------------|----------|----------|---------
1  | alice    | alice@example.com  | pass123  | OrgA     | True
2  | bob      | bob@example.com    | pass456  | OrgB     | False


## Implemented models and their relationships
The application uses SQLAlchemy to define several models representing various entities in the application. These models include `User`, `Template`, `Document`, `DocumentAccess`, and `Signature`. Each model is linked to corresponding tables in the database, and relationships between these models are established to ensure data integrity and facilitate efficient data retrieval. These models are interconnected through various relationships like One-to-Many and Many-to-One.


### User Model

The User model represents the users of the application. Each user belongs to an organization and can create and access documents. Users can also be designated as admins.

* Relationships:
    * One-to-Many with Document: A user can create many documents.
    * One-to-Many with DocumentAccess: A user can create many document access records.


- Maps to a `users` table in the database

    ```python
    __tablename__ = 'users'
    ```

- Table has columns `id` (primary key), `username`, `email`, `password`, `org_name`, and `is_admin`

    ```python
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    org_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean(), default=False)
    ```

- Has attributes `documents` and `document_accesses` which are lists of all documents and document access records created by the user. Upon deletion of a user, all related document access records will also be deleted.

    ```python
    documents: Mapped[list['Document']] = relationship('Document', back_populates='users')
    document_accesses: Mapped[list['DocumentAccess']] = relationship('DocumentAccess', back_populates='user', cascade='all, delete')
    ```

### Template Model
The Template model represents document templates that users can use to create documents.

* Relationships:
    * One-to-Many with Document: A template can be used in many documents.

- Maps to a `templates` table in the database

    ```python
    __tablename__ = 'templates'
    ```

- Table has columns `id` (primary key), `name`, and `structure`

    ```python
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    structure: Mapped[dict] = mapped_column(JSON, nullable=False)
    ```

- Has an attribute called `documents`, which is a list of all documents using the template.

    ```python
    documents: Mapped[list['Document']] = relationship('Document', back_populates='template')
    ```

### Document Model

The Document model represents documents created by users. Each document belongs to a user and is based on a template.

* Relationships:
    * Many-to-One with User: A document is created by a user.
    * Many-to-One with Template: A document is based on a template.
    * One-to-Many with DocumentAccess: A document can have many access records.
    * One-to-Many with Signature: A document can have many signatures.

- Maps to a `documents` table in the database

    ```python
    __tablename__ = 'documents'
    ```

- Table has columns `id` (primary key), `org_name`, `document_type`, `document_number`, `date`, `content`, `template_id` (foreign key), and `user_id` (foreign key)

    ```python
    id: Mapped[int] = mapped_column(primary_key=True)
    org_name: Mapped[str] = mapped_column(String(80), nullable=False)
    document_type: Mapped[str] = mapped_column(String(40), nullable=False)
    document_number: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now())
    content: Mapped[dict] = mapped_column(JSON, nullable=False)
    template_id: Mapped[int] = mapped_column(Integer, ForeignKey('templates.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    ```

- Has attributes `template`, `users`, `document_accesses`, and `signatures` which link to related templates, users, document access records, and signatures. Upon deletion of a document, all related document access records and signatures will also be deleted.

    ```python
    template: Mapped['Template'] = relationship('Template', back_populates='documents')
    users: Mapped['User'] = relationship('User', back_populates='documents')
    document_accesses: Mapped[list['DocumentAccess']] = relationship('DocumentAccess', back_populates='document', cascade='all, delete')
    signatures: Mapped[list['Signature']] = relationship('Signature', back_populates='document', cascade='all, delete')
    ```

### DocumentAccess Model
The DocumentAccess model represents access records for documents, allowing users to share and control access to documents.

* Relationships:
    * Many-to-One with Document: A document access record is related to a document.
    * Many-to-One with User: A document access record is created by a user.

- Maps to a `document_accesses` table in the database

    ```python
    __tablename__ = 'document_accesses'
    ```

- Table has columns `id` (primary key), `share_link`, `expires_at`, `purpose`, `signed`, `access_time`, `visits`, `document_id` (foreign key), and `user_id` (foreign key)

    ```python
    id: Mapped[int] = mapped_column(primary_key=True)
    share_link: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now() + timedelta(days=3), nullable=False)
    purpose: Mapped[str] = mapped_column(String, nullable=False)
    signed: Mapped[bool] = mapped_column(Boolean(), default=False)
    access_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    visits: Mapped[int] = mapped_column(default=0)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey('documents.id', ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    ```

- Has attributes `document` and `user` which link to related documents and users.

    ```python
    document: Mapped['Document'] = relationship('Document', back_populates='document_accesses')
    user: Mapped['User'] = relationship('User', back_populates='document_accesses')
    ```

### Signature Model
The Signature model represents signatures on documents.

* Relationships:
    * Many-to-One with Document: A signature is related to a document.

- Maps to a `signatures` table in the database

    ```python
    __tablename__ = 'signatures'
    ```

- Table has columns `id` (primary key), `timestamp`, `signature_data`, `signer_name`, `signer_email`, and `document_id` (foreign key)

    ```python
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=db.func.current_timestamp(), nullable=False)
    signature_data: Mapped[str] = mapped_column(Text, nullable=False)
    signer_name: Mapped[str] = mapped_column(String(80), nullable=False)
    signer_email: Mapped[str] = mapped_column(String(160), nullable=False)
    document_id: Mapped[int] = mapped_column(Integer, ForeignKey('documents.id'), nullable=False)
    ```

- Has an attribute called `document`, which links to the related document.

    ```python
    document: Mapped['Document'] = relationship('Document', back_populates='signatures')
    ```

### Queries Using Model Relationships

**Get all documents for a user:**
```python
user_id = 1
documents = db.session.query(Document).filter_by(user_id=user_id).all()
```

**Get all documents for an organization:**
```python
org_name = 'OrgA'
documents = db.session.query(Document).filter_by(org_name=org_name).all()
```

**Get document access records for a document:**
```python
document_id = 1
access_records = db.session.query(DocumentAccess).filter_by(document_id=document_id).all()
```

**Get signatures for a document:**
```python
document_id = 1
signatures = db.session.query(Signature).filter_by(document_id=document_id).all()
```

### Summary

This project uses SQLAlchemy to define and manage the relationships between models, ensuring data integrity and enabling efficient data retrieval through SQL queries. The models include `User`, `Template`, `Document`, `DocumentAccess`, and `Signature`, each with specific relationships that facilitate the creation, sharing, and management of documents within an organization. This relational database design ensures a scalable and maintainable system for handling document workflows.


### Query examples with SQLAlchemy to access data using the models' relationships:

Get all documents for a given user:

```
user_id = 1
documents = db.session.query(Document).filter_by(user_id=user_id).all()
```

Get all documents for an organization:

```
org_name = 'OrgA'
documents = db.session.query(Document).filter_by(org_name=org_name).all()
```

Get signatures for a document:

```
document_id = 1
signatures = db.session.query(Signature).filter_by(document_id=document_id).all()
```


## API Endpoint documentation
For each endpoint, the following are the HTTP verb, route, required body/header data and responses:

### Users

### **Description: Gets a list of all users from the current user's organization**

* HTTP verb: GET

* Route: /users

* Required data: 

Body | Header 
---|----------
None | Valid JWT    

* Expected responses: 

Body | Header 
---|----------
JSON object of the users (id, username, email, org_name, is_admin) | HTTP Status Code 200 OK    

* Example:

![ex](/docs/RouteTests/users_get.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 401 Unauthorized | {"msg": "Missing Authorization Header"}
HTTP Status Code 403 Forbidden | {"msg": "Invalid Token"}

### **Description: Registers a new user (all fields are required)**

* HTTP verb: POST

* Route: /users/register

* Required data: 

Body | Header 
---|----------
{"username": "string", "email": "string", "password": "string", "org_name": "string"} | None

* Expected responses: 

Body | Header 
---|----------
JSON object of the new user (id, username, email, org_name, is_admin) | HTTP Status Code 201 Created

* Example:

![ex](/docs/RouteTests/user_register.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 400 Bad Request | {"error": "Email already registered"}

![ex](/docs/RouteTests/failed/email_already_rego.png)

### **Description: Login and generate JWT**

* HTTP verb: POST

* Route: /users/login

* Required data: 

Body | Header 
---|----------
{"email": "string", "password": "string"} | None

* Expected responses: 

Body | Header 
---|----------
{"token": "JWT token"} | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/users_login.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 401 Unauthorized | {"error": "Invalid email or password"}

![ex](/docs/RouteTests/failed/login_invalid_user.png)

### **Description: Admin can create a new admin user account**

* HTTP verb: POST

* Route: /users/create

* Required data: 

Body | Header 
---|----------
{"username": "string", "email": "string", "password": "string", "org_name": "string", "is_admin": "boolean"} | Valid JWT (admin)

* Expected responses: 

Body | Header 
---|----------
JSON object of the new user (id, username, email, org_name, is_admin) | HTTP Status Code 201 Created

* Example:

![ex](/docs/RouteTests/users_create_admin.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 400 Bad Request | {"error": "Email already registered"}
HTTP Status Code 403 Forbidden | {"msg": "Admin access required"}

### **Description: Admin can delete a user account**

* HTTP verb: DELETE

* Route: /users/int:id

* Required data: 

Body | Header 
---|----------
None | Valid JWT (admin)

* Expected responses: 

Body | Header 
---|----------
{"message": "User deleted successfully"} | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/user_delete.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 403 Forbidden | {"msg": "Admin access required"}
HTTP Status Code 404 Not Found | {"msg": "Not Found"}

### Documents

### **Description: Get all the documents created by the current logged in user**

* HTTP verb: GET

* Route: /documents/user/int:user_id

* Required data: 

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the documents | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/documents_get_user.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 404 Not Found | {"error": "Not Found"}

### **Description: Gets all documents for the current user's organization**

* HTTP verb: GET

* Route: /documents/org

* Required data: 

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the documents | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/documents_get_org.png)

### **Description: Get a specific document by the document ID**

* HTTP verb: GET

* Route: /documents/int:document_id

* Required data: 

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the document | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/documents_get_one.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 404 Not Found | {"msg": "Not Found"}

### **Description: Get all documents from the database (Admin only)**

* HTTP verb: GET

* Route: /documents

* Required data: 

Body | Header 
---|----------
None | Valid JWT (admin)

* Expected responses: 

Body | Header 
---|----------
JSON object of all documents | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/documents_get_all.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 403 Forbidden | {"msg": "Admin access required"}

### **Description: Create new document(s) (using an available template)**

* HTTP verb: POST

* Route: /documents

* Required data: 

Body | Header 
---|----------
{"document_type": "string", "content": "JSON object", "template_id": "int"} | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the new document | HTTP Status Code 201 Created

* Example:

![ex](/docs/RouteTests/documents_create.png)

* Failure Example(s):

![ex](/docs/RouteTests/failed/document_missing_data.png)

### **Description: Update an existing document (must be document creator/owner)**

* HTTP verb: PUT, PATCH

* Route: /documents/int:document_id

* Required data: 

Body | Header 
---|----------
{"document_type": "string", "content": "JSON object"} | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the updated document | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/documents_update.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 404 Not Found | {"msg": "Not Found"}

### **Description: Delete a document (must be document creator/owner)**

* HTTP verb: DELETE

* Route: /documents/int:document_id

* Required data: 

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
{"message": "Document deleted successfully"} | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/documents_delete.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 404 Not Found | {"msg": "Not Found"}

### Templates

### **Description: Gets all templates available for creating documents, including the required fields for each template**

* HTTP verb: GET

* Route: /templates

* Required data: 

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of all templates serialized in TemplateSchema format | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/templates_get.png)

### **Description: Create a new document template (Admin only)**

* HTTP verb: POST

* Route: /templates

* Required data: 

Body | Header 
---|----------
{"name": "string", "structure": "JSON object"} | Valid JWT (admin)

* Expected responses: 

Body | Header 
---|----------
JSON object of the newly created template serialized in TemplateSchema format | HTTP Status Code 201 Created

* Example:

![ex](/docs/RouteTests/templates_create.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 400 Bad Request | {"error": "Template with this name already exists"}
HTTP Status Code 403 Forbidden | {"msg": "Admin access required"}

![ex](/docs/RouteTests/failed/template_exists.png)

### **Description: Delete a template (Admin only)**

* HTTP verb: DELETE

* Route: /templates/int:id

* Required data: 

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
{"message": "Template deleted successfully"} | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/templates_delete.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 404 Not Found | {"msg": "Not found"}
HTTP Status Code 400 Bad Request | {"error": "Cannot delete template. It's being used by one or more documents."}

![ex](/docs/RouteTests/failed/template_cannot_delete.png)

### Document_Accesses (document sharing links)

### **Description: Create a document access link (link expires in 3 days)**

* HTTP verb: POST

* Route: /access

* Required data: 
- The purpose of the document access link creation is required (either 'Sign' or 'Review')

Body | Header 
---|----------
{"document_id": "int", "purpose": "string"} | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the new document access link (document_id, share_link, expires_at, purpose) | HTTP Status Code 201 Created

* Example:

![ex](/docs/RouteTests/accesses_link_creeate.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 400 Bad Request | {"error": "Invalid 'Purpose'. Valid options are: 'Review' or 'Sign'"}

![ex](/docs/RouteTests/failed/accesses_sign_purpose.png)

### **Description: Send a document to be signed by anyone with the unique document access link**

* HTTP verb: POST

* Route: /access/uuid:share_link/sign

* Required data:

Body | Header 
---|----------
{"signature_data": "string", "signer_name": "string", "signer_email": "string"} | None

* Expected responses: 

Body | Header 
---|----------
JSON object of the new signature (signature_data, signer_name, signer_email, timestamp) | HTTP Status Code 201 Created

* Example:

![ex](/docs/RouteTests/accesses_sign.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 403 Forbidden | {"error": "share link has expired"}
HTTP Status Code 400 Bad Request | {"error": "Document has already been signed"}
HTTP Status Code 404 Not Found | {"msg": "Not found"}

![ex](/docs/RouteTests/failed/already_signed.png)

### **Description: Send the unique document access link for anyone to view**

* HTTP verb: GET

* Route: /access/uuid:share_link

* Required data:

Body | Header 
---|----------
None | None

* Expected responses: 

Body | Header 
---|----------
JSON object of the document access data | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/open_access_link.png)

* Failure Example(s):

Header | Body 
---|----------
HTTP Status Code 404 Not Found | {"error": "please create a document access link first"}

![ex](/docs/RouteTests/failed/accesses_link_required.png)

### **Description: Get all unsigned document access links created by the current user**

* HTTP verb: GET

* Route: /access/unsigned

* Required data:

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the unsigned document access links (excluding document) | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/accesses_get_all_unsigned.png)

### **Description: Get all signed document access links created by the current user**

* HTTP verb: GET

* Route: /access/signed

* Required data:

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the signed document access links | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/accesses_signed.png)

### **Description: Sort document access links by the number of link visits**

* HTTP verb: GET

* Route: /access/visits

* Required data:

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the document access links sorted by visits | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/accesses_visits.png)


### Signatures

### **Description: Get the most recent documents that were signed (within the last 24 hours)**

* HTTP verb: GET

* Route: /signatures

* Required data:

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the signed documents from the last 24 hours | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/signatures_all_24.png)

### **Description: Get all signatures details for a specified document ID**

* HTTP verb: GET

* Route: /signatures/document/int:document_id

* Required data:

Body | Header 
---|----------
None | Valid JWT

* Expected responses: 

Body | Header 
---|----------
JSON object of the signature details (timestamp, signature_data, signer_name, signer_email) for the specified document | HTTP Status Code 200 OK

* Example:

![ex](/docs/RouteTests/signatures_one.png)

## Style Guide
All code and code comments are written in reference to PEP 8 - Style Guide ()

## Reference List
- alchemy
-marshmallow
-text
-flask
-python
-stack overflow 
-error codes
