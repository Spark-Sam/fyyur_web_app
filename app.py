#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# DONE: connect to a local postgresql database
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # DONE: implement database migration using Flask-Migrate
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(200))
    website = db.Column(db.String(200))
    genres = db.Column(db.String(200))
    shows = db.relationship('Show', backref='Venue', lazy=True)
    def __repr__(self):
        return f'<Venue {self.name} city {self.city}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # DONE: implement database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120)) 
    shows = db.relationship('Show', backref = 'Artist', lazy = True)
    def __repr__(self):
        return f'<Artist id {self.id} name {self.name}>'

# DONE Implement Show and Artist models, and all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key = True)
  artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'),nullable = False)
  venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id'),nullable = False)
  start_time = db.Column(db.DateTime(timezone = True))
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: implement real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  cities= set(Venue.query.with_entities(Venue.city).all())
  venueList=[]
  currentCity=''
  for city in cities:
    venuesByCity=Venue.query.filter(Venue.city==city[0])
    for venue in venuesByCity:
      num_upcoming_shows = Show.query.filter(Show.venue_id==venue.id, Show.start_time>datetime.now()).count()
      if currentCity != venue.city:
        venueList.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows":num_upcoming_shows}]
        })
        currentCity = venue.city
      else: 
          venueList[- 1]["venues"].append({
            "id": venue.id,
            "name":venue.name,
            "num_upcoming_shows":num_upcoming_shows
          })
            
  return render_template('pages/venues.html', areas=venueList);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on artists with partial string search. Ensured it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venueSearchResults = Venue.query.filter(Venue.name.ilike('%' + request.form.get('search_term', '') + '%')).all()
  response={
    "count": len(venueSearchResults),
    "data": []
  }
  for venue in venueSearchResults:
    response["data"].append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": Show.query.filter(Show.venue_id==venue.id,Show.start_time>datetime.now()).count()
    })
    
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  upcoming_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time > datetime.now()).all()
  past_shows= Show.query.filter_by(venue_id=venue_id).filter(Show.start_time < datetime.now()).all()
  upcomingshowData = []
  pastShowData = []
  for show in upcoming_shows:
    upcomingshowData.append({
      "artist_id": show.Artist.id,
      "artist_name": show.Artist.name,
      "artist_image_link": show.Artist.image_link,
      "start_time": str(show.start_time)
    })
  for show in past_shows:
    pastShowData.append({
      "artist_id": show.Artist.id,
      "artist_name": show.Artist.name,
      "artist_image_link": show.Artist.image_link,
      "start_time": str(show.start_time)
    })
  d = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres.split(','),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "past_shows": pastShowData,
    "upcoming_shows": upcomingshowData,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)

  }
  
  return render_template('pages/show_venue.html', venue=d)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: insert form data as a new Venue record in the db, instead
    newVenue = Venue()
    error = False
  # DONE: modified data to be the data object returned from db insertion
    try:
        newVenue.name = request.form.get('name')
        newVenue.city = request.form.get('city')
        newVenue.state = request.form.get('state')
        newVenue.address = request.form.get('address')
        newVenue.phone = request.form.get('phone')
        newVenue.image_link = request.form.get('image_link')
        newVenue.facebook_link = request.form.get('facebook_link')
        newVenue.seeking_talent = True if request.form.get('seeking_talent')!= None else False
        newVenue.seeking_description = request.form.get('seeking_description')
        newVenue.website = request.form.get('website')
        newVenue.genres = ','.join(request.form.getlist('genres'))

        db.session.add(newVenue)
        db.session.commit()

  # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
        db.session.close()
        if(error):
            abort (400)
            
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods = ['DELETE'])
def delete_venue(venue_id):
  # DONE: endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venueDelete = Venue.query.get(venue_id)
        db.session.delete(venueDelete)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return venueDelete

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: real data returned from querying the database
  artist_data = Artist.query.all()
  data = []
  for artist in artist_data:
    data.append({
      "id":artist.id,
      "name":artist.name
    })
    
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensured it is case-insensitive.
  
  artistSearchResults = Artist.query.filter(Artist.name.ilike('%' + request.form.get('search_term', '') + '%')).all()
  response = {
    "count": len(artistSearchResults),
    "data": []
  }
  for artist in artistSearchResults:
    num_upcoming_shows = Show.query.filter(Show.artist_id==artist.id, Show.start_time>datetime.now()).count()
    response["data"].append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": num_upcoming_shows
    })
    
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  past_shows = Show.query.join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time<datetime.now()).all()
  upcoming_shows = Show.query.join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time>datetime.now()).all()
  past_shows_data=[]
  upcoming_shows_data = []
  for show in upcoming_shows:
    venue=Venue.query.get(show.venue_id)
    upcoming_shows_data.append({
      "venue_id":show.Venue.id,
      "venue_name":show.Venue.name,
      "venue_image_link":show.Venue.image_link,
      "start_time":str(show.start_time)
    })

  for show in past_shows:
    past_shows_data.append({
      "venue_id":show.Venue.id,
      "venue_name":show.Venue.name,
      "venue_image_link":show.Venue.image_link,
      "start_time":str(show.start_time)
    })

  artist_data = {
    "id": artist.id,
    "name": artist.name,
    "genres": [artist.genres],
    "city":artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows":past_shows_data,
    "upcoming_shows": upcoming_shows_data,
    "past_shows_count": len(past_shows_data),
    "upcoming_shows_count": len(upcoming_shows_data),
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods = ['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_data=Artist.query.get(artist_id)
  artist = {
    "id": artist_data.id,
    "name": artist_data.name,
    "genres": artist_data.genres.split(','),
    "city": artist_data.city,
    "state": artist_data.state,
    "phone": artist_data.phone,
    "website": artist_data.website,
    "facebook_link": artist_data.facebook_link,
    "seeking_venue": True,
    "seeking_description": artist_data.seeking_description,
    "image_link": artist_data.image_link
  }
  # DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error=False
  try:
    artistData = Artist.query.get(artist_id)
    
    artistData.name = request.form.get('name')
    artistData.genres = ','.join(request.form.getlist('genres'))
    artistData.city = request.form.get('city')
    artistData.state = request.form.get('state')
    artistData.phone = request.form.get('phone')
    artistData.facebook_link = request.form.get('facebook_link')
    artistData.image_link = request.form.get('image_link')
    artistData.website = request.form.get('website_link')
    artistData.seeking_venue = True if request.form.get('seeking_venue')!=None else False
    artistData.seeking_description = request.form.get('seeking_description')
    db.session.add(artistData)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods = ['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venueEdit = Venue.query.get(venue_id)
  venue = {
    "id": venueEdit.id,
    "name": venueEdit.name,
    "genres": venueEdit.genres.split(','),
    "address": venueEdit.address,
    "city": venueEdit.city,
    "state": venueEdit.state,
    "phone": venueEdit.phone,
    "website": venueEdit.website,
    "facebook_link": venueEdit.facebook_link,
    "seeking_talent": True if venueEdit.seeking_talent else False,
    "seeking_description": venueEdit.seeking_description,
    "image_link": venueEdit.image_link
  }
  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    error=False
    try:
        venueToBeUpdated=Venue.query.get(venue_id)

        venueToBeUpdated.name = request.form.get('name')
        venueToBeUpdated.genres = ','.join(request.form.getlist('genres'))
        venueToBeUpdated.city = request.form.get('city')
        venueToBeUpdated.address = request.form.get('address')
        venueToBeUpdated.state = request.form.get('state')
        venueToBeUpdated.phone = request.form.get('phone')
        venueToBeUpdated.facebook_link = request.form.get('facebook_link')
        venueToBeUpdated.image_link = request.form.get('image_link')
        venueToBeUpdated.website = request.form.get('website_link')
        venueToBeUpdated.seeking_talent = True if request.form.get('seeking_venue')!=None else False
        venueToBeUpdated.seeking_description = request.form.get('seeking_description')
        db.session.add(venueToBeUpdated)
        db.session.commit()
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
    newArtist = Artist()
    error=False
  # DONE: modified data to be the data object returned from db insertion
    try:
        newArtist.name = request.form.get('name')
        newArtist.city = request.form.get('city')
        newArtist.state = request.form.get('state')
        newArtist.phone = request.form.get('phone')
        newArtist.genres = ','.join(request.form.getlist('genres'))
        newArtist.image_link = request.form.get('image_link')
        newArtist.facebook_link = request.form.get('facebook_link')
        newArtist.website = request.form.get('website')
        newArtist.seeking_venue = True if request.form.get('seeking_venue')!=None else False
        newArtist.seeking_description = request.form.get('seeking_description')

        db.session.add(newArtist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Artist ' + newArtist.name + ' could not be listed.')
    finally:
        db.session.close()

  # on successful db insert, flash success
    
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: implemented real venues data.
  showsList = Show.query.join(Artist).join(Venue).all()
  sdata = []
  for show in showsList:
    sdata.append({
      "venue_id": show.venue_id,
      "venue_name": show.Venue.name,
      "artist_id": show.Artist.id,
      "artist_name":show.Artist.name,
      "artist_image_link": show.Artist.image_link,
      "start_time": str(show.start_time)
    })
    
  return render_template('pages/shows.html', shows = sdata)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form = form)

@app.route('/shows/create', methods = ['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: inserted form data as a new Show record in the db, instead
    error = False
    try:
        newShow = Show()
        newShow.artist_id = request.form.get('artist_id')
        newShow.venue_id = request.form.get('venue_id')
        newShow.start_time = request.form.get('start_time')
        db.session.add(newShow)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
  # on successful db insert, flash success
      
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
    app.debug=True

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
