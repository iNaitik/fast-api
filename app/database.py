from sqlalchemy import create_engine
# create_engine is a function that creates a new SQLAlchemy engine instance, 
# which is used to manage the connection to the database and execute SQL queries.
from sqlalchemy.orm import declarative_base 
# declarative_base is a function that returns a new base class from which all 
# mapped classes should inherit. It is used to define the database models in SQLAlchemy.
from sqlalchemy.orm import sessionmaker
# sessionmaker is a function that creates a new SQLAlchemy session factory,
# which is used to create new database sessions that can be used to interact with the database.
from app.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip - address/host_name>:<port>/<database_name>"
SQL_ALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"

# create the database engine 
# the engine is responsible for managing the connection to the database and executing SQL queries
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

# create a session local class that will be used to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a base class for our models to inherit from
Base = declarative_base()


def get_db():
    db = SessionLocal() # create a new database session
    try:
        yield db # yield the database session to be used in the endpoint functions
    finally:
        db.close() # close the database session after the request is completed




# ------------------------------------------------------------------------------------------------
# The code snippet below is used to connect to the PostgreSQL database using 
# the psycopg2 library.
# The code is commented out because we are using SQLAlchemy to manage the database connection 
# and queries instead of psycopg2.


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# try:
#     conn = psycopg2.connect(host = 'localhost',database="fastapi",user = 'postgres',
#                             password = '1353',cursor_factory=RealDictCursor)
#     # cursor_factory=RealDictCursor is used to return the data in the form of a dictionary instead of a tuple
#     cursor = conn.cursor()
#     print("Database connection was successful") 
# except Exception as error:
#     print("Failed to connect to database")
#     print("Error: ", error)
#     time.sleep(3) # wait for 3 seconds before trying to connect again
# ------------------------------------------------------------------------------------------------