from fastapi  import FastAPI ,Response,status,HTTPException,Depends,APIRouter
from .. import database,auth,schema,models
from sqlalchemy.orm import Session
import uuid

router=APIRouter(prefix="/votes")

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(payload:schema.Vote,db:Session=Depends(database.get_db),user_id:str=Depends(auth.get_current_user)):
    try:
        uuid.UUID(payload.post_id)
    except:
        return {"message":"invalid uuid"} 
   
    vote_query=db.query(models.Votes).filter(
        models.Votes.post_id==payload.post_id,models.Votes.user_id==user_id
    )
    found_vote=vote_query.first()
    if payload.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="alredy voted")
        new_vote=models.Votes(user_id=user_id,post_id=payload.post_id)
        db.add(new_vote)
        db.commit()
        return {"message":"voted"}
    elif dir==0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="you havent voted")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"like deleted"}
        
