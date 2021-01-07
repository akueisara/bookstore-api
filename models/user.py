import enum

from fastapi import Query
from pydantic import BaseModel


class Role(enum.Enum):
    admin: str = "admin"
    personel: str = "personel"


class User(BaseModel):
    name: str
    password: str
    mail: str = Query(None, regex=r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
    role: Role
