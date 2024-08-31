from pydantic import BaseModel


class PayOutInDB(BaseModel):
    id: int
    ticket_number: str  # 打款单号
    fee: float  # 打款金额
    progress: str
    contract_id: str  # 合同id
    contact: str
    payment: str  # 打款方式
    credential: str  # 打款凭证url
    arrival_date: str  # 到账日期
    activated: bool  # 已经过管理员确认,确认后只有管理员可修改
    remark: str
    applicant: str  # 提交申请人
    Beneficiary: str  # 收款方


class AddPayOut(BaseModel):
    ticket_number: str  # 打款单号
    fee: float  # 打款金额
    progress: str
    contract_id: str  # 合同id
    contact: str
    payment: str  # 打款方式
    credential: str  # 打款凭证url
    arrival_date: str  # 到账日期
    activated: bool  # 已经过管理员确认,确认后只有管理员可修改
    remark: str
    applicant: str  # 提交申请人
    Beneficiary: str  # 收款方
