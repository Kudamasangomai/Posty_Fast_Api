import auth,user
import models
import schemas
from models import Post
from datetime import datetime
from database import get_session
from sqlalchemy.orm import Session
from database import Base ,engine
from sqlalchemy.orm import joinedload
from fastapi import FastAPI , Depends,HTTPException ,status
from fastapi.security import OAuth2PasswordBearer,HTTPBasic ,HTTPBasicCredentials


# Create the database
Base.metadata.create_all(engine)
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
app.include_router(user.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/posts" ,tags=["Posts"])
def posts(db: Session = Depends(get_session)):
    posts = db.query(models.Post).filter(Post.published== True).all()
    return posts

@app.get("/posts/{id}", status_code=status.HTTP_200_OK ,tags=["Posts"],response_model=schemas.PostResponse )
def post(id:int ,credentials: HTTPBasicCredentials = Depends(security),db: Session = Depends(get_session)):
    user = auth.authenticate_user(credentials=credentials, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    #eager load
    post = db.query(Post).options(joinedload(Post.owner)).filter(Post.id == id).first()

    # post = db.query(models.Post).get(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not Found")
    post_response = schemas.PostResponse(
        id=post.id,
        title=post.title,
        post=post.post,
        published=post.published,
        created_at=post.created_at.isoformat(),
        updated_at=post.updated_at.isoformat(),
        user_id=post.user_id,
        user_name=post.owner.name  # Access the related user's name
    )

    return post_response
    # return post


@app.post("/posts" ,status_code=status.HTTP_201_CREATED,tags=["Posts"])
def store(request: schemas.Post,credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_session)):
    user = auth.authenticate_user(credentials, db)
    print(user)
    newpost = models.Post(
        title = request.title,
        post = request.post,
        user_id=user.id
        )
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post Not Found")
    finally:
        db.close()
    

@app.delete("/posts/{id}" ,tags=["Posts"])
def destory(id:int, db: Session = Depends(get_session)):
    post = db.query(models.Post).get(id)
    if post is None:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND, 
          detail="Post Not Found")
    db.delete(post)
    db.commit()
    db.close()
    return {"message": "Post was deleted successfully."}


@app.post("/posts/publish", tags=['Posts'])
def publish_post(id:int , db : Session = Depends(get_session)):
        post = db.query(models.Post).get(id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                  detail="Post Not Found")

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





