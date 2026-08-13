from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


# ==========================================
# 1. USER SCHEMAS
# ==========================================

# Base schema for shared attributes
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

# Incoming request schema for registration (includes password)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Outgoing response schema (excludes password hash)
class UserResponse(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


# ==========================================
# 2. COMMENT SCHEMAS
# ==========================================

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


# ==========================================
# 3. BLOG POST SCHEMAS
# ==========================================

class PostBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    content: str = Field(..., min_length=5)

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=150)
    content: Optional[str] = Field(None, min_length=5)

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    comments: List[CommentResponse] = []

    class Config:
        from_attributes = True


# ==========================================
# 4. AUTHENTICATION & TOKEN SCHEMAS
# ==========================================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None