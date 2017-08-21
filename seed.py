"""Utility file to seed music database from test data files that I created. """

import datetime
# from sqlalchemy import func

from model import (User, Concert, Event, Instrument, Owner, PerformanceGroup,
                   Performer, Piece, PieceFile, Provider, Setlist, SheetMusic,
                   Roster, PerformerInstrument, Assignment, AssignedSet,
                   connect_to_db, db)
from server import app


def load_users():
    """Load users from user.txt into database."""

    print "Users"

    for i, row in enumerate(open("data/user.txt")):
        row = row.rstrip()
        fname, lname, email, password, title, phone = row.split(", ")

        user = User(fname=fname,
                    lname=lname,
                    email=email,
                    password=password,
                    phone=phone)

        # Add to the session.
        db.session.add(user)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_performance_groups():
    """Load performance groups from perfgroup.txt into database."""

    print "Performance Groups"

    for i, row in enumerate(open("data/perfgroup.txt")):
        row = row.rstrip()

        perf_group_code, name, description, end, start = row.split(", ")

        start_date = datetime.datetime.strptime(start, "%m/%d/%Y")

        if end:
            end_date = datetime.datetime.strptime(end, "%m/%d/%Y")
        else:
            end_date = None

        perfgroup = PerformanceGroup(perf_group_code=perf_group_code,
                                     name=name,
                                     description=description,
                                     start_date=start_date,
                                     end_date=end_date)

        # Add to the session.
        db.session.add(perfgroup)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_owners():
    """Load owners from owner.txt into database."""

    print "Owners"

    for i, row in enumerate(open("data/owner.txt")):
        row = row.rstrip()

        name, contact = row.split(", ")

        owner = Owner(name=name,
                      contact=contact)

        # Add to the session.
        db.session.add(owner)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_performers():
    """Load performers from performer.txt into database."""

    print "Performers"

    for i, row in enumerate(open("data/performer.txt")):
        row = row.rstrip()

        fname, lname, email, phone, start, end, rate, notes = row.split("| ")

        start_date = datetime.datetime.strptime(start, "%m/%d/%Y")

        if end:
            end_date = datetime.datetime.strptime(end, "%m/%d/%Y")
        else:
            end_date = None

        # Convert hourly rate to cents, to store as an integer in dbase.
        if rate:
            hourly_rate = int(float(rate) * 100)
        else:
            hourly_rate = None

        performer = Performer(fname=fname,
                              lname=lname,
                              email=email,
                              phone=phone,
                              start_date=start_date,
                              end_date=end_date,
                              hourly_rate=hourly_rate,
                              notes=notes)

        # Add to the session.
        db.session.add(performer)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_instruments():
    """Load instruments from instrument.txt into database."""

    print "Instruments"

    for i, row in enumerate(open("data/instrument.txt")):
        row = row.rstrip()

        instrument_code, name = row.split(", ")

        instrument = Instrument(instrument_code=instrument_code,
                                name=name)

        # Add to the session.
        db.session.add(instrument)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_performer_instruments():
    """Load performer_instruments from perfinstrument.txt into database."""

    print "Performer Instruments"

    for i, row in enumerate(open("data/perfinstrument.txt")):
        row = row.rstrip()

        performer_id, instrument_code = row.split(", ")

        perfinstrument = PerformerInstrument(performer_id=performer_id,
                                             instrument_code=instrument_code)

        # Add to the session.
        db.session.add(perfinstrument)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_rosters():
    """Load rosters from roster.txt into database."""

    print "Rosters"

    for i, row in enumerate(open("data/roster.txt")):
        row = row.rstrip()

        perf_group_code, performer_id, name = row.split(", ")

        roster = Roster(perf_group_code=perf_group_code,
                        performer_id=performer_id,
                        name=name)

        # Add to the session.
        db.session.add(roster)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_providers():
    """Load providers from provider.txt into database."""

    print "Providers"

    for i, name in enumerate(open("data/provider.txt")):
        name = name.rstrip()

        provider = Provider(name=name)

        # Add to the session.
        db.session.add(provider)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_pieces():
    """Load pieces from piece.txt into database."""

    print "Pieces"

    for i, row in enumerate(open("data/piece.txt")):
        row = row.rstrip()

        title, pg_id, genre, comp, lyric, pub_yr, ovoice, okey, lang = row.split(", ")

        piece = Piece(title=title,
                      page_id=pg_id,
                      genre=genre,
                      composer=comp,
                      lyricist=lyric,
                      publication_year=pub_yr,
                      original_voicing=ovoice,
                      original_key=okey,
                      original_language=lang)

        # Add to the session.
        db.session.add(piece)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_sheets():
    """Load sheet music from sheet.txt into database."""

    print "Sheet Music"

    for i, row in enumerate(open("data/sheet.txt")):
        row = row.rstrip()

        (pid, oid, prid, url, cpdl, ed, vc, inst,
         lang, key, time, scr, lic) = row.split(", ")

        sheet = SheetMusic(piece_id=pid,
                           owner_id=oid,
                           provider_id=prid,
                           music_url=url,
                           cpdl_num=cpdl,
                           editor=ed,
                           voicing=vc,
                           instrumentation=inst,
                           language=lang,
                           key=key,
                           time_signature=time,
                           score_type=scr,
                           license_type=lic)

        # Add to the session.
        db.session.add(sheet)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_piecefiles():
    """Load piece (audio) files from piecefile.txt into database."""

    print "Piece Files"

    for i, row in enumerate(open("data/piecefile.txt")):
        row = row.rstrip()

        sheet_id, description = row.split(", ")

        piecefile = PieceFile(sheet_id=sheet_id,
                              description=description)

        # Add to the session.
        db.session.add(piecefile)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_assignments():
    """Load assignments from assignment.txt into database."""

    print "Assignments"

    for i, row in enumerate(open("data/assignment.txt")):
        row = row.rstrip()

        sheet_id, roster_id, pi_id = row.split(", ")

        assignment = Assignment(sheet_id=sheet_id,
                                roster_id=roster_id,
                                pi_id=pi_id)

        # Add to the session.
        db.session.add(assignment)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_setlists():
    """Load setlists from setlist.txt into database."""

    print "Setlists"

    for i, row in enumerate(open("data/setlist.txt")):
        row = row.rstrip()

        name, notes = row.split("| ")

        setlist = Setlist(name=name,
                          notes=notes)

        # Add to the session.
        db.session.add(setlist)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_assigned_sets():
    """Load setlists from setlist.txt into database."""

    print "Assigned Sets"

    for i, row in enumerate(open("data/assignset.txt")):
        row = row.rstrip()

        assignment_id, setlist_id = row.split(", ")

        assignset = AssignedSet(assignment_id=assignment_id,
                                setlist_id=setlist_id)

        # Add to the session.
        db.session.add(assignset)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_concerts():
    """Load concerts from concert.txt into database."""

    print "Concerts"

    for i, row in enumerate(open("data/concert.txt")):
        row = row.rstrip()

        user_id, name, description = row.split(", ")

        concert = Concert(user_id=user_id,
                          name=name,
                          description=description)

        # Add to the session.
        db.session.add(concert)

    # Commit the session/data to the dbase.
    db.session.commit()


def load_events():
    """Load events from event.txt into database."""

    print "Events"

    for i, row in enumerate(open("data/event.txt")):
        row = row.rstrip()

        concert_id, setlist_id, name, location, start, end = row.split(", ")

        start_day_time = datetime.datetime.strptime(start, "%b-%d-%Y-%H:%M")
        end_day_time = datetime.datetime.strptime(end, "%b-%d-%Y-%H:%M")

        event = Event(concert_id=concert_id,
                      setlist_id=setlist_id,
                      name=name,
                      location=location,
                      start_day_time=start_day_time,
                      end_day_time=end_day_time)

        # Add to the session.
        db.session.add(event)

    # Commit the session/data to the dbase.
    db.session.commit()

#  ??????????? USE TEST DB, OR DO I NEED THE BELOW FOR ALL INT PKs? ?????????????
#
# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_performance_groups()
    load_owners()
    load_performers()
    load_instruments()
    load_performer_instruments()
    load_rosters()
    load_providers()
    load_pieces()
    load_sheets()
    load_piecefiles()
    load_assignments()
    load_setlists()
    load_assigned_sets()
    load_concerts()
    load_events()

    # set_val_user_id()
