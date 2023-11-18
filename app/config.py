TORTOISE_ORM = {
    "connections": {"default": "sqlite://./db/db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
