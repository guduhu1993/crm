from pydantic import BaseModel


class UserInDB(BaseModel):
    username: str
    phone: str
    password: str
    is_active: bool = False


class UserCreate(BaseModel):
    username: str
    phone: str
    password: str


class Username(BaseModel):
    username: str


class User(BaseModel):
    username: str
    phone: str
    is_active: bool


class UserLogin(BaseModel):
    username: str
    password: str


class UserPassword(BaseModel):
    password: str
