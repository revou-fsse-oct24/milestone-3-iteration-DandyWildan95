from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from src.models.user import User, db

account_bp = Blueprint('account', __name__)

@account_bp.route('/create', methods=['POST'])
@login_required
def create_account():
    """
    Create a new bank account for the current user
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    account_type = data.get('account_type')
    initial_balance = data.get('initial_balance', 0)
    
    if not account_type:
        return jsonify({'message': 'Account type is required'}), 400
    
    try:
        # Here you would typically create an Account model and associate it with the current user
        # For now, this is a placeholder
        new_account = {
            'user_id': current_user.id,
            'account_type': account_type,
            'balance': initial_balance
        }
        
        # In a real implementation, you'd save this to a database
        return jsonify({
            'message': 'Account created successfully',
            'account': new_account
        }), 201
    
    except Exception as e:
        return jsonify({'message': 'Account creation failed', 'error': str(e)}), 500

@account_bp.route('/list', methods=['GET'])
@login_required
def list_accounts():
    """
    List all accounts for the current user
    """
    try:
        # In a real implementation, you'd query the accounts associated with the current user
        accounts = [
            {
                'id': 1,
                'account_type': 'Savings',
                'balance': 1000.00
            },
            {
                'id': 2,
                'account_type': 'Checking',
                'balance': 500.00
            }
        ]
        
        return jsonify({
            'message': 'Accounts retrieved successfully',
            'accounts': accounts
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve accounts', 'error': str(e)}), 500

@account_bp.route('/<int:account_id>', methods=['GET'])
@login_required
def get_account_details(account_id):
    """
    Get details of a specific account
    """
    try:
        # In a real implementation, you'd verify the account belongs to the current user
        account = {
            'id': account_id,
            'account_type': 'Savings',
            'balance': 1000.00,
            'user_id': current_user.id
        }
        
        return jsonify({
            'message': 'Account details retrieved successfully',
            'account': account
        }), 200
    
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve account details', 'error': str(e)}), 500