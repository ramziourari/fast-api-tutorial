# main.py
import time

from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

import models
from database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import exc

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    id: int = None
    title: str
    content: str
    published: bool = True


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
def create_post(post: Post, db: Session = Depends(get_db)):
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
def delete_posts(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (id,))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="couldn't delete post with id {id}.",
        )
    conn.commit()
    return {"deleted": deleted_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE  posts SET title = %s, content = %s, publish = %s
           WHERE id = %s RETURNING *;
        """,
        (post.title, post.content, post.publish, id),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    return updated_post
