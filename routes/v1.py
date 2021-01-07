from fastapi import FastAPI, Body, Header, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from models.jwt_user import JWTUser
from models.user import User
from models.author import Author
from models.book import Book
from utils.secuirty import authenticate_user, create_jwt_token, check_jwt_token

app_v1 = FastAPI(openapi_prefix="/v1")


# Save bookstore admin to db
@app_v1.post("/user", status_code=HTTP_201_CREATED)
# async def post_user(user: User, x_custom: str = Header(...)):
async def post_user(user: User, x_custom: str = Header("default"), jwt: bool = Depends(check_jwt_token)):
    return {
        "request_body": user,
        "custom_header": x_custom
    }


# Check if a given user exists
@app_v1.get("/user")
async def get_user_validation(password: str):
    return {"query_parameter": password}


# Get specific books
# @app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["name", "year"])
@app_v1.get("/book/{isbn}", response_model=Book, response_model_exclude=["author"])
async def get_book_with_isbn(isbn: str):
    author_dict = {
        "name": "author1",
        "books": ["book1", "book2"]
    }
    author1 = Author(**author_dict)
    book_dict = {
        "isbn": "isbn1",
        "name": "book1",
        "year": 2019,
        "author": author1
    }
    book1 = Book(**book_dict)
    return book1


# Get all books of a given author with order type and category
@app_v1.get("/author/{id}/book")
async def get_authors_books(id: int, category: str, order: str = "asc"):
    return {
        "id": str(id),
        "order": order,
        "category": category,
    }


# Update author's name
@app_v1.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name": name}


# Save user and author to db
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
    return {
        "file_size": str(len(profile_photo))
    }


@app_v1.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username, "password": form_data.password}
    jwt_user = JWTUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    return {"token": jwt_token}