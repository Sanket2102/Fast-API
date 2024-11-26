# Importing necessary libraries
from fastapi import FastAPI, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

# Initializing FastAPI instance
app = FastAPI()

# Class for getting a structured input
class Post(BaseModel):
    title: str
    content: str
    # rating: Optional[int] = None

# Temporary storage for posts
my_posts = [{"title":"title of post 1", "content":"content of post 2", "id":1},
            {"title":"Favourite foods", "content":"my favourite food item is pizza", "id":2}]

# Our First API with the root path
@app.get("/")
async def root():
    return({"message":"Hello Python"})

# This API returns all the posts saved in our list [my_posts] in a json format
@app.get("/posts")
def get_posts():
    return({"data":my_posts})

# This API creates a new post without storing it anywhere
# @app.post("/posts")
# def create_post(post: Post):
#     print(f"{post.title},Rating: {post.rating}")
#     return({"message":"Operation run successfully"})


# This API creates a post and store it in our local memory
@app.post("/posts")
def create_post(post: Post):
    post = post.dict()
    post["id"] = (len(my_posts) + 1) 
    my_posts.append(post)
    return({"message":f"post updated successfully. Post: {post}"})

# This function returns the post with a specific id
def find_post(id):
    for items in my_posts:
        if items["id"] == id:
            return items

# This API returns the post with a specific id to the user
@app.get("/posts/uid/{id}")
def load_post(id: int):
    print(id)
    post = find_post(id)
    return("Check complete: ", post)
