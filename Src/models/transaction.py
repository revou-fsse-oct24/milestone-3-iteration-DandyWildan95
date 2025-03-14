from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .utils.validators import validate_transaction_amount
from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    transaction_uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    
    # Enhanced transaction types
    transaction_type = Column(Enum(
        'deposit', 
        'withdrawal', 
        'transfer', 
        'bill_payment', 
        'investment', 
        'recurring_payment',
        'refund',
        name='transaction_types'
    ), nullable=False)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default='USD')
    description = Column(String(255), nullable=True)
    
    # Additional metadata fields
    metadata = Column(JSON, nullable=True)
    
    # For transfers and bill payments
    destination_account = Column(String(16), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship('User', back_populates='transactions')
    account = relationship('Account', back_populates='transactions')

    def __init__(self, user_id, account_id, transaction_type, amount, 
                 currency='USD', description=None, destination_account=None, metadata=None):
        # Validate transaction amount
        amount_valid, amount_msg = validate_transaction_amount(amount)
        if not amount_valid:
            raise ValueError(f"Invalid transaction amount: {amount_msg}")

        self.user_id = user_id
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.amount = amount
        self.currency = currency
        self.description = description
        self.destination_account = destination_account
        self.metadata = metadata or {}

    def to_dict(self):
        """
        Convert transaction object to dictionary for API response
        Includes additional metadata and UUID
        """
        return {
            'id': self.id,
            'transaction_uuid': self.transaction_uuid,
            'user_id': self.user_id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'currency': self.currency,
            'description': self.description,
            'destination_account': self.destination_account,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @classmethod
    def create_transaction(cls, user_id, account_id, transaction_type, amount, 
                            currency='USD', description=None, destination_account=None, metadata=None):
        """
        Factory method to create and validate a transaction
        Supports additional metadata and validation
        """
        transaction = cls(
            user_id=user_id, 
            account_id=account_id, 
            transaction_type=transaction_type, 
            amount=amount,
            currency=currency,
            description=description,
            destination_account=destination_account,
            metadata=metadata
        )
        return transaction

    def add_metadata(self, key, value):
        """
        Add or update metadata for the transaction
        """
        if self.metadata is None:
            self.metadata = {}
        self.metadata[key] = value