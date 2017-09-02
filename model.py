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


class Group(db.Model):
    """Group model, for each choir, small group, band, trio, etc."""

    __tablename__ = "groups"

    # create the db columns.
    group_code = db.Column(db.String(48),
                           primary_key=True,
                           nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(2048))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Group code=%s name=%s>" % (self.group_code,
                                            self.name)


class Owner(db.Model):
    """Owner model, owner/license holder for piece."""

    __tablename__ = "owners"

    #create the db columns.
    owner_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
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
                             autoincrement=True)
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
    """Performer's Instruments model, association for instruments for each 
       performer."""

    __tablename__ = "performer_instruments"

    # create the db columns.
    pi_id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
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


class PerformerGroup(db.Model):
    """PerformerGroup model, association for performers in specific groups
       (rosters)."""

    __tablename__ = "performer_groups"

    # create the db columns.
    perf_group_id = db.Column(db.Integer,
                              primary_key=True,
                              autoincrement=True)
    group_code = db.Column(db.String(48),
                           db.ForeignKey('groups.group_code'),
                           nullable=False)
    performer_id = db.Column(db.Integer,
                             db.ForeignKey('performers.performer_id'),
                             nullable=False)

    # Define a relationship w/Group class via group_code foreign key.
    group = db.relationship('Group', backref='performer_groups')

    # Define a relationship w/Performer class via performer_id foreign key.
    performer = db.relationship('Performer', backref='performer_groups')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<performer_group id=%d name=%s>" % (self.performer_group_id, self.name)


class Provider(db.Model):
    """Provider model, source for the sheet music or media."""

    __tablename__ = "providers"

    # create the db columns.
    provider_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    name = db.Column(db.String(96), nullable=False)

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Provider id=%d name=%s>" % (self.provider_id, self.name)


class Piece(db.Model):
    """Piece model, for each piece (can have multiple editions)."""

    __tablename__ = "pieces"

    # create the db columns.
    piece_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    # page_id = this is from CPDL API, they have "page id" that is useful! create
    # a disparate "page id" system for uploads, like initial letter(s)? #########
    page_id = db.Column(db.Integer)
    composer = db.Column(db.String(248), nullable=False)
    lyricist = db.Column(db.String(248))
    publication_year = db.Column(db.String(56))
    original_num_voices = db.Column(db.Integer)
    original_voicing = db.Column(db.String(56))
    original_language = db.Column(db.String(56))
    original_instrumentation = db.Column(db.String(248))
    text_original = db.Column(db.String(2048))
    text_english = db.Column(db.String(2048))
    description = db.Column(db.String(2048))

    # Function to check whether a piece is in the session user's library.
    def is_users_piece(self, user_id):
        """checks if a user is associated with this piece."""

        is_found = False

        for upiece in self.user_pieces:
            if upiece.user_id == user_id:
                is_found = True

        return is_found


    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Piece piece_id=%d title=%s composer=%s>" % (self.piece_id,
                                                             self.title,
                                                             self.composer)


class SheetMusic(db.Model):
    """The sheet music for a particular edition/version of a piece."""

    __tablename__ = "sheets"

    # create the db columns.
    sheet_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    # ASK = OK for this FK to be nullable? (piece not yet owned/borrowed...)
    piece_id = db.Column(db.Integer,
                         db.ForeignKey('pieces.piece_id'))
    music_url = db.Column(db.String(248))
    cpdl_num = db.Column(db.String(10))
    editor = db.Column(db.String(248))
    edition_notes = db.Column(db.String(596),
                              nullable=False)
    arranger = db.Column(db.String(248))
    num_voices = db.Column(db.Integer)
    voicing = db.Column(db.String(248))
    instrumentation = db.Column(db.String(248))
    language = db.Column(db.String(48))
    alt_language = db.Column(db.String(48))
    key = db.Column(db.String(48))
    time_signature = db.Column(db.String(48))
    tempo = db.Column(db.String(128))
    score_type = db.Column(db.String(248))
    license_type = db.Column(db.String(40))
    num_lic_owned = db.Column(db.Integer)
    # price_per = db.Column(db.??type?) ?????????Add this later, maybe?

    # Define a relationship w/Piece class via piece_id foreign key.
    piece = db.relationship('Piece', backref='sheets')

    # Function to check whether a sheet is in the session user's library.
    def is_users_sheet(self, user_id):
        """checks if a user is associated with this sheet."""

        is_found = False

        for usheet in self.user_sheets:
            if usheet.user_id == user_id:
                is_found = True

        return is_found

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Sheet id=%d title=%s>" % (self.sheet_id,
                                           self.piece.title)


