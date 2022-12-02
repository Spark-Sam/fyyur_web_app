import os
from dotenv import load_dotenv


# Enable debug mode.
DEBUG = True

# Connect to the database
load_dotenv()
#DB_NAME = os.environ.get("DB_NAME")
#DB_USER = os.environ.get("DB_USER")
#DB_PASSWORD = os.environ.get("DB_PASSWORD")

# TODO IMPLEMENT DATABASE URL
#SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@localhost:5432/{}'.format(DB_USER, DB_PASSWORD, DB_NAME)
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
