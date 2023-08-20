from app import models, schemas
from sqlalchemy import exc
from fastapi import status, Depends, HTTPException, APIRouter
from typing import Optional
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List
import oauth2
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/")
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .offset(skip)
        .limit(limit)
        .all()
    )
    results = (
        (
            db.query(models.Post, func.count(models.Post.user_id).label("users"))
            .join(models.User, models.Post.user_id == models.User.id, isouter=True)
            .group_by(models.Post.id)
        )
        .filter(models.Post.title.contains(search))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return results


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(user_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.Post).filter(models.Post.id == id)
        posts = query.first()
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post id {id} not found!!"
        )
    return posts


@router.delete("/{id}")
def delete_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"couldn't delete post with id {id}.",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return status.HTTP_204_NO_CONTENT


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"couldn't delete post with id {id}.",
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