class AudioFile(db.Model):
    """Holds any midi or other sound files for the piece (you tube also okay)."""

    __tablename__ = "audiofiles"

    # create the db columns.
    file_id = db.Column(db.Integer,
                        primary_key=True,
                        autoincrement=True)
    sheet_id = db.Column(db.Integer,
                         db.ForeignKey('sheets.sheet_id'),
                         nullable=False)
    file_type = db.Column(db.String(48),
                          nullable=False)
    voicing_details = db.Column(db.String(248))
    url = db.Column(db.String(248))

    # Define a relationship w/Sheet class via sheet_id foreign key.
    sheet = db.relationship('SheetMusic', backref='audiofiles')

    # Function to check whether a file is in the session user's library.
    def is_users_file(self, user_id):
        """checks if a user is associated with this file."""

        is_found = False

        for ufile in self.user_files:
            if ufile.user_id == user_id:
                is_found = True

        return is_found

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<File id=%d sheet=%s type=%s>" % (self.file_id,
                                                  self.sheet.sheet_id,
                                                  self.file_type)


class Genre(db.Model):
    """Genre model."""

    __tablename__ = "genres"

    #create the db columns.
    genre_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    name = db.Column(db.String(248),
                     nullable=False)

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Genre id=%s name=%s>" % (self.genre_id,
                                          self.name)


class PieceGenre(db.Model):
    """Piece & its Genres association model."""

    __tablename__ = "piece_genres"

    #create the db columns.
    pg_id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    genre_id = db.Column(db.Integer,
                         db.ForeignKey('genres.genre_id'))
    piece_id = db.Column(db.Integer,
                         db.ForeignKey('pieces.piece_id'))

    # Define a relationship w/Piece class via piece_id foreign key.
    piece = db.relationship('Piece', backref='piece_genres')

    # Define a relationship w/Genre class via genre_id foreign key.
    genre = db.relationship('Genre', backref='piece_genres')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Piece Genres piece=%s genre=%s>" % (self.piece.title,
                                                     self.genre.name)


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
    name = db.Column(db.String(128),
                     nullable=False)
    description = db.Column(db.String(2048))
    # ???? Add more meta data re: tix, attire, etc?

    # Define a relationship w/User class via user_id foreign key.
    user = db.relationship('User', backref='concerts')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Concert id=%d name=%s>" % (self.concert_id, self.name)


class Setlist(db.Model):
    """Setlist model. Association of Sheet Music for a Concert. Setlist can apply
       to various events & have various performer/instrument assignments at each
       event."""

    __tablename__ = "setlists"

    # create the db columns.
    setlist_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    sheet_id = db.Column(db.Integer,
                         db.ForeignKey('sheets.sheet_id'),
                         nullable=False)
    concert_id = db.Column(db.Integer,
                           db.ForeignKey('concerts.concert_id'),
                           nullable=False)
    sheet_finalized = db.Column(db.Boolean)

    # Define a relationship w/Sheet class via sheet_id foreign key.
    sheet = db.relationship('SheetMusic', backref='setlists')

    # Define a relationship w/Concert class via concert_id foreign key.
    concert = db.relationship('Concert', backref='setlists')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<Setlist id=%d concert=%s, sheet=%s>" % (self.setlist_id,
                                                          self.concert.name,
                                                          self.sheet.sheet_id))


class Event(db.Model):
    """Event model, a specific Concert + Setlist."""

    __tablename__ = "events"

    # create the db columns.
    event_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True)
    concert_id = db.Column(db.Integer,
                           db.ForeignKey('concerts.concert_id'))
    name = db.Column(db.String(128))
    location = db.Column(db.String(256))
    start_day_time = db.Column(db.DateTime)
    end_day_time = db.Column(db.DateTime)
    # ???? Add re: site-or-day-specific stuff, or just this logistics field?
    event_logistics = db.Column(db.String(2048))

    # Define a relationship w/Concert class via concert_id foreign key.
    concert = db.relationship('Concert', backref='events')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<Event id=%d location=%s start_day_time=%s>"
                % (self.event_id, self.location, self.start_day_time))


class Assignment(db.Model):
    """Assignment model, association of specific performer/instruments for each
       sheet."""

    __tablename__ = "assignments"

    # create the db columns.
    assignment_id = db.Column(db.Integer,
                              primary_key=True,
                              autoincrement=True)
    sheet_id = db.Column(db.Integer,
                         db.ForeignKey('sheets.sheet_id'),
                         nullable=False)
    pi_id = db.Column(db.Integer,
                      db.ForeignKey('performer_instruments.pi_id'))

    # Define a relationship w/SheetMusic class via sheet_id foreign key.
    sheet = db.relationship('SheetMusic', backref='assignments')

    # Define a relationship w/PerformerInstument class via pi_id foreign key.
    performer_instrument = db.relationship('PerformerInstrument',
                                           backref='assignments')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<Assignment id=%d, sheet_id=%d, pi_id=%d>" %
                (self.assignment_id,
                 self.sheet.sheet_id,
                 self.performer_instrument.pi_id))


