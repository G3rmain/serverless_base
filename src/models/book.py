from pydantic import BaseModel


class Book(BaseModel):
    number: int
    title: str
    original_title: str
    release_date: str
    description: str
    pages: int
    cover: str
    index: int
