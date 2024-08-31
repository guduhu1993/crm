from pydantic import BaseModel

from model.user import UserInfo


class ResponseSuccess(BaseModel):
    success: bool
    data: UserInfo

class ResponseToken(BaseModel):
    access_token: str
    refresh_token:str
    expires: str

class ResponseTokenSuccess(BaseModel):
    success: bool
    data: ResponseToken