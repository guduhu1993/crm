from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy import String
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, Optional
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer, OAuth2
from auth.token_auth import make_token_for_login, get_current_active_user, record_token, refresh_token_info
from model.businesses import ShowBusiness, BusinessInDB, AddBusiness
from model.certificates import CertificateInDB, AddCertificate
from model.contracts import ContractInDB, AddContract
from model.payin import PayInInDB, AddPayIn
from model.payout import PayOutInDB, AddPayOut
from model.response import ResponseSuccess
from model.roles import RolesInDB, AddRole
from model.user import User, UserInfo, UserInformation, UserPassword, Username
from model.providers import ProvidersInDB, ShowProvider, AddProvider
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
    add_payout_info, get_payouts_info, add_user_info, change_password_info, upload_image_info, get_roles_info,
    add_role_info, modify_role_info, delete_role_info,
)
from common import utils
from model.jwt import Token
from fastapi import Request
import base64

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
    if username_is_exist(form_data.username, db):  # 用户名是否已存在
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        db_user = User(username=form_data.username, phone=phone, is_active=False)
        create_user(db_user, form_data.password, db)
    return db_user


# 登陆成功后签发token
@app.post("/token", response_model=UserInfo)
async def login_user(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
) -> UserInfo:
    print(form_data.username)
    db_user = get_user(form_data.username, db)
    if not db_user or not utils.check_password(db_user.password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    login_token = make_token_for_login(form_data)
    record_token(login_token, db_user.id, db)

    user_info_data = UserInfo(
        **login_token.dict(),
        avatar=db_user.avatar if db_user.avatar else "",
        username=db_user.username,
        nickname=db_user.nickname if db_user.nickname else '',
        role=[db_user.role, ] if db_user.role else [],
        phone=db_user.phone if db_user else '',
        is_active=db_user.is_active
    )
    # response_data = ResponseSuccess(success=True, data=user_info_data)
    return user_info_data


@app.post("/refresh_token", response_model=Token)
async def refresh_token(
        refreshToken: Annotated[Token, Depends()],
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
) -> Token:
    response_refresh_token = refresh_token_info(refreshToken, current_user, db)
    return response_refresh_token


@app.get("/user_info", response_model=User)
def user_info(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    db_user = get_user(current_user.username, db)
    return db_user


# data:image/png;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCABRAE8DASIAAhEBAxEB/8QAHQABAAICAwEBAAAAAAAAAAAAAAYIBQoDBwkLBP/EACkQAAEEAgEEAgMAAgMAAAAAAAMBAgQFAAYHCBESEwkUFRYhI0EKJDL/xAAbAQABBQEBAAAAAAAAAAAAAAAAAgMEBggJB//EACoRAAICAQQBAwMEAwAAAAAAAAIDAQQFAAYREgcTIUEIFCIJFTEyJEJR/9oADAMBAAIRAxEAPwDUnxjGekap mMlLNG3YlF 0j07aSayrXOTY2a/bPovFjnMe78u2Itf4se1zHL9js1zXNXsqKmRbHWocmFy5LVQ0IYqWrNcMWX9WL7RHcC DHkZ J0s1sX19RZh3GDDuBD3Cf4Me0R2Gfgo5ifidMZJda0zcN0knh6dqmy7ZLiiWRJi61RWl7JjgawhHGOCriyihEgwlepCNaxGCI5XeLHKmClw5dfJPCnxZEKZGI4MmJLAWNJjlYvZ4jgM1hREav8AHMIxrmr/ABUTI0NUTDSLFy0BEjVBjLAEv6kYRPYRL/WZiIn4506dO2usm4yrYCnYNi0WjQ0az2K49VaXkMKaa Y9QAIiDmO0RzGvz4zL0Gv3213Ndrur0lvsmwW8lsOpoqCtm3FzaS3oqsi11ZXBkzZsl6NcrQRgFK5GqqNVEXM1u/HfIHGdx vcj6LuPH9/6WSfwe76zd6pcfXJ/wCD/jL6DAm l/ZfAvo8Hf6cuNlbqDaCkVquNxiieuoTlxaYgC6m4K8l6pqEvxJghICXtMxPtpMV7BIK0KHTWBgqOxCjlANKOwrJsD6YsKPcQkoKY94jjUOxjGSNM6ZJ9IHRm3TUA7O9g9bLtFAPYSEd4DHRvtYjbZ73908WMgLIc53dPFqKvf8AmRjGOoZCXJdKwbCmrZKmRytkAcFK2R8gfHUo RmY0tZ mxbOon0MT6HHIn1KC6lHyJccFHzEzGtl6MKEyEAEMcVlcyKIUUMZgmwmwmiawIwDEiAbFQCNaJg0QSC8UYnh2TNejmButM5T5AZp7YrdZbtl02obB8PoJGbNKipX pVF O9yF h6V9KQ/Sguw/FM5aXf XLWHWcc0G471Ng25o2u1OpVt7cEBPfZlZAiUUOuDJ7FDNMdkQVYNixzON6kAvsVF9U4nwbdWUnjn9uNsfF0PcX17bEPGR7m3dcdlRCLVSb4VM/XQXnr7o2OybIqverQlugoryj9g3vvJ3keljqmI27YTOKI7NpxGpxAbVQuK1cgEOEz1I5ieGPlaphIelPMDzP9Q3jDaadtVt87jw2zDylpq8b 83Bh9xoilT4rglRsTj6xOV93fsCmmkjr/ctRyPa93x5xNFF0rcczNKhQY0icCxXcjgYD8jM3CJZzItqS4MNjTFO1GA/HMkq54KV9aISqD1udT/5SOmWNNqY3UZptUMVlVvi1HJoIIH dhWGcyLS7UcYWKxx6w6iqLSU/sQsKTWEK701pHJXX46OebHgrma54O5BSTSUO93j9flQbXxhv1Tk6rO pjNmjkNa KSyMB s2QnOY5s9lQ4viyGTNg3YKCn2qiuNa2CBHtaK/rZtPb1spiEjzq6wjkiy4xm/7YUBXsVUVHNVUcxzXIipzk3CzLeOfJTstJvfXuW25CCMi/wA/GXnFNukclMxLKxd0BB8 m1Fex1GJXGu1XjJOyvqk lTH7OSrG0b FwlLbvFdapDb 6sDRVGFz9QUjExTyqvQyDDr8RZp5DJ431mHFgtUE/49Vdxeax6ibKQyuLzLBBpoaxZiR1s4nHMtbZLM2vtI77CxpGxDgA2k0ZisA5uqikkH92Ow13vnOh8Zn6J5UvcXVw96g8haa7iN5frNti7BIsxg2mLCc/8A7jq4miLsMq0CBVjPkwqg0tqljwnM1aubePeQ j7n 5o9W2fadTtKGZ a4/3jW7ix1y kazZOK os4FxTTI06JLGNpa2xWNJGrLGDNGn NGK7qvk3mXlvmi1iXfLnJe9clWtfHfErZu77Rc7KWsikUali1iW0yUytjGeIZTggsAI5m 8rHmVXqrIeAbW6fN2E83Y/fExgys4POhjYrvLIQOMo1ELxdWzD4QOMyA15i4JgpqU2rdWUOMidPPSz5JfsbYG4vC e2cVbcmLZnNu32scoay7Lb9mX3Xp9KWMuUzPmm1ZsTYlFW0t4K6hrrXGMZrTWbNMYxho1P J99l8Vcp8acoQIgp87jff9N32HBkK5ATZen7FW7DHiGVqtcgpJq5gSK1zXIx7uyov9z6Dmh7vrXJelaryDp1iG21bc6Gr2ShsAPERsittogpkZSekhWDkCYX0y4/sc LKGaMXsUT2p86TNkn4Pur9SMuekTerbu4TbHb GjzjqquF3fN3DSIvkPsnrVT7bVBUv9a7ZUTsjIwsvuw8uFO zHOmBVkJD0SniIG0uCgAmf PGZCP5mWQoYj8p1zq/UR8L3N7 PcZ5NwSjflvGo3ZzNRYkZ29pZJlcrtsBjtMngbSF3mREAI42xlbDTn7ZQz1h82HSEXQt7qerPj6vLF1/fJ8Wo5MbX bEpOQQC70u0tSOJn04 0woqR5cn2p47HWpIeRZd6NuWh6HupGL1D8O1si2sAF5H0wcbXt7hqXvMknALwrNnUTuz3R9jiC wUzUULbcNpFYqJHai 0vMHFepc3cY7vxPvML72rb3QTKG0E1ex4/vahIVlDeioorGosBRLWtOi/4J8OMX  HZdEblTR YOjvnLe Nv2XZ9K3XS7OVTfsOqW9zq8m8oZTWSqm5r5lbKiTHU xVBodnHEp3t9UhAm7mERraH518X19zIS9BhTaywT6lyVSwK1woiLdZojIl9vfWMO/Eu0PT3iJFXQ9Hfo6/Xnk9kUL2yNwQ7PWtq4hGMv4YrsIt7g2SlnTb VptaLAnK7OuN/ZmSxcqLEXaSCZD7rLNf0  XyTpa1PD8NyxF5DZY30kKDRv3x6WSMMUlZatErvqFvBRPxyGOxqGBaLFERVlvF4dZmr/ZNi2uyNdbTfXWy3EhrWntr 0nXFkdrFcrGmnWJ5MojWq5ytR5XI1XO7du65hcq z9vFtbb9HCnbK8dX1yN8jIBJPex5AlZEcgpcs6jElMlMScwMl1jb/m7yYry95K3Bv1GFXgEZf9vUjHC0LDxTjsdVxy33bIKSFi5YGtDWmKhFYkCBlgphpsYy/wB8afRPsPXn1Q0HC9cOZE1eNre2bZv2zgC0sbV6Koo5gqmXKUisGrrTcJeuUccCO9xHWLzjY4UWQ8dxpV1WrddD7SqNdjB 6vPEyTRqj dq64FwTDVUriyw0FCTCBZCsSORGfHrln7Oq zCXWSUuSVVrQBWbbp/FFSsLDUsrNpxBXrgbFibmAJGMTJRQHGMZF1J0yXaDvWz8ZbtqvIemWZqfatMvqzY6GxA8jHR7KqlDlA9iDeNTRTKNY82K5yCmQyninRwTEa6I4xQkQEJgUiYFBCQzwQkM8iUTHvExMRMTH8Tpi1VrXq1ilcQq1UtodVtVrCxaixWsLJT0OUcSDFOUZLYs4kTAiEomJmNb /Sh1LaT1W8K6pyzp0uKkiwhgg7jrwy UzUN0ixg/ntdmhe9xxsjynqerkG7JZ00iBZC7jlNRNbj50Nq442Dqf0mr1OVV2G6apxnHp SJVWQBnQppb61sdfobcoDPRt3W1ko02RGOJkqNXXFUwpSMcEEXyJ0vlDkzjdbFeO RN60JbeOSJbLpe3X rLaRCieEsWxWjsIKzY5AkIIgZPtG8T3jc1WOciwuTJkTJB5cs5pUuUYsmTJkleeRJkHe4pjnMVziGMYjnEKUjnPI9znvcrlVVuWY3ezL4hWObUEXySis2ZOJEiTPMElcDEgTC9zmSmBiSAYKC5HDPhP6J8f4X815Tybit52LW3V18xW2ztcaJpt1UZsJUdXM5MrbF36uLQRLqQuqDLbwq3HmhlUlWOHGMZS9bt0y6XRx1 dSHQlP5HsenrY6WiPylRUlFs7bugi3jETXbptxT2lY4hI54VpDaW2qvJTGgHq7 1ZJrzTmVU6spbjENWD0WKzY7ot121bC SiGoeEg1ZSMwUQQz7TEwQlAmEiYiULWZKalwTEMQ5NhRSInAOQwWqPqcEBdGAJdSEhnjgomJmJYxjF6RpjGMNGmMYw0aYxjDRpjGMNGmMYw0aYxjDRpjGMNGmMYw0aYxjDRr/2Q==
# data:image/png;base64,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 HTTP/1.1" 200 OK


def storage_image(image_base64: str, output_direction_path: str, image_name: str):
    """
        将Base64编码的图片保存到磁盘。
        :param base64_md5:
        :param image_base64: Base64编码的图片字符串
        :param output_direction_path: 输出文件路径
        """
    try:
        # 去除可能存在的Base64字符串前缀（如 'data:image/png;base64,'）
        if 'data:image/png;base64,' in image_base64:
            image_base64: str = image_base64.replace('data:image/png;base64,', '')
        # 解码Base64字符串
        image_data = base64.b64decode(image_base64)
        # 将解码后的数据写入文件
        output_file_path = output_direction_path + image_name + '.png'
        with open(output_file_path, 'wb') as file:
            file.write(image_data)
        print(f"图片已成功保存到 {output_file_path}")
        return image_name
    except Exception as e:
        print(f"保存图片时出错: {e}")
    return


@app.get("/upload_image", response_model=str)
def upload_image(
        current_user: Annotated[User, Depends(get_current_active_user)],
        image_base64: str,
        flag: str,
        db: Session = Depends(get_db),
):
    image_base64 = image_base64.replace(' ', '+')
    output_direction_path = 'static/avatar/'
    base64_md5 = utils.hash_password(image_base64)
    image_name = base64_md5
    if flag == 'avatar':
        image_name = current_user.username
    base64_md5 = storage_image(image_base64, output_direction_path, image_name)
    user_id = upload_image_info(current_user.id, base64_md5, db)
    return 'http://localhost/avatar/' + image_name + '.png'


# 管理员激活/注销用户账号
@app.post("/activate_username", response_model=str)
def activate_username(
        username: str, activate_sign: bool, db: Session = Depends(get_db)
):
    activate_user = modify_user_activation(username, activate_sign, db)
    return activate_user


@app.post("/add_user_information", response_model=UserInformation)
def add_user_information(
        form_data: UserInformation,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    user_info = add_user_info(form_data, current_user.id, db)
    return user_info


@app.post("/change_password", response_model=str)
def change_password(
        form_data: UserPassword,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    db_user = get_user(current_user.username, db)
    if (form_data.new == form_data.old) or (form_data.new != form_data.new1):
        print(form_data.new, form_data.new1, form_data.old)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = change_password_info(form_data.new, current_user.username, db)
    return username


#####################################################################################################
@app.get("/roles", response_model=list[RolesInDB])
def roles(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    if current_user.username != 'admin':
        return []
    roles_list = get_roles_info(db)
    return roles_list


# 添加角色信息
@app.post("/role", response_model=int)
def add_role(
        form_data: AddRole,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    if current_user.username != 'admin':
        return 0
    role_id = add_role_info(form_data, db)
    return role_id


@app.post("/modify_role", response_model=int)
def modify_role(
        form_data: RolesInDB,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    if current_user.username != 'admin':
        return 0
    role_id = modify_role_info(form_data, db)
    return role_id


@app.get("/delete_role", response_model=int)
def delete_role(
        role_id: str,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db)):
    if current_user.username != 'admin':
        return
    role_id = delete_role_info(role_id, db)
    return role_id


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
        form_data: AddProvider,
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


@app.get("/delete_provider", response_model=str)
def delete_provider(provider_id: str, current_user: Annotated[User, Depends(get_current_active_user)],
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
        form_data: AddBusiness,
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


@app.get("/delete_business", response_model=str)
def delete_business(business_id: str, current_user: Annotated[User, Depends(get_current_active_user)],
                    db: Session = Depends(get_db)):
    business_name = delete_business_info(business_id, current_user.id, db)
    return business_name


#########################################################################################
# 证书信息
@app.get("/certificates", response_model=list[CertificateInDB])
def certificates(
        certificate_belong_to: str,
        certificate_belong_type: bool,
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Session = Depends(get_db),
):
    certificates_list = get_certificates_info(certificate_belong_to, certificate_belong_type, db)
    return certificates_list


@app.post("/certificate", response_model=CertificateInDB)
def add_certificate(
        form_data: AddCertificate,
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


@app.get("/delete_certificate", response_model=str)
def delete_certificate(certificate_id: str, current_user: Annotated[User, Depends(get_current_active_user)],
                       db: Session = Depends(get_db)):
    certificate_id = delete_certificate_info(certificate_id, db)
    return certificate_id


#########################################################################################
# 合同
@app.post("/contract", response_model=ContractInDB)
def add_contract(
        form_data: AddContract,
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


@app.get("/delete_contract", response_model=str)
def delete_contract(contract_id: str, current_user: Annotated[User, Depends(get_current_active_user)],
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
        form_data: AddPayIn,
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


@app.get("/delete_payin", response_model=str)
def delete_payin(payin_id: str, current_user: Annotated[User, Depends(get_current_active_user)],
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
        form_data: AddPayOut,
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


@app.get("/delete_payout", response_model=str)
def delete_payout(payout_id: str, current_user: Annotated[User, Depends(get_current_active_user)],
                  db: Session = Depends(get_db)):
    payout_id = delete_payout_info(payout_id, db)
    return payout_id


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
