from fastapi  import FastAPI ,Response,status,HTTPException,Depends,APIRouter
from typing import List
import uuid
from sqlalchemy.orm import Session
from ..database import engine,SessionLocal,get_db
from ..schema import Post,sendPost,createUser,sendUser,outpost
from .. import models
from ..auth import get_current_user
from typing import Optional
from sqlalchemy import func
import json
router=APIRouter(prefix="/posts")

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=sendPost)
async def create_post(payload:Post,db:Session=Depends(get_db),user_id:str=Depends(get_current_user)):
    # cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",[paylod.title,paylod.content,paylod.published])
    # new_post=cur.fetchone()
    # conn.commit()
    # return new_post
    val=payload.dict()
    val["user_id"]=user_id
    new_post=models.Post(**val)
    print(new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(new_post)
    return new_post

# @router.get("/",response_model=List[outpost])
@router.get("/")
async def get_post(db:Session=Depends(get_db),id:str=Depends(get_current_user)):
    # post=db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
    models.Votes, models.Votes.post_id == models.Post.id, isouter=True
               ).group_by(models.Post.id).all()
    results=[{"post":i[0],"votes":i[1]} for i in results]
    return results
    # cur.execute('''SELECT * FROM posts''')
    # return_post=cur.fetchall()
    # return return_post
    

@router.get("/{id}",response_model=sendPost)
async def get_post(id:str,res:Response,db:Session=Depends(get_db),user_id:str=Depends(get_current_user)):
    try:
        uuid.UUID(id)
    except:
        return {"message":"invalid uuid"}    
    # cur.execute('''SELECT * FROM posts WHERE id = %s''',[id])
    # found_post=cur.fetchone()
    # if not found_post:
        # res.status_code=status.HTTP_404_NOT_FOUND
        # return {"not found"}
    # return found_post
    found_post=db.query(models.Post).filter(models.Post.id==id).first()
    return found_post


@router.put("/{id}",response_model=sendPost)
async def update_post(payload:Post,id:str,res:Response ,db:Session=Depends(get_db),user_id:str=Depends(get_current_user)): 
    try:
        uuid.UUID(id)
    except:
        return {"message":"invalid uuid"}    
    # cur.execute('''UPDATE posts 
                    # SET title=%s, content=%s,published=%s 
                    #   WHERE id = %s RETURNING *''',[payload.title, payload.content,payload.published ,id])
    # updated_post=cur.fetchone()
    # if not updated_post:
    #     res.status_code=status.HTTP_404_NOT_FOUND
    #     return {"not found"}
    # conn.commit()      
    # return updated_post
    if user_id!=id:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="not allowed to change others post")
    updated_post=db.query(models.Post).filter(models.Post.id==id)
    if not updated_post.first():
        res.status_code=status.HTTP_404_NOT_FOUND
        return {"not found"}
    val=payload.dict()
    print(val)
    updated_post.update({"title":val["title"]},synchronize_session=False)
    db.commit()
    return updated_post.first()


@router.delete("/{id}")
async def delete_post(id:str,res:Response,db:Session=Depends(get_db),user_id:str=Depends(get_current_user)):
    try:
        uuid.UUID(id)
    except:
        return {"message":"invalid uuid"}    
    if user_id!=id:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="not allowed to change others post")
    # cur.execute('''DELETE FROM posts WHERE id = %s RETURNING *''',[id])
    # delete_post=cur.fetchone()
    # if not delete_post:
    #     res.status_code=status.HTTP_404_NOT_FOUND
    #     return {"not found"}
    # conn.commit()      
    # return delete_post
    post=db.query(models.Post).filter(models.Post.id==id)
    if not post.first():
        res.status_code=status.HTTP_404_NOT_FOUND
        return {"not found"}
    post.delete(synchronize_session=False)
    db.commit()
    return "deleted"

