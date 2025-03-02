import os

def get_async_postgres_uri():
    host = os.environ.get("DB_HOST", "postgres")
    port = 5432
    password = os.environ.get("DB_PASSWORD", "Student123#")
    user, db_name = "student", "postgres"
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
