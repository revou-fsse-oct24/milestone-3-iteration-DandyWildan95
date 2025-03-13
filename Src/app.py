from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables
load_dotenv()

# Initialize extensions
from .models.user import db
ma = Marshmallow()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Production-specific configurations
    config_name = os.getenv('FLASK_ENV', 'development')
    
    # Database configuration
    if config_name == 'production':
        # Heroku PostgreSQL configuration
        database_url = os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://')
        if not database_url:
            raise ValueError("No DATABASE_URL set for production environment")
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Default to local development database
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('LOCAL_DATABASE_URL', 'sqlite:///development.db')
    
    # Common configurations
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    
    # JWT Manager
    jwt = JWTManager(app)
    
    # API initialization
    api = Api(app)
    
    # Import and register resources
    from .resources.user_resource import (
        UserRegistration, 
        UserLogin, 
        UserProfile, 
        UserRefresh
    )
    from .resources.account_resource import (
        AccountList, 
        AccountDetail
    )
    from .resources.transaction_resource import (
        TransactionList, 
        TransactionDetail
    )
    
    # Register routes
    api.add_resource(UserRegistration, '/auth/register')
    api.add_resource(UserLogin, '/auth/login')
    api.add_resource(UserRefresh, '/auth/refresh')
    api.add_resource(UserProfile, '/users/me')
    
    api.add_resource(AccountList, '/accounts')
    api.add_resource(AccountDetail, '/accounts/<int:account_id>')
    
    api.add_resource(TransactionList, '/transactions')
    api.add_resource(TransactionDetail, '/transactions/<int:transaction_id>')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
