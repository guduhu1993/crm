from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordRequestForm
from auth.token_auth import make_token_for_login, get_current_active_user
from model.businesses import ShowBusiness, BusinessInDB
from model.certificates import CertificateInDB
from model.contracts import ContractInDB
from model.payin import PayInInDB
from model.payout import PayOutInDB
from model.user import User
from model.providers import ProvidersInDB, ShowProvider
from sql_app.database import get_db
from crud import (
    add_provider_info,
    username_is_exist,
    create_user,
    get_user,
    modify_user_activation,
    get_providers_info,
    modify_provider_info,
    delete_provider_info,
    get_businesses_info,
    modify_business_info,
    delete_business_info, add_business_info, add_certificate_info, get_certificates_info, modify_certificate_info,
    delete_certificate_info, add_contract_info, get_contract_info, modify_contract_info, delete_contract_info,
    get_payins_info, modify_payin_info, delete_payin_info, add_payin_info, modify_payout_info, delete_payout_info,
    add_payout_info, get_payouts_info,
)
from common import utils
from model.jwt import Token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register/", response_model=User)
def register_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        phone: str,
        db: Session = Depends(get_db),
):
    print(form_data)
    if username_is_exist(form_data.username, db):  # 用户名是否已存在
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        db_user = User(username=form_data.username, phone=phone, is_active=False)
        create_user(db_user, form_data.password, db)
    return db_user


# 登陆成功后签发token
@app.post("/token", response_model=Token)
async def login_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
) -> Token:
    print(form_data.username)
    db_user = get_user(form_data.username, db)
    if not db_user or not utils.check_password(db_user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    login_token = make_token_for_login(form_data)
    return login_token


@app.get("/user_info", response_model=User)
def user_info(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    db_user = get_user(current_user.username, db)
    return db_user


# 管理员激活/注销用户账号
@app.post("/activate_username", response_model=str)
def activate_username(
        username: str, activate_sign: bool, db: Session = Depends(get_db)
):
    activate_user = modify_user_activation(username, activate_sign, db)
    return activate_user


#######################################################################################################
# 人才客户
# 展示人才列表信息
@app.get("/providers", response_model=list[ShowProvider])
def providers(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    providers_list = get_providers_info(current_user.id, db)
    return providers_list


# 添加人才信息
@app.post("/provider", response_model=ShowProvider)
def add_provider(
        form_data: ProvidersInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    provider = add_provider_info(form_data, current_user.id, db)
    return provider


@app.post("/modify_provider", response_model=ProvidersInDB)
def modify_provider(
        form_data: ProvidersInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    provider = modify_provider_info(form_data, current_user.id, db)
    return provider


@app.get("/delete_provider", response_model=int)
def delete_provider(provider_id: int, current_user: Annotated[User, Depends(get_current_active_user)],
                    db: Session = Depends(get_db)):
    provider_id = delete_provider_info(provider_id, current_user.id, db)
    return provider_id


###########################################################################################
# 企业客户
# 展示企业列表信息
@app.get("/businesses", response_model=list[ShowBusiness])
def businesses(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    businesses_list = get_businesses_info(current_user.id, db)
    return businesses_list


@app.post("/business", response_model=ShowBusiness)
def add_business(
        form_data: BusinessInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    business = add_business_info(form_data, current_user.id, db)
    return business


@app.post("/modify_business", response_model=BusinessInDB)
def modify_business(
        form_data: BusinessInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    business = modify_business_info(form_data, current_user.id, db)
    return business


@app.get("/delete_business", response_model=int)
def delete_business(business_id: int, current_user: Annotated[User, Depends(get_current_active_user)],
                    db: Session = Depends(get_db)):
    business_name = delete_business_info(business_id, current_user.id, db)
    return business_name


#########################################################################################
# 证书信息
@app.get("/certificates", response_model=list[CertificateInDB])
def certificates(
        certificate_belong_to: int,
        certificate_belong_type: bool,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    certificates_list = get_certificates_info(certificate_belong_to, certificate_belong_type, db)
    return certificates_list


@app.post("/certificate", response_model=CertificateInDB)
def add_certificate(
        form_data: CertificateInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    certificate = add_certificate_info(form_data, db)
    return certificate


@app.post("/modify_certificate", response_model=CertificateInDB)
def modify_certificate(
        form_data: CertificateInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    certificate = modify_certificate_info(form_data, db)
    return certificate


@app.get("/delete_certificate", response_model=int)
def delete_certificate(certificate_id: int, current_user: Annotated[User, Depends(get_current_active_user)],
                       db: Session = Depends(get_db)):
    certificate_id = delete_certificate_info(certificate_id, db)
    return certificate_id


#########################################################################################
# 合同
@app.post("/contract", response_model=ContractInDB)
def add_contract(
        form_data: ContractInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    contract = add_contract_info(form_data, current_user.id, db)
    return contract


@app.get("/contracts", response_model=list[ContractInDB])
def providers(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    contracts_list = get_contract_info(current_user.id, db)
    return contracts_list


@app.post("/modify_contract", response_model=ContractInDB)
def modify_contract(
        form_data: ContractInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    contract = modify_contract_info(form_data, current_user.id, db)
    return contract


@app.get("/delete_contract", response_model=int)
def delete_contract(contract_id: int, current_user: Annotated[User, Depends(get_current_active_user)],
                    db: Session = Depends(get_db)):
    contract_id = delete_contract_info(contract_id, current_user.id, db)
    return contract_id


###########################################################################################################
# 入款
@app.get("/payins/{contract_id}", response_model=list[PayInInDB])
def payins(
        contract_id: str,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    payins_list = get_payins_info(contract_id, db)
    return payins_list


# 添加人才信息
@app.post("/payin", response_model=PayInInDB)
def add_payin(
        form_data: PayInInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    payin = add_payin_info(form_data, db)
    return payin


@app.post("/modify_payin", response_model=PayInInDB)
def modify_payin(
        form_data: PayInInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    payin = modify_payin_info(form_data, db)
    return payin


@app.get("/delete_payin", response_model=int)
def delete_payin(payin_id: int, current_user: Annotated[User, Depends(get_current_active_user)],
                 db: Session = Depends(get_db)):
    payin_id = delete_payin_info(payin_id, db)
    return payin_id


###########################################################################################################
# 出款
@app.get("/payouts/{contract_id}", response_model=list[PayOutInDB])
def payouts(
        payout_id: str,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    payouts_list = get_payouts_info(payout_id, db)
    return payouts_list


# 添加人才信息
@app.post("/payout", response_model=PayOutInDB)
def add_payout(
        form_data: PayOutInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    payout = add_payout_info(form_data, db)
    return payout


@app.post("/modify_payout", response_model=PayOutInDB)
def modify_payout(
        form_data: PayOutInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    payout = modify_payout_info(form_data, db)
    return payout


@app.get("/delete_payout", response_model=int)
def delete_payout(payout_id: int, current_user: Annotated[User, Depends(get_current_active_user)],
                  db: Session = Depends(get_db)):
    payout_id = delete_payout_info(payout_id, db)
    return payout_id


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
