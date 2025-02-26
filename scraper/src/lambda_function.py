import json
from typing import Any

from adapters.factories.scraper_factory import ScraperFactory
from pydantic import ValidationError

from handlers.save_courses import SaveCourseraCoursesHandler
from model.events import ScrapeEvent
import config
from adapters.repository import SqlAlchemyRepository
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker 


DEFAULT_ASYNC_SESSION_FACTORY = async_sessionmaker(
    bind=create_async_engine(
        config.get_async_postgres_uri(),
        pool_size=10,
        isolation_level="REPEATABLE READ",
    ),
    class_=AsyncSession,
    expire_on_commit=False,
)


async def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> None:
    try:
        #body = json.loads(event["body"])
        #scrape_event = ScrapeEvent(**body)
        async with DEFAULT_ASYNC_SESSION_FACTORY() as session:
            repository = SqlAlchemyRepository(session)
            scraper = await ScraperFactory.create_scraper()
        
            await SaveCourseraCoursesHandler.handle(repository, scraper)

    except ValidationError as e:
        message = f"{e.__class__.__name__}: {e}"
        print(message)
    except Exception as e:
        message = f"{e.__class__.__name__}: {e}"
        print(message)

asyncio.run(lambda_handler(
    {
        "platform": "coursera",
    },
    {},
))
