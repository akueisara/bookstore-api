from fastapi import Body, Header, File, APIRouter, HTTPException
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from models.user import User
from models.author import Author
from models.book import Book
from utils.db_functions import db_insert_personel, db_check_personel, db_get_book_with_isbn, db_get_author, \
    db_get_author_from_id, db_patch_author_name
from utils.helper_functions import upload_image_to_server
import utils.redis_object as re
import pickle

app_v1 = APIRouter()


# Save bookstore admin to db
@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
# async def post_user(user: User, x_custom: str = Header(...)):
# async def post_user(user: User, x_custom: str = Header("default"), jwt: bool = Depends(check_jwt_token)):
async def post_user(user: User, x_custom: str = Header("default")):
    await db_insert_personel(user)
    return {"result": f"personel {user.name} is created"}


# Check if a given user exists
@app_v1.post("/login", tags=["User"])
async def get_user_validation(username: str = Body(...), password: str = Body(...)):
    redis_key = f"{username},{password}"
    result = await re.redis.get(redis_key)

    # Redis has the data
    if result:
        if result == "true":
            return {"source": "redis", "is_valid": True}
        else:
            return {"source": "redis", "is_valid": False}
    # Redis does not have the data
    else:
        result = await db_check_personel(username, password)
        await re.redis.set(redis_key, str(result), expire=10)

        return {"source": "db", "is_valid": result}


# Get specific books
# @app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"])
@app_v1.get("/book/{isbn}", response_model=Book, response_model_exclude=["author"], tags=["Book"])
async def get_book_with_isbn(isbn: str):
    result = await re.redis.get(isbn)

    if result:
        result_book = pickle.loads(result)
    else:
        try:
            book = await db_get_book_with_isbn(isbn)
            author = await db_get_author(book["author"])
            author_obj = Author(**author)
            book["author"] = author_obj
            result_book = Book(**book)
        except Exception as _:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND)

        await re.redis.set(isbn, pickle.dumps(result_book))

    return result_book


# Get all books of a given author with order type and category
@app_v1.get("/author/{id}/book", tags=["Book"])
async def get_authors_books(id: int, order: str = "asc"):
    author = await db_get_author_from_id(id)
    if author is not None:
        books = author["books"]
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)
        return {"books": books}
    else:
       return {"result": "no author with corresponding id !"}


# Update author's name
@app_v1.patch("/author/{id}/name")
async def patch_author_name(id: int, name: str = Body(..., embed=True)):
    await db_patch_author_name(id, name)
    return {"result": "name is updated"}


# Only for demo
@app_v1.post("/user/author")
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {
        "user": user,
        "author": author,
        "bookstore_name": bookstore_name
    }


# Update user's photo
@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    await upload_image_to_server(profile_photo)
    return {"file_size": len(profile_photo)}
