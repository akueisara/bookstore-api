from fastapi import Header, APIRouter
from starlette.status import HTTP_201_CREATED

from models.user import User

app_v2 = APIRouter()


# Save bookstore admin to db
@app_v2.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header("default")):
    return {
        "request_body": "it is version 2",
        "custom_header": x_custom
    }