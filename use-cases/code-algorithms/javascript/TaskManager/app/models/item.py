from pydantic import BaseModel, Field
from typing import Optional, List

class ItemBase(BaseModel):
    """Base model for item data"""
    name: str = Field(..., min_length=1, max_length=100, description="The name of the item")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description")
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    tags: List[str] = Field(default=[], description="List of tags for the item")

class ItemCreate(ItemBase):
    """Model for creating a new item"""
    pass

class ItemResponse(ItemBase):
    """Model for item responses that includes the ID"""
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop",
                "description": "Powerful development machine",
                "price": 1299.99,
                "tags": ["electronics", "computers"]
            }
        }