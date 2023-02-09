from passlib.context import CryptContext
from env import Env
from datetime import datetime, timedelta
import jwt

pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

env = Env()

ALGORITHM = "HS256"
SECRET_KEY = env.SECRET_KEY


def create_password_hash(password):
    return pwt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwt_context.verify(plain_password, hashed_password)


def verify_password(plain_password, hashed_password):
    return pwt_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwt_context.hash(password)


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_authorization_token(token: str):
    if token is None:
        return None
    if token.startswith("Bearer "):
        token = token[7:]
    return token
