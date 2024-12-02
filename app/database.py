# Import necessary libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from urllib.parse import quote

load_dotenv() # Load the varibales store in the .env file

# Stores environment variables into python variables to establish connection
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
encoded_password = quote(password)  # Encode the password to handle special characters in the password
port = int(os.getenv("DB_PORT"))

# URI to connect to our MySQL database using pymysql
DATABASE_URI = f"mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}"


# Create a connection to the database using the provided DATABASE_URI
engine = create_engine(DATABASE_URI)

# Create a session factory that will be used to create session objects for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models. It will be used to define ORM classes for database tables
Base = declarative_base()

# Function to open database instance and perform CRUD operations
def get_db():
    db = SessionLocal()  # Create a new database session
    try:
        yield db  # Return the session to be used in the context (e.g., inside a route handler)
    finally:
        db.close()
