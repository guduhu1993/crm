from datetime import datetime, timezone

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, ARRAY
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./crm.db"

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    "postgresql://postgres:123456@localhost:5432/crm"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 创建数据库模型
class dbUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    nickname = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    wechat_number = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    role = Column(Integer, default=2)  # 1: admin \ 2 user
    access_token = Column(String, unique=True, index=True)
    expires = Column(String, default=datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"))
    avatar = Column(String)


class dbRoles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)
    role_label = Column(String, unique=True, index=True)
    status = Column(Boolean, default=True)
    privileges = Column(ARRAY(Integer), default=[1, 2])


class dbProvider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True, index=True)
    provider_name = Column(String, nullable=False, index=True)
    gender = Column(String, default="男", nullable=False)
    id_card = Column(String, index=True)
    phone = Column(String, index=True, nullable=False)
    email = Column(String, index=True)
    wechat_number = Column(String, index=True)
    bank_card = Column(String, index=True)
    social_security = Column(String, index=True)
    # source_type = Column(String)
    source_id = Column(Integer, index=True, nullable=False)
    remark = Column(String)


class dbBusiness(Base):
    __tablename__ = "business"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, nullable=False, index=True)
    tax_number = Column(String, nullable=False, index=True)
    # source_type = Column(String)
    source_id = Column(Integer, index=True, nullable=False)
    contact = Column(String, index=True)
    phone = Column(String, index=True, nullable=False)
    wechat_number = Column(String, index=True)
    bank_card = Column(String, index=True)
    business_license = Column(String, nullable=False)
    social_security = Column(String, nullable=False)
    remark = Column(String)


class dbCertificate(Base):
    __tablename__ = "certificate"

    id = Column(Integer, primary_key=True, index=True)
    certificate_number = Column(String, unique=True, nullable=False, index=True)
    certificate_name = Column(String, nullable=False, index=True)
    belong_type = Column(Boolean, index=True)
    belong_to = Column(Integer, index=True)
    validity_begin = Column(String, index=True)
    validity_end = Column(String, index=True)
    validity_user = Column(String, index=True)  # 用证单位
    is_using = Column(Boolean)
    remark = Column(String)


class dbContract(Base):
    __tablename__ = "contract"

    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String, unique=True, index=True)  # 合同编号
    party_a = Column(String, nullable=False, index=True)
    party_b = Column(String, nullable=False, index=True)
    date_begin = Column(String, index=True)
    date_end = Column(String, index=True)
    amount = Column(String)  # 合同约定金额
    paid_period = Column(String)  # 支付周期
    fee = Column(Float)
    # source_type = Column(String)
    source_id = Column(Integer, index=True)  # 业务员
    activated = Column(Boolean, default=False, index=True)  # 已经过管理员确认
    remark = Column(String)


class dbPayIn(Base):
    __tablename__ = "pay_in"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, unique=True, index=True)  # 打款单号
    payer = Column(String, nullable=False, index=True)
    fee = Column(Float)  # 打款金额
    progress = Column(String, index=True)
    contract_id = Column(String, index=True)  # 合同id
    payment = Column(String)  # 打款方式
    credential = Column(String)  # 打款凭证url
    arrival_date = Column(String)  # 到账日期
    activated = Column(Boolean, default=False, index=True)  # 已经过管理员确认,确认后只有管理员可修改
    remark = Column(String)


class dbPayOut(Base):
    __tablename__ = "pay_out"

    id = Column(Integer, primary_key=True, index=True)
    ticket_number = Column(String, unique=True, nullable=False, index=True)  # 打款单号
    applicant = Column(String, index=True)  # 申请人
    fee = Column(Float)  # 打款金额
    progress = Column(String, index=True)
    contact = Column(String, index=True)  # 联系人
    contract_id = Column(String, index=True)  # 合同id
    payment = Column(String)  # 打款方式
    credential = Column(String)  # 打款凭证url
    Beneficiary = Column(String)  # 收款方
    arrival_date = Column(String)  # 到账日期
    activated = Column(Boolean, default=False, index=True)  # 已经过管理员确认
    remark = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
