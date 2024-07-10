from sqlalchemy import Column ,Integer ,String ,Boolean ,DateTime ,func
from database import Base
from pydantic import BaseModel


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True)
    post = Column(String(255))
    published = Column(Boolean,default=False)
    created_at = Column(DateTime , default=func.now())
    updated_at = Column(DateTime , default=func.now())