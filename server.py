from flask import Flask, redirect, request, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined


app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SPVushgp-23%&o23858"


# YOUR ROUTES GO HERE


# @app.route('/', methods=['GET', 'POST'])
# def show_homepage():
#     """Displays the homepage to greet user and get their name."""

#     if request.method == 'POST':
#         session = {}
#         return redirect('/')

#     if session.get('name') and session['name'] != 'None':
#         return redirect('/top-melons')

#     return render_template("homepage.html")


# @app.route('/get-name')
# def add_user_name():
#     """Takes user name from homepage input, adds it to session, and redirects
#     user to the top-melons page."""
#     # Save form data from the home page as user_name
#     user_name = request.args.get('name')
#     # Add user's name to the session at key name.
#     session['name'] = user_name

#     return redirect('/top-melons')


# @app.route('/top-melons')
# def show_top_melons():
#     """Displays the most loved melons by name, number of loves, and image."""

    # Checks for a session, and redirects to homepage if none found. I can't get
    # this flash message to work!!!!! WHY? I dunno...tried it also from TY page.
#     if not session.get('name'):
#         flash('Oops, please re-enter a name to see our most loved melons!')
#         return redirect('/')
#     # renders the top-melons page, passing in the dictionary of MOST_LOVED_MELONS
#     return render_template("top-melons.html",
#                            top_melons=MOST_LOVED_MELONS)


# @app.route('/love-melon', methods=['GET', 'POST'])
# def love_a_melon():
#     """Takes in a user's loved melon and adds one to the num_loves count.
#     Displays the thank-you page to the user."""

#     # Gets form data, updates num_count in dict & takes user to TY page.
#     if request.method == 'POST':
#         loved_melon = str(request.form.get('love-a-melon'))
#         MOST_LOVED_MELONS[loved_melon]['num_loves'] += 1
#         flash('You have loved our {melon}!'.format(melon=MOST_LOVED_MELONS[loved_melon]['name']))
#         return redirect('/thank-you')
#     # If no form data returned, returns to top-melon page.
#     if request.method == 'GET':
#         return redirect('/top-melons')


# @app.route('/thank-you', methods=['GET', 'POST'])
# def return_home():
#     """Shows user thank you page and offers to return them to a new session,
#     at the home page."""

#     return render_template('thank-you.html',
#                            user_name=session['name'])


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension

    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
