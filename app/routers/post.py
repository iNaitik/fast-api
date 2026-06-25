from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import oauth2, schemas,models
from typing import Optional
from app.database import get_db


# prefix is used to define a common path for all the routes defined in this router.
# tags is used to group the routes defined in this router under a common tag in the 
# OpenAPI documentation.
router = APIRouter(
     prefix="/posts",
     tags=["Posts"]
)

@router.get("/",response_model=list[schemas.PostOut])
async def get_posts(db:Session = Depends(get_db), 
                    current_user = Depends(oauth2.get_current_user),
                    limit: int = 10,skip: int = 0,search: Optional[str] = ""):

    # cursor.execute("SELECT * FROM posts") # execute the SQL query to fetch all the posts from the database
    # posts = cursor.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # query the database to get all the posts from the database using SQLAlchemy ORM
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, 
        isouter=True).group_by(models.Post.id).all()

    return results



#1.
# async def create_posts(payload: dict = Body(...)):  # Body is imported from FastAPI to read request body data,
    # parse all fields, convert them into a dictionary,
    # and assign the result to payload.

#2.
# Using the Post schema lets FastAPI validate the request payload structure.
# Instead of accepting a raw dictionary, the Post model enforces correct fields and types.

#3.
# With the Post model, the request data is validated and then used to build a new Post record
# that is persisted to the database through SQLAlchemy ORM.

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)): # post:Post is used to receive the data from the request body and validate it using the Post model
        
# ------------------------------------------------------------------------------------------
        # cursor.execute("INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *",
        #                (post.title,post.content,post.published))
        # new_post = cursor.fetchone()
        # conn.commit() # commit the changes to the database
# ------------------------------------------------------------------------------------------
# title is the name of the column in the database, post.title is the value of the title field in the request body
# Instead of title = post.title, content = post.content, published = post.published this
# we can also use **post.dict() or **post.model_dump() to unpack the fields of the post object 
# and pass them as keyword arguments to the Post model constructor
        new_post = models.Post(owner_id=current_user.id, **post.model_dump())
        db.add(new_post) # add the new post object to the database session
        db.commit() # commit the changes to the database
        db.refresh(new_post) # refresh the new post object to get the id of the new post from the database

        return new_post


@router.get("/{id}",response_model=schemas.PostOut)
async def get_post(id:int ,db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):  
    #  cursor.execute("SELECT * FROM posts WHERE id = %s",(str(id),)) # execute the SQL query to fetch the post with the given id from the database
    #  posts = cursor.fetchone()

    # posts = db.query(models.Post).filter(models.Post.id == id).first()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, 
        isouter=True).group_by(models.Post.id).first()

# --------------------------------------------------------------------------
    # if posts and posts.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
# --------------------------------------------------------------------------

    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found")
    
    return results

@router.delete("/{id}",response_model=schemas.Post)
async def delete_post(id:int,db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *",(str(id),)) # execute the SQL query to delete the post with the given id from the database
    # deleted_post = cursor.fetchone()
    # conn.commit() # commit the changes to the database

    deleted_post = db.query(models.Post).filter(models.Post.id == id).first() # query the database to get the post with the given id using SQLAlchemy ORM
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
# --------------------------------------------------------------------------
    # if deleted_post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
# --------------------------------------------------------------------------

    db.delete(deleted_post) # delete the post from the database
    db.commit() # commit the changes to the database
    return deleted_post

@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED,response_model=schemas.Post)
async def update_post(id:int,post:schemas.PostUpdate,db:Session = Depends(get_db), 
                      current_user = Depends(oauth2.get_current_user)): #post:Post is used to receive the data from the request body and validate it using the Post model
    # cursor.execute("UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *",
    #                (post.title,post.content,post.published,id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == id).first() # query the database to get the post with the given id using SQLAlchemy ORM
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

# --------------------------------------------------------------------------
    # if updated_post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
# --------------------------------------------------------------------------

    updated_post.title = post.title # type: ignore # update the title of the post
    updated_post.content = post.content # type: ignore # update the content of the post
    db.commit() # commit the changes to the database
    db.refresh(updated_post) # refresh the updated post object to get the updated data from the database
    return updated_post