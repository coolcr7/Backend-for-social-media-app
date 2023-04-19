from fastapi  import FastAPI ,Response,status,HTTPException,Depends,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..schema import login
from sqlalchemy.orm import Session
from ..database import engine,SessionLocal,get_db
from  .. import models
from .. import utils
from ..auth import create_jwt_token


router=APIRouter(prefix="/login")

@router.post("/")
def login(payload:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==payload.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invail credintial")
    if not utils.Hasher.verify_password(payload.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invail credintial11")
    token=create_jwt_token(data={"id":str(user.id)})
    return {"token":token,"type":"Bearer"}
    
    