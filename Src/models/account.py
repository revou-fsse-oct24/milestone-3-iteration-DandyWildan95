from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .utils.validators import validate_account_number
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    account_number = Column(String(16), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Account types
    account_type = Column(Enum(
        'checking', 
        'savings', 
        'investment', 
        'business', 
        name='account_types'
    ), default='checking')
    
    balance = Column(Float, default=0.0)
    currency = Column(String(3), default='USD')
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')

    def __init__(self, user_id, account_number, account_type='checking', initial_balance=0.0, currency='USD'):
        # Validate account number
        account_valid, account_msg = validate_account_number(account_number)
        if not account_valid:
            raise ValueError(f"Invalid account number: {account_msg}")

        self.user_id = user_id
        self.account_number = account_number
        self.account_type = account_type
        self.balance = initial_balance
        self.currency = currency

    def update_balance(self, amount):
        """
        Update account balance
        """
        self.balance += amount
        return self.balance

    def to_dict(self):
        """
        Convert account object to dictionary for API response
        """
        return {
            'id': self.id,
            'account_number': self.account_number,
            'user_id': self.user_id,
            'account_type': self.account_type,
            'balance': self.balance,
            'currency': self.currency,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }