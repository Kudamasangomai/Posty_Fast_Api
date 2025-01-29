import models
import schemas
import bcrypt
from models import User
from typing import Annotated
from datetime import timedelta,datetime
from database import get_session
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from jose import jwt
from jwt import decode, encode, PyJWTError
from fastapi import Depends ,HTTPException ,status
from fastapi.security import (
    HTTPBasic ,HTTPBasicCredentials ,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)
router = APIRouter(tags=["Auth"] )

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer  = OAuth2PasswordBearer(tokenUrl="token")


db_dependency = Annotated[Session,Depends(get_session)]

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


security = HTTPBasic()


@router.post("/register")
def register(request:schemas.User, db: Session = Depends(get_session)):
          try:                
                user = models.User(
                      name = request.name ,
                      username = request.username ,
                      email = request.email,
                     password = bcrypt_context.hash(request.password)
                  #     password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
                      )
                db.add(user)
                db.commit()
                db.refresh(user)
                return user
          except IntegrityError:
                   db.rollback()
                   raise HTTPException(
                         status_code=status.HTTP_409_CONFLICT,
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
              status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Invalid credentials")
    
      return {"message": "Login successful"}

# def authenticate_user(credentials :HTTPBasicCredentials,db: Session= Depends(get_session)):
#     user = db.query(User).filter(User.username == credentials.username).first()
#     if not user or not pwd_context.verify(credentials.password, user.password):
#         raise HTTPException(
#               status_code=status.HTTP_401_UNAUTHORIZED,
#                detail="Invalid credentials")
#     return user



#dependency
def get_auth_user(credentials :HTTPBasicCredentials = Depends(security),db: Session= Depends(get_session)):
      return authenticate_user(credentials,db)





@router.post("/token" ,response_model=schemas.Token)
async def login_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                      db:db_dependency):
      user = authenticate_user(form_data.username,form_data.password,db)

      if not user:
        raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
             detail="Could not validate")
      token = create_access_token(user.username ,user.id ,timedelta(minutes=1))
      return {'access_token':token,'token_type':'bearer'}

## use this for jwt
def authenticate_user(username:str ,password:str ,db):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid credentials")
    return user

def create_access_token(username:str ,user_id:int , expires_delta: timedelta):
    encode = {'sub':username ,'id':user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
      #   user_id:int  = payload.get("id")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return {'username':username}
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

 
 