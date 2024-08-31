from datetime import datetime

from pydantic import BaseModel


class UserInDB(BaseModel):
    username: str
    phone: str
    password: str
    is_active: bool = False


class UserInfo(BaseModel):
    avatar: str  # "https://avatars.githubusercontent.com/u/44761321",
    username: str  # "admin",
    nickname: str  # "小铭",
    phone: str
    is_active: bool
    role: list  # a admin; c common,
    access_token: str  # "eyJhbGciOiJIUzUxMiJ9.admin",
    expires: str  # "2030/10/30 00:00:00"



class UserInformation(BaseModel):
    avatar: str  # "https://avatars.githubusercontent.com/u/44761321",
    nickname: str  # "小铭",
    phone: str

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
    new: str
    new1: str
    old: str

