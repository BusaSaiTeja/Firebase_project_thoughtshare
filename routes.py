from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import create_user, get_user_by_email, check_password  # Import functions
from flask_login import login_user, login_required, logout_user, current_user

routes = Blueprint('routes', __name__)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Check user credentials using Firebase Authentication
        if check_password(email, password):
            user = get_user_by_email(email)
            if user:
                login_user(user)  # Log the user in with Flask-Login
                flash('Login successful!', 'success')
                return redirect(url_for('routes.home'))  # Redirect to home
            else:
                flash('User not found. Please check your credentials.', 'danger')
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html')

@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the email already exists
        if get_user_by_email(email):
            flash('Email already exists. Please log in.', category='error')
            return redirect(url_for('routes.login'))

        create_user(username, email, password)
        flash('Account created! You can now log in.', category='success')
        return redirect(url_for('routes.login'))
    
    return render_template('signup.html')

@routes.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))
