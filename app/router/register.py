from fastapi  import FastAPI ,Response,status,HTTPException,Depends,APIRouter
from typing import List
import uuid

from sqlalchemy.orm import Session
from ..database import engine,SessionLocal,get_db
from ..schema import Post,sendPost,createUser,sendUser
from ..utils import Hasher
from .. import models


router=APIRouter(prefix="/register")


@router.post("/",response_model=sendUser)
def create_user(payload:createUser,db:Session=Depends(get_db)):
    payload.password=Hasher.get_password_hash(payload.password)
    new_user=models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=sendUser)
async def get_post(id:str,res:Response,db:Session=Depends(get_db)):
    try:
        uuid.UUID(id)
    except:
        return {"message":"invalid uuid"}    
    found_user=db.query(models.User).filter(models.User.id==id).first()
    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no such user")
    return found_user
