# models.py
# This file defines the database models for the application using SQLAlchemy's ORM (Object-Relational Mapping) system.
# The Post class represents a post in the database and inherits from the Base class defined 
# in database

# If we want to create a new table in the database, we can simply define a 
# new class that inherits from Base and specifies the table name and columns, 
# and SQLAlchemy will take care of creating the table in the database 
# when we run the application.

# The Post class has several attributes that correspond to the columns in the posts table in 
# the database, such as id, title, content, published, and created_at. 
# Each attribute is defined using SQLAlchemy's Column class, which specifies the data type 
# and other properties of the column.

from .database import Base
from sqlalchemy import Column, ForeignKey,Integer,String,Boolean, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='TRUE',nullable=False )
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable=False) 
    # this is used to store the id of the user who created the post, 
    # it is a foreign key that references the id column in the users table
    owner = relationship("User") 
    # this is used to define the relationship between the Post and User models,
    # it allows us to access the user object associated with a post using the 
    # owner attribute of the Post model, and also allows us to access the posts associated 
    # with a user using the posts attribute of the User model that we will define in the 
    # User model.
    phone_number = Column(String, nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete = "CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete = "CASCADE"),primary_key=True)