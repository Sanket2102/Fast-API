from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    # rating: Optional[int] = None

my_posts = [{"title":"title of post 1", "content":"content of post 2", "id":1},
            {"title":"Favourite foods", "content":"my favourite food item is pizza", "id":2}]


@app.get("/")
async def root():
    return({"message":"Hello Python"})

@app.get("/posts")
def get_posts():
    return({"data":my_posts})

# @app.post("/posts")
# def create_post(post: Post):
#     print(f"{post.title},Rating: {post.rating}")
#     return({"message":"Operation run successfully"})

@app.post("/posts")
def create_post(post: Post):
    post = post.dict()
    post["id"] = (len(my_posts) + 1) 
    my_posts.append(post)
    return({"message":f"post updated successfully. Post: {post}"})

def find_post(id):
    for items in my_posts:
        if items["id"] == id:
            output = items
        break
    return output

@app.get("/posts/{id}")
def load_post(id):
    print(id)
    post = find_post(id)
    return("Check complete: ", post)