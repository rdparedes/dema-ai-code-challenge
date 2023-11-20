from typing import List, Optional
from .models import Product, Product_Pydantic

import strawberry
from strawberry.asgi import GraphQL


@strawberry.type
class ProductType:
    product_id: Optional[str]
    name: str
    quantity: int
    category: str
    sub_category: str
    orders: List["OrderType"]


@strawberry.type
class OrderType:
    order_id: str
    currency: str
    quantity: int
    shipping_cost: float
    amount: float
    channel: str
    channel_group: str
    campaign: Optional[str]
    date_time: str


@strawberry.type
class Query:
    # TODO: Implement filtering and pagination with strawberry
    @strawberry.field
    async def products(
        self,
        name: Optional[str] = None,
        category: Optional[str] = None,
        sub_category: Optional[str] = None,
    ) -> List[ProductType]:
        query = Product.all()

        if name is not None:
            query = query.filter(name__icontains=name)
        if category is not None:
            query = query.filter(category__icontains=category)
        if sub_category is not None:
            query = query.filter(sub_category__icontains=sub_category)

        products = await Product_Pydantic.from_queryset(
            query.prefetch_related("orders")
        )

        return products


schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)
