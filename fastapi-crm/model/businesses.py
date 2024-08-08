from pydantic import BaseModel


class BusinessInDB(BaseModel):
    id:int
    business_name: str
    tax_number: str
    wechat_id: str
    phone: str
    bank_card: int
    social_security: str
    source: int
    contact: str
    business_license: str
    remark: str| None = None


class ShowBusiness(BaseModel):
    id: int
    business_name: str
    tax_number: str
    wechat_id: str
    phone: str
    source: int
    contact: str
    remark: str| None = None
