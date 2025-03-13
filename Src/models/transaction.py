from datetime import datetime
from .user import db

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # deposit, withdrawal, transfer
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')
    
    # For transfers
    source_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)
    destination_account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)

    account = db.relationship('Account', back_populates='transactions')
    source_account = db.relationship('Account', foreign_keys=[source_account_id])
    destination_account = db.relationship('Account', foreign_keys=[destination_account_id])

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'transaction_type': self.transaction_type,
            'amount': float(self.amount),
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status
        }