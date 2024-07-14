from pydantic import (BaseModel,field_validator,Field,EmailStr )

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
