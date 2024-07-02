# API for dynamically generating PDFs - QuickDoc API

GitHub repository: https://github.com/Kasun1Don/PDF-MANAGEMENT-FLASK-API

## 1. The Problem and Solution

Documents are central to professional communication, wether it be invoices, contracts,reports and brochures. Businesses generate billions of PDFs daily. Traditional methods for generating PDFs based on real-time business data often required complex processes varying from manual data entry to custom scripting involving multiple handoffs between  different software systems. A PDF generation API addresses these challenges by providing a more automated and efficient way to create documents with real-time data. What takes hours can be done in seconds. 

Example use cases:
* Automating contract generation with pre-defined legal clauses and personalized data.
* Generating invoices with real-time product details and pricing.
* Healthcare records

An AIIM (Association for Intelligent Information Management) study on the benefits of document processing automation shows organizations can reduce document processing times by an average of 80% with automation. Much of this is attributed to a 30 - 50% reduction in the time that staff spend on document related tasks (Association for Intelligent Information Management, 2024). 

With the QuickDoc API, businesses can tailor documents to their specific needs using custom templates, which combine pre-defined layouts with dynamic data fields. The API seamlessly merges data with the template, generating a complete and customized PDF document. JSON data is sent from the client to the API to fill the template fields accordingly.

Furthermore, the API enables document signatures and tracking link views for shared document links.

The endpoints offer additional business functionality, such as tracking which documents still require signatures and have not yet been signed.

## 2. Project Tracking

The project progress was tracked using a 'GitHub Projects' Kanban board and daily standups. This proved convenient to have the project management tool in the same location as source control. The Kanban board started with "Backlog", "In progress" and "Done" columns, however due to multiple ideas for future functionality an "Extra Features" column was added.

The following are screen captures of the project progress tracking through the course of the project.

### DATE: 26th June 2024

![kanban](/docs/Kanban/1.png)

### DATE: 26th June 2024

![kanban](/docs/Kanban/2.png)

### DATE: 27th June 2024

![kanban](/docs/Kanban/3.png)

### DATE: 28th June 2024

![kanban](/docs/Kanban/4.png)

### DATE: 28th June 2024

![kanban](/docs/Kanban/5.png)

### DATE: 30th June 2024

![kanban](/docs/Kanban/6.png)

### Agile project management through Stand Ups

Below are a few examples of daily standups:

![kanban](/docs/StandUps/1.png){: width="150"} | ![kanban](/docs/StandUps/2.png) | ![kanban](/docs/StandUps/3.png) | 


## 3. Third party services packages and dependencies used in the project

### Third Party Services, Packages, and Dependencies

The application leverages several third-party services, packages, and dependencies. They facilitate various aspects of web development, from database interactions and authentication to data validation and serialization. Below is a detailed description of each:

1. **bcrypt==4.1.3**:
    - **Purpose**: Used for hashing passwords.
    - **Description**: bcrypt is a password hashing function designed for secure password storage. It incorporates a salt to protect against rainbow table attacks and is computationally expensive to resist brute-force attacks. It is crucial for ensuring that user passwords are stored securely in the database. This ensures that even if two users have the same password, their hashes will be different, enhancing security. Bcrypt is used to hash passwords before storing them in the database and to verify user passwords during authentication.

2. **Flask==3.0.3**:
    - **Purpose**: Web framework for building the application.
    - **Description**: Flask is a lightweight WSGI web application framework. It is designed with simplicity and flexibility in mind, allowing developers to build scalable web applications quickly. Flask's modular nature and extensive documentation make it an excellent choice for building RESTful APIs and web services.

3. **Flask-Bcrypt==1.0.1**:
    - **Purpose**: Integration of bcrypt with Flask.
    - **Description**: Flask-Bcrypt is a Flask extension that provides bcrypt hashing utilities for Flask applications. It simplifies the use of bcrypt within the Flask context, making it easier to hash passwords and verify them during authentication processes.

4. **Flask-JWT-Extended==4.6.0**:
    - **Purpose**: JWT (JSON Web Token) authentication for Flask.
    - **Description**: Flask-JWT-Extended adds support for using JSON Web Tokens to Flask for user authentication. JWTs are a secure way to transmit information between parties as a JSON object. This package provides tools for creating, decoding, and managing JWTs, enabling secure user authentication and session management.

5. **marshmallow==3.21.3**:
    - **Purpose**: Object serialization and deserialization.
    - **Description**: Marshmallow is an ORM/ODM/framework-agnostic library for converting complex data types, such as objects, to and from native Python data types. It is used for data validation, serialization, and deserialization, making it easier to handle API request and response data in a structured way.

