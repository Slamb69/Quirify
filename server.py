"""Music Project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Concert, Event, Instrument, Owner, PerformanceGroup,
                   Performer, Piece, AudioFile, Provider, Setlist, SheetMusic,
                   Roster, PerformerInstrument, Assignment, AssignedSet,
                   connect_to_db, db)

import requests
# To get text from CPDL pages, need Beautiful Soup!!
from bs4 import BeautifulSoup
# For Beautiful Soup, need lxml's html
from lxml import html
# For Beautiful Soup, need regex
import re

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form.get("email")
    password = request.form.get("password")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    title = request.form.get("title")
    phone = request.form.get("phone")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("User already exists, please log in.")
        return redirect("/register")  # NOTE = currently reg/login on SAME page
    else:
        user = User(email=email,
                    password=password,
                    fname=fname,
                    lname=lname,
                    title=title,
                    phone=phone)

        db.session.add(user)
        db.session.commit()

        session["user_id"] = user.user_id

        flash("User %s added." % email)
        return redirect("/users/%s" % user.user_id)


# @app.route('/login', methods=['GET'])   # NOTE = currently reg/login on SAME page
# def login_form():
#     """Show login form."""

#     return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user - please correct the email, or register.")
        return redirect("/register") # NOTE = currently reg/login on SAME page

    if user.password != password:
        flash("Incorrect password.")
        return redirect("/register") # NOTE = currently reg/login on SAME page

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/search")
def search_cpdl():
    """Search CPDL.org choralwiki for pieces (by composer, name, etc)."""

    value = request.args.get("search")

    payload = {'gsrsearch': value}

    r1 = requests.get('http://www1.cpdl.org/wiki/api.php?action=query&format=json&prop=info&generator=search&gsrlimit=max', params=payload)

    results = r1.json()

    results = parse_search_results(results)

    results.sort(key=lambda x: x[1])

    return render_template("search_result.html", results=results)


@app.route("/page_search")
def search_cpdl_page():
    """Search CPDL.org choralwiki for a specific PIECE's page."""

    value = request.args.get("page_id")

    payload = {'pageid': value}

    # cpdl_search = 'http://www1.cpdl.org/wiki/api.php?action=parse&format=json&pageid=3788'

    r1 = requests.get('http://www1.cpdl.org/wiki/api.php?action=parse&format=json', params=payload)

    results = r1.json()

    cpdls = parse_page_results(results)

    return render_template("piece_page.html", cpdls=cpdls)


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)

    return render_template("user.html", user=user)


@app.route("/pieces_list")
def pieces_list():
    """Show list of pieces."""

    pieces = Piece.query.order_by('title').all()

    return render_template("pieces_list.html", pieces=pieces)


@app.route("/pieces/<int:piece_id>", methods=['GET'])
def piece_detail(piece_id):
    """Show logged in user info about a piece. allow them to choose a specific
    sheet music version of the piece, if any are available."""

    user_id = session.get("user_id")

    piece = Piece.query.get(piece_id)

    return render_template("piece_page.html", piece=piece)


@app.route("/sheets/<int:sheet_id>", methods=['GET'])
def sheet_detail(sheet_id):
    """Show logged in user info about a specific sheet of music & associated
       files. Allow them to assign parts to performers and/or add the sheet
       to a setlist."""

    user_id = session.get("user_id")

    sheet = SheetMusic.query.get(sheet_id)

    return render_template("sheet_page.html", sheet=sheet)


# ****** HELPER FUNCTIONS: **************************


def parse_search_results(results):
    """Converts search results page id and title data into a dictionary and
       returns its items as a list of tuples."""

    pages = results['query']['pages']

    data = {}

    for page_id, page in pages.items():
        title = page['title']
        data[page_id] = title

    return data.items()


def parse_page_results(results):
    """Returns each page's results."""

    # Get all the image files from the page, and cut out the first 2 items, we
    # then have all of the sheet music and audio files.
    images = results['parse']['images']
    images = images[2:]

    # Pull data from the page's html - first, get the page "text" from the json.
    page_txt = results['parse']['text']['*']

    # Make beautiful soup from page text's html
    soup = BeautifulSoup(page_txt, "lxml")

    # Get CPDL numbers for each piece's sheet music / midi
    cpdl_nums = map(lambda x: x.string, soup('font'))

    # Get each piece of sheet music (.pdf) and audio files for each "user/editor"
    # and save as a dict of files by each
    pieces_dict_list = []

    # OOPS - some pages have no PDF, links to a WEB PAGE...don't really want to
    # offer files on these, just show piece data??? Hmm...decide! For now,
    # proceeding with what to do if there ARE pdf (sheet music) files.
    if images != []:
        pieces_dict = {'pdf': get_file_url(images[0])}
        # Since all records have the pdf first, then audio files, using pdf to
        # split list of "images", AKA files!
        for image in images[1:]:
            if image.split('.')[-1] == 'pdf':
                pieces_dict_list.append(pieces_dict)
                pieces_dict = {'pdf': get_file_url(image)}
            else:
                pieces_dict[str(image.split('.')[-1])] = get_file_url(image)
        pieces_dict_list.append(pieces_dict)
    else:
        pass # ADD HERE = maybe alert/flash that no files + user upload option?

    # Using unique cpdl numbers as the keys, join up the above files data as the
    # values, using zip.
    pieces_by_cpdl = {cpdl: piece for cpdl, piece in zip(cpdl_nums,
                                                         pieces_dict_list)}

    # One way to get the text titles for the text/translations:
    text_titles = map(lambda x: list(x[0].descendants)[1],
                      filter(lambda x: x, map(lambda x: x('big'), soup('b'))))

    # ****** Not yet returning full page results!! Need to finish getting all 
    # page data from API's json!! *******************
    return pieces_by_cpdl
    # data = {}

    # for page_id, page in pages.items():
    #     title = page['title']
    #     data[page_id] = title

    # return data.items()


def get_file_url(image):
    """Takes an image name, sends request to cpdl, and returns the image's url."""
    # Puts the image into the payload.
    payload = {
        'titles': 'File:' + image,
        'iiprop': 'url',
    }
    # Sends request to cpdl.org & captures the request's results as r4.
    r4 = requests.get(
        'http://www1.cpdl.org/wiki/api.php?action=query&format=json&prop=imageinfo',
        params=payload,
    )

    # Gets the url data from the results json and saves it as 'url'.
    url = r4.json()['query']['pages'].values()[0]['imageinfo'][0]['url']

    return url


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
