from flask import Blueprint, render_template, current_app, session, jsonify, request, redirect, url_for
from flask_pymongo import PyMongo
from datetime import datetime, timedelta
from urllib.parse import quote, unquote
import json
import os
from dotenv import load_dotenv
# import zukiPy

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
                        daily_totals[entry_date][nutrient] += float(amount)

        # Now, populate the tracking_data with the totals for each nutrient
        for i, date in enumerate(tracking_data['dates']):
            tracking_data['calories'][i] = daily_totals[date]['Calorie']
            tracking_data['carbs'][i] = daily_totals[date]['Carb']
            tracking_data['fats'][i] = daily_totals[date]['Fat']
            tracking_data['proteins'][i] = daily_totals[date]['Protein']

    return render_template('chart.html', data=tracking_data)

@views.route('/add_to_tracking', methods=['POST'])
def add_to_tracking():
    if 'username' not in session:
        return redirect(url_for('home'))

    mongo = PyMongo(current_app)
    user_collection = mongo.db.User
    user_data = user_collection.find_one({"Username": session['username']})

    if not user_data:
        return "User data not found", 404

    today = datetime.now().strftime('%Y%m%d')
    total_energy = float(request.form.get('total_energy', 0))
    total_carbs = float(request.form.get('total_carbs', 0))
    total_fat = float(request.form.get('total_fat', 0))
    total_protein = float(request.form.get('total_protein', 0))

    entry_found = False
    if 'intake_history' not in user_data:
        user_data['intake_history'] = []
    for entry in user_data['intake_history']:
        if entry['date'] == today:
            entry['intakes'][0]['Calorie'] = "{:.2f}".format(float(entry['intakes'][0].get('Calorie', '0')) + total_energy)
            entry['intakes'][1]['Carb'] = "{:.2f}".format(float(entry['intakes'][1].get('Carb', '0')) + total_carbs)
            entry['intakes'][2]['Fat'] = "{:.2f}".format(float(entry['intakes'][2].get('Fat', '0')) + total_fat)
            entry['intakes'][3]['Protein'] = "{:.2f}".format(float(entry['intakes'][3].get('Protein', '0')) + total_protein)
            entry_found = True
            break
    if not entry_found:
        user_data['intake_history'].append({
            'date': today,
            'intakes': [
                {'Calorie': "{:.2f}".format(total_energy)},
                {'Carb': "{:.2f}".format(total_carbs)},
                {'Fat': "{:.2f}".format(total_fat)},
                {'Protein': "{:.2f}".format(total_protein)}
            ]
        })

    user_collection.update_one({"Username": session['username']}, {"$set": user_data})
    return redirect(url_for('views.tracking'))

# About route
@views.route('/about')
def about():
    return "<h1>About</h1>"

# Results Route
@views.route('/results')
def results():
    def load_nutrient_data():
        with open('./website/data/nutrient_data.json', 'r') as f:
            nutrient_dict = json.load(f)
        return nutrient_dict
    nutrient_dict = load_nutrient_data()
    encoded_classes = request.args.get('detected_classes', '')
    serialized_classes = unquote(encoded_classes)
    results = json.loads(serialized_classes) if serialized_classes else []
    
    enriched_results = []
    total_mass = total_energy = total_protein = total_fat = total_carbohydrates = 0
    for item in results:
        food_name = item['name']
        mass = item['mass']
        if food_name in nutrient_dict:
            nutrients = nutrient_dict[food_name]
            factor = mass / 100.0
            energy = nutrients['energy'] * factor
            protein = nutrients['protein'] * factor
            fat = nutrients['fat'] * factor
            carbohydrates = nutrients['carbohydrates'] * factor
            
            total_mass += mass
            total_energy += energy
            total_protein += protein
            total_fat += fat
            total_carbohydrates += carbohydrates
            
            enriched_item = {
                "name": food_name,
                "mass": "{:.2f}".format(mass),
                "energy": "{:.2f}".format(nutrients['energy'] * factor),
                "fat": "{:.2f}".format(nutrients['fat'] * factor),
                "carbohydrates": "{:.2f}".format(nutrients['carbohydrates'] * factor),
                "protein": "{:.2f}".format(nutrients['protein'] * factor)
            }
            enriched_results.append(enriched_item)

    # Format totals to two decimal places
    formatted_totals = {
        'total_mass': "{:.2f}".format(total_mass),
        'total_energy': "{:.2f}".format(total_energy),
        'total_protein': "{:.2f}".format(total_protein),
        'total_fat': "{:.2f}".format(total_fat),
        'total_carbs': "{:.2f}".format(total_carbohydrates)
    }

    return render_template('results.html', results=enriched_results, **formatted_totals)

# Profile route
@views.route('/profile')
def profile():
    mongo = PyMongo(current_app)
    user_collection = mongo.db.User
    user_data = user_collection.find_one({"Username": session['username']})  # Fetch one document from the collection
    if user_data:
        user_data.pop('_id', None)  # Remove the '_id' since it's not JSON serializable
    return render_template('profile.html', user=user_data)

# #Recommend route
# @views.route('/recommend', methods=['GET', 'POST'])
# async def index():
#     load_dotenv()
#     api_key = os.getenv("OPENAI_API_KEY")
#     zukiAI = zukiPy.zukiCall(api_key, "gpt-4")

#     if request.method == 'POST':
#         prompt = request.form['prompt']
#         if prompt:
#             # If you want to experience it from zukijourney
#             gpt_response = await zukiAI.zuki_chat.sendMessage(session['username'], prompt)
#             print("Chat Response:", gpt_response)
#             #with open('./website/static/user_response.txt', 'r', encoding='utf-8') as file:
#             #    gpt_response = file.read()
#             return render_template('recommend.html', prompt=prompt, response=gpt_response)
    

#     return render_template('recommend.html', prompt='', response='')