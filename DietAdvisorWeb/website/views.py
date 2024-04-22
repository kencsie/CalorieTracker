from flask import Blueprint, render_template

views = Blueprint('views', __name__)

# Define the root route (the home page)
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# Tracking meal history route
@views.route('/tracking')
def tracking():
    return "<h1>Tracking</h1>"

# About route
@views.route('/about')
def about():
    return "<h1>About</h1>"
