from pydantic import (BaseModel,Field,EmailStr)

# BaseModel is used for defining input/output data validation (Pydantic schema).
# used for validation 

class Post(BaseModel):
    title:str = Field(min_length=5)
    post:str = Field(min_length = 3)
    # user_id:int

class PostResponse(BaseModel):
    id: int
    title: str
    post: str
    user_name: str

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