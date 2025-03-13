# c:\Tugas Revou\Module-3-Dandy\Src\utils\logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging(app):
    """
    Configure comprehensive logging for the application
    
    Args:
        app (Flask): Flask application instance
    """
    # Ensure logs directory exists
    log_dir = os.path.join(app.root_path, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # File Handler for detailed logs
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'revobank.log'), 
        maxBytes=10240,  # 10 KB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Console Handler for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app.logger.addHandler(console_handler)

    # Set logging level based on environment
    app.logger.setLevel(logging.INFO if app.config['ENV'] == 'production' else logging.DEBUG)