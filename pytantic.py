import datetime
from typing import Dict, List, Tuple, Set
from pydantic import BaseModel


class Book(BaseModel):
    name: str
    price: float = 10.0
    year: datetime.datetime


book1 = {"name": "book1", "price": 11.0, "year": datetime.datetime.now()}

book_object = Book(**book1)

print(book_object.price)


def print_book(book: Book):
    print(book)


def print_name_of_the_book(book_name: str, year: datetime, price: float):
    print(book_name, year, price)


# def print_name_of_the_books(name_book_list: Dict[str, int]):
# def print_name_of_the_books(name_book_list: Tuple[str]):
# def print_name_of_the_books(name_book_list: Set[int]):
def print_name_of_the_books(name_book_list: List[str]):
    pass