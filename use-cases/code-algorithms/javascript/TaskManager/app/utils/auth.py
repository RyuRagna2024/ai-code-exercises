from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.schemas import TokenData

# ------------------------------------------
# Configuration Settings
# ------------------------------------------
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password Context for Hashing & Verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 Scheme specifying the token endpoint URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ------------------------------------------
# Utility Functions
# ------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify raw password against stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate bcrypt hash for raw password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Encode JWT access token with expiration timestamp."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)