6. **marshmallow-sqlalchemy==1.0.0**:
    - **Purpose**: Integration of SQLAlchemy models with Marshmallow.
    - **Description**: Marshmallow-SQLAlchemy is an integration library that adds SQLAlchemy support to Marshmallow. It provides serialization and deserialization of SQLAlchemy models, allowing seamless conversion between database records and Python objects for API responses and requests.

7. **psycopg2-binary==2.9.9**:
    - **Purpose**: PostgreSQL database adapter.
    - **Description**: psycopg2-binary is a PostgreSQL adapter for Python. It is used to connect and interact with the PostgreSQL database from within a Python application. It supports the full range of SQL operations, providing a robust and efficient way to perform database queries and transactions.

8. **PyJWT==2.8.0**:
    - **Purpose**: JSON Web Token implementation in Python.
    - **Description**: PyJWT is a Python library for encoding and decoding JSON Web Tokens. It is used in conjunction with Flask-JWT-Extended to create, sign, and verify JWTs. This ensures secure transmission of information between the client and server in a stateless manner.

9. **python-dotenv==1.0.1**:
    - **Purpose**: Environment variable management.
    - **Description**: python-dotenv is a library for loading environment variables from a .env file into the environment. It is useful for managing configuration settings, such as database URLs and secret keys, without hardcoding them into the application, thereby enhancing security and flexibility. In the app, environment variables like the SQLAlchemy database URI and JWT secret key are stored in a .env file, ensuring they are not hard-coded into the application.

10. **SQLAlchemy==2.0.31**:
    - **Purpose**: SQL toolkit and Object-Relational Mapping (ORM) library.
    - **Description**: SQLAlchemy is a comprehensive SQL toolkit and ORM for Python. It provides a full suite of well-known enterprise-level persistence patterns, designed for efficient and high-performing database access. SQLAlchemy allows developers to work with databases using Python objects, facilitating complex queries and database management.

11. **Werkzeug==3.0.3**:
    - **Purpose**: WSGI utility library for Python.
    - **Description**: Werkzeug is a comprehensive WSGI web application library. It is a key component of Flask, providing routing, debugging, and server functionalities. Werkzeug enhances the development process by offering utilities for request and response handling, URL routing, and error catching.

## 4. Benefits and drawbacks of the PostgreSQL database system
PostgreSQL is the chosen database system for this application. Below is a examination of the benefits and drawbacks of selecting PostgreSQL:

| **Benefits**                                                                                                       | **Drawbacks**                                                                                                     |
|--------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| **ACID Compliance:** PostgreSQL ensures Atomicity, Consistency, Isolation, and Durability, which are crucial for maintaining data integrity and reliability. This is especially important for applications requiring robust transaction management, such as document handling and user authentication. | **Complexity:** PostgreSQL's rich feature set and advanced capabilities can make it more complex to set up and manage compared to simpler databases. This may require more expertise and effort from database administrators. |
| **Extensibility:** PostgreSQL is highly extensible, allowing users to define their own data types, operators, and index methods. This flexibility is beneficial for customizing the database to fit the specific needs of the project. | **Resource Intensive:** PostgreSQL can be more resource-intensive in terms of memory and CPU usage, particularly when handling complex queries or high-concurrency environments. This might necessitate more powerful hardware. |
| **Open Source:** Being open-source, PostgreSQL is free to use and has a large community of developers contributing to its continuous improvement. This ensures regular updates, security patches, and a wealth of third-party tools and extensions, which can enhance the development process. | **Learning Curve:** Due to its extensive capabilities and advanced features, PostgreSQL has a steeper learning curve for new users, especially those coming from simpler database systems like MySQL. |
| **Advanced SQL Compliance:** PostgreSQL supports a wide range of SQL standards, including complex queries, joins, views, triggers, and stored procedures. This ensures compatibility with various applications and simplifies the migration process from other SQL databases. | |
| **Performance Optimization:** With features like advanced indexing techniques, query optimization, and efficient memory management, PostgreSQL can handle large datasets and high-concurrency workloads effectively. This is beneficial for managing multiple users and documents in the project. While MySQL offers good performance, PostgreSQL's advanced indexing and optimization features often provide better performance for complex queries and large datasets. | |
| **Security Features:** PostgreSQL offers robust security features, including SSL support for encrypted connections, data encryption, and a flexible and powerful access-control system. This is essential for protecting sensitive user and document data. | |

## 5. Features, purpose and functionality of the SQLAlchemy ORM
This application utilizes SQLAlchemy for its ORM (Object-Relational Mapping) system. SQLAlchemy facilitates seamless integration between Python and SQL databases by automatically translating Python class operations into SQL statements. This enables querying relational databases in a "Pythonic" way, significantly reducing the need for direct SQL use.

Features and functionalities of SQLAlchemy ORM include:

- **Establishing database connection**: To interact with the PostgreSQL database, a connection must be first established. Below is a demonstration of how SQLAlchemy is used to initialize the database connection in a Flask application:

    ```python
    from flask import Flask

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://user:password@localhost:5432/mydatabase'
    ```

