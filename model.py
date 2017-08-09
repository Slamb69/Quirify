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
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    title = db.Column(db.String(75))

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<User id=%d fname=%s lname=%s email=%s>" % (self.user_id,
                                                            self.fname,
                                                            self.lname,
                                                            self.email)


class Provider(db.Model):
    """Provider model, source for the sheet music or media."""

    __tablename__ = "providers"

    # create the db columns.
    provider_id = db.Column(db.Integer,
                            primary_key=True,
                            autoincrement=True,
                            nullable=False)
    name = db.Column(db.String(50), nullable=False)

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Provider id=%d name=%s>" % (self.provider_id,
                                             self.name)


class Group(db.Model):
    """Group model, for each choir, band, trio, etc."""

    __tablename__ = "groups"

    # create the db columns.
    group_code = db.Column(db.String(4),
                           primary_key=True,
                           nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return "<Group code=%d name=%s>" % (self.group_code,
                                            self.name)


class Piece(db.Model):
    """Piece model, for each piece (sheet music)."""

    __tablename__ = "pieces"

    # create the db columns.
    piece_id = db.Column(db.Integer,
                         primary_key=True,
                         autoincrement=True,
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    provider_id = db.Column(db.Integer,
                            db.ForeignKey('providers.provider_id'),
                            nullable=False)
    name = db.Column(db.String(150), nullable=False)
    page_id = db.Column(db.Integer)
    music_url = db.Column(db.String(100))

    instrumentation = db.Column(db.String(100))

    # Define a relationship w/User class via user_id foreign key.
    user = db.relationship('User', backref='pieces')

    # Define a relationship w/Provider class via provider_id foreign key.
    provider = db.relationship('Provider', backref='pieces')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<Piece piece_id=%d, name=%s>" % (self.piece_id, self.name)


class Setlist(db.Model):
    """Setlist model."""

    __tablename__ = "setlists"

    # create the db columns.
    setlist_id = db.Column(db.Integer,
                           primary_key=True,
                           autoincrement=True,
                           nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    group_code = db.Column(db.String(4),
                           db.ForeignKey('groups.group_code'),
                           nullable=False)
    # Not sure on this - pull time estimates from individual pieces, so we can
    # compare to the below? Want to check against a target of actual MUSIC
    # duration (without) intermission & moving around, etc.
    target_duration = db.Column(db.Integer) # Is Int OK, or use "Time"??
    name = db.Column(db.String(30))
    notes = db.Column(db.String(200))

    # Define a relationship w/User class via user_id foreign key.
    user = db.relationship('User', backref='setlists')

    # Define a relationship w/Provider class via provider_id foreign key.
    group = db.relationship('Group', backref='setlists')

    # define repr function to print some useful info re:db objects.
    def __repr__(self):
        """Print more useful info."""
        return ("<Setlist setlist_id=%d, name=%s>" % (self.piece_id, self.name)



# End Part 1


##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print "Connected to DB."


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///animals'
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

    connect_to_db(app)
    print "Connected to DB."
