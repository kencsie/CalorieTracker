from flask import Blueprint, render_template, current_app
from flask_pymongo import PyMongo

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

# Profile route
@views.route('/profile')
def profile(username="Foo"):
    mongo = PyMongo(current_app)
    user_collection = mongo.db.User
    user_data = user_collection.find_one({"Username": username})  # Fetch one document from the collection
    if user_data:
        user_data.pop('_id', None)  # Remove the '_id' since it's not JSON serializable
    return render_template('profile.html', user=user_data)
