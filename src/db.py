from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker 
from contextlib import asynccontextmanager
from orm import Base
import config


engine = create_async_engine(
    config.get_async_postgres_uri(),
    pool_size=10,
    isolation_level="REPEATABLE READ",
)

@asynccontextmanager
async def get_async_db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    LocalSession = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    async_session = LocalSession()
    
    try:
        yield async_session
    finally:
        await async_session.close()
