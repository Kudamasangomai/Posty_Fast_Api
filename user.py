import models
from models import User
from schemas import Userinfo
from database import get_session
from sqlalchemy.orm import Session
from auth import authenticate_user
from fastapi import APIRouter, Depends
from fastapi import Depends, HTTPException ,status

router = APIRouter(prefix="/users" ,tags=["Users"] )

        
@router.get("/",response_model=list[Userinfo])
def users(db:  Session = Depends(get_session)):
    users = db.query(models.User).all()
    return users

@router.get("/current_user",response_model=Userinfo)
def current_user(user: User = Depends(authenticate_user)):
    return user

@router.get("/{id}",response_model=Userinfo)
def users(id:int ,db:  Session = Depends(get_session)):
    user = db.query(models.User).get(id)

    if user is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                  detail="User Not Found")
    return user

