from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.schemas import PostCreate, PostUpdate, PostResponse, CommentCreate, CommentResponse
from app.dependencies import get_current_user

router = APIRouter(prefix="/posts", tags=["Blog Posts"])

# In-memory post database list
fake_posts_db = []

# ==========================================
# 1. CREATE & READ POSTS
# ==========================================

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, 
    current_user: dict = Depends(get_current_user)
):
    """Create a new post attached to the authenticated user."""
    new_post = {
        "id": len(fake_posts_db) + 1,
        "title": post.title,
        "content": post.content,
        "author_id": current_user["id"],
        "created_at": datetime.utcnow(),
        "comments": []
    }
    fake_posts_db.append(new_post)
    return new_post


@router.get("/", response_model=List[PostResponse])
async def list_posts(
    search: Optional[str] = Query(None, description="Search term for title or content"),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Max items to return")
):
    """Retrieve posts with optional keyword search and pagination."""
    results = fake_posts_db

    # Search filtering
    if search:
        search_lower = search.lower()
        results = [
            p for p in results 
            if search_lower in p["title"].lower() or search_lower in p["content"].lower()
        ]

    # Pagination slicing
    return results[skip : skip + limit]


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    """Fetch a single blog post by its ID."""
    for post in fake_posts_db:
        if post["id"] == post_id:
            return post
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with ID {post_id} not found"
    )

# ==========================================
# 2. UPDATE & DELETE POSTS
# ==========================================

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a post. Only the post author is allowed to update."""
    for post in fake_posts_db:
        if post["id"] == post_id:
            # Check ownership
            if post["author_id"] != current_user["id"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to edit this post"
                )
            
            if post_update.title is not None:
                post["title"] = post_update.title
            if post_update.content is not None:
                post["content"] = post_update.content
            return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with ID {post_id} not found"
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Delete a post. Only the post author is allowed to delete."""
    for index, post in enumerate(fake_posts_db):
        if post["id"] == post_id:
            if post["author_id"] != current_user["id"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to delete this post"
                )
            fake_posts_db.pop(index)
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with ID {post_id} not found"
    )

# ==========================================
# 3. COMMENTS ON POSTS
# ==========================================

@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    current_user: dict = Depends(get_current_user)
):
    """Add a comment to a specific blog post."""
    for post in fake_posts_db:
        if post["id"] == post_id:
            new_comment = {
                "id": len(post["comments"]) + 1,
                "post_id": post_id,
                "author_id": current_user["id"],
                "content": comment.content,
                "created_at": datetime.utcnow()
            }
            post["comments"].append(new_comment)
            return new_comment

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Post with ID {post_id} not found"
    )