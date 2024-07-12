### Fast API

-  run the app uvicorn main:app --reload 

## migrations

- Alembic is a lightweight database migration tool for usage with the SQLAlchemy
- SQLAlchemy is Database Toolkit for Python.

- creating a migration ->  alembic revision --autogenerate -m "add_timestamps_columns_to_post_table"
- running the migration -> alembic upgrade head


## Authentication