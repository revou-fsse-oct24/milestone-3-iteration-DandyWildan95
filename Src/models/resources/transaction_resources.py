from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.transaction import Transaction
from src.models.account import Account
from src.models.base import db
from sqlalchemy import or_

class TransactionListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        
        # Get all accounts for the current user
        user_accounts = Account.query.filter_by(user_id=current_user_id).all()
        account_ids = [account.id for account in user_accounts]

        # Get transactions for these accounts
        transactions = Transaction.query.filter(Transaction.account_id.in_(account_ids)).all()
        return [transaction.to_dict() for transaction in transactions], 200

class TransactionResource(Resource):
    @jwt_required()
    def get(self, transaction_id):
        current_user_id = get_jwt_identity()
        
        # Get all accounts for the current user
        user_accounts = Account.query.filter_by(user_id=current_user_id).all()
        account_ids = [account.id for account in user_accounts]

        # Find the transaction and ensure it belongs to user's accounts
        transaction = Transaction.query.filter(
            Transaction.id == transaction_id,
            Transaction.account_id.in_(account_ids)
        ).first()

        if not transaction:
            return {'message': 'Transaction not found or access denied'}, 404
        
        return transaction.to_dict(), 200

class TransactionCreationResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        
        parser = reqparse.RequestParser()
        parser.add_argument('account_id', type=int, required=True, help='Account ID is required')
        parser.add_argument('transaction_type', type=str, required=True, help='Transaction type is required')
        parser.add_argument('amount', type=float, required=True, help='Amount is required')
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        # Verify account ownership
        account = Account.query.filter_by(id=args['account_id'], user_id=current_user_id).first()
        if not account:
            return {'message': 'Account not found or access denied'}, 403

        # Validate transaction type
        valid_types = ['deposit', 'withdrawal', 'transfer']
        if args['transaction_type'] not in valid_types:
            return {'message': f'Invalid transaction type. Must be one of {valid_types}'}, 400

        # Additional validation for withdrawal and transfer
        if args['transaction_type'] in ['withdrawal', 'transfer']:
            if args['amount'] > account.balance:
                return {'message': 'Insufficient funds'}, 400

        new_transaction = Transaction(
            account_id=args['account_id'],
            transaction_type=args['transaction_type'],
            amount=args['amount'],
            description=args.get('description')
        )

        try:
            # Update account balance
            if args['transaction_type'] == 'deposit':
                account.balance += args['amount']
            elif args['transaction_type'] in ['withdrawal', 'transfer']:
                account.balance -= args['amount']

            db.session.add(new_transaction)
            db.session.commit()
            return new_transaction.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error creating transaction', 'error': str(e)}, 500

def register_transaction_resources(api):
    api.add_resource(TransactionListResource, '/transactions')
    api.add_resource(TransactionCreationResource, '/transactions')
    api.add_resource(TransactionResource, '/transactions/<int:transaction_id>')

def register_additional_resources(api):
    # Placeholder for future additional resources like bill payments, investments
    pass