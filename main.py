import auth,user ,post
from database import Base ,engine
from fastapi import FastAPI 
from fastapi.security import OAuth2PasswordBearer,HTTPBasic

# Create the database
Base.metadata.create_all(engine)

security = HTTPBasic()

# Initialize the application
app = FastAPI(
    title="Posty API",
    description="API for my Post Application . ",
    summary="Just learning API development with Fast API",
    contact={"name" : "Kudakwashe Masangomai", "email" : "kudam775@gmail.com" },
    # dependencies= [Depends(security)]  global BasicAuth protection
)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")






