from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(String(5000), nullable=False)
    published = Column(Boolean, default=True)

