import hashlib


def hash_password(password):
    """生成密码哈希，不推荐用于密码存储"""
    password = password.encode('utf-8')
    hashed = hashlib.sha256(password).hexdigest()
    return hashed


def check_password(hashed_password, user_password):
    """校验密码"""
    if hashed_password == hash_password(user_password):
        return True
    else:
        return False
