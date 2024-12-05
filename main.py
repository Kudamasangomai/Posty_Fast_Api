import auth
import models
import schemas
import bcrypt
from datetime import datetime
from sqlalchemy.orm import Session
from database import Base ,engine ,sessionLocal
from fastapi import FastAPI , Depends,HTTPException ,status
from fastapi.security import OAuth2PasswordBearer,HTTPBasic ,HTTPBasicCredentials
from models import User

# Create the database
Base.metadata.create_all(engine)

# Helper function to get the database session
def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()

security = HTTPBasic()

# Initialize the application
app = FastAPI(
    title="Posty API",
    description="API for my Post Application . ",
    summary="Just learning API development with Fast API",
    contact={"name" : "Kudakwashe Masangomai", "email" : "kudam775@gmail.com" },
    # This is global BasicAuth protection i.e all routes are protected
    # dependencies= [Depends(security)]  
)
app.include_router(auth.router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/posts" ,tags=["Posts"])
def posts(db: Session = Depends(get_session)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", status_code=status.HTTP_200_OK ,tags=["Posts"]  )
def post(id:int ,credentials: HTTPBasicCredentials = Depends(security),db: Session = Depends(get_session)):
    
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


    post = db.query(models.Post).get(id)
    if post is None:
        raise HTTPException(status_code=404,detail="Post not Found")
    return post


@app.post("/posts" ,status_code=status.HTTP_201_CREATED,tags=["Posts"])
def store(request: schemas.Post,credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_session)):
    newpost = models.Post(post = request.post)
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost


@app.put("/posts/{id}" ,tags=["Posts"])
def update(id:int, request:schemas.Post, db: Session = Depends(get_session)):
    try:
       postobj = db.query(models.Post).filter_by(id=id).first()
       postobj.post = request.post
       postobj.updated_at = datetime.now()
       db.commit()
       return postobj

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    finally:
        db.close()
    

@app.delete("/posts/{id}" ,tags=["Posts"])
def destory(id:int, db: Session = Depends(get_session)):
    post = db.query(models.Post).get(id)
    if post is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    db.delete(post)
    db.commit()
    db.close()
    return {"message": "Post was deleted successfully."}


@app.post("/posts/publish", tags=['Posts'])
def publish_post(id:int , db : Session = Depends(get_session)):
        post = db.query(models.Post).get(id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")

        post.published = not post.published
        db.commit()
        message = "Post published successfully" if post.published else "Post unpublished successfully"
        return {"message": message}


@app.post("/posts/likepost" ,tags=['Posts'])
async def like_post(id:int ,db: Session = Depends(get_session)):
    return {"liked button"}

@app.get("/search/{search}" , tags=["Posts"])
def search(search:str, db: Session = Depends(get_session)): 
    searchresults = db.query(models.Post).filter(models.Post.post.contains(search)).all()
    if searchresults:
        return searchresults 
    return {"message":"No results found"}



def authenticate_user(db: Session, username: str,password:str):
    user = db.query(User).filter(User.username == username).first()
    if user and user.password == password:
        return user  # Valid user
    return None 

@app.get("/users", tags=["Users"])
async def users(db:  Session = Depends(get_session)):
    users = db.query(models.User).all()
    return users


     