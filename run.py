from datetime import datetime

import aioredis
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED

from models.jwt_user import JWTUser
from routes.v1 import app_v1
from routes.v2 import app_v2
from utils import redis_object as re
from utils.const import TOKEN_SUMMARY, TOKEN_DESCRIPTION, REDIS_URL
from utils.db_object import db
from utils.secuirty import check_jwt_token, authenticate_user, create_jwt_token

app = FastAPI(
    title="Bookstore API Documentation",
    description="It is the API that is used for bookstores", version="1.0.0"
)

app.include_router(app_v1, prefix="/v1", dependencies=[Depends(check_jwt_token)])
app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token)])


@app.on_event("startup")
async def connect_db():
    await db.connect()
    re.redis = await aioredis.create_redis_pool(REDIS_URL)


@app.on_event("shutdown")
async def disconnect_db():
    await db.disconnect()

    re.redis.close()
    await re.redis.wait_closed()


@app.post("/token", description=TOKEN_DESCRIPTION, summary=TOKEN_SUMMARY)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username, "password": form_data.password}
    jwt_user = JWTUser(**jwt_user_dict)
    user = await authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    # modify request
    # if not any(word in str(request.url) for word in ["/token", "/docs", "/openapi.json"]):
    #     try:
    #         jwt_token = request.headers["Authorization"].split("Bearer ")[1]
    #         is_valid = await check_jwt_token(jwt_token)
    #     except Exception as e:
    #         is_valid = False
    #
    #     if not is_valid:
    #         return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)

    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response
