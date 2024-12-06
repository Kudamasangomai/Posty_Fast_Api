import models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import sessionLocal
from schemas import Userinfo
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
import bcrypt


security = HTTPBasic()
router = APIRouter(prefix="/users" ,tags=["Users"] )
def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()
        
@router.get("/", tags=["Users"],response_model=list[Userinfo])
async def users(db:  Session = Depends(get_session)):
    users = db.query(models.User).all()
    return users

@router.get("/{id}", tags=["Users"],response_model=Userinfo)
async def users(id:int ,db:  Session = Depends(get_session)):
    user = db.query(models.User).get(id)
    return user

