from database import Base
from sqlalchemy import Column ,Integer ,String ,Boolean ,DateTime ,func


# Base is used for defining the structure of a database table at DB Level (SQLAlchemy model).
# BaseModel is used for defining input/output data validation (Pydantic schema).
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True)
    title = Column(String(100), nullable=True)
    post = Column(String(255))
    published = Column(Boolean,default=False)
    created_at = Column(DateTime , default=func.now())
    updated_at = Column(DateTime , default=func.now())

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),nullable=False)
    username = Column(String(255),nullable=False ,unique=True)
    email = Column(String(255),nullable=False ,unique=True)
    password = Column(String(255),nullable=False)
    created_at = Column(DateTime , default=func.now())
    updated_at = Column(DateTime , default=func.now())