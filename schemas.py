from pydantic import (BaseModel,field_validator,Field,EmailStr)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///post.db")
sessionLocal = sessionmaker(bind=engine,expire_on_commit=False)

#used for validation 

class Post(BaseModel):
    post:str = Field(min_length = 3)

    @field_validator('post')
    @classmethod
    def not_empty(cls ,v):
        if not v.strip():
            raise ValueError('post field must not be empty')
        return v

    
class User(BaseModel):
    name: str = Field(min_length=5)
    username : str = Field(min_length=4)
    email: EmailStr
    password: str = Field(min_length=3)

    @field_validator('username','email')
    def validate_email(cls,username,email,**kwargs,):
          db = sessionLocal()
          try:
            db_user = db.query(User).filter((User.username == username)  | (User.email == email)).first()

            if db_user:
                raise ValueError('Username already registered')
          finally:
            db.close()
            return username
            return v

class Userlogin(BaseModel):
    username : str = Field(min_length=4)
    email: EmailStr