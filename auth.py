from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import sessionLocal

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
         user = models.User(name = request.name ,username = request.username ,
                    email = request.email, password = request.password ,)
         db.add(user)
         db.commit()
         db.refresh(user)
         return user