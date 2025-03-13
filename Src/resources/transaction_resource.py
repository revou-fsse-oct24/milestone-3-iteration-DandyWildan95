from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from ..models.transaction import Transaction, db
from ..models.account import Account
from ..models.user import User
from ..utils.schemas import TransactionSchema

class TransactionList(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve all transactions for the current user's accounts
        ---
        tags:
          - Transactions
        security:
          - bearerAuth: []
        parameters:
          - in: query
            name: type
            type: string
            enum: ['deposit', 'withdrawal', 'transfer']
          - in: query
            name: start_date
            type: string
            format: date
          - in: query
            name: end_date
            type: string
            format: date
        responses:
          200:
            description: List of transactions
          404:
            description: User not found
        """
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        # Get user's account IDs
        account_ids = [account.id for account in user.accounts]
        
        # Base query
        query = Transaction.query.filter(
            or_(
                Transaction.account_id.in_(account_ids),
                Transaction.source_account_id.in_(account_ids),
                Transaction.destination_account_id.in_(account_ids)
            )
        )
        
        # Optional filtering
        transaction_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if transaction_type:
            query = query.filter_by(transaction_type=transaction_type.upper())
        
        if start_date:
            query = query.filter(Transaction.timestamp >= start_date)
        
        if end_date:
            query = query.filter(Transaction.timestamp <= end_date)
        
        transactions = query.order_by(Transaction.timestamp.desc()).all()
        return [transaction.to_dict() for transaction in transactions], 200
    
    @jwt_required()
    def post(self):
        """
        Create a new transaction (deposit, withdrawal, transfer)
        ---
        tags:
          - Transactions
        security:
          - bearerAuth: []
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - account_id
                - transaction_type
                - amount
              properties:
                account_id:
                  type: integer
                transaction_type:
                  type: string
                  enum: ['DEPOSIT', 'WITHDRAWAL', 'TRANSFER']
                amount:
                  type: number
                destination_account_id:
                  type: integer
                description:
                  type: string
        responses:
          201:
            description: Transaction created successfully
          400:
            description: Invalid transaction
          403:
            description: Unauthorized
        """
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate account ownership
        account = Account.query.get(data['account_id'])
        if not account or account.user_id != current_user_id:
            return {'message': 'Invalid or unauthorized account'}, 403
        
        transaction_type = data['transaction_type'].upper()
        amount = float(data['amount'])
        
        # Transaction type-specific logic
        if transaction_type == 'DEPOSIT':
            account.balance += amount
        elif transaction_type == 'WITHDRAWAL':
            if account.balance < amount:
                return {'message': 'Insufficient funds'}, 400
            account.balance -= amount
        elif transaction_type == 'TRANSFER':
            # Validate destination account
            dest_account_id = data.get('destination_account_id')
            if not dest_account_id:
                return {'message': 'Destination account required for transfer'}, 400
            
            destination = Account.query.get(dest_account_id)
            if not destination:
                return {'message': 'Destination account not found'}, 404
            
            if account.balance < amount:
                return {'message': 'Insufficient funds'}, 400
            
            account.balance -= amount
            destination.balance += amount
        else:
            return {'message': 'Invalid transaction type'}, 400
        
        # Create transaction record
        transaction = Transaction(
            account_id=account.id,
            transaction_type=transaction_type,
            amount=amount,
            description=data.get('description', ''),
            source_account_id=account.id if transaction_type == 'TRANSFER' else None,
            destination_account_id=dest_account_id if transaction_type == 'TRANSFER' else None
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return transaction.to_dict(), 201

class TransactionDetail(Resource):
    @jwt_required()
    def get(self, transaction_id):
        """
        Retrieve details of a specific transaction
        ---
        tags:
          - Transactions
        security:
          - bearerAuth: []
        parameters:
          - in: path
            name: transaction_id
            required: true
            type: integer
        responses:
          200:
            description: Transaction details retrieved
          403:
            description: Unauthorized access
          404:
            description: Transaction not found
        """
        current_user_id = get_jwt_identity()
        transaction = Transaction.query.get(transaction_id)
        
        if not transaction:
            return {'message': 'Transaction not found'}, 404
        
        # Check if the user owns the account related to this transaction
        account = Account.query.get(transaction.account_id)
        if not account or account.user_id != current_user_id:
            return {'message': 'Unauthorized access to transaction'}, 403
        
        return transaction.to_dict(), 200

        # Additional method in transaction_resource.py
def validate_transaction_limits(self, account, amount, transaction_type):
    """
    Validate transaction against account limits
    
    Args:
        account (Account): Source account
        amount (float): Transaction amount
        transaction_type (str): Type of transaction
    
    Raises:
        ValueError: If transaction violates account limits
    """
    # Daily transaction limit
    daily_transactions = Transaction.query.filter(
        Transaction.account_id == account.id,
        Transaction.timestamp >= datetime.now() - timedelta(days=1)
    ).all()
    
    daily_total = sum(t.amount for t in daily_transactions)
    
    # Example limits (these would be configurable)
    DAILY_LIMIT = 10000  # $10,000 daily limit
    MAX_SINGLE_TRANSACTION = 5000  # $5,000 per transaction
    
    if amount > MAX_SINGLE_TRANSACTION:
        raise ValueError(f"Transaction amount exceeds maximum limit of ${MAX_SINGLE_TRANSACTION}")
    
    if daily_total + amount > DAILY_LIMIT:
        raise ValueError(f"Daily transaction limit of ${DAILY_LIMIT} would be exceeded")