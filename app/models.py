from typing import List, Optional
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator


class Order(Model):
    order_id = fields.CharField(max_length=255, pk=True)
    currency = fields.CharField(max_length=10)
    quantity = fields.IntField()
    shipping_cost = fields.FloatField()
    amount = fields.FloatField()
    channel = fields.CharField(max_length=100)
    channel_group = fields.CharField(max_length=100)
    campaign = fields.CharField(max_length=100, null=True)
    date_time = fields.DatetimeField(auto_now_add=True)
    product = fields.ForeignKeyField("models.Product", related_name="orders")

    def __str__(self) -> str:
        return self.order_id


class Product(Model):
    product_id = fields.CharField(max_length=255, pk=True)
    name = fields.CharField(max_length=255)
    quantity = fields.IntField()
    category = fields.CharField(max_length=255)
    sub_category = fields.CharField(max_length=255)

    orders: fields.ReverseRelation[Order]

    def __str__(self) -> str:
        return self.name

    class PydanticMeta:
        read_only = (
            "orders",
            "product_id",
        )


Order_Pydantic = pydantic_model_creator(Order, name="Order")


class ProductIn_Pydantic(
    pydantic_model_creator(Product, name="ProductIn", exclude_readonly=True)
):
    name: Optional[str] = None
    quantity: Optional[int] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None


class Product_Pydantic(pydantic_model_creator(Product, name="Product")):
    orders: List[Order_Pydantic] = []
