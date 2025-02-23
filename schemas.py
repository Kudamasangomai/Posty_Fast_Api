from pydantic import (BaseModel,Field,EmailStr)
from datetime import datetime
from typing import List,Optional

# BaseModel is used for defining input/output data validation (Pydantic schema).
# used for validation 
class Userinfo(BaseModel):
    id:int
    name :str
    username :str
    email: EmailStr

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    title:str = Field(min_length=5)
    post:str = Field(min_length = 3)


class PostUpdate(BaseModel):
    title:str = Field(min_length=5)
    post:str = Field(min_length = 3)
  

class LikeResponse(BaseModel):
    # id: int
    user: Userinfo

class CommentCreate(BaseModel):
    comment :str = Field(min_length=1)

class CommentResponse(BaseModel):
    user :Userinfo
    comment : str

class PostResponse(BaseModel):
    id: int
    title: str
    post: str
    created_at : datetime
    user: Userinfo
    likes_count: int = 0
    comments_count: int = 0
    likes: list[LikeResponse] 
    comments: Optional[List[CommentResponse]] = [] 
    

    class Config:
        orm_mode = True

   # user create request 
class User(BaseModel):
    name: str = Field(min_length=5)
    username : str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=3)

class UserloginRequest(BaseModel):
    username : str = Field(min_length=3)
    email: EmailStr

class Token(BaseModel):
    access_token:str
    token_type: str