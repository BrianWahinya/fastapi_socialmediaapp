from turtle import pos
from typing import Optional
from urllib import response
from fastapi import Body, FastAPI, Response
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
async def create_posts(post: Post, response: Response):
    if not post:
        response.status_code = 404
    else:
        postdict = post.dict()
        print(postdict)
        postdict['id'] = randrange(0, 1000000)
        available_posts.append(postdict)
        return {"info": f"{postdict['id']} successfully added"}


@app.get("/posts?id={id}")
async def get_post(id: int):
    print(id)
    filtered_posts = []
    for p in available_posts:
        if p['id'] == id:
            filtered_posts.append(p)
    return {"data": filtered_posts}


@app.get("/posts/latest")
async def get_latest_post():
    num_of_posts = len(available_posts)
    if num_of_posts > 0:
        post = available_posts[num_of_posts - 1]
        return {"latestpost": post}
    return {"message": "no posts available"}
