# Importing necessary library
from fastapi import FastAPI
import app.models as models
from app.database import engine
from app.routers import post, user, auth

# This creates the table in our Database
models.Base.metadata.create_all(bind=engine)


# initializing our app
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"This is a Social Media platform"}

