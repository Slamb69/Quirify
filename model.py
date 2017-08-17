"""Models and database functions for music db."""

from flask_sqlalchemy import SQLAlchemy

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Part 1: Compose ORM

class User(db.Model):
    """User model."""

    __tablename__ = "users"

    # create the db columns.
    user_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True,
                        nullable=False)
    fname = db.Column(db.String(48), nullable=False)
    lname = db.Column(db.String(48), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    title = db.Column(db.String(128))
    phone = db.Column(db.String(48))

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<User id=%d fname=%s lname=%s email=%s>" % (self.user_id,
                                                            self.fname,
                                                            self.lname,
                                                            self.email)


class PerformanceGroup(db.Model):
    """Group model, for each choir, small group, band, trio, etc."""

    __tablename__ = "performance_groups"

    # create the db columns.
    perf_group_code = db.Column(db.String(48),
                                primary_key=True,
                                nullable=False)
    # user_id = db.Column(db.Integer,
    #                     db.ForeignKey('users.user_id'),
    #                     nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(2048))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    # # Define a relationship w/User class via user_id foreign key.
    # user = db.relationship('User', backref='perf_groups')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<PerformanceGroup code=%s name=%s>" % (self.perf_group_code,
                                                       self.name)


# ????????? ASK ABOUT THIS - how best to do it - one-one w/user, group? if so,
# do I still use foreign key? Want to allow for other owners...if borrowing!!)
class Owner(db.Model):
    """Owner model, owner/license holder for piece."""

    __tablename__ = "owners"

    #create the db columns.
    owner_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True,
                         nullable=False)
    name = db.Column(db.String(128), nullable=False)
    contact = db.Column(db.String(128))

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Owner id=%d name=%s contact=%s>" % (self.owner_id,
                                                     self.fname,
                                                     self.contact)


class Performer(db.Model):
    """Performer model."""

    __tablename__ = "performers"

    #create the db columns.
    performer_id = db.Column(db.Integer,
                             primary_key=True,
                             autoincrement=True,
                             nullable=False)
    fname = db.Column(db.String(128), nullable=False)
    lname = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))
    phone = db.Column(db.String(48))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    hourly_rate = db.Column(db.Integer)
    notes = db.Column(db.String(2048))

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Performer id=%d fname=%s lname=%s>" % (self.performer_id,
                                                        self.fname,
                                                        self.lname)


class Instrument(db.Model):
    """Instrument model - voice types and/or instruments played."""

    __tablename__ = "instruments"

    #create the db columns.
    instrument_code = db.Column(db.String(48),
                                primary_key=True,
                                nullable=False)
    name = db.Column(db.String(128), nullable=False)

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Instrument id=%s name=%s>" % (self.instrument_code,
                                               self.name)


class PerformerInstrument(db.Model):
    """Performer's Instruments model, all instruments for each performer."""

    __tablename__ = "performer_instruments"

    # create the db columns.
    pi_id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True,
                      nullable=False)
    performer_id = db.Column(db.Integer,
                             db.ForeignKey('performers.performer_id'))
    instrument_code = db.Column(db.String(48),
                                db.ForeignKey('instruments.instrument_code'))

    # Define a relationship w/Performer class via performer_id foreign key.
    performer = db.relationship('Performer', backref='performer_instruments')

    # Define a relationship w/Instrument class via instrument_code foreign key.
    instrument = db.relationship('Instrument', backref='performer_instruments')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<PerformerInstrument pi_id=%d perf_id=%s inst_code=%s>"
                % (self.piece_id, self.performer_id, self.instrument_code))


class Roster(db.Model):
    """Roster model, performers in specific groups."""

    __tablename__ = "rosters"

    # create the db columns.
    roster_id = db.Column(db.Integer,
                          primary_key=True,
                          autoincrement=True)
    perf_group_code = db.Column(db.String(48),
                                db.ForeignKey('performance_groups.perf_group_code'),
                                nullable=False)
    performer_id = db.Column(db.Integer,
                             db.ForeignKey('performers.performer_id'),
                             nullable=False)
    name = db.Column(db.String(128), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    # Define a relationship w/PerformanceGroup class via perf_group_code foreign key.
    perf_group = db.relationship('PerformanceGroup', backref='rosters')

    # Define a relationship w/Performer class via performer_id foreign key.
    performer = db.relationship('Performer', backref='rosters')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Roster id=%d name=%s>" % (self.roster_id, self.name)


class Provider(db.Model):
    """Provider model, source for the sheet music or media."""

    __tablename__ = "providers"

    # create the db columns.
    provider_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Provider id=%d name=%s>" % (self.provider_id, self.name)


class SoundFiles(db.Model):
    """Holds any midi or other sound files for the piece."""
        # create the db columns.
    file_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    piece_id = db.Column(db.Integer,
                         db.ForeignKey('pieces.piece_id'),
                         nullable=False)

    # Define a relationship w/Piece class via piece_id foreign key.
    piece = db.relationship('Piece', backref='sound_files')


class Piece(db.Model):
    """Piece model, for each piece (sheet music)."""

    __tablename__ = "pieces"

    # create the db columns.
    piece_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    # ASK = OK for this FK to be nullable? (piece not yet owned/borrowed...)
    owner_id = db.Column(db.Integer,
                         db.ForeignKey('owners.owner_id'))
    provider_id = db.Column(db.Integer,
                            db.ForeignKey('providers.provider_id'),
                            nullable=False)
    title = db.Column(db.String(150), nullable=False)
    # page_id = this is from CPDL API, they have "page id" that is useful!
    page_id = db.Column(db.Integer)
    cpdl_num = db.Column(db.String(5))
    music_url = db.Column(db.String(150))
    genre = (db.String(248))             # ??? NEEDS GENRE TABLE?
    composer = db.Column(db.String(248), nullable=False)
    lyricist = db.Column(db.String(248))
    arranger = db.Column(db.String(248))
    publication_year = db.Column(db.String(48))
    original_language = db.Column(db.String(48))
    voicing = db.Column(db.String(248))
    instrumentation = db.Column(db.String(248))
    key = db.Column(db.String(48))
    time_signature = (db.String(48))
    tempo = db.Column(db.String(128))
    text_original = db.Column(db.String(2048))
    text_english = db.Column(db.String(2048))
    score_type = db.Column(db.String(248))
    license_type = db.Column(db.String(40))
    num_lic_owned = db.Column(db.Integer)
    description = (db.String(2048))
    # price_per = db.Column(db.???) ?????????Add this later, maybe - type?

    # Define a relationship w/Owner class via owner_id foreign key.
    owner = db.relationship('Owner', backref='pieces')

    # Define a relationship w/Provider class via provider_id foreign key.
    provider = db.relationship('Provider', backref='pieces')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Piece piece_id=%d title=%s composer=%s>" % (self.piece_id,
                                                             self.title,
                                                             self.composer)


