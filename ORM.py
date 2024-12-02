# Importing necessary library
import pymysql
from fastapi import FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import time
import models
from database import engine, get_db
from sqlalchemy.orm import Session

# This creates the table in our Database
models.Base.metadata.create_all(bind=engine)

# Load environment variables
load_dotenv()


# initializing our app
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = 1

@app.get("/")
def root():
    return {"message":"This is a Social Media platform"}

@app.get("/sqlalchemy/posts")
def view_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/sqlalchemy/posts/uid/{id}")
def fetch_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts with the given id is found")
    return post

@app.post("/sqlalchemy/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db:Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.delete("/sqlalchemy/posts/uid/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found with the given id")
    post.delete()
    db.commit()

@app.put("/sqlalchemy/posts/uid/{id}")
def update_post(post:Post, id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    requested_post = post_query.first()
    if not requested_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found with the given id")
    
    post_query.update(post.dict())
    db.commit()

    return post_query.first()
