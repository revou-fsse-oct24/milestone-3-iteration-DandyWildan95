from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .utils.auth import AuthManager
from .utils.validators import validate_email_address, validate_password
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum('user', 'admin', name='user_roles'), default='user')
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    accounts = relationship('Account', back_populates='user', cascade='all, delete-orphan')
    transactions = relationship('Transaction', back_populates='user')

    def __init__(self, username, email, password, full_name=None, phone_number=None):
        # Validate email
        email_valid, email_msg = validate_email_address(email)
        if not email_valid:
            raise ValueError(f"Invalid email: {email_msg}")

        # Validate password
        password_valid, password_msg = validate_password(password)
        if not password_valid:
            raise ValueError(f"Invalid password: {password_msg}")

        self.username = username
        self.email = email
        self.password_hash = AuthManager.hash_password(password)
        self.full_name = full_name
        self.phone_number = phone_number

    def check_password(self, password):
        """
        Check if provided password is correct
        """
        return AuthManager.verify_password(self.password_hash, password)

    def to_dict(self):
        """
        Convert user object to dictionary for API response
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def generate_token(self):
        """
        Generate authentication token for the user
        """
        return AuthManager.generate_token(self.id, self.role)