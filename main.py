import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

posts = [
    {
        "id": 1,
        "title": "penguin",
        "text": "Penguins are a group of aquatic flightless birds."
    },
    {
        "id": 2,
        "title": "tigers",
        "text": "Tigers are the largest living cat species and a member of the genus Panthera"
    },
    {
        "id": 3,
        "title": "Koalas",
        "text": "Koala is arboreal herbivorous marsupial native to Australia"
    }
]

users = []

app = FastAPI()

#get for testing
@app.get("/", tags=["test"])
def greet():
    return {"hello": "world"}

#get all posts
@app.get("/posts", tags=["post"])
def get_post():
    return {"data":posts}

#get single post {id}
@app.get("/posts/{id}", tags=["post"])
def get_one_post(id : int):
    if id > len(posts):
        return {
            "error": "Post not found"
        }
    for post in posts:
        if post["id"]== id:
            return {
                "data":post
                }
#Post single
@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
def add_post(post : PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info": "Post added"
    }

# crear a nuevo usiario
@app.post("/user/signup", tags=["user"])
def user_signup(user : UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False
#login
@app.post("/user/login", tags=["user"])
def user_login(user : UserSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "detalles de entrada invalidos"
        }