from sqlalchemy.orm import Session
from model.user import User
from common import utils
from sql_app.database import dbUser


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
    else:
        print("User not found.")
    return username
