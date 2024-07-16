                #This file containes the environment variabales


from pydantic_settings import BaseSettings # for envionment variable

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int



# import the information from .env file
    class Config:
        env_file = ".env"

# creating an instance of the Settings.
settings = Settings()
