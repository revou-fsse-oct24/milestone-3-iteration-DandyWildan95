from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.account import Account
from src.models.base import db
import random

class AccountListResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        accounts = Account.query.filter_by(user_id=current_user_id).all()
        return [account.to_dict() for account in accounts], 200

class AccountResource(Resource):
    @jwt_required()
    def get(self, account_id):
        current_user_id = get_jwt_identity()
        account = Account.query.filter_by(id=account_id, user_id=current_user_id).first()
        
        if not account:
            return {'message': 'Account not found or access denied'}, 404
        
        return account.to_dict(), 200

    @jwt_required()
    def put(self, account_id):
        current_user_id = get_jwt_identity()
        account = Account.query.filter_by(id=account_id, user_id=current_user_id).first()
        
        if not account:
            return {'message': 'Account not found or access denied'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('account_type', type=str)
        parser.add_argument('is_active', type=bool)
        args = parser.parse_args()

        try:
            if args['account_type']:
                account.account_type = args['account_type']
            if args['is_active'] is not None:
                account.is_active = args['is_active']

            db.session.commit()
            return account.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error updating account', 'error': str(e)}, 500

    @jwt_required()
    def delete(self, account_id):
        current_user_id = get_jwt_identity()
        account = Account.query.filter_by(id=account_id, user_id=current_user_id).first()
        
        if not account:
            return {'message': 'Account not found or access denied'}, 404

        try:
            db.session.delete(account)
            db.session.commit()
            return {'message': 'Account deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error deleting account', 'error': str(e)}, 500

class AccountCreationResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        
        parser = reqparse.RequestParser()
        parser.add_argument('account_type', type=str, required=True, help='Account type is required')
        parser.add_argument('initial_balance', type=float, default=0.0)
        args = parser.parse_args()

        # Generate unique account number
        account_number = f'RB{random.randint(10000000, 99999999)}'

        new_account = Account(
            user_id=current_user_id,
            account_number=account_number,
            account_type=args['account_type'],
            balance=args['initial_balance']
        )

        try:
            db.session.add(new_account)
            db.session.commit()
            return new_account.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error creating account', 'error': str(e)}, 500

def register_account_resources(api):
    api.add_resource(AccountListResource, '/accounts')
    api.add_resource(AccountCreationResource, '/accounts')
    api.add_resource(AccountResource, '/accounts/<int:account_id>')