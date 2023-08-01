from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    published: bool


class UserBase(BaseModel):
    id: int
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserBase

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    users: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str]

    class Config:
        orm_mode = True


class Vote(BaseModel):
    dir: conint(le=1)
    post_id: int
