from dotenv import load_dotenv
from pathlib import Path  # python3.6+
import os

# set path to env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
print(load_dotenv())

class Config:
    """Set Flask configuration vars from .env file."""

    # Load in enviornemnt variables
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    HOST_SERVER = os.getenv('HOST_SERVER')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER_PORT = os.getenv('SERVER_PORT')
    TESTING = os.getenv('TESTING')
