from flask import request, jsonify
from flask_restful import Resource
from ..user import User, db
from ..utils.auth import token_required, AuthManager
from ..utils.validators import validate_email_address, validate_password

class UserRegistrationResource(Resource):
    def post(self):
        """
        Create a new user account
        """
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return {'error': f'{field} is required'}, 400
        
        try:
            # Validate email and password
            email_valid, email_msg = validate_email_address(data['email'])
            if not email_valid:
                return {'error': email_msg}, 400
            
            password_valid, password_msg = validate_password(data['password'])
            if not password_valid:
                return {'error': password_msg}, 400
            
            # Check if user already exists
            if User.query.filter_by(username=data['username']).first():
                return {'error': 'Username already exists'}, 409
            
            if User.query.filter_by(email=data['email']).first():
                return {'error': 'Email already registered'}, 409
            
            # Create new user
            new_user = User(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                full_name=data.get('full_name'),
                phone_number=data.get('phone_number')
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            return {
                'message': 'User created successfully',
                'user': new_user.to_dict(),
                'token': new_user.generate_token()
            }, 201
        
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {'error': 'An unexpected error occurred'}, 500

class UserProfileResource(Resource):
    @token_required()
    def get(self):
        """
        Retrieve the profile of the currently authenticated user
        """
        user_id = request.user['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        return user.to_dict(), 200
    
    @token_required()
    def put(self):
        """
        Update the profile of the currently authenticated user
        """
        user_id = request.user['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        data = request.get_json()
        
        # Optional fields that can be updated
        if 'full_name' in data:
            user.full_name = data['full_name']
        
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        
        # Email update with validation
        if 'email' in data:
            email_valid, email_msg = validate_email_address(data['email'])
            if not email_valid:
                return {'error': email_msg}, 400
            
            # Check if new email is already in use
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 409
            
            user.email = data['email']
        
        # Password update with validation
        if 'password' in data:
            password_valid, password_msg = validate_password(data['password'])
            if not password_valid:
                return {'error': password_msg}, 400
            
            user.password_hash = AuthManager.hash_password(data['password'])
        
        try:
            db.session.commit()
            return user.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'error': 'An unexpected error occurred'}, 500

class UserLoginResource(Resource):
    def post(self):
        """
        User login endpoint
        """
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return {'error': 'Username and password are required'}, 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            return {
                'message': 'Login successful',
                'token': user.generate_token(),
                'user': user.to_dict()
            }, 200
        
        return {'error': 'Invalid credentials'}, 401