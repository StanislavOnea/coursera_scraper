import json
from typing import Any

from pydantic import ValidationError

from handlers.scraper import SaveCourseraCoursesHandler
from adapters.beautiful_soup import BeatifulSoupScraper
from model.events import ScrapeEvent
import config
from adapters.repository import SqlAlchemyRepository
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri(),
        isolation_level="REPEATABLE READ",
    )
)


def lambda_handler(event: dict[str, Any], context: dict[str, Any]) -> None:
    try:
        body = json.loads(event["body"])
        scrape_event = ScrapeEvent(**body)
        session = DEFAULT_SESSION_FACTORY()
        repository = SqlAlchemyRepository(session)
        SaveCourseraCoursesHandler.handle(repository, BeatifulSoupScraper)

    except ValidationError as e:
        message = f"{e.__class__.__name__}: {e}"
        print(message)
    except Exception as e:
        message = f"{e.__class__.__name__}: {e}"
        print(message)
