## Fyyur Project Details

-----

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

Data models have been built to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

To run it you will have to setup some of the services and components manually. If you run into technical hitches, kindly feel free to let me know by raising an issue on the project's repo. https://github.com/spark-sam/fyyur_web_app 

### Overview

Capablilities of the application include the following, if not more, using a PostgreSQL database:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

We want Fyyur to be the next new platform that artists and musical venues can use to find each other, and discover new music shows. Let's make that happen!

## Tech Stack (Dependencies)

### 1. Backend Dependencies
The tech stack will include the following:
 * **A virtual environment** provided in the workspace (if working locally, see README)
 * **SQLAlchemy ORM** to be the ORM library of choice
 * **PostgreSQL** as the database of choice
 * **Python3** and **Flask** as the server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install SQLAlchemy
pip install --upgrade pip
pip install postgres
pip install Flask
pip install Flask-Migrate
```
> **Note** - If the specific version of a package is not mentioned, then the default latest stable package will be installed. 

### 2. Frontend Dependencies
It's recommended that you have **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for the website's frontend. If you are working locally, further instructions are contained in the repo README file.(NOT NESSESARY)

Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```


## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` --  Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` --  Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` --  Defines the forms used to create new artists, shows, and venues.
* `app.py` --  Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `app.py` --  Defines the data models that set up the database tables.
* `config.py` --  Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.


#### Data Handling with `Flask-WTF` Forms
The starter codes use an interactive form builder library called [Flask-WTF](https://flask-wtf.readthedocs.io/). This library provides useful functionality, such as form validation and error handling. You can peruse the Show, Venue, and Artist form builders in `forms.py` file. The WTForms are instantiated in the `app.py` file. For example, in the `create_shows()` function, the Show form is instantiated from the command: `form = ShowForm()`. To manage the request from Flask-WTF form, each field from the form has a `data` attribute containing the value from user input. For example, to handle the `venue_id` data from the Venue form, you can use: `show = Show(venue_id=form.venue_id.data)`, instead of using `request.form['venue_id']`.


##### Bucket List

Looking forward to:

*  Implement artist availability. An artist can list available times that they can be booked. Restrict venues from being able to create shows with artists during a show time that is outside of their availability.
* Show Recent Listed Artists and Recently Listed Venues on the homepage, returning results for Artists and Venues sorting by newly created. Limit to the 10 most recently listed items.
* Implement Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.



## Development Setup
1. **Setup a virtual environment** 
```
This depends on the distro or operating system you are on. (Please use a YouTube tutorial)
```
2. **Install the dependencies:**
```
pip install -r requirements.txt
```
3. **Install Postgres and create a Postgres User:**(Please use a YouTube tutorial)

4. **Create a db in Postgres by the name "fyyur":**

5. **Change the credentials in the config.py file to suite your Postgres Database**
```
database_user = DB_USER      --   # Enter the user_name you used to create the db (fyyur)
database_pass = DB_PASSWORD  --   # Enter the password you created

database_name = DB_NAME      --   # Enter the db_name. It should be "fyyur"
```

6. **Run the below commands (in the directory) to setup the tables in Postgres using the models:**
```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
7. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

8. **Verify on the Browser**<br>
Navigate to project homepage in the virtual desktop (by clicking the DESKTOP button in the workspace) [http://127.0.0.1:5000/] (http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) or in your local virtual environment. 