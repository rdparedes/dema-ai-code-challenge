import asyncio
import re
import sqlite3
import sys
from pathlib import Path

import pandas as pd

current_dir = Path(__file__).parent.absolute()

connection = sqlite3.connect("db/db.sqlite3")
cursor = connection.cursor()

# Smoke test to ensure that the database has the tables we expect
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
assert ("product",) in tables
assert ("order",) in tables


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


async def import_csv(file_path, table_name: str, debug=False):
    df = pd.read_csv(file_path)
    df.columns = [camel_to_snake(col) for col in df.columns]
    for _, row in df.iterrows():
        values = []
        for _, value in row.items():
            if isinstance(value, str):
                value = f"'{value}'"
            elif pd.isna(value):
                value = "NULL"
            values.append(value)

        joined = ", ".join(str(v) for v in values)
        sql = f"INSERT INTO \"{table_name}\" ({', '.join(df.columns)}) VALUES ({joined}) ON CONFLICT DO NOTHING;"

        if debug:
            print("sql", sql)

        cursor.execute(sql)
    connection.commit()

    print(f"Imported {file_path.stem} successfully.")


async def run_migrations(debug=False):
    inventory_csv_path = Path(current_dir, "inventory.csv")
    orders_csv_path = Path(current_dir, "orders.csv")
    await import_csv(inventory_csv_path, "product", debug=debug)
    await import_csv(orders_csv_path, "order", debug=debug)


if __name__ == "__main__":
    is_debug = any(arg in ["-d", "--debug"] for arg in sys.argv)
    asyncio.run(run_migrations(debug=is_debug))
