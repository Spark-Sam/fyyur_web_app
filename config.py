import os
from dotenv import load_dotenv

SECRET_KEY = os.urandom(32)
# Enable debug mode.
DEBUG = True

# Connect to the database
load_dotenv()
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PATH = os.environ.get("DB_PATH")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWORD, DB_PATH, DB_PORT, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False
