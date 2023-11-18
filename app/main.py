from typing import List

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .config import TORTOISE_ORM
from .models import Product, Product_Pydantic, ProductIn_Pydantic
from .graphql import graphql_app


app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/products", response_model=List[Product_Pydantic])
async def get_products(page: int = 1, page_size: int = 10):
    products = await Product_Pydantic.from_queryset(
        Product.all()
        .limit(page_size)
        .offset((page - 1) * page_size)
        .prefetch_related("orders")
    )
    return products


@app.put("/products/{product_id}", response_model=Product_Pydantic)
async def update_product(product_id: str, new_data: ProductIn_Pydantic):
    await Product.filter(product_id=product_id).update(
        **new_data.model_dump(exclude_none=True)
    )
    return await Product_Pydantic.from_queryset_single(
        Product.get(product_id=product_id)
    )


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
