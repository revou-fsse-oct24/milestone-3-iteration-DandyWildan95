# c:\Tugas Revou\Module-3-Dandy\Src\utils\error_handlers.py
from flask import jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """
    Register global error handlers for the Flask application
    
    Args:
        app (Flask): Flask application instance
    """
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """
        Handle Marshmallow validation errors
        
        Returns:
            JSON response with validation error details
        """
        return jsonify({
            'message': 'Validation Error',
            'errors': error.messages
        }), 400

    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        """
        Handle database-related errors
        
        Returns:
            JSON response with database error details
        """
        # Log the full error for server-side tracking
        app.logger.error(f"Database Error: {str(error)}")
        
        return jsonify({
            'message': 'Database Error',
            'description': 'An unexpected database error occurred'
        }), 500

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        """
        Handle HTTP exceptions
        
        Returns:
            JSON response with HTTP error details
        """
        return jsonify({
            'message': error.name,
            'description': error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """
        Handle unexpected errors
        
        Returns:
            JSON response with generic error message
        """
        # Log the full error for server-side tracking
        app.logger.error(f"Unexpected Error: {str(error)}")
        
        return jsonify({
            'message': 'Internal Server Error',
            'description': 'An unexpected error occurred'
        }), 500