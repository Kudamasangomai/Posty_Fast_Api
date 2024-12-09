from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column ,Integer ,String ,Boolean ,DateTime ,func ,ForeignKey


# Base is used for defining the structure of a database table at DB Level (SQLAlchemy model).
# BaseModel is used for defining input/output data validation (Pydantic schema).
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True)
    title = Column(String(100), nullable=True)
    post = Column(String(255))
    user_id = Column(Integer,ForeignKey("users.id") ,nullable=False)
    published = Column(Boolean,default=False)
    created_at = Column(DateTime , default=func.now())
    updated_at = Column(DateTime , default=func.now())

    user = relationship("User" ,back_populates="posts")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),nullable=False)
    username = Column(String(255),nullable=False ,unique=True)
    email = Column(String(255),nullable=False ,unique=True)
    password = Column(String(255),nullable=False)
    created_at = Column(DateTime , default=func.now())
    updated_at = Column(DateTime , default=func.now())

    posts = relationship("Post", back_populates="user")