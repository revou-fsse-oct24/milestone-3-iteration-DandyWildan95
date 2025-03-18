from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
import os
import secrets

# Import secret keys directly
import secret_key
import jwt_secret_key

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Update database URI configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'mysql://revobank_user:Bangsat1@localhost/revobank'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Use environment variables or generated keys
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secret_key.SECRET_KEY)
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', jwt_secret_key.JWT_SECRET_KEY)
    
    # JWT Configuration
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Create API
    api = Api(app)

    # Import and register resources
    from src.resources.user_resources import register_user_resources
    from src.resources.account_resources import register_account_resources
    from src.resources.transaction_resources import (
        register_transaction_resources, 
        register_additional_resources
    )

    # Register resources
    register_user_resources(api)
    register_account_resources(api)
    register_transaction_resources(api)
    register_additional_resources(api)

    # Health check route
    @app.route('/')
    def health_check():
        return 'RevoBank API is running!', 200

    return app