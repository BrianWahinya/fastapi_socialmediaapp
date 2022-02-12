from ast import Delete
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
import time

import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import Integer

from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',
                                user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Db conn success")
        break
    except Exception as error:
        print("Failed conn: ", error)
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class User(BaseModel):
    firstname: str
    lastname: str
    email: str


class PostDelete(BaseModel):
    id: str


class PostUpdate(BaseModel):
    update: list


class UserDelete(BaseModel):
    id: str


available_posts = []

# ************* MAIN ROOT ROUTE/PATH OPERAION


@app.get("/")
async def root():
    return {"message": "Hello World!"}

# ************* GET ALL POSTS/USERS

# using a cursor


@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data posts": posts}

# using sqlalchemy


@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return {"data users": all_users}

# ************* POST SINGLE POST/USER


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, response: Response):
    postdict = post.dict()
    print(postdict)
    postdict['id'] = randrange(0, 1000000)
    available_posts.append(postdict)
    return {"info": f"{postdict['id']} successfully added"}

# using sqlalchemy


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Session = Depends(get_db)):
    # use this
    # new_user = models.User(firstname=user.firstname,
    #                        lastname=user.lastname, email=user.email)
    # or
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"inserted data": new_user}

# ************* GET SINGLE POST/USER


@app.get("/posts?id={id}")
async def get_post(id: int):
    print(id)
    filtered_posts = []
    for p in available_posts:
        if p['id'] == id:
            filtered_posts.append(p)
    return {"data": filtered_posts}


# using sqlalchemy
@app.get("/users/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    one_user = db.query(models.User).filter(models.User.id == id).first()
    if not one_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")
    return {"data": one_user}


# ************* GET LATEST POST


@app.get("/posts/latest")
async def get_latest_post(response: Response):
    num_of_posts = len(available_posts)
    if num_of_posts > 0:
        post = available_posts[num_of_posts - 1]
        return {"latestpost": post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "message": "no posts available"})

# ************* DELETE SINGLE OR MULTIPLE POSTS


@app.delete("/posts", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(id: PostDelete):
    iddict = id.dict()
    to_be_deleted_ids = iddict['id'].rstrip(', ').split(',')
    present_posts_ids = []
    deleted_posts = []
    undeleted_posts = []

    for p in available_posts:
        present_posts_ids.append(p['id'])

    for param in to_be_deleted_ids:
        elem = int(param) if param.isdigit() else param
        if elem not in present_posts_ids:
            undeleted_posts.append(elem)
        else:
            for i, p in enumerate(available_posts):
                if p['id'] == elem:
                    available_posts.pop(i)
                    deleted_posts.append(elem)
    return {
        "message": {
            "deleted": deleted_posts,
            "undeleted": undeleted_posts
        }
    }

# using sqlalchemy


@app.delete("/users")
async def delete_user(user: UserDelete, db: Session = Depends(get_db)):
    delete_user = db.query(models.User).filter(models.User.id == user.id)
    if delete_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User: {user.id} does not exist")
    delete_user.delete(synchronize_session=False)
    db.commit()
    return {"message": f"User: {user.id} deleted successfully"}

# ************* UPDATE SINGLE OR MULTIPLE POSTS


@app.put("/posts")
async def update_post(post: PostUpdate):
    postdict = post.dict()
    updatePosts = postdict['update']
    print(updatePosts)
    posts = []
    for p in updatePosts:
        for i, ap in enumerate(available_posts):
            if str(p['id']) == str(ap['id']):
                posts.append({"message": p['id'], "index": i})
    return posts
