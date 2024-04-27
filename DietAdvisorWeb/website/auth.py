from flask import Blueprint, request, redirect, url_for, render_template, session, current_app, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import os

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    def get_user_profile(gender, age, weight, height, physical_activity):
        age = float(age)
        weight = float(weight)
        height = float(height)
        physical_activity = float(physical_activity)

        BMR_offset = 5 if gender == 'm' else -161
        BMR = (10 * weight) + (6.25 * height) - (5 * age) + BMR_offset
        TDEE = BMR * physical_activity

        return {'gender':gender, 'age':age, 'weight':weight, 'height':height, 'physical_activity_multiplier':physical_activity, 'BMR':BMR, 'TDEE':TDEE}

    mongo = PyMongo(current_app)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        age = request.form.get('age')
        weight = request.form.get('weight')
        height = request.form.get('height')
        physical_activity = request.form.get('physical_activity')
        user_collection = mongo.db.User

        # Check if user exists
        user = user_collection.find_one({'Username': username})
        if user:
            flash('Username already exists', 'error')  # Using flash to send error messages
            return redirect(url_for('auth.register'))  # Redirect back to the registration page

        # Hash password and store user
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        #Get user profile
        user_profile = get_user_profile(gender, age, weight, height, physical_activity)
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
