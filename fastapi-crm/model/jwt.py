from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    exp: str
    user: dict


class TokenData(BaseModel):
    username: str | None = None