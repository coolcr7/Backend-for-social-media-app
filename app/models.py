from .database import Base
from sqlalchemy import Column,Integer,Boolean,String,text,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID

class Post(Base):
    __tablename__="posts"
    id=Column(UUID,server_default=text("uuid_generate_v4()") ,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='true',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),server_default=text("now()"),nullable=False)
    user_id=Column(UUID,ForeignKey("users.id",ondelete="CASCADE"),nullable=False )

class User(Base):
    __tablename__="users"
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    id=Column(UUID,unique=True,nullable=False,server_default=text("uuid_generate_v4()"),primary_key=True)

class Votes(Base):
    __tablename__="votes"
    user_id=Column(UUID,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)    
    post_id=Column(UUID,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    
