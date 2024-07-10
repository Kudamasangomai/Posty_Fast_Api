from pydantic import (BaseModel,field_validator )

#used for validation 

class Post(BaseModel):
    post:str

    @field_validator('post')
    @classmethod
    def not_empty(cls ,v):
        if not v.strip():
            raise ValueError('must not be empty')
        return v