import json
from typing import Any

from scraper_factory import ScraperFactory
from pydantic import ValidationError

from courses_service import SaveCourseraCoursesHandler
from events import ScrapeEvent
from repository import SqlAlchemyAsyncRepository
import asyncio
from db import get_async_db_session


async def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> None:
    try:
        #body = json.loads(event["body"])
        #scrape_event = ScrapeEvent(**body)
        async with get_async_db_session() as session:
            repository = SqlAlchemyAsyncRepository(session)
            scraper = ScraperFactory.create_scraper()
        
            await SaveCourseraCoursesHandler.handle(repository, scraper)

    except ValidationError as e:
        message = f"{e.__class__.__name__}: {e}"
        print(message)
    except Exception as e:
        message = f"{e.__class__.__name__}: {e}"
        print(message)


if __name__ == "__main__":
    asyncio.run(lambda_handler(
        {
            "platform": "coursera",
        },
        {},
    ))
