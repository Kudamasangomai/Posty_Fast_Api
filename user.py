import models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import sessionLocal
from schemas import Userinfo
from fastapi import Depends, HTTPException ,status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
from models import User
from auth import authenticate_user



router = APIRouter(prefix="/users" ,tags=["Users"] )
def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()

        
@router.get("/",response_model=list[Userinfo])
async def users(db:  Session = Depends(get_session)):
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

