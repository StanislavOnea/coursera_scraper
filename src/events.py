from pydantic import BaseModel


class Event(BaseModel):
    pass


class ScrapeEvent(Event):
    platform: str
    offset: int | None = None
