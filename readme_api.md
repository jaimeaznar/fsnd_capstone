# API Usage

The API can be accessed at: .

## Testing and mock data

Mock data has been loaded into the database so that `DELETE` endpoints function correctly during testing. 
For the delete test to work it is necessary to have a .jpg file named `'tomahawk'` in the `/static/img/` directory.


## Error handling

```
{
    "success": False,
    "error": error,
    "message": error message
}
```

The API will return one of the following errors when a request fails:

```
- 400 -- Bad Request - The request could not be understood by the server
- 401 -- AuthError - Error message
- 403 -- Forbidden - forbidden
- 404 -- Not Found - The requested resource could not be found
- 405 -- Method Not Allowed - The specified method is not allowed for the endpoint
- 500 -- Internal Server Error - The server encountered an unexpected condition

```

## Database Schema

Here is a representation of the db schema (models.py):


Company
- id (primary key)
- name
- city
- state
- address
- phone

Product
- id (primary key
- name
- image
- description
- company_id (foreign key to company.id)

Every field must be populated. Constraints are enforced in the backend so that no fields are null. 


## Role Based Access Control

There are 2 roles utilized in this project. They are `Director` and `Manager`. All `CRUD`endpoints require the user to be authenticated with one of the roles listed above.

### Permission Overview

Director

- get:company
- post:company
- patch:company
- delete:company
- get:product
- post:product
- patch:product
- delete:product

Manager

- patch:company
- patch:product

Users (2) have already been set up with each of the 2 available roles (credentials will be provided in the project submission details). JWT token has an expirating time of 24 hrs.

## Requests

The capstone project API endpoints are accessed using HTTP requests and JSON request bodies. Each endpoint uses the appropriate HTTP verb for the action it performs. This API utilizes the GET, POST, PATCH, and DELETE methods. The most convenient method of accessing this API is using the Postman tool, however, the curl tool is also an option.

### Method/Action
```
- GET - retrieve company and product information for a particular company or product
- POST - create a new company or product
- PATCH - patch an existing company or product
- DELETE - delete an existing company or prodcuct
```

### Responses
The API will return when a request succeeds:

- 200 -- OK - request successful


# Endpoint Overview

Postman can be used. Make sure token is send along with requests for all CRUD endpoints.

# COMPANY -- GET | POST | PATCH | DELETE 

## GET /
This endpoint doesn't require authentication
Returns index html

## GET /api/companies

This endpoint doesn't require authentication.
Returns a list of all `companies` in the database.
The endpoint will return a status code of 200 if successful, or 404 if no players are found.

Sample response for db with 1 company:
```
{
    "companies": [
        {
            "address": "Kepak madrid",
            "city": "Madrid",
            "name": "Kepak",
            "phone": "12345",
            "state": "Madrid"
        }
    ],
    "success": true
}
```

## GET /api/companies/search
```
{
    "products": {
        "count": 1,
        "data": [
            {
                "address": "Kepak madrid",
                "city": "Madrid",
                "id": 1,
                "name": "Kepak",
                "phone": "12345",
                "state": "Madrid"
            }
        ]
    },
    "search_term": "Kepak",
    "success": true
}
```

## GET /api/companies/<int:company_id>

```
{
    "company": {
        "address": "Kepak madrid",
        "city": "Madrid",
        "id": 1,
        "name": "Kepak",
        "phone": "12345",
        "state": "Madrid"
    },
    "success": true
}
```

## GET /api/companies/create
Returns 200 (template rendered ok)
```
{
    'success': True,
}
```

## POST /companies/create
```
{
    "company": {
        "address": "test address",
        "city": "test city",
        "name": "test name",
        "phone": "test phone",
        "state": "test state"
    },
    "success": true
}
```

## GET /api/companies/<int:company_id>/edit
for company with id = 2. Id might change so check db for current existing ids.
```
{
    "company": {
        "address": "test address",
        "city": "test city",
        "name": "test name",
        "phone": "test phone",
        "state": "test state"
    },
    "success": true
}
```

## POST /api/companies/<int:company_id>/edit
for company with id = 2 patching name
```
{
    "company": {
        "address": "test address",
        "city": "test city",
        "name": "test name patched",
        "phone": "test phone",
        "state": "test state"
    },
    "success": true
}
```

## DELETE /api/companies/<int:company_id>/edit
```
{
    "id": 2,
    "success": true
}
```

# PRODUCT -- GET | POST | PATCH | DELETE

## GET /api/products
```
{
    "products": [
        {
            "description": "descripcion solomillo",
            "image": "static/img/img_solomillo.jpg",
            "name": "solomillo"
        },
        {
            "description": "descripcion tomahawk",
            "image": "static/img/tomahawk.jpg",
            "name": "tomahawk"
        }
    ],
    "success": true
}
```

## GET /api/products/search (?search_term=solomillo)
```
{
    "products": {
        "count": 1,
        "data": [
            {
                "description": "descripcion solomillo",
                "id": 1,
                "name": "solomillo"
            }
        ]
    },
    "search_term": "solomillo",
    "success": true
}
```
## GET /api/products/<int:product_id> 
for product with id = 2
```
{
    "data": {
        "description": "descripcion tomahawk",
        "id": 2,
        "image": "static/img/tomahawk.jpg",
        "name": "tomahawk"
    },
    "success": true
}
```

## GET /api/products/create
Return 200 ok if form template renders
```
{
    "success": true
}
```

## POST /api/products/create
```
{
    "new_product": {
        "company_id": "1",
        "description": "post test description",
        "image": "post test image.jpg",
        "name": "post name test"
    },
    "success": true
}
```

## GET /api/products/<int:product_id>/edit
for product with id = 2
```
{
    "id": 2,
    "name": "tomahawk",
    "success": true
}
```

## POST /api/products/<int:product_id>/edit
for product with id = 2
```
{
    "product_id": 2,
    "success": true
}
```

## DELETE /api/products/<ing:product_id>/delete
for product with id = 1
```{
    "product": {
        "company_id": 1,
        "description": "descripcion solomillo",
        "image": "static/img/img_solomillo.jpg",
        "name": "solomillo"
    },
    "success": true
}```

