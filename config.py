import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
database_user = DB_USER #Enter the user_name you used to create the db (fyyur)
database_pass = DB_PASSWORD #Enter the password you created
database_url = 'localhost:5432'
database_name = DB_NAME #Enter the db_name. It should be "fyyur"

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(database_user, database_pass, database_url, database_name)
SQLALCHEMY_TRACK_MODIFICATIONS = False
