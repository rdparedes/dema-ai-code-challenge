## Scope & Limitations

For tech stack of this solution, I took the freedom to choose a few libraries and frameworks that I haven't used before but I wanted to try out, such as FastAPI, Tortoise ORM and Aerich.

Regarding the exercise's scope, I decided to focus on architecting all the pieces and implementing the core features, but I left aside automated testing, custom error handling and other details that would be necessary for a production-ready solution.

### What was done

- List inventory, including pagination and filtering by name, category and subcategory
- Update inventory - update a product's name, quantity, category and/or subcategory
- GraphQL API

### What's missing

- The GraphQL API returns products, but does not have _GraphQL native_ pagination or filtering. The GraphQL API is implemented using Strawberry, which is a very simple and lightweight library, and it is very easy to integrate with FastAPI.
- Bulk update support for Update Inventory
- Sorting support for List Inventory


## Setup

#### Requirements:

- Python 3.7+ (tested with Python 3.11.6)

This project was created using poetry:

```bash
pip install poetry

# Install the dependencies
poetry install

# Start a virtual environment to run the server
poetry shell
```

Run the server

```bash
uvicorn app.main:app --root-path app/ --reload
```

## Importing data from the csv files:

```bash
python scripts/import_data.py -d
```

## Database migrations

The database already contains all the necessary data, changes can be done with Aerich

```bash
# To create a new migration
aerich migrate

# To upgrade the database
aerich upgrade
```

## GraphQL

Start the server:

```bash
strawberry server app.graphql:schema
```

The graphql playground will be available at http://localhost:8000/graphql

## Sample HTTP requests

```bash
# Get all products
curl -X GET "http://localhost:8000/products?page_size=15"
curl -X GET "http://localhost:8000/products?page_size=15&category=clothing"
curl -X GET "http://localhost:8000/products?page_size=15&sub_category=blouse"

# Update a product
curl -X PUT -H 'Content-Type: application/json' -d '{"name": "foobar"}' "http://localhost:8000/products/prod1548%23prod104001000080"
```
