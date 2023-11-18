from typing import List

import strawberry
from strawberry.asgi import GraphQL

from .models import Product, Product_Pydantic


@strawberry.type
class ProductType:
    product_id: str
    name: str
    quantity: int
    category: str
    sub_category: str


@strawberry.type
class OrderType:
    order_id: str
    currency: str
    quantity: int
    shipping_cost: float
    amount: float
    channel: str
    channel_group: str
    campaign: str
    date_time: str
    product: ProductType


@strawberry.type
class Query:
    @strawberry.field
    async def products(self, page: int = 1, page_size: int = 10) -> List[ProductType]:
        products = await Product_Pydantic.from_queryset(
            Product.all()
            .limit(page_size)
            .offset((page - 1) * page_size)
            .prefetch_related("orders")
        )
        return products

    @strawberry.field
    async def product(self, product_id: str) -> ProductType:
        product = await Product_Pydantic.from_queryset_single(
            Product.get(product_id=product_id)
        )
        return product


schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)
