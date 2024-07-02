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

DATE:

DATE:

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
(how to answer this - structure)


## API Endpoint documentation

Users

Documents

For each endpoint, the following are the HTTP verb, route, required body/header data and response:

### Users

* **Description: Gets a list of all users from the current user's organization**

* HTTP verb: GET

* Route: /users

* Required body/header data: 

Body | Header 
---|----------
None | Valid JWT    

* Expected response: 

Body | Header 
---|----------
JSON object of the users (id, username, email, org_name, is_admin) | HTTP Status Code 200 OK    

* Example:

![ERD](/docs/API_ERD.jpeg)

* Failure Example(s):

![ERD](/docs/API_ERD.jpeg)


### Documents

### Templates

### Document_Accesses

### Signatures



### 

## Style guide
All code and code comments are written in reference to PEP 8 - Style Guide ()

## Reference List
- alchemy
-marshmallow
-text
-flask
-python
-stack overflow 
-error codes
