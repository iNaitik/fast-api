from fastapi import FastAPI
from app.database import engine
from app.routers import post,user,auth,votes
from fastapi.middleware.cors import CORSMiddleware
#----------------------------------------------------------------------------------------------
# to hash the password using bcrypt algorithm and to verify the password 
# when the user tries to log in

# deprecated="auto" is used to automatically mark the bcrypt algorithm as 
# deprecated in the future when it is no longer considered secure, 
# and to use a more secure algorithm instead. 
# This helps to ensure that the application remains secure over time as new vulnerabilities 
# are discovered and new algorithms are developed.
#------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------
# create the database tables based on the models defined in the models.py file
# --------- models.Base.metadata.create_all(bind = engine) ----------------------
# This the command that tolds the SQLAlchemy to create the tables in the database based on 
# the models defined in the models.py file.

# But we no longer need to use this command because we are using Alembic to manage the 
# database migrations, and Alembic will automatically create the tables in the database 
# when we run the migration commands.
# ---------------------------------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"], # allow all origins to access the API
    allow_credentials=True, # allow cookies to be sent with requests
    allow_methods=["*"], # allow all HTTP methods to be used
    allow_headers=["*"], # allow all headers to be sent with requests
)

app.include_router(post.router) # include the post router to define the routes for the post-related endpoints
app.include_router(user.router) # include the user router to define the routes for the user-related endpoints
app.include_router(auth.router) # include the auth router to define the routes for the authentication-related endpoints
app.include_router(votes.router) # include the votes router to define the routes for the vote-related endpoints



@app.get("/")   
async def root():
    return {"message": "Hello from the Deployed application"}





