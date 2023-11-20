from typing import List, Optional

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .config import TORTOISE_ORM
from .models import Product, Product_Pydantic, ProductIn_Pydantic
from .graphql import graphql_app


app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/products", response_model=List[Product_Pydantic])
async def get_products_handler(
    page: int = 1,
    page_size: int = 10,
    name: Optional[str] = None,
    category: Optional[str] = None,
    sub_category: Optional[str] = None,
):
    query = Product.all()

    if name is not None:
        query = query.filter(name__icontains=name)
    if category is not None:
        query = query.filter(category__icontains=category)
    if sub_category is not None:
        query = query.filter(sub_category__icontains=sub_category)

    products = await Product_Pydantic.from_queryset(
        query.limit(page_size).offset((page - 1) * page_size).prefetch_related("orders")
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
