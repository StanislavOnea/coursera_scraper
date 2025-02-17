from pydantic import BaseModel, HttpUrl, field_validator
from typing import List

class Course(BaseModel):
    name: str
    tags: str | None = None
    difficulty: str | None = None
    instructor_name: str | None = None
    url: str
    summary: str
    description: str
    reviews: int | None = None
    duration: str | None = None
    enrolled: int | None = None
    rating: float | None = None
    language: str | None = "English"
    price: str | None = None
    image_url: str

    @field_validator('url', 'image_url', mode='before')
    @classmethod
    def url_validator(cls, value: str) -> str:
        HttpUrl(value)
        return value
