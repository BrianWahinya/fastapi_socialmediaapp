from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    return {
        "data": [
            {1: "Post One"},
            {2: "Post Two"}
        ]
    }


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.post("/createposts")
async def create_posts(post: Post):
    print(post)
    return {"post": f"title: {post.title}, content: {post.content}, published: {post.published}, rating: {post.rating}"}
