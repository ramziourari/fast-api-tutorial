# main.py
import time
from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
import schemas
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import errors

import models
from database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import exc
import utils

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="postgres",
            user="postgres",
            password="2298367600",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("connection successful")
        break
    except psycopg2.Error as e:
        time.sleep(2)
        print("connection failed...")
        print(e)


@app.get("/")
async def root():
    return {"message": "hello there!!"}


@app.get("/posts/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post(
    "/posts/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.Post).filter(models.Post.id == id)
        posts = query.first()
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post id {id} not found!!"
        )
    return posts


@app.delete("/posts/{id}")
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"couldn't delete post with id {id}.",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return status.HTTP_204_NO_CONTENT


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)
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


@app.post(
    "/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_pwd(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except exc.IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Unique violation entry, email already used",
        )


@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user {id} not found"
        )
    return user


@app.get("/users/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no users found"
        )
    return users


@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    user.delete(synchronize_session=False)
    db.commit()
    return status.HTTP_204_NO_CONTENT
