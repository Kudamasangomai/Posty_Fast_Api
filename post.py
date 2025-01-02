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




router = APIRouter(prefix="/posts" ,tags=["Posts"] )

#dependency check if user is authenticated and authorized(is the owner) to take acction on Post Model
def is_owner(postid:int ,  db: Session = Depends(get_session),user: User = Depends(get_auth_user)):
      post = db.query(Post).filter(Post.id == postid).first()

      if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post Not Found")
      
      if post.user_id != user.id:
          raise HTTPException(status_code=403, detail="Not authorized to access this post")
      return post


@router.get("/" ,status_code=status.HTTP_200_OK ,response_model = list[PostResponse ] ,summary="Get All Posts")
def posts(db: Session = Depends(get_session)):
    posts = db.query(Post).options(
                            joinedload(Post.user),
                            joinedload(Post.comments)
                            ).filter(Post.published == True).all()
    return posts


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


@router.post("/" ,status_code=status.HTTP_201_CREATED ,response_model = PostResponse, summary="Create A Post")
def store( request: PostCreate,
           user: User = Depends(auth.get_auth_user),
           db: Session = Depends(get_session)):

    newpost = Post( **request.model_dump(),user_id=user.id)
    db.add(newpost)
    db.commit()
    db.refresh(newpost)
    return newpost


@router.put("/{id}",response_model=PostResponse,summary="Update A Post")
def update(request:PostUpdate ,post:Post = Depends(is_owner), db: Session = Depends(get_session)): 
    post.post = request.post
    post.title = request.title
    db.commit()
    return post
 
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT,summary="Delete A Post" )
def destory(post: Post =Depends(is_owner), db: Session = Depends(get_session)):
    db.delete(post)
    db.commit()
    return "Post was deleted successfully"

@router.post("/{id}/publish" ,summary="Publish A Post")
def publish_post(post:Post = Depends(is_owner), db : Session = Depends(get_session)):
        
    post.published = not post.published
    db.commit()
    db.refresh(post)
    message = "Post published successfully" if post.published else "Post unpublished successfully"
    return {"message": message}


@router.post("/{id}/likepost",summary="Like A Post" )
def like_post(id:int ,user: User = Depends(auth.get_auth_user),db: Session = Depends(get_session)):
    post = db.query(Post).filter(Post.id == id).first()
    likedpost = Like(
        user_id= user.id,
        post_id = post.id
        )
    db.add(likedpost)
    db.commit()
    db.refresh(likedpost)
    return {"message": "Post liked successfully"}


@router.get("/search/{search}",response_model=list[PostResponse])
def search(search:str, db: Session = Depends(get_session)): 
    searchresults = db.query(Post).filter(Post.post.contains(search)).all()
    if searchresults:
        return searchresults 
    return {"message":"No results found"}


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
    