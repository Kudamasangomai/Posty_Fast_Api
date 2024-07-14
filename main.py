import models
import schemas
from typing import List
from typing import Annotated
from datetime import datetime
from sqlalchemy.orm import Session
from database import Base ,engine ,sessionLocal
from fastapi import FastAPI , Body , Depends ,Query ,HTTPException ,status
from fastapi.security import OAuth2PasswordBearer ,OAuth2PasswordRequestForm ,HTTPBasic ,HTTPBasicCredentials

Base.metadata.create_all(engine)

def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()

security = HTTPBasic()
app = FastAPI(
    title="Posty API",
    description="API for my Post application . ",
    summary="Just learning API devlopment with Fast API",
    contact={"name" : "Kudakwashe Masangomai", "email" : "kudam775@gmail.com" },
    # This is global BasicAuth protection i.e all routes are protected
    # dependencies= [Depends(security)] 
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fakeuserdb ={
    1:{'user':'Kuda'},
    2:{'user':'Tamie'},
    3:{'user':'Thelma'},
}

@app.post("/register"  ,tags=['Auth'])
def register(request:schemas.User, db: Session = Depends(get_session)):
    user = models.User(
        name = request.name ,
        username = request.username ,
        email = request.email,        
        password = request.password ,
        )
   
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
         
@app.get("/posts" ,tags=["Posts"])
def posts(db: Session = Depends(get_session), ):
    posts = db.query(models.Post).all()
    return posts

@app.get("/{id}",status_code=status.HTTP_200_OK ,tags=["Posts"])
def post(id:int ,db: Session = Depends(get_session)):
    post = db.query(models.Post).get(id)

    if post is None:
        raise HTTPException(status_code=404,detail="Post not Found")
    return post


@app.post("/" ,tags=["Posts"])
def store(post:schemas.Post, db: Session = Depends(get_session)):
    post = models.Post(post = post.post)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.put("/{id}" ,tags=["Posts"])
def update(id:int, post:schemas.Post, db: Session = Depends(get_session)):
    try:
       postobj = db.query(models.Post).filter_by(id=id).first()
       postobj.post = post.post
       postobj.updated_at = datetime.now()
       db.commit()
       return postobj

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    finally:
        db.close()
    

@app.delete("/{id}" ,tags=["Posts"])
def destory(id:int, db: Session = Depends(get_session)):
    post = db.query(models.Post).get(id)
    if post is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    db.delete(post)
    db.commit()
    db.close()
    return {"message": "Post was deleted successfully."}

@app.get("/search/{search}" , tags=["Posts"])
def search(search:str, db: Session = Depends(get_session)): 
    searchq = db.query(models.Post).filter(models.Post.post.contains(search)).all()
    if searchq:
        return searchq
    return {"message":"No results found"}

@app.post("/publish", tags=['Posts'])
def publish_post(id:int , db : Session = Depends(get_session)):
        post = db.query(models.Post).get(id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")

        post.published = not post.published
        db.commit()
        message = "Post published successfully" if post.published else "Post unpublished successfully"
        return {"message": message}


@app.post("/likepost/" ,tags=['Posts'])
async def like_post():
    return {"liked button"}
         
@app.post("/user/signup", tags=["Users"])
async def create_user(user: schemas.User):
    return (user)

@app.get("/users/", tags=["Users"])
def users():
    return fakeuserdb


     