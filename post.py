import auth,user
from auth import get_auth_user
from models import Post ,User ,Like
from database import get_session
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from fastapi.security import HTTPBasic
from schemas import PostCreate,PostUpdate , PostResponse
from fastapi import APIRouter , Depends,HTTPException ,status


router = APIRouter(prefix="/posts" ,tags=["Posts"] )

#dependency check if user is authenticated and authorized to take certain action
def is_owner(postid:int ,  db: Session = Depends(get_session),user: User = Depends(get_auth_user)):
      post = db.query(Post).filter(Post.id == postid).first()

      if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
      
      if post.user_id != user.id:
          raise HTTPException(status_code=403, detail="Not authorized to access this post")
      return post


@router.get("/" ,status_code=status.HTTP_200_OK ,response_model = list[PostResponse ])
def posts(db: Session = Depends(get_session)):
    posts = db.query(Post).options(joinedload(Post.user)).filter(Post.published == True).all()
    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK ,response_model = PostResponse )
def post(id:int ,user: User = Depends(auth.get_auth_user),db: Session = Depends(get_session)):

    #eager load
    post = db.query(Post).options(joinedload(Post.user),joinedload(Post.likes)).filter(Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not Found")
    return post


@router.post("/" ,status_code=status.HTTP_201_CREATED)
def store(request: PostCreate ,user: User = Depends(auth.get_auth_user), db: Session = Depends(get_session)):

    newpost = Post(
        title = request.title,
        post = request.post,
        user_id=user.id
        )
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost


@router.put("/{id}",response_model=PostResponse)
def update(request:PostUpdate ,post:Post = Depends(is_owner), db: Session = Depends(get_session)): 
    post.post = request.post
    post.title = request.title
    db.commit()
    return post
 
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT )
def destory(post: Post =Depends(is_owner), db: Session = Depends(get_session)):
    db.delete(post)
    db.commit()
    return {"message": "Post was deleted successfully."}

@router.post("/publish/{id}")
def publish_post(post:Post = Depends(is_owner), db : Session = Depends(get_session)):

        post.published = not post.published
        db.commit()
        db.refresh(post)
        message = "Post published successfully" if post.published else "Post unpublished successfully"
        return {"message": message}


@router.post("/likepost/{id}" )
def like_post(id:int ,user: User = Depends(auth.get_auth_user),db: Session = Depends(get_session)):
    post = db.query(Post).filter(Post.id == id).first()
    likedpost = Like(
        user_id= user.id,
        post_id = post.id
        )
    db.add(likedpost)
    db.commit()
    db.refresh(likedpost)
    return {"liked button"}


@router.get("/search/{search}",response_model=list[PostResponse])
def search(search:str, db: Session = Depends(get_session)): 
    searchresults = db.query(Post).filter(Post.post.contains(search)).all()
    if searchresults:
        return searchresults 
    return {"message":"No results found"}


@router.post("/comment/{id}")
def comment_post(id:int ,user: User = Depends(auth.get_auth_user),db: Session = Depends(get_session)):
    return user