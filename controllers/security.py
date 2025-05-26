import bcrypt
import secrets
import rsa
import hashlib

def hashPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def checkPassword(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))

def randomToken() -> str:
    return secrets.token_hex(128)

def hash_token(input: str) -> str:
    return hashlib.sha256(input.encode()).hexdigest()

def genKeys() -> tuple:
    return rsa.newkeys(2048)