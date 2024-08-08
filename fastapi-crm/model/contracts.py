from pydantic import BaseModel


class ContractInDB(BaseModel):
    id: int
    contract_number: str  # 合同编号
    party_a: int
    party_b: int
    date_begin: str
    date_end: str
    amount: str  # 合同约定金额
    paid_period: int  # 支付周期
    fee: float
    source: int  # 业务员
    activated: bool #已经过管理员确认
    remark: str
