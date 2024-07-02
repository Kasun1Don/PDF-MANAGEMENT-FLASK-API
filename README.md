# API for dynamically generating PDFs - QuickDoc API


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
![ERD](/docs/API_ERD.jpeg)


The above is my entity relationship diagram (ERD) using crows foot notation. The design was developed through normalisation (explian normalisation process) and why --> the steps overview. Below is an example of normalisation process for the `documents` entity:

FIRST NORMAL FORM


SECOND


THIRD


## Implemented models and their relationships
(how to answer this - structure)


## API Endpoint documentation
- Success documentation
-Failure (code snippets -table)

Users

Documents

For each endpoint, the following are the HTTP verb, route, required body/header data and response:

### Users

Description: 

HTTP verb:

Route:

Required body/header data: 

Expected response:

Example:

Failure Example:


### Documents

### Templates

### Document_Accesses

### Signatures



### 

## Style guide
All code comments are in style guide or comment style guide in the project documentation. (pep 8)

## Reference List
- alchemy
-marshmallow
-text
-flask
-python
-stack overflow 
-error codes
