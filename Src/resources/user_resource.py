from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity
)
from marshmallow import ValidationError
from ..models.user import User, db
from ..utils.schemas import UserSchema

class UserRegistration(Resource):
    def post(self):
        """
        Register a new user
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - username
                - email
                - password
              properties:
                username:
                  type: string
                email:
                  type: string
                password:
                  type: string
        responses:
          201:
            description: User successfully registered
          400:
            description: Validation error
        """
        try:
            user_schema = UserSchema()
            data = user_schema.load(request.get_json())
            
            # Check if user already exists
            if User.query.filter_by(username=data['username']).first():
                return {'message': 'Username already exists'}, 400
            
            if User.query.filter_by(email=data['email']).first():
                return {'message': 'Email already exists'}, 400
            
            # Create new user
            new_user = User(
                username=data['username'],
                email=data['email']
            )
            new_user.set_password(data['password'])
            
            db.session.add(new_user)
            db.session.commit()
            
            return {
                'message': 'User created successfully',
                'user_id': new_user.id
            }, 201
        
        except ValidationError as err:
            return err.messages, 400
        except Exception as e:
            db.session.rollback()
            return {'message': str(e)}, 500

class UserLogin(Resource):
    def post(self):
        """
        User login
        ---
        tags:
          - Authentication
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - username
                - password
              properties:
                username:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Successful login
          401:
            description: Invalid credentials
        """
        try:
            data = request.get_json()
            user = User.query.filter_by(username=data['username']).first()
            
            if user and user.check_password(data['password']):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user_id': user.id
                }, 200
            
            return {'message': 'Invalid credentials'}, 401
        
        except Exception as e:
            return {'message': str(e)}, 500

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        """
        Get current user profile
        ---
        tags:
          - User
        security:
          - bearerAuth: []
        responses:
          200:
            description: User profile retrieved
          404:
            description: User not found
        """
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        return user.to_dict(), 200
    
    @jwt_required()
    def put(self):
        """
        Update user profile
        ---
        tags:
          - User
        security:
          - bearerAuth: []
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                first_name:
                  type: string
                last_name:
                  type: string
                phone_number:
                  type: string
        responses:
          200:
            description: Profile updated successfully
          404:
            description: User not found
        """
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        data = request.get_json()
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phone_number = data.get('phone_number', user.phone_number)
        
        db.session.commit()
        return user.to_dict(), 200

class UserRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh access token
        ---
        tags:
          - Authentication
        security:
          - bearerAuth: []
        responses:
          200:
            description: New access token generated
        """
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        return {'access_token': new_access_token}, 200