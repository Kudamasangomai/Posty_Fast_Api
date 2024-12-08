from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# MySQL connection details
DATABASE_URL = "mysql+pymysql://root@localhost:3306/fastapiblog"

# Purpose: Connects to the database.
# Parameters: "sqlite:///post.db": The database URL. 
# In this case, it specifies a SQLite database file named post.db.
engine = create_engine("sqlite:///post.db")
# engine = create_engine(DATABASE_URL, echo=True)


# Purpose: Defines the base class for all your database models.
Base =  declarative_base()

# Purpose: Creates a database session factory.
#  bind=engine: Associates the session with the database connection (engine).
# expire_on_commit=False: Prevents the session from expiring objects after committing, so you can continue using them after a commit.
sessionLocal = sessionmaker(bind=engine,expire_on_commit=False)


# Helper function to get the database session
def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()