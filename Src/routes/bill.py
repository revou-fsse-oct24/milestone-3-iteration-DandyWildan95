from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.models.bill import Bill
from src.models.account import Account

bill_bp = Blueprint('bill', __name__)

@bill_bp.route('/bills', methods=['POST'])
@jwt_required()
def create_bill():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['biller_name', 'due_date', 'amount', 'account_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate amount is positive
    if data['amount'] <= 0:
        return jsonify({'error': 'Bill amount must be positive'}), 400
    
    # Parse date
    try:
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Verify account exists and belongs to user
    account = Account.query.get(data['account_id'])
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    if account.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access to account'}), 401
    
    # Verify sufficient balance
    if account.balance < data['amount']:
        return jsonify({'error': 'Insufficient balance for bill payment'}), 400
    
    # Create new bill
    bill = Bill(
        user_id=current_user_id,
        biller_name=data['biller_name'],
        due_date=due_date,
        amount=data['amount'],
        account_id=data['account_id']
    )
    
    bill.save()
    return jsonify({'message': 'Bill scheduled successfully', 'bill': bill.to_dict()}), 201

@bill_bp.route('/bills', methods=['GET'])
@jwt_required()
def get_bills():
    current_user_id = get_jwt_identity()
    
    # Query bills for current user
    bills = Bill.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'bills': [bill.to_dict() for bill in bills]
    }), 200

@bill_bp.route('/bills/<int:bill_id>', methods=['PUT'])
@jwt_required()
def update_bill(bill_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Find the bill
    bill = Bill.query.get(bill_id)
    
    # Check if bill exists
    if not bill:
        return jsonify({'error': 'Bill not found'}), 404
    
    # Authorize user
    if bill.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access'}), 401
    
    # Update fields if provided
    if 'biller_name' in data:
        bill.biller_name = data['biller_name']
    
    if 'due_date' in data:
        try:
            bill.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    if 'amount' in data:
        if data['amount'] <= 0:
            return jsonify({'error': 'Bill amount must be positive'}), 400
        bill.amount = data['amount']
    
    if 'account_id' in data:
        # Verify account exists and belongs to user
        account = Account.query.get(data['account_id'])
        if not account:
            return jsonify({'error': 'Account not found'}), 404
        
        if account.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized access to account'}), 401
        
        # Verify sufficient balance
        if account.balance < bill.amount:
            return jsonify({'error': 'Insufficient balance for bill payment'}), 400
        
        bill.account_id = data['account_id']
    
    if 'status' in data:
        valid_statuses = ['pending', 'paid', 'cancelled']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
        bill.status = data['status']
    
    bill.save()
    return jsonify({'message': 'Bill updated successfully', 'bill': bill.to_dict()}), 200

@bill_bp.route('/bills/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(bill_id):
    current_user_id = get_jwt_identity()
    
    # Find the bill
    bill = Bill.query.get(bill_id)
    
    # Check if bill exists
    if not bill:
        return jsonify({'error': 'Bill not found'}), 404
    
    # Authorize user
    if bill.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access'}), 401
    
    # Soft delete - update status to cancelled
    bill.status = 'cancelled'
    bill.save()
    
    return jsonify({'message': 'Bill cancelled successfully'}), 200
