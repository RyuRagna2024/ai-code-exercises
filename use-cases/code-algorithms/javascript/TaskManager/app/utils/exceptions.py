from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class TodoNotFoundError(Exception):
    """Raised when a To-Do item is not found"""
    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        self.message = f"To-Do item with ID {todo_id} not found"
        super().__init__(self.message)

def add_exception_handlers(app: FastAPI) -> None:
    """Add custom exception handlers to the FastAPI application"""

    @app.exception_handler(TodoNotFoundError)
    async def todo_not_found_handler(request: Request, exc: TodoNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "Validation error in request data",
                "errors": exc.errors()
            }
        )