from sqlalchemy import Boolean, Column, Integer, String, text, NVARCHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import DATETIMEOFFSET

from .database import Base

class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="1", nullable=False)
    created_at = Column(DATETIMEOFFSET, nullable=False, 
                        server_default=text('SYSDATETIMEOFFSET()'))
    owner_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), 
                      nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(NVARCHAR(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DATETIMEOFFSET, nullable=False, 
                        server_default=text('SYSDATETIMEOFFSET()'))

class Vote(Base):
    __tablename__ = "Votes"
    user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), 
                     primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("Posts.id", ondelete="NO ACTION"), 
                     primary_key=True, nullable=False)

