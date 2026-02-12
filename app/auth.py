from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)

# Predefined admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check for admin login
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Create or get admin user
            admin_user = User.query.filter_by(username=ADMIN_USERNAME).first()
            if not admin_user:
                admin_user = User(
                    username=ADMIN_USERNAME,
                    email='admin@quizapp.com',
                    role='admin'
                )
                admin_user.set_password(ADMIN_PASSWORD)
                db.session.add(admin_user)
                db.session.commit()
            
            login_user(admin_user)
            return redirect(url_for('main.dashboard'))
        
        # Check for teacher/student login
        user = User.query.filter_by(username=username).first()
        
        if user is None:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        return redirect(url_for('main.dashboard'))
    
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role')
        
        # Validation
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('auth.register'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return redirect(url_for('auth.register'))
        
        if role not in ['teacher', 'student']:
            flash('Invalid role selected', 'danger')
            return redirect(url_for('auth.register'))
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            role=role
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'Registration successful! You can now login as {role}.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
