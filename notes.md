# Fast API 
these are notes for my first api crud app With FAST API. i am just learning the basics

-  pip install fastapi uvicorn 
-  uvicorn is application server used to serve Python web applications that adhere to the ASGI specification.
-  create folder project a create a file main.py(or your prefered name but i.e the entry point) 
-  run the app - uvicorn main:app --reload 
-  access the api  docs via http://localhost:8000/docs and boom Swagger has done it for you (loved this after having     struggled in documenting laravel Api with swagger)


## Models

- models are classes which reperents the structue and valiadation of data used in your api
- they are two whichh are pydantic and SQLAlchemy models
- Pydantic focus on Validation and serialization / Deserialization  and does the more       advanced validation before it reaches the Db
- SQLalchemy Reperents DB tables,relationships and define how data is stored and retrieved in Db and does the validation at Db Level

## Schemas
- schemas Defines the Pydantic models used to validate input and output data.


## Migrations

- Alembic is a lightweight database migration tool for usage with the SQLAlchemy
- SQLAlchemy is Database Toolkit for Python.
- creating a migration ->  alembic revision --autogenerate -m "add_timestamps_columns_to_post_table"
- running the migration -> alembic upgrade head

## Relationships

### relationships between User and Post models

This is a one-to-many relationship, meaning one User can have multiple Post
back_populates="posts": This creates a bidirectional relationship between post and user

### In Post model:
- user = relationship("User" ,back_populates="posts")

### In User Model
- posts = relationship("Post", back_populates="user")
- profile = relationship("Profile", back_populates="user", uselist=False)

### In Profile Model
-  one to one with User Model
-  user = relationship("User", back_populates="profile")




## Authentication

### HTTP Basic Auth
- the simplest way to authenticate is using username and password
- HTTPBasic Instance creates a security dependency that ensures clients provide a username     and password using HTTP  Basic Authentication.
Depends(security) - This dependency injection ensures that each request checks for credentials and provides them to the route


###  JWTS (JSON Web Token)

- install pyjwt[crypto] .( a library for encoding and decoding JWTs using Python)
- install "python-jose[crytography]"
- install python-multipart
- saw fire