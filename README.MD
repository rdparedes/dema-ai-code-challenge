This project was created using poetry. To install poetry, run the following command:

```bash
pip install poetry
```

To install the dependencies, run the following command:

```bash
poetry install
```

Then it's necessary to start a virtual environment with poetry:

```bash
poetry shell
```

Then run the server:

```bash
uvicorn app.main:app --root-path app/ --reload
```

---

Importing data from the csv files:

```bash
python scripts/import_data.py
```

---

Sample queries:

```bash
# Get all products
curl -X GET "http://localhost:8000/products?page_size=15"

# Update a product
```bash
curl -X PUT -H 'Content-Type: application/json' -d '{"name": "foobar"}' "http://localhost:8000/products/prod1548%23prod104001000080"
```
