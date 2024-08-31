from typing import Optional

from fastapi import HTTPException
from pymysql import NULL
from sqlalchemy.orm import Session

from model.businesses import BusinessInDB, AddBusiness
from model.certificates import CertificateInDB, AddCertificate
from model.contracts import ContractInDB, AddContract
from model.payin import PayInInDB, AddPayIn
from model.payout import PayOutInDB, AddPayOut
from model.providers import ProvidersInDB, AddProvider
from model.roles import RolesInDB, AddRole
from model.user import User, UserInfo, UserInformation, UserPassword, Username
from common import utils
from sql_app.database import dbUser, dbProvider, dbBusiness, dbCertificate, dbContract, dbPayIn, dbPayOut, dbRoles


def add_user_info(form_data: UserInformation, current_user_id, db):
    db_user = db.query(dbUser).filter(dbUser.id == current_user_id).first()
    update_data = form_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(username: str, db):
    return db.query(dbUser).filter(dbUser.username == username).first()


def username_is_exist(username: str, db):
    if db.query(dbUser).filter(dbUser.username == username).first():
        return True
    else:
        return False


def create_user(user: User, password: str, db):
    hashed_password = utils.hash_password(password)  # hash密码
    db_user = dbUser(**user.dict(), password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def modify_user_activation(username: str, activate_sign: bool, db):
    db_user = db.query(dbUser).filter(dbUser.username == username).first()
    if db_user:
        db_user.is_active = activate_sign
        db.commit()
        db.refresh(db_user)
    else:
        print("User not found.")
    return username


def change_password_info(password: str, username: str, db):
    db_user = db.query(dbUser).filter(dbUser.username == username).first()
    if db_user:
        db_user.password = utils.hash_password(password)  # hash密码password
        db.commit()
        db.refresh(db_user)
    else:
        print("User not found.")
    return username


def upload_image_info(user_id: int, image_md5: str, db):
    db_user = db.query(dbUser).filter(dbUser.id == user_id).first()
    if db_user:
        db_user.avatar = image_md5  # hash密码password
        db.commit()
        db.refresh(db_user)
    else:
        print("User not found.")
    return user_id


#####################################################################################################
def get_roles_info(db):
    return db.query(dbRoles).filter(dbRoles.id > 0).all()


def add_role_info(form_data: AddRole, db):
    db_role = dbRoles(**form_data.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def modify_role_info(form_data: RolesInDB, db):
    db_role = db.query(dbRoles).filter(dbRoles.id == form_data.id).first()
    if db_role:
        if form_data != db_role:
            update_data = form_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_role, key, value)
            db.commit()
            db.refresh(db_role)
            return db_role.id
        else:
            print("provider没有变化")
    else:
        print("provider没查到")
    return db_role.id


def delete_role_info(role_id: str, db):
    if role_id != NULL:
        db_role = db.query(dbRoles).filter(dbRoles.id == role_id).first()
        if db_role:
            db.delete(db_role)
            db.commit()
    else:
        print("role_id为空")
    return role_id


#######################################################################################################
# 人才客户
def get_providers_info(current_user_id: int, db):
    return db.query(dbProvider).filter(dbProvider.source_id == current_user_id).all()


def add_provider_info(form_data: AddProvider, current_user_id: int, db):
    # form_data.source_id = current_user_id
    db_provider = dbProvider(**form_data.dict(), source_id=current_user_id)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


def modify_provider_info(form_data: ProvidersInDB, current_user_id: int, db):
    db_provider = db.query(dbProvider).filter(dbProvider.id == form_data.id).first()
    print('current_user_id', current_user_id)
    print('db_provider.source_id', db_provider.id)
    if current_user_id != db_provider.source_id:
        print("无权修改其他来源的信息")
        raise HTTPException(status_code=404, detail="Item not found")

    if db_provider:
        if form_data != db_provider:
            form_data.source_id = current_user_id
            update_data = form_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_provider, key, value)
            db.commit()
            db.refresh(db_provider)
            return db_provider
        else:
            print("provider没有变化")
    else:
        print("provider没查到")
    return db_provider


