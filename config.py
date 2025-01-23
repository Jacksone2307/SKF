from os import environ
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Establish .env variables"""
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")
    TESTING = environ.get("TESTING")

    DB_URI = environ.get("DB_URI")
    echo_string = environ.get('DB_ECHO')
    
    DB_ECHO = False
    if echo_string.lower().strip() == "true":
        DB_ECHO = True

