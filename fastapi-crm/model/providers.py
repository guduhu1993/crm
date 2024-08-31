from pydantic import BaseModel


class ProvidersInDB(BaseModel):
    id: int
    provider_name: str
    phone: str
    email: str
    wechat_number: str
    gender: str
    id_card: str
    bank_card: str
    social_security: str
    # source_type: str
    source_id: int
    remark: str | None = None


class ShowProvider(BaseModel):
    id: int
    provider_name: str
    phone: str
    email: str
    wechat_number: str
    gender: str
    id_card: str
    source_id: int
    remark: str | None = None


class AddProvider(BaseModel):
    provider_name: str
    phone: str
    email: str
    wechat_number: str
    gender: str
    id_card: str
    bank_card: str
    social_security: str
    # source_type: str
    # source_id: int
    remark: str | None = None
