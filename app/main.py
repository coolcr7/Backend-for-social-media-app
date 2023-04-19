from fastapi  import FastAPI ,Response,status,HTTPException,Depends
from fastapi.params import Body
from .utils import Hasher
from typing import List
import random
import psycopg2
from psycopg2.extras import RealDictCursor 
import getpass
import time 
import uuid
from . import models
from sqlalchemy.orm import Session
from .database import engine,SessionLocal,get_db
from .schema import Post,sendPost,createUser,sendUser
from .router import post,register,login,votes
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

username = getpass.getuser()
print("The current OS username is:", username)
# while 1:
#     try:
#         conn=psycopg2.connect(database="fastapi",user="postgres",cursor_factory=RealDictCursor,password="password")
#         cur=conn.cursor()
#         print("connection made succsesfull")
#         break
#     except Exception as error:
#         print("connection faile")
#         print(error)  
#         time.sleep(5)  

app=FastAPI()

origins=["google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(register.router)
app.include_router(login.router)
app.include_router(votes.router)

# posts=[{"title":"cs","content":"something","id":123}]
# def find_post(id):
#     for i in posts:
#         if i["id"]==id:
#             return i
#     return {}    
# def update(post,id):
#     if not post:return {}
    


@app.get("/")
async def root():
    return {"message": "Hlo World"}

