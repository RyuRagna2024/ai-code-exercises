from fastapi import APIRouter, Path, Query, status
from typing import List, Optional

from ..models.todo import TodoCreate, TodoResponse
from ..utils.exceptions import TodoNotFoundError

router = APIRouter(prefix="/todos", tags=["todos"])

# In-memory mock database
fake_todos_db = {}
todo_counter = 0

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    """Create a new To-Do item"""
    global todo_counter
    todo_counter += 1

    todo_dict = todo.model_dump() if hasattr(todo, "model_dump") else todo.dict()
    new_todo = {**todo_dict, "id": todo_counter, "completed": False}

    fake_todos_db[todo_counter] = new_todo
    return new_todo

@router.get("/", response_model=List[TodoResponse])
async def list_todos(
    completed: Optional[bool] = Query(None, description="Filter items by status: true for completed, false for pending")
):
    """List all to-do items with optional status filtering"""
    todos = list(fake_todos_db.values())

    if completed is not None:
        todos = [t for t in todos if t["completed"] == completed]

    return todos

@router.patch("/{todo_id}/complete", response_model=TodoResponse)
async def mark_todo_completed(
    todo_id: int = Path(..., gt=0, description="The ID of the to-do item to mark as completed")
):
    """Mark a specific to-do item as completed"""
    if todo_id not in fake_todos_db:
        raise TodoNotFoundError(todo_id)

    fake_todos_db[todo_id]["completed"] = True
    return fake_todos_db[todo_id]

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int = Path(..., gt=0, description="The ID of the to-do item to delete")
):
    """Delete a specific to-do item"""
    if todo_id not in fake_todos_db:
        raise TodoNotFoundError(todo_id)

    del fake_todos_db[todo_id]
    return None