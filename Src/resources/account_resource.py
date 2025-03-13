from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.account import Account, db
from ..models.user import User
from ..utils.schemas import AccountSchema
import uuid

class AccountList(Resource):
    @jwt_required()
    def get(self):
        """
        Retrieve all accounts for the current user
        ---
        tags:
          - Accounts
        security:
          - bearerAuth: []
        responses:
          200:
            description: List of user accounts
          404:
            description: User not found
        """
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return {'message': 'User not found'}, 404
        
        accounts = Account.query.filter_by(user_id=current_user_id).all()
        return [account.to_dict() for account in accounts], 200
    
    @jwt_required()
    def post(self):
        """
        Create a new account for the current user
        ---
        tags:
          - Accounts
        security:
          - bearerAuth: []
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - account_type
              properties:
                account_type:
                  type: string
                  enum: ['savings', 'checking', 'business']
        responses:
          201:
            description: Account created successfully
          400:
            description: Invalid account type
        """
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate account type
        account_type = data.get('account_type', 'savings').lower()
        valid_types = ['savings', 'checking', 'business']
        
        if account_type not in valid_types:
            return {'message': f'Invalid account type. Must be one of {valid_types}'}, 400
        
        # Generate unique account number
        account_number = str(uuid.uuid4())[:12].replace('-', '')
        
        new_account = Account(
            user_id=current_user_id,
            account_number=account_number,
            account_type=account_type,
            balance=0.00
        )
        
        db.session.add(new_account)
        db.session.commit()
        
        return new_account.to_dict(), 201

class AccountDetail(Resource):
    @jwt_required()
    def get(self, account_id):
        """
        Retrieve details of a specific account
        ---
        tags:
          - Accounts
        security:
          - bearerAuth: []
        parameters:
          - in: path
            name: account_id
            required: true
            type: integer
        responses:
          200:
            description: Account details retrieved
          403:
            description: Unauthorized access
          404:
            description: Account not found
        """
        current_user_id = get_jwt_identity()
        account = Account.query.get(account_id)
        
        if not account:
            return {'message': 'Account not found'}, 404
        
        if account.user_id != current_user_id:
            return {'message': 'Unauthorized access to account'}, 403
        
        return account.to_dict(), 200
    
    @jwt_required()
    def put(self, account_id):
        """
        Update account details
        ---
        tags:
          - Accounts
        security:
          - bearerAuth: []
        parameters:
          - in: path
            name: account_id
            required: true
            type: integer
          - in: body
            name: body
            schema:
              type: object
              properties:
                is_active:
                  type: boolean
        responses:
          200:
            description: Account updated successfully
          403:
            description: Unauthorized access
          404:
            description: Account not found
        """
        current_user_id = get_jwt_identity()
        account = Account.query.get(account_id)
        
        if not account:
            return {'message': 'Account not found'}, 404
        
        if account.user_id != current_user_id:
            return {'message': 'Unauthorized access to account'}, 403
        
        data = request.get_json()
        
        # Only allow updating specific fields
        if 'is_active' in data:
            account.is_active = data['is_active']
        
        db.session.commit()
        return account.to_dict(), 200
    
    @jwt_required()
    def delete(self, account_id):
        """
        Delete an account
        ---
        tags:
          - Accounts
        security:
          - bearerAuth: []
        parameters:
          - in: path
            name: account_id
            required: true
            type: integer
        responses:
          200:
            description: Account deleted successfully
          403:
            description: Unauthorized access
          404:
            description: Account not found
        """
        current_user_id = get_jwt_identity()
        account = Account.query.get(account_id)
        
        if not account:
            return {'message': 'Account not found'}, 404
        
        if account.user_id != current_user_id:
            return {'message': 'Unauthorized access to account'}, 403
        
        # Prevent deletion if account has non-zero balance
        if account.balance > 0:
            return {'message': 'Cannot delete account with remaining balance'}, 400
        
        db.session.delete(account)
        db.session.commit()
        
        return {'message': 'Account deleted successfully'}, 200