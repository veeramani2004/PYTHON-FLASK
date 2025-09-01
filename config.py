from os import environ
from dotenv import load_dotenv

load_dotenv()

# print(environ.get("LOCAL_DATABASE_URL"))
# print(environ.items())


class Config:
    # Connection String
    SQLALCHEMY_DATABASE_URI = environ.get("LOCAL_DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
