from flask import Blueprint, render_template, request, redirect, url_for, flash, session,send_from_directory
from app import db  # Assuming you are using SQLAlchemy
from app.models import User,DeviceEnergy,EnergyLog  # Assuming you have a User model in models.py
from flask import jsonify, request
import matplotlib
from datetime import datetime
matplotlib.use('Agg')  # Set Matplotlib to use the non-GUI backend
def is_valid_path(path):
    return os.path.exists(path)
import matplotlib.pyplot as plt
#from app.tasks import increment_energy_consumed
# Create the blueprint

import os
user_routes = Blueprint('user_routes', __name__)

 # Or whatever you want to do with the task


# Landing page route
@user_routes.route('/')
def index():
    return render_template('index.html')


@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check user credentials
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            flash('Login successful!', 'success')
            session['user_id'] = user.id
            session['email_id'] = user.email_address

            return redirect(url_for('user_routes.user_home'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')

@user_routes.route('/logout', methods=['POST'])
def logout():
    # End the session or clear session data
    session.clear()
    return  render_template('login.html')  # Redirect to the homepage or login page

@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            role = request.form['role']
            password = request.form['password']
            email_address = request.form['email_address']  # Retrieve email address

            # Check if email address is already taken (optional step)
            existing_user = User.query.filter_by(email_address=email_address).first()
            if existing_user:
                flash('Email address is already registered!', 'danger')
                return redirect(url_for('user_routes.register'))

            # Create a new user object (storing plain text password)
            user = User(username=username, role=role, password=password, email_address=email_address)
            db.session.add(user)
            db.session.commit()

            flash('Registration successful!', 'success')  # Flash a success message
            return render_template('index.html')  # Redirect to the home page after success

        except Exception as e:
            flash(f"Registration failed: {str(e)}", 'danger')  # Flash a failure message
            return redirect(url_for('user_routes.register'))  # Redirect back to registration form

    return render_template('register.html')

@user_routes.route('/user_home')
def user_home():
    if is_valid_path('./static/ref.jpg'):
        os.remove('./static/ref.jpg')
    if 'user_id' not in session:
        return redirect(url_for('user_routes.login'))  # Ensure user is logged in
    
    user_id = session['user_id']
    # Fetch the user from the database
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    # Fetch energy data from User model
    energy_consumed = user.energy_consumed  # This assumes this is being tracked in the User model
    energy_released = user.energy_released  # Similarly for energy_released

    # Fetch energy data from the EnergyLog for released energy
    logs = EnergyLog.query.filter_by(user_id=user.id).all()
    total_released = sum(log.energy_change for log in logs if log.type == 'released')

    # Fetch devices' energy consumption (assuming a many-to-one relationship with User)
    devices = DeviceEnergy.query.filter_by(user_id=user.id).all()  # Assuming Device is a model tracking devices
    device_consumptions = [{
        'device_name': device.device_type, 
        'energy_consumed': device.energy_consumed  # Assuming device has 'energy_consumed' field
    } for device in devices]
    
    print("devices are: ", device_consumptions)

    # Generate and save the pie chart for device energy consumption
    device_names = [device['device_name'] for device in device_consumptions]
    energy_values = [device['energy_consumed'] for device in device_consumptions]
    
    if energy_values:  # Avoid division by zero error if no device data
        fig, ax = plt.subplots()
        ax.pie(energy_values, labels=device_names, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

        # Ensure the directory exists for saving the image
        if not os.path.exists('static/energy_charts'):
            os.makedirs('static/energy_charts')

        # Save the plot as an image file in static folder
        chart_path = './static/ref.jpg'
        plt.savefig(chart_path)

        # Pass the image URL to the frontend for rendering

        return render_template(
            'user_home.html',
            user=user,
            energy_consumed=energy_consumed,
            energy_released=total_released,
            device_consumptions=device_consumptions,  # Pass device data
            chart_url=chart_path  # Pass the generated chart URL to the frontend
        )
    else:
        # Handle case where device energy consumption is empty
        return render_template(
            'user_home.html',
            user=user,
            energy_consumed=energy_consumed,
            energy_released=total_released,
            device_consumptions=device_consumptions,  # Pass device data
            chart_path=None  # No chart available if no devices are found
        )
    
