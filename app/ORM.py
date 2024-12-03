# Importing necessary library
from fastapi import FastAPI, HTTPException, Response, status, Depends
import app.models as models,app.schemas as schemas, app.utils as utils
from app.database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
from app.routers import post, user, auth
# from passlib.context import CryptContext

# # Hashing algortihm to hash password before storing in database
# pwd_context = CryptContext(schemas=["bcrypt"], deprecated='auto')

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

