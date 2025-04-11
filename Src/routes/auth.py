from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from src.models.user import User, db
from werkzeug.security import check_password_hash
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Validate email format."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_password(password):
    """
    Validate password strength:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Check for missing fields
    if not all([username, email, password]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Validate email
    if not validate_email(email):
        return jsonify({'message': 'Invalid email format'}), 400
    
    # Validate password
    if not validate_password(password):
        return jsonify({
            'message': 'Password must be at least 8 characters long and contain uppercase, lowercase, and numeric characters'
        }), 400

    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Create new user
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not all([username, password]):
        return jsonify({'message': 'Missing username or password'}), 400

    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user)
        return jsonify({
            'message': 'Login successful', 
            'user': {
                'id': user.id, 
                'username': user.username, 
                'email': user.email
            }
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    }), 200