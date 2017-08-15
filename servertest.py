"""Music Project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

# ?????????????? See next line -> Do I need to add every table? Individually?
# from model import (connect_to_db, db, User, Provider, Piece, Owner,
#                    PerformanceGroup, Concert)

import requests

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/search")
def search_pieces():
    """Search for pieces."""

    value = request.args.get("search")

    payload = {'gsrsearch': value}

    # cpdl_search = 'http://www.cpdl.org/wiki/api.php?action=query&format=json&prop=info&generator=search'

    r1 = requests.get('http://www.cpdl.org/wiki/api.php?action=query&format=json&prop=info&generator=search&gsrlimit=max', params=payload)

    results = r1.json()

    def parse_search_results(results):
        """Returns search results page id and title data as a dictionary."""

        pages = results['query']['pages']

        data = {}

        for page_id, page in pages.items():
            title = page['title']
            data[page_id] = title

        return data.items()

    results = parse_search_results(results)

    results.sort(key=lambda x: x[1])

    return render_template("search_result.html", results=results)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
