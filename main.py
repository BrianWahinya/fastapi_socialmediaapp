from turtle import pos
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


available_posts = []


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/posts")
async def get_posts():
    return {"data": available_posts}


@app.post("/posts")
async def create_posts(post: Post):
    postdict = post.dict()
    postdict['id'] = randrange(0, 1000000)
    print(postdict)
    available_posts.append(postdict)
    return {"info": f"{postdict['id']} successfully added"}
