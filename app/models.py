from . import db


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    actors = db.Column(db.UnicodeText, nullable=True)
    also_known_as = db.Column(db.UnicodeText, nullable=True)
    country = db.Column(db.UnicodeText, nullable=True)
    directors = db.Column(db.UnicodeText, nullable=True)
    film_locations = db.Column(db.UnicodeText, nullable=True)
    genres = db.Column(db.UnicodeText, nullable=True)
    language = db.Column(db.UnicodeText, nullable=True)
    plot_simple = db.Column(db.UnicodeText, nullable=True)
    poster = db.Column(db.UnicodeText, nullable=True)
    rating = db.Column(db.UnicodeText, nullable=True)
    rating_count = db.Column(db.UnicodeText, nullable=True)
    release_date = db.Column(db.UnicodeText, nullable=True)
    runtime = db.Column(db.UnicodeText, nullable=True)
    title = db.Column(db.UnicodeText, unique=True, index=True)
    type = db.Column(db.UnicodeText, nullable=True)
    writers = db.Column(db.UnicodeText, nullable=True)
    year = db.Column(db.UnicodeText, nullable=True)
    cinemas = db.relationship('Release', back_populates='movie')

    def __repr__(self):
        return "<Movie(id='%d', title='%s')>" % (self.id, self.title)


class Cinema(db.Model):
    __tablename__ = 'cinemas'
    id = db.Column(db.Integer, primary_key=True)
    cityName = db.Column(db.UnicodeText, nullable=True)
    cinemaName = db.Column(db.UnicodeText, unique=True, index=True)
    address = db.Column(db.UnicodeText, nullable=True)
    telephone = db.Column(db.UnicodeText, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    trafficRoutes = db.Column(db.UnicodeText, nullable=True)
    movies = db.relationship('Release', back_populates='cinema')

    def __repr__(self):
        return "<Cinema(id='%d', cinemaName='%s')>" % (self.id, self.cinemaName)


class Release(db.Model):
    __tablename__ = 'releases'
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinemas.id'), primary_key=True)
    broadcasts = db.relationship('Broadcast', backref='release')
    movie = db.relationship('Movie', back_populates='cinemas')
    cinema = db.relationship('Cinema', back_populates='movies')

    def __repr__(self):
        return "<Release(movie_id='%d', cinema_id='%d')>" \
               % (self.movie_id, self.cinema_id)


class Broadcast(db.Model):
    __tablename__ = 'broadcasts'
    id = db.Column(db.Integer, primary_key=True)
    hall = db.Column(db.UnicodeText)
    price = db.Column(db.UnicodeText)
    time = db.Column(db.UnicodeText)
    movie_id = db.Column(db.Integer)
    cinema_id = db.Column(db.Integer)
    __table_args__ = (db.ForeignKeyConstraint(['movie_id', 'cinema_id'],
                                              ['releases.movie_id', 'releases.cinema_id']),
                      {})
    seats = db.relationship('Seat', backref='broadcast')

    def __repr__(self):
        return "<Broadcast(id='%d', time='%s')>" % (self.id, self.time)


class Seat(db.Model):
    __tablename__ = 'seats'
    broadcast_id = db.Column(db.Integer, db.ForeignKey('broadcasts.id'), primary_key=True)
    row = db.Column(db.Integer, primary_key=True)
    col = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "<Seat(broadcast_id='%s', row='%d', col='%d')>" \
               % (self.broadcast_id, self.row, self.col)
