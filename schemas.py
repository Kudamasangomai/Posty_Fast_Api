from pydantic import (BaseModel,Field,EmailStr)
from datetime import datetime

# BaseModel is used for defining input/output data validation (Pydantic schema).
# used for validation 

class PostCreate(BaseModel):
    title:str = Field(min_length=5)
    post:str = Field(min_length = 3)

class PostUser(BaseModel):
    name:str

class PostResponse(BaseModel):
    id: int
    title: str
    post: str
    created_at : datetime
    user: PostUser # Nested Schema

    class Config:
        orm_mode = True

    
class User(BaseModel):
    name: str = Field(min_length=5)
    username : str = Field(min_length=4)
    email: EmailStr
    password: str = Field(min_length=3)

class UserloginRequest(BaseModel):
    username : str = Field(min_length=4)
    email: EmailStr


class Userinfo(BaseModel):
    id:int
    name :str
    username :str
    email: EmailStr
    class Config:
        orm_mode = True