from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import oauth2, schemas,models
from app.database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote,db:Session = Depends(get_db), 
               current_user = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {vote.post_id} does not exists")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                        models.Vote.user_id == current_user.id).first()
    if vote.dir == 1:
        if vote_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user with id: {current_user.id} has already voted on post with id: {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
# -------------------------------------------------------------------------------------------
# See we have set the post_id and user_id in the Vote table as primary key, 
# so we can only have one vote per user per post, if we try to add another vote for the same post by the same user,
# it will raise an error because of the primary key constraint, 
# so we need to check if the user has already voted for the post before adding a new vote, 
# if the user has already voted for the post, we will raise an error with 
# status code 409 (Conflict) and a message indicating that the user has already voted 
# for the post, if the user has not voted for the post, 
# we will create a new vote object and add it to the database, 
# then we will commit the changes to the database and refresh the new vote object to get 
# the id of the new vote from the database, 
# finally we will return a message indicating that the vote was successfully added.

# The primary key constraint will handle the check for duplicate votes but it will
# throw a ugly error message 
# so we are doing the check manually to raise a more user-friendly error message.
# -------------------------------------------------------------------------------------------
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully added vote"}
    else:
        if not vote_query:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"vote does not exists")
        deleted_vote = vote_query
        if not deleted_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"vote does not exists")
        db.delete(deleted_vote)
        db.commit()
        return {"message": "successfully deleted vote"}
    

