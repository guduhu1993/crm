from pydantic import BaseModel


class ProvidersInDB(BaseModel):
    id:int
    provider_name: str
    phone: str
    email: str
    wechat_id: str
    gender: bool
    id_card: str
    bank_card: str
    social_security: str
    source: int
    remark: str | None = None


class ShowProvider(BaseModel):
    id: int
    provider_name: str
    phone: str
    email: str
    wechat_id: str
    gender: bool
    id_card: str
    remark: str | None = None
