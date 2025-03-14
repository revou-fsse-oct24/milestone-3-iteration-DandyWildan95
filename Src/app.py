from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///revobank.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development_secret_key')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Create API
    api = Api(app)

    # Health check route
    @app.route('/')
    def health_check():
        return 'RevoBank API is running!', 200

    return app
