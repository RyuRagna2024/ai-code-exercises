from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import UserCreate, UserResponse, Token
from app.utils.auth import get_password_hash, verify_password, create_access_token
from app.dependencies import fake_users_db

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    """Register a new user and store hashed password in our mock DB."""
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Store user with hashed password
    user_dict = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "email": user.email,
        "hashed_password": get_password_hash(user.password),
        "is_active": True,
        "created_at": user_dict.get("created_at")
    }
    fake_users_db[user.username] = user_dict
    return user_dict

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate credentials from form data and return a Bearer JWT."""
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}