class EventAssignment(db.Model):
    """Assigned set model. Association table."""

    __tablename__ = "event_assignments"

    # create the db columns.
    evtassign_id = db.Column(db.Integer,
                             primary_key=True,
                             autoincrement=True)
    assignment_id = db.Column(db.Integer,
                              db.ForeignKey('assignments.assignment_id'),
                              nullable=False)
    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.event_id'),
                         nullable=False)
    notes = db.Column(db.String(248))

    # Define a relationship w/Assignment class via assignment_id foreign key.
    assignment = db.relationship('Assignment', backref='event_assignments')

    # Define a relationship w/Setlist class via setlist_id foreign key.
    event = db.relationship('Event', backref='event_assignments')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<Event Assignment id=%d, event_id=%d, assignment_id=%d>"
                % (self.evtassign_id,
                   self.event.event_id,
                   self.assignment.assignment_id))


class SheetMusicProvider(db.Model):
    """A sheet music object's provider (source) - association table."""

    __tablename__ = "sheet_providers"

    # create the db columns.
    shtprov_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True)
    sheet_id = db.Column(db.Integer,
                         db.ForeignKey('sheets.sheet_id'))
    provider_id = db.Column(db.Integer,
                            db.ForeignKey('providers.provider_id'))

    # Define a relationship w/SheetMusic class via sheet_id foreign key.
    sheet = db.relationship('SheetMusic', backref='sheet_providers')

    # Define a relationship w/Provider class via provider_id foreign key.
    provider = db.relationship('Provider', backref='sheet_providers')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<Sheet Provider id=%d, sheet_id=%d, provider_id=%d>" %
                (self.shtprov_id, self.sheet.sheet_id, self.provider.provider_id))


class SheetMusicOwner(db.Model):
    """A sheet music object's owner (license holder) - association table."""

    __tablename__ = "sheet_owners"

    # create the db columns.
    shtowner_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True)
    sheet_id = db.Column(db.Integer,
                         db.ForeignKey('sheets.sheet_id'))
    owner_id = db.Column(db.Integer,
                         db.ForeignKey('owners.owner_id'))

    # Define a relationship w/Sheet class via sheet_id foreign key.
    sheet = db.relationship('SheetMusic', backref='sheet_owners')

    # Define a relationship w/Owner class via owner_id foreign key.
    owner = db.relationship('Owner', backref='sheet_owners')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<Sheet Owner id=%d, sheet_id=%d, owner_id=%d>" %
                (self.shtowner_id, self.sheet.sheet_id, self.owner.owner_id))

################# ASSOCIATION TABLES FOR SAVING TO USER ####################


class UserPiece(db.Model):
    """User piece object, associating each user with their pieces."""

    __tablename__ = "user_pieces"

    # create the db columns.
    up_id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    piece_id = db.Column(db.Integer,
                         db.ForeignKey('pieces.piece_id'),
                         nullable=False)

    # Define a relationship w/User class via user_id foreign key.
    user = db.relationship('User', backref='user_pieces')

    # Define a relationship w/Piece class via piece_id foreign key.
    piece = db.relationship('Piece', backref='user_pieces')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<User Piece f=%s l=%s piece=%s>" % (self.user.fname,
                                                    self.user.lname,
                                                    self.piece.title)


class UserSheet(db.Model):
    """User sheet object, associating each user with their sheets (of music)."""

    __tablename__ = "user_sheets"

    # create the db columns.
    us_id = db.Column(db.Integer,
                      primary_key=True,
                      autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    sheet_id = db.Column(db.Integer,
                         db.ForeignKey('sheets.sheet_id'),
                         nullable=False)

    # Define a relationship w/User class via user_id foreign key.
    user = db.relationship('User', backref='user_sheets')

    # Define a relationship w/SheetMusic class via sheet_id foreign key.
    sheet = db.relationship('SheetMusic', backref='user_sheets')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<User Sheet f=%s l=%s sheet=%s>" % (self.user.fname,
                                                    self.user.lname,
                                                    self.sheet.version_description)


class UserAudioFile(db.Model):
    """User AudioFile object, associating each user with their audio (youtube)
       files."""

    __tablename__ = "user_files"

    # create the db columns.
    uaf_id = db.Column(db.Integer,
                       primary_key=True,
                       autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    file_id = db.Column(db.Integer,
                        db.ForeignKey('audiofiles.file_id'),
                        nullable=False)

    # Define a relationship w/User class via user_id foreign key.
    user = db.relationship('User', backref='user_files')

    # Define a relationship w/AudioFile class via file_id foreign key.
    audiofile = db.relationship('AudioFile', backref='user_files')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<User File f=%s l=%s file=%s>" % (self.user.fname,
                                                  self.user.lname,
                                                  self.file.file_type)


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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///musictest'
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
