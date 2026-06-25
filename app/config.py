from pydantic_settings import BaseSettings, SettingsConfigDict

# The Settings class is used to define the configuration settings for the application,
# such as the database connection details and the secret key for authentication.    
class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int  

    model_config = SettingsConfigDict(env_file=".env")
# this is used to specify the name of the environment file that contains the configuration 
# settings, in this case, it is set to ".env", which means that the application will look 
# for a file named ".env" in the root directory of the project to load the 
# configuration settings from it.

settings = Settings() #type: ignore
# create an instance of the Settings class to access the configuration settings in the 
# application using the settings variable, for example, we can access the database password 
# using settings.database_password