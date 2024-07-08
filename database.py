from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///post.db")

Base =  declarative_base()


sessionLocal = sessionmaker(bind=engine,expire_on_commit=False)