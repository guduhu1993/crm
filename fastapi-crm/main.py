from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from auth.token_auth import make_token_for_login, get_current_active_user
from model.user import User
from sql_app.database import get_db
from crud import username_is_exist, create_user, get_user, modify_user_activation
from common import utils
from model.jwt import Token

app = FastAPI()


@app.post("/register/", response_model=User)
def register_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], phone: str,
                  db: Session = Depends(get_db)):
    if username_is_exist(form_data.username, db):  # 用户名是否已存在
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        db_user = User(username=form_data.username, phone=phone, is_active=False)
        create_user(db_user, form_data.password, db)
    return db_user


# 登陆成功后签发token
@app.post("/token", response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     db: Session = Depends(get_db)) -> Token:
    db_user = get_user(form_data.username, db)
    if not db_user or not utils.check_password(db_user.password, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    login_token = make_token_for_login(form_data)
    return login_token


@app.get("/user_info", response_model=User)
def user_info(current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    db_user = get_user(current_user.username, db)
    return db_user


# 管理员激活/注销用户账号
@app.post("/activate_username", response_model=str)
def activate_username(
        username: str,
        activate_sign: bool,
        db: Session = Depends(get_db)):
    activate_user = modify_user_activation(username, activate_sign, db)
    return activate_user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
