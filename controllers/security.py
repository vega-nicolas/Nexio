import bcrypt
import secrets
import rsa

def hashPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def checkPassword(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

def randomToken() -> str:
    return secrets.token_hex(32)

def genKeys() -> tuple:
    return rsa.newkeys(2048)