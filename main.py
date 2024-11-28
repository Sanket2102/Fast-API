# Importing necessary library
import pymysql
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Establishing MySQL connection
try:
    connection = pymysql.connect(host = os.getenv("DB_HOST"),
                                database = os.getenv("DB_NAME"),
                                user = os.getenv("DB_USER"),
                                password = os.getenv("DB_PASSWORD"),
                                port = int(os.getenv("DB_PORT" , 3306)))
    print("Database successfully connected")
except Exception as error:
    print(f"Connection to Database failed. Error: {error}")
cursor = connection.cursor()

# initializing our app
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = 1

@app.get("/")
def root():
    return {"message":"This is a Social Media platform"}

@app.get("/posts")
def view_posts():
    cursor.execute("SELECT title, content, id from posts")
    posts = cursor.fetchall()
    return posts

@app.get("/posts/uid/{id}")
def fetch_post(id: int):
    select_query = "SELECT title, content from posts where id = %s"

    cursor.execute(select_query,(id,))
    posts = cursor.fetchall()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts with the given id is found")
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = post.dict()  # Convert the input Post object to a dictionary
    
    # Parameterized query for the INSERT operation
    insert_query = "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)"
    insert_values = (post['title'], post['content'], post['published'])
    cursor.execute(insert_query, insert_values)
    
    # Parameterized query for the SELECT operation
    select_query = "SELECT title, content FROM posts WHERE title = %s"
    cursor.execute(select_query, (post['title'],))
    connection.commit()
    output = cursor.fetchall()  # Fetch all rows matching the condition
    
    return output

@app.delete("/posts/uid/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id:int):
    select_query = "select id from posts where id = %s"
    delete_query = "DELETE FROM posts where id = %s"
    cursor.execute(select_query, (id,))
    post = cursor.fetchall()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No post found with the given id")
    cursor.execute(delete_query, (id,))
    connection.commit()

@app.put("/posts/uid/{id}")
def update_post(post:Post, id: int):
    post = post.dict()
    update_query = "UPDATE posts set title = %s, content = %s, published = %s where id = %s" 
    updated_content = (post["title"],post["content"],post["published"], id)
    cursor.execute(update_query, updated_content)
    connection.commit()


# Closing the connections
# cursor.close()
# connection.close()