import os
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Permissions:
    """
    Defines granular permissions for different user roles
    """
    # User Permissions
    USER_READ_PROFILE = 'user:read_profile'
    USER_UPDATE_PROFILE = 'user:update_profile'
    
    # Account Permissions
    ACCOUNT_LIST = 'account:list'
    ACCOUNT_CREATE = 'account:create'
    ACCOUNT_READ = 'account:read'
    ACCOUNT_UPDATE = 'account:update'
    ACCOUNT_DELETE = 'account:delete'
    
    # Transaction Permissions
    TRANSACTION_LIST = 'transaction:list'
    TRANSACTION_CREATE = 'transaction:create'
    TRANSACTION_READ = 'transaction:read'
    
    # Role-based permission mappings
    ROLE_PERMISSIONS = {
        'user': [
            USER_READ_PROFILE,
            USER_UPDATE_PROFILE,
            ACCOUNT_LIST,
            ACCOUNT_CREATE,
            ACCOUNT_READ,
            ACCOUNT_UPDATE,
            TRANSACTION_LIST,
            TRANSACTION_CREATE,
            TRANSACTION_READ
        ],
        'admin': [
            # Admin gets all permissions
            USER_READ_PROFILE,
            USER_UPDATE_PROFILE,
            ACCOUNT_LIST,
            ACCOUNT_CREATE,
            ACCOUNT_READ,
            ACCOUNT_UPDATE,
            ACCOUNT_DELETE,
            TRANSACTION_LIST,
            TRANSACTION_CREATE,
            TRANSACTION_READ
        ]
    }

class AuthManager:
    SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')
    TOKEN_EXPIRATION = 24  # hours

    @staticmethod
    def hash_password(password):
        """
        Hash password using secure method
        """
        return generate_password_hash(password, method='pbkdf2:sha256')

    @staticmethod
    def verify_password(stored_password, provided_password):
        """
        Verify provided password against stored hash
        """
        return check_password_hash(stored_password, provided_password)

    @classmethod
    def generate_token(cls, user_id, role='user', permissions=None):
        """
        Generate JWT token with role and permissions
        """
        # If no specific permissions provided, use role-based permissions
        if permissions is None:
            permissions = Permissions.ROLE_PERMISSIONS.get(role, [])
        
        payload = {
            'user_id': user_id,
            'role': role,
            'permissions': permissions,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=cls.TOKEN_EXPIRATION)
        }
        return jwt.encode(payload, cls.SECRET_KEY, algorithm='HS256')

    @classmethod
    def decode_token(cls, token):
        """
        Decode and validate JWT token
        """
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None

def permission_required(*required_permissions):
    """
    Decorator to check for specific permissions
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check for token in Authorization header
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
            
            if not token:
                logger.warning("Authentication token is missing")
                return jsonify({
                    'message': 'Authentication token is missing',
                    'error': 'Unauthorized'
                }), 401
            
            # Decode token
            payload = AuthManager.decode_token(token)
            
            if payload is None:
                logger.warning("Invalid or expired token")
                return jsonify({
                    'message': 'Invalid or expired token',
                    'error': 'Unauthorized'
                }), 401
            
            # Check permissions
            user_permissions = payload.get('permissions', [])
            
            # Check if user has all required permissions
            if not all(perm in user_permissions for perm in required_permissions):
                logger.warning(f"Insufficient permissions. Required: {required_permissions}")
                return jsonify({
                    'message': 'Insufficient permissions',
                    'error': 'Forbidden'
                }), 403
            
            # Attach user information to request for further processing
            request.user = payload
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def token_required(roles=None):
    """
    Decorator to require authentication and optional role-based access
    Maintains backward compatibility with existing code
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check for token in Authorization header
            token = None
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None
            
            if not token:
                logger.warning("Authentication token is missing")
                return jsonify({
                    'message': 'Authentication token is missing',
                    'error': 'Unauthorized'
                }), 401
            
            # Decode token
            payload = AuthManager.decode_token(token)
            
            if payload is None:
                logger.warning("Invalid or expired token")
                return jsonify({
                    'message': 'Invalid or expired token',
                    'error': 'Unauthorized'
                }), 401
            
            # Check role-based access if roles are specified
            if roles and payload.get('role') not in roles:
                logger.warning(f"Role {payload.get('role')} not in allowed roles: {roles}")
                return jsonify({
                    'message': 'Insufficient permissions',
                    'error': 'Forbidden'
                }), 403
            
            # Attach user information to request for further processing
            request.user = payload
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator