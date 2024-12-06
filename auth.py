import models
import schemas
import bcrypt
from database import sessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI , Body , Depends ,Query ,HTTPException ,status

router = APIRouter(tags=["Auth"] )
def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()
@router.post("/register")
def register(request:schemas.User, db: Session = Depends(get_session)):
          try:                
                user = models.User(
                      name = request.name ,
                      username = request.username ,
                      email = request.email,
                      password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
                      )
                db.add(user)
                db.commit()
                db.refresh(user)
                return user
          except IntegrityError:
                   db.rollback()
                   raise HTTPException(
                         status_code=status.HTTP_400_BAD_REQUEST,
                         detail="Username or email already registered")
          except Exception as e:
                db.rollback()
                raise HTTPException(
                      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                      detail=f"An error occurred: {str(e)}")
  

@router.post("/login")
def login(username:str,password:str, db: Session = Depends(get_session)):
      usercheck = db.query(models.User).filter(models.User.username== username).first()
      
      if not usercheck and bcrypt.checkpw(password.encode('utf-8'), usercheck.password.encode('utf-8')):
        raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
             detail="Invalid username or password")
    
      return {"message": "Login successful"}