- **Defining database models**: Database tables and relationships are defined using Python classes, with each class representing a database table and each instance corresponding to a row in that table. For example, the Document model demonstrates how to declare a primary key, set up foreign keys, and establish relationships with other tables. Here's an example of the Document model:

    ```python
    from sqlalchemy import ForeignKey
    from sqlalchemy.orm import Mapped, mapped_column, relationship
    from datetime import datetime
    from typing import List
    import uuid

    class Document(db.Model):
        __tablename__ = 'documents'
        
        id: Mapped[int] = mapped_column(primary_key=True)
        org_name: Mapped[str] = mapped_column(String(80), nullable=False)
        document_type: Mapped[str] = mapped_column(String(40), nullable=False)
        document_number: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
        date: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=lambda: datetime.now())
        content: Mapped[dict] = mapped_column(JSON, nullable=False)
        template_id: Mapped[int] = mapped_column(Integer, ForeignKey('templates.id'), nullable=False)
        user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="SET NULL"), nullable=True)

        template: Mapped['Template'] = relationship('Template', back_populates='documents')
        users: Mapped['User'] = relationship('User', back_populates='documents')
        document_accesses: Mapped[List['DocumentAccess']] = relationship('DocumentAccess', back_populates='document', cascade='all, delete')
        signatures: Mapped[List['Signature']] = relationship('Signature', back_populates='document', cascade='all, delete')
    ```

    In this example, the `Document` class corresponds to a `documents` table. The primary key is `id`, with `template_id` and `user_id` as foreign keys. Relationships with `Template`, `User`, `DocumentAccess`, and `Signature` classes are established.

- **Performing CRUD operations**: SQLAlchemy models and sessions allow for create, read, update, and delete operations on the database. Examples involving the `documents` table include:

    Read operation:

    ```python
    @documents_bp.route("/", methods=['GET'])
    @jwt_required()
    def get_all_documents():
        user_id = get_jwt_identity()
        stmt = db.select(Document).filter_by(user_id=user_id)
        documents = db.session.scalars(stmt).all()
        return DocumentSchema(many=True).dump(documents), 200
    ```

    Above is a SQLAlchemy statement to select all `Document` objects created by the current user. The statement is executed, and the `.all()` method returns the results as a list. The results are serialized into JSON format using the marshmallow schema `DocumentSchema`.

    Create operation:

    ```python
    @documents_bp.route("/", methods=['POST'])
    @jwt_required()
    def create_document():
        user_id = get_jwt_identity()
        document_info = DocumentSchema(only=['document_type', 'content', 'template_id']).load(request.json, unknown='exclude')
        document = Document(
            org_name=document_info['org_name'],
            document_type=document_info['document_type'],
            content=document_info['content'],
            template_id=document_info['template_id'],
            user_id=user_id
        )
        db.session.add(document)
        db.session.commit()
        return DocumentSchema().dump(document), 201
    ```

    Here, JSON data is loaded from the request body using a marshmallow schema. A new `Document` object is created with this information. The new `Document` object is added to the database session and committed, saving the changes. A JSON response with the details of the new `Document` record is returned.

## 6. Entity Relationship Diagram (ERD)

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


## 7. Implemented models and their relationships
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
    * One-to-Many with Signature: A document can potentially have many signatures.

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
### SQLAlchemy queries to access data using the models' relationships:

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

## 8. API Endpoint documentation
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
All code and code comments are written in reference to PEP 8 (The Python Enhancement Proposals, 2024).


## Reference List
Association for Intelligent Information Management (AIIM). (n.d.). How to Choose the Best Document Automation Software. Available at: https://www.ibml.com/blog/how-to-choose-the-best-document-automation-software/.

Flask. (2024). Welcome to Flask — Flask Documentation (3.0.x). Available at: https://flask.palletsprojects.com/en/3.0.x/.

Marshmallow. (2024). Marshmallow Documentation. Available at: https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html.

Mozilla Developer Network (MDN). (2024). HTTP Response Status Codes. Available at: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status.

Python Software Foundation. (2024). The Python Standard Library. Available at: https://docs.python.org/3/.

SQLAlchemy. (2024). SQLAlchemy Documentation. Available at: https://docs.sqlalchemy.org/en/20/.

Stack Overflow. (2024). Can we set a default UUID for the ID field (primary key) in a Flask model. Available at: https://stackoverflow.com/questions/78297444/can-we-set-a-default-uuid-for-the-id-field-primary-key-in-a-flask-model.

The Python Enhancement Proposals (PEP). (2024). PEP 8 – Style Guide for Python Code. Available at: https://peps.python.org/pep-0008/#:~:text=The%20Python%20standard%20library%20is,inside%20parentheses%2C%20brackets%20and%20braces.


