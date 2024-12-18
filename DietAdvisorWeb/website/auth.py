from flask import Blueprint, request, redirect, url_for, render_template, session, current_app, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    def get_user_profile(gender, birth, weight, height, physical_activity, weight_option, weight_option_amonut):
        physical_activity_table = {'Sedentary':1.2, 'Lightly active':1.375, 'Moderately active':1.55, 'Very active':1.725, 'Super active':1.9}
        
        birth_date = datetime(int(birth[2]), int(birth[1]), int(birth[0]))
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        weight = float(weight)
        height = float(height)
        weight_option_amonut = round(float(weight_option_amonut) * 7700 / 30, 2)

        BMR_offset = 5 if gender == 'm' else -161
        BMR = round((10 * weight) + (6.25 * height) - (5 * age) + BMR_offset, 2)
        TDEE = round(BMR * physical_activity_table[physical_activity], 2)

        return {'gender':gender, 'age':age, 'weight':weight, 'height':height, 'physical_activity_multiplier':physical_activity, 'weight_option':weight_option, 'weight_option_amonut':weight_option_amonut, 'BMR':BMR, 'TDEE':TDEE}

    mongo = PyMongo(current_app)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        birth = [request.form.get('birth_day'), request.form.get('birth_month'), request.form.get('birth_year')]
        weight = request.form.get('weight')
        height = request.form.get('height')
        physical_activity = request.form.get('physical_activity')
        weight_option = request.form.get('weight_option')
        weight_option_amount = request.form.get('weight_option_amount')
        user_collection = mongo.db.User

        # Check if user exists
        user = user_collection.find_one({'Username': username})
        if user:
            flash('Username already exists', 'error')  # Using flash to send error messages
            return redirect(url_for('auth.register'))  # Redirect back to the registration page

        # Hash password and store user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        #Get user profile
        user_profile = get_user_profile(gender, birth, weight, height, physical_activity, weight_option, weight_option_amount)
        user_data = {'Username': username, 'Password': hashed_password}
        user_data.update(user_profile)
        
        user_collection.insert_one(user_data)

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    mongo = PyMongo(current_app)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_collection = mongo.db.User

        user = user_collection.find_one({'Username': username})
        if user and check_password_hash(user['Password'], password):
            session['user_id'] = str(user['_id'])  # Use user ID for the session
            session['username'] = str(user['Username'])
            return redirect(url_for('views.home'))

        flash('Invalid login credentials', 'error')  # Adding flash message for login error
        return redirect(url_for('auth.login'))  # Redirect back to the login page

    return render_template('login.html')

@auth.route('/logout')
def logout():
    #Remove session
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('views.home'))
