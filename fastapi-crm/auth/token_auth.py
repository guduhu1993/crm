from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session
from crud import get_user
from sql_app.database import get_db
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from common.utils import check_password
from model.user import UserInDB, UserLogin
from model.jwt import Token, TokenData
from dotenv import load_dotenv
from config import Settings

load_dotenv()
settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt, expire.strftime("%Y%m%d%H%M%S")


def make_token_for_login(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    print(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token, exp = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, exp=exp)


# 根据token
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
        current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_manager_user(
        current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    if not current_user.is_manager:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
