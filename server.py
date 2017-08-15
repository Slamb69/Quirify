"""Music Project."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

# ?????????????? See next line -> Do I need to add every table? Individually?
from model import (connect_to_db, db, User, Provider, Piece, Owner,
                   PerformanceGroup, Concert)


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


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    title = request.form["title"]
    phone = request.form["phone"]

    user = User.query.filter_by(email=email).first()

    if user:
        flash("User already exists, please log in.")
        return redirect("/login")
    else:
        user = User(email=email,
                    password=password,
                    fname=fname,
                    lname=lname,
                    title=title,
                    phone=phone)

        db.session.add(user)
        db.session.commit()

        flash("User %s added." % email)
        return redirect("/users/%s" % user.user_id)


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user - please correct the email, or register.")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password.")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


# @app.route("/search", methods=["POST"])
# def search_pieces():
#     """Search for pieces."""

#     payload = request.form.get["search"]
#     return render_template("results_list.html", results=results)


# @app.route("/users/<int:user_id>")
# def user_detail(user_id):
#     """Show info about user."""

#     user = (User.query.options(db.joinedload('pieces')
#             .joinedload('performance_groups').get(user_id))

#     return render_template("user.html",
#                             user=user,
#                             groups=user.perf_groups)


@app.route("/pieces_list")
def pieces_list():
    """Show list of pieces."""

    pieces = Piece.query.order_by('title').all()
    return render_template("pieces_list.html", pieces=pieces)


# @app.route("/pieces/<int:piece_id>", methods=['GET'])
# def piece_detail(piece_id):
#     """Show logged in user info about a piece. allow them to assign parts to
#        performers, or add the piece to a setlist."""

#     print "made it here"

#     user_id = session.get("user_id")

#     piece = Piece.query.get(piece_id)

#     return render_template(
#         "piece.html",

#         )


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def movie_detail_process(movie_id):
#     """Add/edit a rating."""

#     # Get form variables
#     score = int(request.form["score"])

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("No user logged in.")

#     rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

#     if rating:
#         rating.score = score
#         flash("Rating updated.")

#     else:
#         rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
#         flash("Rating added.")
#         db.session.add(rating)

#     db.session.commit()

#     return redirect("/movies/%s" % movie_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
