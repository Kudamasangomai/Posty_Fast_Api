import auth
from typing import Optional
from auth import get_auth_user
from sqlalchemy.sql import func
from database import get_session
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models import Post ,User ,Like ,Comment
from schemas import PostCreate,PostUpdate , PostResponse , CommentCreate
from fastapi import APIRouter , Depends,HTTPException ,status,UploadFile,File
from auth import get_current_user
from typing import Annotated


router = APIRouter(prefix="/api/posts" ,tags=["Posts"] )

user_dependency = Annotated[dict,Depends(get_current_user)]

#dependency check if user is authenticated and authorized(is the owner) to take acction on Post Model
def is_owner(postid:int ,  db: Session = Depends(get_session),user: User = Depends(get_auth_user)):
      post = db.query(Post).filter(Post.id == postid).first()

      if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
      
      if post.user_id != user.id:
          raise HTTPException(status_code=403, detail="Not authorized to access this post")
      return post


#Get all Posts
@router.get("/" ,status_code=status.HTTP_200_OK ,response_model = list[PostResponse] ,summary="Get All Posts")
def posts(user: user_dependency, db: Session = Depends(get_session),skip: int = 0, limit: int = 2 ):
    posts = db.query(Post).options(
                            joinedload(Post.user),
                            joinedload(Post.comments)
                            ).filter(Post.published == True).offset(skip).limit(limit).all()
    
    # I hope there is a better way than this
    for post in posts:
        post.likes_count = db.query(Like).filter(Like.post_id == post.id).count()
        post.comments_count = db.query(Comment).filter(Comment.post_id == post.id).count()

    return posts


#Get single Post 
@router.get("/{id}", status_code=status.HTTP_200_OK ,response_model = PostResponse,summary="Get Single Post" )
def post(id:int ,user: User = Depends(auth.get_auth_user),db: Session = Depends(get_session)):
    post = db.query(Post).options(
                        #eager load
                        joinedload(Post.user),
                        joinedload(Post.likes),
                        joinedload(Post.comments)
                        ).filter(Post.id == id).first()
 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not Found")
   
    
    likes_count = db.query(Like).filter(Like.post_id == id).count()
    comments_count = db.query(Comment).filter(Comment.post_id == id).count()

    post = post.__dict__
    post['likes_count'] = likes_count
    post['comments_count'] = comments_count
    return post

#Create Post Endpoint
@router.post("/" ,status_code=status.HTTP_201_CREATED ,response_model = PostResponse, summary="Create A Post")
def store( request: PostCreate,
           user: User = Depends(auth.get_auth_user),
           db: Session = Depends(get_session)):

    newpost = Post( **request.model_dump(),user_id=user.id)
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost

#Update Post Endpoint
@router.put("/{id}",response_model=PostResponse,summary="Update A Post")
def update(request:PostUpdate ,post:Post = Depends(is_owner), db: Session = Depends(get_session)): 
    post.post = request.post
    post.title = request.title
    db.commit()
    return post
 
 #Delete Post Endpoint
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT,summary="Delete A Post" )
def destory(post: Post =Depends(is_owner), db: Session = Depends(get_session)):
    db.delete(post)
    db.commit()
    return "Post was deleted successfully"

# Publish Post End Point 
@router.post("/{id}/publish" ,summary="Publish A Post")
def publish_post(post:Post = Depends(is_owner), db : Session = Depends(get_session)):
    post.published = not post.published
    db.commit()
    db.refresh(post)
    message = "Post published successfully" if post.published else "Post unpublished successfully"
    return {"message": message}

#Like post Endpoint
@router.post("/{id}/likepost",summary="Like A Post" )
def like_post(id:int ,user: User = Depends(auth.get_auth_user),db: Session = Depends(get_session)):
    post = db.query(Post).filter(Post.id == id).first()

    # show error if Post Does Exist
    if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")

    #if post Exist check if User liked ir
    liked = db.query(Like).filter( User.id == Like.user_id, Post.id ==id).first()

    #if user liked it Remove the post to peform a toggle(like unlike)
    if liked:
        db.delete(liked)
        db.commit()
        return {"message": "Post Unliked successfully"}
    #if not liked add user info to db as liked
    likedpost = Like(
        user_id= user.id,
        post_id = post.id
        )
    db.add(likedpost)
    db.commit()
    db.refresh(likedpost)
    return {"message": "Post liked successfully"}

# Search Post End Point
@router.get("/search/{search}",response_model=list[PostResponse])
def search(search:str, db: Session = Depends(get_session)): 
    searchresults = db.query(Post).filter(Post.post.contains(search)).all()
    if searchresults:
        return searchresults 
    return {"message":"No results found"}

# Comment A Post End Point
@router.post("/{id}/comment")
def comment_post(id:int ,request :CommentCreate ,user: User = Depends(auth.get_auth_user),db: Session = Depends(get_session)):
    post = db.query(Post).filter(Post.id == id).first()
    comment = Comment(
        user_id= user.id, post_id = post.id, comment = request.comment
        )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"message": "Comment Saved"}
    