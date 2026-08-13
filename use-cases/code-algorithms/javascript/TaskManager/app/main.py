from fastapi import FastAPI
from app.routes import auth, posts

app = FastAPI(
    title="FastAPI Blog API",
    description="Mini blog application created for FastAPI Documentation Navigation exercise",
    version="1.0.0"
)

# Register routes
app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Blog API! Visit /docs to test the interactive Swagger UI."}