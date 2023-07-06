# main.py
import time
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    id: int
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
        cur = conn.cursor()
        print("connection successful")
        break
    except psycopg2.Error as e:
        time.sleep(2)
        print("connection failed...")
        print(e)


@app.get("/")
async def root():
    return {"message": "hello there!!"}


@app.post("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id + "haha"}


@app.get("/user/me")
async def read_user_me():
    """Get current user info."""
    return {"user_id": "current user Id"}


@app.get("/user/{post_id}")
async def get_user(post_id: int):
    """Get Id of user."""
    return {"post": f"this is {post_id}"}


@app.post("/items/")
async def create_item(post: Post):
    """Create an item."""
    post_dict = post.dict()
    return post_dict


@app.put("/items/{item_id}")
async def create_item_by_Id(post_id: int, post: Post):
    """Create an item by id and Item."""
    return {"item_id": post_id, **post.dict()}
