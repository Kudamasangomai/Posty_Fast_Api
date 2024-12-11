import auth,user
from models import Post
from datetime import datetime
from database import get_session
from sqlalchemy.orm import Session
from database import Base ,engine
from sqlalchemy.orm import joinedload
from schemas import PostCreate , PostResponse
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

@app.get("/posts" ,status_code=status.HTTP_200_OK ,tags=["Posts"],response_model = list[PostResponse ])
def posts(db: Session = Depends(get_session)):
    posts = db.query(Post).options(joinedload(Post.user)).filter(Post.published == True).all()
    return posts

@app.get("/posts/{id}", status_code=status.HTTP_200_OK ,tags=["Posts"],response_model = PostResponse )
def post(id:int ,credentials: HTTPBasicCredentials = Depends(security),db: Session = Depends(get_session)):
    auth.authenticate_user(credentials=credentials, db=db)
  
    #eager load
    post = db.query(Post).options(joinedload(Post.user)).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not Found")
    return post


@app.post("/posts" ,status_code=status.HTTP_201_CREATED,tags=["Posts"])
def store(request: PostCreate ,credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_session)):
    user = auth.authenticate_user(credentials, db)
    print(user)
    newpost = Post(
        title = request.title,
        post = request.post,
        user_id=user.id
        )
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost


@app.put("/posts/{id}" ,tags=["Posts"])
def update(id:int, request:PostCreate,  credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_session)):
    user = auth.authenticate_user(credentials=credentials, db=db)
    postobj = db.query(Post).filter_by(id=id).first()

    # Check if the authenticated user is the owner of the post
    # so i can create a depedency for this right 
    if postobj.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not the owner of this post"
        )
    postobj.post = request.post
    postobj.title = request.title
    postobj.updated_at = datetime.now()
    try:    
       
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
    post = db.query(Post).get(id)
    if post is None:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND, 
          detail="Post Not Found")
    db.delete(post)
    db.commit()
    db.close()
    return {"message": "Post was deleted successfully."}


@app.post("/posts/publish", tags=['Posts'])
def publish_post(id:int ,credentials: HTTPBasicCredentials = Depends(security), db : Session = Depends(get_session)):
        post = db.query(Post).get(id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                  detail="Post Not Found")

        post.published = not post.published
        db.commit()
        message = "Post published successfully" if post.published else "Post unpublished successfully"
        return {"message": message}


@app.post("/posts/likepost" ,tags=['Posts'])
async def like_post(id:int ,credentials: HTTPBasicCredentials = Depends(security),db: Session = Depends(get_session)):
    return {"liked button"}

@app.get("/search/{search}" , tags=["Posts"])
def search(search:str, db: Session = Depends(get_session)): 
    searchresults = db.query(Post).filter(Post.post.contains(search)).all()
    if searchresults:
        return searchresults 
    return {"message":"No results found"}





