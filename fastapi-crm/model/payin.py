from pydantic import BaseModel


class PayInInDB(BaseModel):
    id: int
    ticket_number: str  # 打款单号
    payer: str
    fee: float  # 打款金额
    progress: str
    contract_id: int  # 合同id
    payment: str  # 打款方式
    credential: str  # 打款凭证url
    arrival_date: str  # 到账日期
    activated: bool  # 已经过管理员确认,确认后只有管理员可修改
    remark: str


class AddPayIn(BaseModel):
    ticket_number: str  # 打款单号
    payer: str
    fee: float  # 打款金额
    progress: str
    contract_id: int  # 合同id
    payment: str  # 打款方式
    credential: str  # 打款凭证url
    arrival_date: str  # 到账日期
    activated: bool  # 已经过管理员确认,确认后只有管理员可修改
    remark: str
