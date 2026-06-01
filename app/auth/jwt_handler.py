from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from app.core.config import settings

JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY not found in environment variables")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

        if "sub" not in payload:
            raise JWTError("Token payload missing subject")

        return payload
    except ExpiredSignatureError:
        raise JWTError("Token has expired")
    except JWTError:
        raise JWTError("Invalid token")