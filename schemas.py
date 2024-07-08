from pydantic import BaseModel

#used for validation 

class Post(BaseModel):
    post:str
