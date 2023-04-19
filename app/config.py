from pydantic import BaseSettings

class Settings(BaseSettings):
    database_host:str="localhost"
    secret_key:str="jalskfjalkjflskjflkjf"
    database_username:str="postgres"
    database_password:str="password"
    database_name:str="fastapi"
    database_port:str="8000"
    algo:str="HS256"
    exp:int=30
    class Config:
        env_file=".env"

settings=Settings()    