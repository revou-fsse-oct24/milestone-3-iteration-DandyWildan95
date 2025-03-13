import re
import secrets
import logging
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..models.user import User
from ..models import db
from datetime import datetime, timedelta
import pyotp

class AuthenticationError(Exception):
    """Custom exception for authentication errors"""
    pass

def validate_password_strength(password):
    """
    Validate password strength with comprehensive rules
    
    Rules:
    - Minimum 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    if len(password) < 12:
        raise AuthenticationError("Password must be at least 12 characters long")
    
    if not re.search(r'[A-Z]', password):
        raise AuthenticationError("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        raise AuthenticationError("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        raise AuthenticationError("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise AuthenticationError("Password must contain at least one special character")
    
    return True

def generate_secure_token(length=32):
    """
    Generate a cryptographically secure random token
    
    Args:
        length (int): Length of the token
    
    Returns:
        str: Secure random token
    """
    return secrets.token_hex(length // 2)

def require_role(allowed_roles):
    """
    Decorator to enforce role-based access control
    
    Args:
        allowed_roles (list): List of roles allowed to access the endpoint
    
    Returns:
        Decorated function
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT token first
            verify_jwt_in_request()
            
            # Get current user
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user:
                return jsonify({'message': 'User not found'}), 404
            
            # Check user role
            if user.role not in allowed_roles:
                logging.warning(f"Unauthorized access attempt by user {user.id} with role {user.role}")
                return jsonify({
                    'message': 'Insufficient permissions',
                    'required_roles': allowed_roles
                }), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def log_security_event(event_type, user_id=None, details=None):
    """
    Log security-related events
    
    Args:
        event_type (str): Type of security event
        user_id (int, optional): ID of the user involved
        details (dict, optional): Additional event details
    """
    log_entry = {
        'event_type': event_type,
        'user_id': user_id,
        'timestamp': datetime.utcnow(),
        'details': details or {}
    }
    
    # In a real-world scenario, this would be logged to a secure logging system
    logging.info(f"Security Event: {log_entry}")

def rate_limit_login(user):
    """
    Implement login attempt rate limiting
    
    Args:
        user (User): User attempting to log in
    
    Returns:
        bool: Whether login attempt is allowed
    """
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = timedelta(minutes=15)
    
    current_time = datetime.utcnow()
    
    # Check if user is currently locked out
    if user.is_locked and user.lock_until > current_time:
        remaining_time = (user.lock_until - current_time).total_seconds() // 60
        raise AuthenticationError(f"Account locked. Try again in {remaining_time} minutes")
    
    # Reset lockout if lockout period has passed
    if user.is_locked and user.lock_until <= current_time:
        user.is_locked = False
        user.login_attempts = 0
        user.lock_until = None
    
    # Increment login attempts
    user.login_attempts += 1
    
    # Lock account if max attempts reached
    if user.login_attempts >= MAX_LOGIN_ATTEMPTS:
        user.is_locked = True
        user.lock_until = current_time + LOCKOUT_DURATION
        
        # Log security event
        log_security_event(
            'account_locked', 
            user_id=user.id, 
            details={'ip_address': request.remote_addr}
        )
        
        db.session.commit()
        raise AuthenticationError("Too many login attempts. Account locked temporarily")
    
    db.session.commit()
    return True

def two_factor_authentication(user):
    """
    Generate and send two-factor authentication code
    
    Args:
        user (User): User requesting 2FA
    
    Returns:
        str: Two-factor authentication code
    """
    # Generate a time-based one-time password
    totp = pyotp.TOTP(user.two_factor_secret)
    code = totp.now()
    
    # Send code via SMS or email (implementation depends on your communication service)
    send_two_factor_code(user.phone_number, code)
    
    return code