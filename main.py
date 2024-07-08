from fastapi import FastAPI , Body , Depends ,Query ,HTTPException
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
    description="API for my blog post application . ",
    summary="Just learning API devlopment with fast api",
    contact={
        "name" : "Kudakwashe Masangomai",
        "email" : "kudam775@gmail.com"
    }
)

# fakedb ={
#     1:{'post':'clean car'},
#     2:{'post':'clean house'},
#     3:{'post':'go fo gym'},
# }


@app.get("/")
def posts(session: Session = Depends(get_session)):
    posts = session.query(models.Post).all()
    return posts

@app.get("/{id}")
def post(id:int ,session: Session = Depends(get_session)):
    post = session.query(models.Post).get(id)
    return post

#pass in parameters
# @app.post("/")
# def store(post:str):
#     newid = len(fakedb.keys()) + 1
#     fakedb[newid] = {"post":post}
#     return fakedb

#this use pydantic
@app.post("/")
def store(post:schemas.Post, session: Session = Depends(get_session)):
    post = models.Post(post = post.post)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

#this one use body request
# @app.post("/")
# def store(body = Body()):
#     newid = len(fakedb.keys()) + 1
#     fakedb[newid] = {"post":body['post']}
#     return fakedb


@app.put("/{id}")
def update(id:int, post:schemas.Post, session: Session = Depends(get_session)):
    postobj = session.query(models.Post).get(id)
    postobj.post = post.post
    session.commit()
    return postobj


@app.delete("/{id}")
def destory(id:int, session: Session = Depends(get_session)):
    post = session.query(models.Post).get(id)
    session.delete(post)
    session.commit()
    session.close()
    return 'Post was deleted...'
