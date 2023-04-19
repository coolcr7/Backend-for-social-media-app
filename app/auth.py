from datetime import datetime, timedelta
from jose import JWTError,jwt
from .schema import token_payload
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from .config import settings

oauth_scheme=OAuth2AuthorizationCodeBearer(tokenUrl="login",authorizationUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algo
ACCESS_TOKEN_EXPIRE_MINUTES = settings.exp

def create_jwt_token(data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str,credential_exeption):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("id")
        if id is None:
            raise credential_exeption
        token_data=token_payload(id=id)
    except JWTError:
        raise credential_exeption   
    return id

def get_current_user(token:str=Depends(oauth_scheme)):
    credential_exeption=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not valid credential",
                                      headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token,credential_exeption)   

