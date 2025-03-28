from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.models.budget import Budget
from src.models.user import User

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/budgets', methods=['POST'])
@jwt_required()
def create_budget():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'amount', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate amount is positive
    if data['amount'] <= 0:
        return jsonify({'error': 'Budget amount must be positive'}), 400
    
    # Parse dates
    try:
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Validate end date is after start date
    if end_date <= start_date:
        return jsonify({'error': 'End date must be after start date'}), 400
    
    # Create new budget
    budget = Budget(
        user_id=current_user_id,
        name=data['name'],
        amount=data['amount'],
        start_date=start_date,
        end_date=end_date
    )
    
    budget.save()
    return jsonify({'message': 'Budget created successfully', 'budget': budget.to_dict()}), 201

@budget_bp.route('/budgets', methods=['GET'])
@jwt_required()
def get_budgets():
    current_user_id = get_jwt_identity()
    
    # Query budgets for current user
    budgets = Budget.query.filter_by(user_id=current_user_id).all()
    
    return jsonify({
        'budgets': [budget.to_dict() for budget in budgets]
    }), 200

@budget_bp.route('/budgets/<int:budget_id>', methods=['PUT'])
@jwt_required()
def update_budget(budget_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Find the budget
    budget = Budget.query.get(budget_id)
    
    # Check if budget exists
    if not budget:
        return jsonify({'error': 'Budget not found'}), 404
    
    # Authorize user
    if budget.user_id != current_user_id:
        return jsonify({'error': 'Unauthorized access'}), 401
    
    # Update fields if provided
    if 'name' in data:
        budget.name = data['name']
    
    if 'amount' in data:
        if data['amount'] <= 0:
            return jsonify({'error': 'Budget amount must be positive'}), 400
        budget.amount = data['amount']
    
    if 'start_date' in data:
        try:
            budget.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid start date format. Use YYYY-MM-DD'}), 400
    
    if 'end_date' in data:
        try:
            budget.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid end date format. Use YYYY-MM-DD'}), 400
    
    # Validate end date is after start date
    if budget.end_date <= budget.start_date:
        return jsonify({'error': 'End date must be after start date'}), 400
    
    budget.save()
    return jsonify({'message': 'Budget updated successfully', 'budget': budget.to_dict()}), 200
