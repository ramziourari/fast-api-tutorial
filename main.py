# main.py
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = 0.0


app = FastAPI()


@app.get("/")
async def welcome_func():
    return {"message": "hello there!!"}


@app.post("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id + "haha"}


@app.get("/user/me")
async def read_user_me():
    """Get current user info."""
    return {"user_id": "current user Id"}


@app.get("/user/{user_id}")
async def get_user(user_id: str):
    """Get Id of user."""
    return {"user": f"this is {user_id}"}


@app.post("/items/")
async def create_item(item: Item):
    """Create an item."""
    item_dict = item.dict()
    price_with_tax = item.price + item.tax
    item_dict.update({"price after tax": price_with_tax})
    return item_dict
