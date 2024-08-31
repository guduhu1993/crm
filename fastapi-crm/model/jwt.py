from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    expires: str


class TokenData(BaseModel):
    username: str | None = None
