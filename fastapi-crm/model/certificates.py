from pydantic import BaseModel


class CertificateInDB(BaseModel):
    id: int
    certificate_number: str
    certificate_name: str
    belong_type: bool
    belong_to: int
    validity_begin: str
    validity_end: str
    validity_user: str
    is_using: bool
    remark: str | None = None


class AddCertificate(BaseModel):
    certificate_number: str
    certificate_name: str
    belong_type: bool
    belong_to: int
    validity_begin: str
    validity_end: str
    validity_user: str
    is_using: bool
    remark: str | None = None
