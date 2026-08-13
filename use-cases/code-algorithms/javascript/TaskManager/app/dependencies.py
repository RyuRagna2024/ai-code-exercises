from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.utils.auth import SECRET_KEY, ALGORITHM, oauth2_scheme
from app.schemas import TokenData

# Temporary in-memory database dictionary (username -> user_dict)
fake_users_db = {}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency that decodes the JWT token from the Request Authorization header,
    validates the payload, and returns the current user object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
        
    return user