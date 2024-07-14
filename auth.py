from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import sessionLocal
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI , Body , Depends ,Query ,HTTPException ,status
import models
import schemas


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
    )
def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()
@router.post("/register"  ,tags=['Auth'])
def register(request:schemas.User, db: Session = Depends(get_session)):
          try:
                user = models.User(name = request.name ,username = request.username ,
                    email = request.email, password = request.password ,)
                db.add(user)
                db.commit()
                db.refresh(user)
                return user
          except IntegrityError:
                   db.rollback()
                   raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")
          except Exception as e:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {str(e)}")
  