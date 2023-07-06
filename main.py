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


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts


# insert a post in DB
@app.post("/posts")
def create_post():
    pass
