"""Music Project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

# ?????????????? See next line -> Do I need to add every table? Individually?
# from model import (connect_to_db, db, User, Provider, Piece, Owner,
#                    PerformanceGroup, Concert)

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


@app.route("/search")
def search_cpdl():
    """Search CPDL.org choralwiki for pieces (by composer, name, etc)."""

    value = request.args.get("search")

    payload = {'gsrsearch': value}

    # cpdl_search = 'http://www.cpdl.org/wiki/api.php?action=query&format=json&prop=info&generator=search'

    r1 = requests.get('http://www.cpdl.org/wiki/api.php?action=query&format=json&prop=info&generator=search&gsrlimit=max', params=payload)

    results = r1.json()

    results = parse_search_results(results)

    results.sort(key=lambda x: x[1])

    return render_template("search_result.html", results=results)


@app.route("/page_search")
def search_cpdl_page():
    """Search CPDL.org choralwiki for a specific PIECE's page."""

    value = request.args.get("page_id")

    payload = {'pageid': value}

    # cpdl_search = 'http://www.cpdl.org/wiki/api.php?action=parse&format=json&pageid=3788'

    r1 = requests.get('http://www.cpdl.org/wiki/api.php?action=parse&format=json', params=payload)

    results = r1.json()

    # return results

    # results = parse_search_results(results)

    # results.sort(key=lambda x: x[1])

    # return render_template("piece_page.html", results=results)

# HELPER FUNCTIONS:**************************


def parse_search_results(results):
    """Converts search results page id and title data into a dictionary and
       returns it's items as a list of tuples."""

    pages = results['query']['pages']

    data = {}

    for page_id, page in pages.items():
        title = page['title']
        data[page_id] = title

    return data.items()


def parse_page_results(results):
    """Returns each page's results."""

    # Get all the image files from the page.
    # images = results['parse']['images']

    # Get a list of all of the sheet music files (.pdfs)

    # sht_music = filter(lambda x: ('.pdf' in x), images)

    # # Get a list of all of the midi files (.mid)

    # midi_file = 


    page_txt = results['parse']['text']['*']

    # Make beautiful soup from page 'text''s html
    soup = BeautifulSoup(page_txt, "lxml")

    # Get CPDL numbers for each piece's sheet music / midi
    cpdl_nums = map(lambda x: x.string, soup('font'))

    # One way to get the text titles for the text/translations:
    text_titles = map(lambda x: list(x[0].descendants)[1],
                      filter(lambda x: x, map(lambda x: x('big'), soup('b'))))

    texts = 

    # data = {}

    # for page_id, page in pages.items():
    #     title = page['title']
    #     data[page_id] = title

    # return data.items()


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
