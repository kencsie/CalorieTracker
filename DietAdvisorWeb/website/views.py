from flask import Blueprint, render_template, current_app, session, jsonify
from flask_pymongo import PyMongo
from datetime import datetime, timedelta

views = Blueprint('views', __name__)

# Define the root route (the home page)
@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# Tracking page route
@views.route('/tracking')
def tracking():
    if 'username' not in session:
        return "Please log in to view this page", 403

    username = session['username']
    mongo = PyMongo(current_app)
    user_collection = mongo.db.User
    user_data = user_collection.find_one({"Username": username})
    
    if not user_data:
        return "User data not found", 404

    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)
    date_format = '%Y%m%d'

    tracking_data = {
        "dates": [],
        "calories": [],
        "carbs": [],
        "fats": [],
        "proteins": []
    }

    for i in range(7):
        date = (start_date + timedelta(days=i)).strftime(date_format)
        tracking_data['dates'].append(date)
        tracking_data['calories'].append(0)
        tracking_data['carbs'].append(0)
        tracking_data['fats'].append(0)
        tracking_data['proteins'].append(0)

    if 'intake_history' in user_data:
        # Initialize a dictionary to hold the sums of nutrients for each day
        daily_totals = {date: {'Calorie': 0, 'Carb': 0, 'Fat': 0, 'Protein': 0}
                        for date in tracking_data['dates']}

        for entry in user_data['intake_history']:
            entry_date = datetime.strptime(entry['date'], date_format).strftime(date_format)
            # Check if the entry date is within the last 7 days
            if entry_date in daily_totals:
                for nutrient_info in entry['intakes']:
                    for nutrient, amount in nutrient_info.items():
                        # Convert amount to integer, and accumulate the totals
                        daily_totals[entry_date][nutrient] += int(amount)

        # Now, populate the tracking_data with the totals for each nutrient
        for i, date in enumerate(tracking_data['dates']):
            tracking_data['calories'][i] = daily_totals[date]['Calorie']
            tracking_data['carbs'][i] = daily_totals[date]['Carb']
            tracking_data['fats'][i] = daily_totals[date]['Fat']
            tracking_data['proteins'][i] = daily_totals[date]['Protein']

    return render_template('chart.html', data=tracking_data)

# About route
@views.route('/about')
def about():
    return "<h1>About</h1>"

# Profile route
@views.route('/profile')
def profile():
    mongo = PyMongo(current_app)
    user_collection = mongo.db.User
    user_data = user_collection.find_one({"Username": session['username']})  # Fetch one document from the collection
    if user_data:
        user_data.pop('_id', None)  # Remove the '_id' since it's not JSON serializable
    return render_template('profile.html', user=user_data)
