from typing import List

from pydantic import BaseModel
from fastapi import Query

from pytantic import Book


class Author(BaseModel):
    name: str
    books: List[str]