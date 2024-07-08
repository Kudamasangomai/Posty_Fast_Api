from typing import List
from fastapi import FastAPI , Body , Depends ,Query ,HTTPException ,status
import schemas
import models
from database import Base ,engine ,sessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()

app = FastAPI(
    title="Posty API",
    description="API for my Post application . ",
    summary="Just learning API devlopment with Fast API",
    contact={
        "name" : "Kudakwashe Masangomai",
        "email" : "kudam775@gmail.com"
    }
)

fakeuserdb ={
    1:{'user':'Kuda'},
    2:{'user':'Tamie'},
    3:{'user':'Thelma'},
}

@app.get("/" ,tags=["Posts"])
def posts(db: Session = Depends(get_session)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/{id}",status_code=status.HTTP_200_OK ,tags=["Posts"])
def post(id:int ,db: Session = Depends(get_session)):
    post = db.query(models.Post).get(id)

    if post is None:
        raise HTTPException(status_code=404,detail="Post not Found")
    return post

#pass in parameters
# @app.post("/")
# def store(post:str):
#     newid = len(fakedb.keys()) + 1
#     fakedb[newid] = {"post":post}
#     return fakedb

#this use pydantic
@app.post("/" ,tags=["Posts"])
def store(post:schemas.Post, db: Session = Depends(get_session)):
    post = models.Post(post = post.post)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

#this one use body request
# @app.post("/")
# def store(body = Body()):
#     newid = len(fakedb.keys()) + 1
#     fakedb[newid] = {"post":body['post']}
#     return fakedb


@app.put("/{id}" ,tags=["Posts"])
def update(id:int, post:schemas.Post, db: Session = Depends(get_session)):
    try:
       postobj = db.query(models.Post).filter_by(id=id).first()
       postobj.post = post.post
       db.commit()
       return postobj

    except Exception as e:
        db.rollback()  # Rollback the session in case of an error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found slslsl")
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


@app.get("/users/", tags=["Users"])
def users():
    return fakeuserdb
