from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST"),
database = os.getenv("DB_NAME"),
user = os.getenv("DB_USER"),
password = os.getenv("DB_PASSWORD"),
port = int(os.getenv("DB_PORT"))

DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()