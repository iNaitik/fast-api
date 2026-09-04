from app import models, oauth2,schemas,utils
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db

# create a new APIRouter instance to define the routes for the user-related endpoints.
router = APIRouter(prefix="/users",
                   tags=["Users"])


@router.post("/", status_code= status.HTTP_201_CREATED,response_model=schemas.UserOut)
async def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash_password(user.password) # hash the password using the bcrypt algorithm
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 

@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db), user_id = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f'user with id: {id} does not exists')
    return user