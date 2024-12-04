from fastapi import Depends, HTTPException, status, APIRouter
import app.models as models, app.schemas as schemas, app.oauth2 as oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix="/posts",tags=["Posts"]
)

@router.get("/",response_model=List[schemas.PostResponse])
def view_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return posts

@router.get("/uid/{id}", response_model=schemas.PostResponse)
def fetch_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts with the given id is found")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db:Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/uid/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found with the given id")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 
    
    post_query.delete(synchronize_session=False)
    db.commit()

@router.put("/uid/{id}", response_model=schemas.PostResponse)
def update_post(post:schemas.PostCreate, id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    requested_post = post_query.first()
    if not requested_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found with the given id")
    
    if requested_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 
    
    post_query.update(post.dict())
    db.commit()

    return post_query.first()
