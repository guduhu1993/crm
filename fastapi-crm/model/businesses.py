from pydantic import BaseModel


class BusinessInDB(BaseModel):
    id: int
    business_name: str
    tax_number: str
    wechat_id: str
    phone: str
    bank_card: str
    social_security: str
    source_type: str
    source_id: int
    contact: str
    business_license: str
    remark: str | None = None


class ShowBusiness(BaseModel):
    id: int
    business_name: str
    tax_number: str
    wechat_number: str
    phone: str
    source_id: int
    contact: str
    remark: str | None = None


class AddBusiness(BaseModel):
    business_name: str
    tax_number: str
    wechat_number: str
    phone: str
    bank_card: str
    social_security: str
    source_id: int
    contact: str
    business_license: str
    remark: str | None = None
