from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas,models,utils,oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login', status_code= status.HTTP_200_OK,response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm is a class provided by FastAPI that defines the expected 
    # structure of the login request payload, which includes the username and password fields. 
    # By using Depends(), we can automatically parse the incoming request data and validate 
    # it against the OAuth2PasswordRequestForm schema.
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")\
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    #acess token
    # create_access_token is a function defined in the oauth2.py file that creates a 
    # JWT token using the user id as the payload.
    access_token = oauth2.create_access_token(data = {"user_id":user.id})

    return {"access_token": access_token, "token_type": "bearer"}