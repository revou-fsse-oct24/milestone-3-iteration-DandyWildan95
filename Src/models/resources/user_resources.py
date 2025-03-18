from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User
from src.models.base import db
from werkzeug.exceptions import BadRequest

class UserRegistrationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('phone_number', type=str)
        args = parser.parse_args()

        # Validate input
        if not args['username'] or not args['email'] or not args['password']:
            return {'message': 'Missing required fields'}, 400

        # Check if user already exists
        if User.query.filter_by(username=args['username']).first():
            return {'message': 'Username already exists'}, 409
        
        if User.query.filter_by(email=args['email']).first():
            return {'message': 'Email already exists'}, 409

        # Create new user
        new_user = User(
            username=args['username'],
            email=args['email'],
            first_name=args.get('first_name'),
            last_name=args.get('last_name'),
            phone_number=args.get('phone_number')
        )
        new_user.set_password(args['password'])
        
        try:
            db.session.add(new_user)
            db.session.commit()
            
            # Generate access token
            access_token = create_access_token(identity=new_user.id)
            
            return {
                'message': 'User created successfully',
                'user': new_user.to_dict(),
                'access_token': access_token
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error creating user', 'error': str(e)}, 500

class UserLoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()
        
        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=user.id)
            return {
                'access_token': access_token,
                'user': user.to_dict()
            }, 200
        
        return {'message': 'Invalid credentials'}, 401

class UserProfileResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if user:
            return user.to_dict(), 200
        
        return {'message': 'User not found'}, 404

    @jwt_required()
    def put(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return {'message': 'User not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str)
        parser.add_argument('first_name', type=str)
        parser.add_argument('last_name', type=str)
        parser.add_argument('phone_number', type=str)
        args = parser.parse_args()

        try:
            # Update user fields if provided
            if args['email']:
                user.email = args['email']
            if args['first_name']:
                user.first_name = args['first_name']
            if args['last_name']:
                user.last_name = args['last_name']
            if args['phone_number']:
                user.phone_number = args['phone_number']

            db.session.commit()
            return user.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error updating user', 'error': str(e)}, 500

def register_user_resources(api):
    api.add_resource(UserRegistrationResource, '/users')
    api.add_resource(UserLoginResource, '/login')
    api.add_resource(UserProfileResource, '/users/me')