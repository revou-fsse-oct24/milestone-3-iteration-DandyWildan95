from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.models.user import User, db
from werkzeug.security import check_password_hash, generate_password_hash

user_bp = Blueprint('user', __name__)

@user_bp.route('/update_profile', methods=['PUT'])
@login_required
def update_profile():
    """
    Update user profile information
    Allows updating username and email
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    # Optional fields that can be updated
    new_username = data.get('username')
    new_email = data.get('email')
    
    # Check if the new username is already taken
    if new_username and new_username != current_user.username:
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 400
        current_user.username = new_username
    
    # Check if the new email is already taken
    if new_email and new_email != current_user.email:
        existing_email = User.query.filter_by(email=new_email).first()
        if existing_email:
            return jsonify({'message': 'Email already exists'}), 400
        current_user.email = new_email
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Profile update failed', 'error': str(e)}), 500

@user_bp.route('/change_password', methods=['PUT'])
@login_required
def change_password():
    """
    Change user password
    Requires current password and new password
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not all([current_password, new_password]):
        return jsonify({'message': 'Missing current or new password'}), 400
    
    # Verify current password
    if not current_user.check_password(current_password):
        return jsonify({'message': 'Current password is incorrect'}), 400
    
    # Set new password
    current_user.set_password(new_password)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Password change failed', 'error': str(e)}), 500

@user_bp.route('/delete_account', methods=['DELETE'])
@login_required
def delete_account():
    """
    Delete user account
    Requires password confirmation
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    password = data.get('password')
    
    if not password:
        return jsonify({'message': 'Password confirmation required'}), 400
    
    # Verify password
    if not current_user.check_password(password):
        return jsonify({'message': 'Incorrect password'}), 400
    
    try:
        db.session.delete(current_user)
        db.session.commit()
        return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Account deletion failed', 'error': str(e)}), 500