import time
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette.status import HTTP_401_UNAUTHORIZED

from models.jwt_user import JWTUser
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY

import jwt

from utils.db_functions import db_check_token_users, db_check_jwt_username

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

# jwt_user_1 = {"username": "user1", "password": "$2b$12$os2gA.EYjJRNdZfx5iHN7em5YZlM2QdRqmKrmPDz.ItAT/.YsOPhW", "disable": False, "role": "admin"}
# fake_jwt_user_1 = JWTUser(**jwt_user_1)


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


# hashed = "$2b$12$os2gA.EYjJRNdZfx5iHN7em5YZlM2QdRqmKrmPDz.ItAT/.YsOPhW"
# print(verify_password("pass1", hashed))
# print(get_hashed_password("secret"))


# Authenticate username and password to give JWT
async def authenticate_user(user: JWTUser):
    potential_users = await db_check_token_users(user)
    is_valid = False
    for db_user in potential_users:
        if verify_password(user.password, db_user["password"]):
            is_valid = True

    if is_valid:
        user.role = "admin"
        return user

    # if fake_jwt_user_1.username == user.username:
    #     if verify_password(user.password, fake_jwt_user_1.password):
    #         user.role = "admin"
    #         return user
    return None


# Create access JWT
def create_jwt_token(user: JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {
        "sub": user.username,
        "role": user.role,
        "exp": expiration
    }
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return jwt_token


# Create whether JWT token is correct
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            is_valid = await db_check_jwt_username(username)
            # if fake_jwt_user_1.username == username:
            if is_valid:
                return final_checks(role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
