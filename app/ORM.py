# Importing necessary library
from fastapi import FastAPI, HTTPException, Response, status, Depends
import app.models as models,app.schemas as schemas, app.utils as utils
from app.database import engine, get_db
from sqlalchemy.orm import Session
from typing import List
# from passlib.context import CryptContext

# # Hashing algortihm to hash password before storing in database
# pwd_context = CryptContext(schemas=["bcrypt"], deprecated='auto')

# This creates the table in our Database
models.Base.metadata.create_all(bind=engine)


# initializing our app
app = FastAPI()

@app.get("/")
def root():
    return {"message":"This is a Social Media platform"}

@app.get("/sqlalchemy/posts")#,response_model=List[schemas.PostResponse])
def view_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/sqlalchemy/posts/uid/{id}", response_model=schemas.PostResponse)
def fetch_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts with the given id is found")
    return post

@app.post("/sqlalchemy/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.delete("/sqlalchemy/posts/uid/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found with the given id")
    post.delete(synchronize_session=False)
    db.commit()

@app.put("/sqlalchemy/posts/uid/{id}", response_model=schemas.PostResponse)
def update_post(post:schemas.PostCreate, id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    requested_post = post_query.first()
    if not requested_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found with the given id")
    
    post_query.update(post.dict())
    db.commit()

    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return "Your account has been created successfully"

@app.get("/users/uid/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    
    return user