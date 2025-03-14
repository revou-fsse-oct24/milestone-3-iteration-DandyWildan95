from flask import request, jsonify
from flask_restful import Resource
from ..account import Account, db
from ..user import User
from ..utils.auth import token_required
from ..utils.validators import validate_account_number
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AccountListResource(Resource):
    @token_required()
    def get(self):
        """
        Retrieve all accounts for the currently authenticated user with pagination
        """
        user_id = request.user['user_id']
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        try:
            # Implement pagination
            paginated_accounts = Account.query.filter_by(user_id=user_id)\
                .paginate(page=page, per_page=per_page, error_out=False)
            
            return {
                'accounts': [account.to_dict() for account in paginated_accounts.items],
                'total': paginated_accounts.total,
                'pages': paginated_accounts.pages,
                'current_page': page
            }, 200
        except Exception as e:
            logger.error(f"Error retrieving accounts: {str(e)}")
            return {'error': 'An unexpected error occurred while retrieving accounts'}, 500
    
    @token_required()
    def post(self):
        """
        Create a new account for the currently authenticated user
        Supports additional account types and initial balance
        """
        user_id = request.user['user_id']
        data = request.get_json()
        
        # Validate user exists
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        # Generate unique account number
        def generate_account_number():
            while True:
                account_num = ''.join([str(random.randint(0, 9)) for _ in range(12)])
                existing_account = Account.query.filter_by(account_number=account_num).first()
                if not existing_account:
                    return account_num
        
        account_number = generate_account_number()
        
        try:
            # Support for more account types
            account_type = data.get('account_type', 'checking')
            valid_account_types = ['checking', 'savings', 'investment', 'business']
            
            if account_type not in valid_account_types:
                return {'error': f'Invalid account type. Must be one of {valid_account_types}'}, 400
            
            new_account = Account(
                user_id=user_id,
                account_number=account_number,
                account_type=account_type,
                initial_balance=float(data.get('initial_balance', 0.0)),
                currency=data.get('currency', 'USD')
            )
            
            db.session.add(new_account)
            db.session.commit()
            
            logger.info(f"New account created for user {user_id}: {account_number}")
            
            return {
                'message': 'Account created successfully',
                'account': new_account.to_dict()
            }, 201
        
        except ValueError as e:
            db.session.rollback()
            logger.error(f"Account creation error: {str(e)}")
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            logger.error(f"Unexpected error in account creation: {str(e)}")
            return {'error': 'An unexpected error occurred'}, 500

    @token_required()
    def delete(self):
        """
        Delete all accounts for the currently authenticated user
        """
        user_id = request.user['user_id']
        accounts = Account.query.filter_by(user_id=user_id).all()
        
        if not accounts:
            return {'error': 'No accounts found'}, 404
        
        try:
            for account in accounts:
                db.session.delete(account)
            db.session.commit()
            
            logger.info(f"All accounts deleted for user {user_id}")
            return {'message': 'All accounts deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting accounts for user {user_id}: {str(e)}")
            return {'error': 'An unexpected error occurred'}, 500

class AccountDetailResource(Resource):
    @token_required()
    def get(self, account_id):
        """
        Retrieve details of a specific account
        """
        user_id = request.user['user_id']
        account = Account.query.filter_by(id=account_id, user_id=user_id).first()
        
        if not account:
            return {'error': 'Account not found'}, 404
        
        return account.to_dict(), 200
    
    @token_required()
    def put(self, account_id):
        """
        Update details of a specific account
        """
        user_id = request.user['user_id']
        account = Account.query.filter_by(id=account_id, user_id=user_id).first()
        
        if not account:
            return {'error': 'Account not found'}, 404
        
        data = request.get_json()
        
        # Optional fields that can be updated
        if 'account_type' in data:
            valid_account_types = ['checking', 'savings', 'investment', 'business']
            if data['account_type'] not in valid_account_types:
                return {'error': f'Invalid account type. Must be one of {valid_account_types}'}, 400
            account.account_type = data['account_type']
        
        if 'currency' in data:
            account.currency = data['currency']
        
        try:
            db.session.commit()
            logger.info(f"Account {account_id} updated successfully")
            return account.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating account {account_id}: {str(e)}")
            return {'error': 'An unexpected error occurred'}, 500
    
    @token_required()
    def delete(self, account_id):
        """
        Delete an account
        Authorization required for account owner
        Prevents deletion of accounts with non-zero balance
        """
        user_id = request.user['user_id']
        account = Account.query.filter_by(id=account_id, user_id=user_id).first()
        
        if not account:
            return {'error': 'Account not found'}, 404
        
        # Prevent deletion of accounts with non-zero balance
        if account.balance > 0:
            return {'error': 'Cannot delete account with remaining balance'}, 400
        
        try:
            # Check for any pending transactions
            pending_transactions = account.transactions
            if pending_transactions:
                return {'error': 'Cannot delete account with existing transactions'}, 400
            
            db.session.delete(account)
            db.session.commit()
            
            logger.info(f"Account {account_id} deleted successfully")
            return {'message': 'Account deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error deleting account {account_id}: {str(e)}")
            return {'error': 'An unexpected error occurred'}, 500