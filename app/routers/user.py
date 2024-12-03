from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
import app.models as models, app.schemas as schemas, app.utils as utils
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users", tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return "Your account has been created successfully"

@router.get("/uid/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")
    
    return user