from .base import db, BaseModel
from sqlalchemy.orm import relationship

class Account(BaseModel):
    __tablename__ = 'accounts'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')

    def to_dict(self):
        """Convert account to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'account_number': self.account_number,
            'account_type': self.account_type,
            'balance': float(self.balance),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }