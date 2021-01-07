from fastapi import FastAPI, Body

from models.user import User
from models.author import Author
from models.book import Book

app = FastAPI()


# Save bookstore admin to db
@app.post("/user")
async def post_user(user: User):
    return {"request_body": user}


# Check if a given user exists
@app.get("/user")
async def get_user_validation(password: str):
    return {"query_parameter": password}


# Get specific books
@app.get("/book/{isbn}")
async def get_book_with_isbn(isbn: str):
    return {"query_changable_paramter": isbn}


# Get all books of a given author with order type and category
@app.get("/author/{id}/book")
async def get_authors_books(id: int, category: str, order: str = "asc"):
    return {
        "id": str(id),
        "order": order,
        "category": category,
    }


# Update author's name
@app.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name": name}


# Save user and author to db
@app.post("/user/author")
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {
        "user": user,
        "author": author,
        "bookstore_name": bookstore_name
    }