def delete_provider_info(provider_id: str, current_user_id: int, db):
    if provider_id != NULL:
        db_provider = db.query(dbProvider).filter(dbProvider.id == provider_id).first()
        if db_provider:
            if current_user_id != db_provider.source_id:
                print("无权修改其他来源的信息")
                raise HTTPException(status_code=401, detail="Item not found")
        db.delete(db_provider)
        db.commit()
    else:
        print("provider_name为空")
    return provider_id


#######################################################################################################
# 企业客户
def get_businesses_info(current_user_id: int, db):
    return db.query(dbBusiness).filter(dbBusiness.source_id == current_user_id).all()


def add_business_info(form_data: AddBusiness, current_user_id: int, db):
    form_data.source_id = current_user_id
    db_business = dbBusiness(**form_data.dict())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business


def modify_business_info(form_data: BusinessInDB, current_user_id: int, db):
    db_business = db.query(dbBusiness).filter(dbBusiness.id == form_data.id).first()
    print(current_user_id)
    print(db_business.source_id)
    if current_user_id != db_business.source_id:
        print("无权修改其他来源的信息")
        raise HTTPException(status_code=401, detail="Item not found")

    if db_business:
        if form_data != db_business:
            form_data.source_id = current_user_id
            update_data = form_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_business, key, value)
            db.commit()
            db.refresh(db_business)
            return db_business
        else:
            print("business没有变化")
    else:
        print("business没查到")
    return db_business


def delete_business_info(business_id: str, current_user_id: int, db):
    print(business_id)
    if business_id != NULL:
        db_business = db.query(dbBusiness).filter(dbBusiness.id == business_id).first()
        if db_business:
            if current_user_id != db_business.source_id:
                print("无权修改其他来源的信息")
                raise HTTPException(status_code=401, detail="Item not found")
            db.delete(db_business)
            db.commit()
        else:
            print("business_id未找到")
    else:
        print("provider_name为空")
    return business_id


#######################################################################################################
# 证书
def add_certificate_info(form_data: AddCertificate, db):
    if form_data.certificate_belong_type:  # 人才证
        if not db.query(dbProvider).filter(dbProvider.id == form_data.belong_to).first():
            print('未找到所属人才')
            raise HTTPException(status_code=402, detail="Item not found")
    else:  # 企业证
        if not db.query(dbBusiness).filter(dbBusiness.id == form_data.belong_to).first():
            print('未找到所属企业')
            raise HTTPException(status_code=402, detail="Item not found")
    db_certificate = dbCertificate(**form_data.dict())
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate


def get_certificates_info(certificate_belong_to: str, certificate_belong_type: bool, db):
    return db.query(dbCertificate).filter(dbCertificate.certificate_belong_type == certificate_belong_type,
                                          dbCertificate.belong_to == certificate_belong_to).all()


def modify_certificate_info(form_data: CertificateInDB, db):
    if form_data.certificate_belong_type:  # 人才证
        if not db.query(dbProvider).filter(dbProvider.id == form_data.belong_to).first():
            print('未找到所属人才')
            raise HTTPException(status_code=402, detail="Item not found")
    else:  # 企业证
        if not db.query(dbBusiness).filter(dbBusiness.id == form_data.belong_to).first():
            print('未找到所属企业')
            raise HTTPException(status_code=402, detail="Item not found")
    db_certificate = db.query(dbCertificate).filter(dbCertificate.id == form_data.id).first()
    update_data = form_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_certificate, key, value)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate


def delete_certificate_info(certificate_id: str, db):
    if certificate_id != NULL:
        db_certificate = db.query(dbCertificate).filter(dbCertificate.id == certificate_id).first()
        if db_certificate:
            db.delete(db_certificate)
            db.commit()
        else:
            print("business_id未找到")
    else:
        print("provider_name为空")
    return certificate_id


#######################################################################################################
# 合同
def add_contract_info(form_data: AddContract, current_user_id, db):
    form_data.source_id = current_user_id
    db_contract = dbContract(**form_data.dict())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract


