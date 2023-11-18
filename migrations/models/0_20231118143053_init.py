from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "product" (
    "product_id" VARCHAR(255) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "quantity" INT NOT NULL,
    "category" VARCHAR(255) NOT NULL,
    "sub_category" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "order" (
    "order_id" VARCHAR(255) NOT NULL  PRIMARY KEY,
    "currency" VARCHAR(10) NOT NULL,
    "quantity" INT NOT NULL,
    "shipping_cost" REAL NOT NULL,
    "amount" REAL NOT NULL,
    "channel" VARCHAR(100) NOT NULL,
    "channel_group" VARCHAR(100) NOT NULL,
    "campaign" VARCHAR(100),
    "date_time" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "product_id" VARCHAR(255) NOT NULL REFERENCES "product" ("product_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
