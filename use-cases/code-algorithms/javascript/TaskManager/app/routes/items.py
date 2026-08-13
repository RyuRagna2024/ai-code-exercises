from fastapi import APIRouter, Path, Query, status
from typing import List, Optional

from ..models.item import ItemCreate, ItemResponse
from ..utils.exceptions import ItemNotFoundError

router = APIRouter(prefix="/items", tags=["items"])

# Mock database (in a real app, this would be a real database)
fake_items_db = {}
item_counter = 0

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Create a new item"""
    global item_counter
    item_counter += 1

    # Create new item with ID
    item_dict = item.model_dump() if hasattr(item, "model_dump") else item.dict()
    new_item = {**item_dict, "id": item_counter}

    # Store in our fake database
    fake_items_db[item_counter] = new_item

    return new_item

@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(
    item_id: int = Path(..., gt=0, description="The ID of the item to retrieve")
):
    """Get a specific item by ID"""
    if item_id not in fake_items_db:
        raise ItemNotFoundError(item_id)

    return fake_items_db[item_id]

@router.get("/", response_model=List[ItemResponse])
async def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of items to return"),
    tag: Optional[str] = Query(None, description="Filter items by tag")
):
    """List items with optional filtering and pagination"""
    items = list(fake_items_db.values())

    # Filter by tag if provided
    if tag:
        items = [item for item in items if tag in item.get("tags", [])]

    # Apply pagination
    return items[skip:skip+limit]