def get_contract_info(current_user_id: int, db):
    return db.query(dbContract).filter(dbContract.source_id == current_user_id).all()


def modify_contract_info(form_data: ContractInDB, current_user_id: int, db):
    db_contract = db.query(dbContract).filter(dbContract.id == form_data.id).first()
    if current_user_id != db_contract.source_id:
        print("无权修改其他来源的信息")
        raise HTTPException(status_code=401, detail="Item not found")

    if db_contract:
        if form_data != db_contract:
            form_data.source_id = current_user_id
            update_data = form_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_contract, key, value)
            db.commit()
            db.refresh(db_contract)
            return db_contract
        else:
            print("db_contract没有变化")
    else:
        print("db_contract没查到")
    return db_contract


def delete_contract_info(contract_id: str, current_user_id: int, db):
    if contract_id != NULL:
        db_contract = db.query(dbContract).filter(dbContract.id == contract_id).first()
        if db_contract:
            if current_user_id != db_contract.source_id:
                print("无权修改其他来源的信息")
                raise HTTPException(status_code=401, detail="Item not found")
        db.delete(db_contract)
        db.commit()
    else:
        print("provider_name为空")
    return contract_id


#######################################################################################################
# 入款
def get_payins_info(contract_id: str, db):
    if contract_id == 'all':
        return db.query(dbPayIn).filter(dbPayIn.id >= 0).all()
    elif contract_id.isdigit():
        print(contract_id)
        print(type(contract_id))
        return db.query(dbPayIn).filter(dbPayIn.contract_id == contract_id).all()
    else:
        raise HTTPException(status_code=401, detail="Item not found")


def add_payin_info(form_data: AddPayIn, db):
    db_payin = dbPayIn(**form_data.dict())
    db.add(db_payin)
    db.commit()
    db.refresh(db_payin)
    return db_payin


def modify_payin_info(form_data: PayInInDB, db):
    db_payin = db.query(dbPayIn).filter(dbPayIn.id == form_data.id).first()
    if db_payin:
        if form_data != db_payin:
            update_data = form_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_payin, key, value)
            db.commit()
            db.refresh(db_payin)
            return db_payin
        else:
            print("db_payin没有变化")
    else:
        print("db_payin没查到")
    return db_payin


def delete_payin_info(payin_id: str, db):
    if payin_id != NULL:
        db_payin = db.query(dbPayIn).filter(dbPayIn.id == payin_id).first()
        if db_payin:
            db.delete(db_payin)
            db.commit()
    else:
        print("provider_name为空")
    return payin_id


#######################################################################################################
# 出款
def get_payouts_info(contract_id: str, db):
    if contract_id == 'all':
        return db.query(dbPayOut).filter(dbPayOut.id >= 0).all()
    elif contract_id.isdigit():
        print(contract_id)
        print(type(contract_id))
        return db.query(dbPayOut).filter(dbPayOut.contract_id == contract_id).all()
    else:
        raise HTTPException(status_code=401, detail="Item not found")


def add_payout_info(form_data: AddPayOut, db):
    db_payout = dbPayOut(**form_data.dict())
    db.add(db_payout)
    db.commit()
    db.refresh(db_payout)
    return db_payout


def modify_payout_info(form_data: PayOutInDB, db):
    db_payout = db.query(dbPayOut).filter(dbPayOut.id == form_data.id).first()
    if db_payout:
        if form_data != db_payout:
            update_data = form_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_payout, key, value)
            db.commit()
            db.refresh(db_payout)
            return db_payout
        else:
            print("db_payout没有变化")
    else:
        print("db_payout没查到")
    return db_payout


def delete_payout_info(payout_id: str, db):
    if payout_id != NULL:
        db_payout = db.query(dbPayOut).filter(dbPayOut.id == payout_id).first()
        if db_payout:
            db.delete(db_payout)
            db.commit()
    else:
        print("db_payout为空")
    return payout_id

#######################################################################################################
