from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db  # Assuming you are using SQLAlchemy
from app.models import User  # Assuming you have a User model in models.py
from flask import jsonify, request

#from app.tasks import increment_energy_consumed
# Create the blueprint


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


            return redirect(url_for('user_routes.user_home'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')

@user_routes.route('/logout', methods=['POST'])
def logout():
    # End the session or clear session data
    session.clear()
    return  render_template('login.html')  # Redirect to the homepage or login page

# Register route
@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            role = request.form['role']
            password = request.form['password']

            # Create a new user object (storing plain text password)
            user = User(username=username, role=role, password=password)
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
    if 'user_id' not in session:
        return redirect(url_for('user_routes.login'))  # Ensure user is logged in
    
    user_id = session['user_id']
    # You can fetch user data with user_id here if you need to render personalized content
    user = User.query.get(user_id)
    
    return render_template('user_home.html', user=user)

