from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict,EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
    # Same as orm_mode = True, this is used to tell pydantic that the data we are receiving
    # is not a dictionary but an ORM model object that is persisted to the database through SQLAlchemy ORM.
    
class UserLogin(BaseModel):
    email: EmailStr
    password:str 



class PostBase(BaseModel):  # Here we can define the properties of the post object
    title: str
    content: str
    published: bool = True  # default value is true
    

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
    # this is used to tell pydantic that the data we are receiving 
    # is not a dictionary but an ORM model object that is persisted to the database 
    # through SQLAlchemy ORM.

    owner: UserOut 
# this is used to include the user object associated with the post in the response model,
# it allows us to access the user object associated with a post using the owner 
# attribute of the Post model, and also allows us to access the posts associated with
# a user using the posts attribute of the User model that we will define in the User model.

class PostOut(BaseModel):
    Post: Post
    votes: int
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]  # direction of the vote, 1 for upvote and 0 for downvote
# Literal is used to specify that the value of the dir field can only be 0 or 1,
# this is used to validate the request payload for the vote endpoint, 
# it ensures that the value of the dir field is either 0 or 1, and if it is not, 
# it will raise a validation error.