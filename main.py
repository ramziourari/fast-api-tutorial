# main.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def welcome_func():
    return {"message": "hello there!!"}


@app.post("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id + "haha"}
