from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    # Create Flask app
    app = Flask(__name__)

    # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Configuration
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'development_secret_key'),
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///revobank.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        FLASK_ENV=os.environ.get('FLASK_ENV', 'development')
    )

    # Override with any passed config
    if config:
        app.config.update(config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Create API
    api = Api(app, prefix='/api/v1')

    # Import and register resources
    from .models.resources.user_resources import UserRegistrationResource, UserLoginResource
    from .models.resources.account_resources import AccountResource
    from .models.resources.transaction_resources import TransactionResource

    # User Resources
    api.add_resource(UserRegistrationResource, '/users/register')
    api.add_resource(UserLoginResource, '/users/login')

    # Account Resources
    api.add_resource(AccountResource, '/accounts', '/accounts/<int:account_id>')

    # Transaction Resources
    api.add_resource(TransactionResource, '/transactions', '/transactions/<int:transaction_id>')

    # Health check route
    @app.route('/')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'RevoBank API is running',
            'environment': app.config['FLASK_ENV']
        }), 200

    # Error handler for 404
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    # Error handler for 500
    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify(error='Internal Server Error'), 500

    return app