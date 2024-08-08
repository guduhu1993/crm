from pydantic import BaseModel


class CertificateInDB(BaseModel):
    id:int
    certificate_number: str
    certificate_name: str
    certificate_belong_type: bool
    belong_to: int
    validity_begin: str
    validity_end: str
    validity_user: int
    is_using: bool
    remark: str| None = None


