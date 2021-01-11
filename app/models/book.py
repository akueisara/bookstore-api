from fastapi.openapi.models import Schema
from pydantic import BaseModel

from models.author import Author
from utils.const import ISBN_DESCRIPTION


class Book(BaseModel):
    isbn: str = Schema(default=None, description=ISBN_DESCRIPTION)
    name: str
    author: Author
    year: int = Schema(default=None, exclusiveMinimum=1900, exclusiveMaximum=2100)