# main.py
import time

from fastapi import FastAPI, status, HTTPException, Depends
import schemas
import psycopg2
from psycopg2.extras import RealDictCursor

import models
from database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import exc

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


@app.get("/posts/")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# insert a post in DB
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    try:
        query = db.query(models.Post).filter(models.Post.id == id)
        posts = query.first()
    except exc.NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post id {id} not found!!"
        )
    return {"data": posts}


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


@app.put("/posts/{id}")
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
    return {"data": post_query.first()}
