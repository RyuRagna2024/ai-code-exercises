from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class TodoBase(BaseModel):
    """Base model for To-Do item data"""
    title: str = Field(..., min_length=1, max_length=100, description="Title of the to-do item")
    description: Optional[str] = Field(None, max_length=500, description="Optional detailed description")
    due_date: Optional[date] = Field(None, description="Optional due date (YYYY-MM-DD)")

class TodoCreate(TodoBase):
    """Model for creating a new to-do item"""
    pass

class TodoResponse(TodoBase):
    """Model for returning a completed to-do item response"""
    id: int
    completed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete FastAPI Exercise",
                "description": "Finish Part 4 challenge and document results",
                "due_date": "2026-08-15",
                "completed": False
            }
        }