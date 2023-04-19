from pydantic import BaseModel,EmailStr,conint  
from datetime import datetime
from typing import Optional
import uuid

class Post (BaseModel):
    title:str
    content:str 
    published:bool=True #default is true  if not passed
    
class sendPost (Post):
    created_at:datetime     
    class Config:
        orm_mode=True

class outpost(BaseModel):
    Post:Post
    votes:int
    class Config:
        orm_mode=True

class createUser(BaseModel):
    email:EmailStr
    password:str

class sendUser(BaseModel):
    email:EmailStr
    id:uuid.UUID
    class Config:
        orm_mode=True

class login(BaseModel):
    email:EmailStr
    password:str
class token(BaseModel):
    token:str
    type:str

class token_payload(BaseModel):
    id:str        

class Vote(BaseModel):
    dir:conint(gt=-1,lt=2)
    post_id:str