class Assignment(db.Model):
    """Assignment model, specific performer/instrument for each piece."""

    __tablename__ = "assignments"

    # create the db columns.
    assignment_id = db.Column(db.Integer,
                              primary_key=True,
                              autoincrement=True)
    piece_id = db.Column(db.Integer,
                         db.ForeignKey('pieces.piece_id'),
                         nullable=False)
    roster_id = db.Column(db.Integer,
                          db.ForeignKey('rosters.roster_id'),
                          nullable=False)
    pi_id = db.Column(db.Integer,
                      db.ForeignKey('performer_instruments.pi_id'))

    # Define a relationship w/Piece class via piece_id foreign key.
    piece = db.relationship('Piece', backref='assignments')

    # Define a relationship w/Roster class via roster_id foreign key.
    roster = db.relationship('Roster', backref='assignments')

    # Define a relationship w/PerformerInstument class via pi_id foreign key.
    performer_instrument = db.relationship('PerformerInstrument',
                                           backref='assignments')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Assignment assignment_id=%d>" % (self.assignment_id)


class Setlist(db.Model):
    """Setlist model. Setlist can be used at various events & with various
       setlist assignments."""

    __tablename__ = "setlists"

    # create the db columns.
    setlist_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    name = db.Column(db.String(64))
    notes = db.Column(db.String(200))

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Setlist setlist_id=%d name=%s>" % (self.setlist_id, self.name)


class AssignedSet(db.Model):
    """Assigned set model. Association table."""

    __tablename__ = "assigned_sets"

    # create the db columns.
    as_id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    assignment_id = db.Column(db.Integer,
                              db.ForeignKey('assignments.assignment_id'),
                              nullable=False)
    setlist_id = db.Column(db.Integer,
                           db.ForeignKey('setlists.setlist_id'),
                           nullable=False)

    # Define a relationship w/Assignment class via assignment_id foreign key.
    assignment = db.relationship('Assignment', backref='assigned_sets')

    # Define a relationship w/Setlist class via setlist_id foreign key.
    setlist = db.relationship('Setlist', backref='assigned_sets')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<AssignedSet as_id=%d>" % (self.as_id)


class Concert(db.Model):
    """Concert object. Can have several events in one concert series."""

    __tablename__ = "concerts"

    # create the db columns.
    concert_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    name = db.Column(db.String(64))
    description = db.Column(db.String(2048))

    # Define a relationship w/User class via user_id foreign key.
    user = db.relationship('User', backref='concerts')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Concert concert_id=%d name=%s>" % (self.concert_id, self.name)


class Event(db.Model):
    """Event model, a specific Concert + Setlist."""

    __tablename__ = "events"

    # create the db columns.
    event_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True,
                         nullable=False)
    concert_id = db.Column(db.Integer,
                           db.ForeignKey('concerts.concert_id'))
    setlist_id = db.Column(db.Integer,
                           db.ForeignKey('setlists.setlist_id'))
    name = db.Column(db.String(64))
    location = db.Column(db.String(256))
    start_day_time = db.Column(db.DateTime)
    end_day_time = db.Column(db.DateTime)
    # ???? Add more meta data re: tix, site-specific stuff, or just notes field?

    # Define a relationship w/Concert class via concert_id foreign key.
    concert = db.relationship('Concert', backref='events')

    # Define a relationship w/Setlist class via setlist_id foreign key.
    setlist = db.relationship('Setlist', backref='events')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<Event event_id=%d location=%s start_day_time=%s>"
                % (self.event_id, self.location, self.start_day_time))


# End Part 1


##############################################################################
# Helper functions

def init_app():
#     # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."

# Configure to use our PostgreSQL database.
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///music'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    # from server import app

    connect_to_db(app)
    print "Connected to DB."

    # create db from this model.
    db.create_all()
