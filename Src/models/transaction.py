from .base import db, BaseModel
from sqlalchemy.orm import relationship

class Transaction(BaseModel):
    __tablename__ = 'transactions'

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)  # e.g., deposit, withdrawal, transfer
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(50), default='completed')

    # Relationships
    account = relationship('Account', back_populates='transactions')

    def to_dict(self):
        """Convert transaction to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type,
            'amount': float(self.amount),
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }