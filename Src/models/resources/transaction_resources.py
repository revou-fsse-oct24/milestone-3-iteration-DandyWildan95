from flask import request, jsonify
from flask_restful import Resource
from ..transaction import Transaction, db
from ..account import Account
from ..utils.auth import token_required
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TransactionListResource(Resource):
    @token_required()
    def get(self):
        """
        Retrieve all transactions for the currently authenticated user
        Supports advanced filtering and pagination
        """
        user_id = request.user['user_id']
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Advanced filtering options
        transaction_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)
        
        try:
            # Base query
            query = Transaction.query.filter_by(user_id=user_id)
            
            # Apply filters
            if transaction_type:
                query = query.filter_by(transaction_type=transaction_type)
            
            if start_date:
                query = query.filter(Transaction.created_at >= datetime.fromisoformat(start_date))
            
            if end_date:
                query = query.filter(Transaction.created_at <= datetime.fromisoformat(end_date))
            
            if min_amount is not None:
                query = query.filter(Transaction.amount >= min_amount)
            
            if max_amount is not None:
                query = query.filter(Transaction.amount <= max_amount)
            
            # Paginate and order results
            paginated_transactions = query.order_by(Transaction.created_at.desc())\
                .paginate(page=page, per_page=per_page, error_out=False)
            
            # Prepare response with pagination metadata
            return {
                'transactions': [transaction.to_dict() for transaction in paginated_transactions.items],
                'total': paginated_transactions.total,
                'pages': paginated_transactions.pages,
                'current_page': page
            }, 200
        
        except Exception as e:
            logger.error(f"Error retrieving transactions: {str(e)}")
            return {'error': 'An unexpected error occurred while retrieving transactions'}, 500
    
    @token_required()
    def post(self):
        """
        Create a new transaction with enhanced validation and support for multiple transaction types
        Supports: deposit, withdrawal, transfer, bill payment, investment
        """
        user_id = request.user['user_id']
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['account_id', 'transaction_type', 'amount']
        for field in required_fields:
            if field not in data:
                return {'error': f'{field} is required'}, 400
        
        try:
            # Validate transaction type
            valid_transaction_types = [
                'deposit', 'withdrawal', 'transfer', 
                'bill_payment', 'investment'
            ]
            transaction_type = data['transaction_type']
            if transaction_type not in valid_transaction_types:
                return {'error': f'Invalid transaction type. Must be one of {valid_transaction_types}'}, 400
            
            # Fetch source account
            account = Account.query.filter_by(id=data['account_id'], user_id=user_id).first()
            if not account:
                return {'error': 'Source account not found'}, 404
            
            # Convert amount to float and validate
            amount = float(data['amount'])
            if amount <= 0:
                return {'error': 'Transaction amount must be positive'}, 400
            
            # Transaction type specific logic
            if transaction_type == 'withdrawal' and account.balance < amount:
                return {'error': 'Insufficient funds for withdrawal'}, 400
            
            if transaction_type == 'transfer':
                # Validate transfer specific requirements
                if 'destination_account' not in data:
                    return {'error': 'Destination account is required for transfers'}, 400
                
                dest_account = Account.query.filter_by(account_number=data['destination_account']).first()
                if not dest_account:
                    return {'error': 'Destination account not found'}, 404
                
                # Optional: Add transfer fee logic
                transfer_fee = amount * 0.01  # 1% transfer fee
                total_amount = amount + transfer_fee
                
                if account.balance < total_amount:
                    return {'error': 'Insufficient funds for transfer including fees'}, 400
            
            # Create transaction
            transaction = Transaction.create_transaction(
                user_id=user_id,
                account_id=data['account_id'],
                transaction_type=transaction_type,
                amount=amount,
                currency=data.get('currency', 'USD'),
                description=data.get('description'),
                destination_account=data.get('destination_account')
            )
            
            # Update account balance based on transaction type
            if transaction_type == 'deposit':
                account.update_balance(amount)
            elif transaction_type == 'withdrawal':
                account.update_balance(-amount)
            elif transaction_type == 'transfer':
                account.update_balance(-total_amount)  # Subtract amount + fee
                dest_account.update_balance(amount)  # Transfer only the base amount
            elif transaction_type == 'bill_payment':
                account.update_balance(-amount)
            elif transaction_type == 'investment':
                account.update_balance(-amount)
            
            db.session.add(transaction)
            db.session.commit()
            
            logger.info(f"Transaction {transaction_type} processed successfully for user {user_id}")
            
            return {
                'message': 'Transaction successful',
                'transaction': transaction.to_dict(),
                'account_balance': account.balance
            }, 201
        
        except ValueError as e:
            db.session.rollback()
            logger.error(f"Transaction error: {str(e)}")
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Unexpected transaction error: {str(e)}")
            return {'error': 'An unexpected error occurred'}, 500

class TransactionDetailResource(Resource):
    @token_required()
    def get(self, transaction_id):
        """
        Retrieve details of a specific transaction
        Ensures user can only access their own transactions
        """
        user_id = request.user['user_id']
        transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
        
        if not transaction:
            return {'error': 'Transaction not found'}, 404
        
        return transaction.to_dict(), 200