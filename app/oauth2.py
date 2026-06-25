from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app import models, schemas,database
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data:dict):
    to_encode = data.copy()

    # set the expiration time for the token by adding the current time to the 
    # ACCESS_TOKEN_EXPIRE_MINUTES constant
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
# encode the token using the jwt.encode function from the jose library, 
# which takes the payload (to_encode), the secret key (SECRET_KEY), and the algorithm (ALGORITHM)
# as arguments and returns the encoded JWT token as a string.

    return encoded_jwt

def verify_access_token(token:str, credentials_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        # extract the user id from the token payload using the get method of the payload dictionary.
        # The data in the payload is stored in the form of a dictionary, 
        # and the user id is stored under the key "user_id".
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id) 
    # create a TokenData object using the id extracted from the token payload.
    except JWTError as e:
        raise credentials_exception
    return token_data
    
def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    # get_current_user is a function that is used to get the current user from the token. 
    # It takes the token as an argument and uses the verify_access_token function to 
    # decode the token and get the user id from the token payload.
    # It then queries the database to get the user object using the user id and 
    # returns the user object.
    # The token is passed as a dependency using the Depends function from FastAPI,
    # which allows us to automatically extract the token from the request header and
    # pass it to the get_current_user function
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail="Could not validate credentials",
                                        headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first() # type: ignore
    return user

