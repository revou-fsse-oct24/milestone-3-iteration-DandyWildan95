from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_login import LoginManager
import os
import logging
from src.routes.budget import budget_bp
from src.routes.transaction_category import transaction_category_bp
from src.routes.bill import bill_bp
from src.routes.auth import auth_bp
from src.models.user import User

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api()
cors = CORS()
login_manager = LoginManager()

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_fallback_secret'),
        JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'dev_fallback_jwt_secret'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'mysql://revobank_user:Bangsat1@localhost/revobank'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        FLASK_ENV=os.environ.get('FLASK_ENV', 'development')
    )

    # Override with test config if provided
    if test_config is not None:
        app.config.from_mapping(test_config)

    # Logging configuration
    logging.basicConfig(
        level=logging.INFO if app.config['FLASK_ENV'] == 'production' else logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Create API instance
    api.init_app(app)

    # Ensure database is created
    with app.app_context():
        try:
            db.create_all()
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"Error creating database tables: {e}")

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

    # Initialize Login Manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(budget_bp)
    app.register_blueprint(transaction_category_bp)
    app.register_blueprint(bill_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Health check route
    @app.route('/')
    def health_check():
        return 'RevoBank API is running!', 200

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        logging.error(f"404 error: {error}")
        return {'message': 'Resource not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        logging.error(f"500 error: {error}")
        db.session.rollback()
        return {'message': 'Internal server error'}, 500

    return app