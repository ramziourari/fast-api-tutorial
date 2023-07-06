# main.py
import time
import random

from fastapi import FastAPI, status, HTTPException, Response
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    id: int = None
    title: str
    content: str
    publish: bool = True


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
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts


# insert a post in DB
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content) VALUES (%s, %s)
           RETURNING *;
        """,
        (post.title, post.content),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return new_post


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"post with id {id} not found",
        )
    return post


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
