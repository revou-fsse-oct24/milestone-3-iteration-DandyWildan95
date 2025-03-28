from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.models.transaction_category import TransactionCategory

transaction_category_bp = Blueprint('transaction_category', __name__)

@transaction_category_bp.route('/transactions/categories', methods=['GET'])
@jwt_required()
def get_transaction_categories():
    # Get all transaction categories
    categories = TransactionCategory.query.all()
    
    return jsonify({
        'categories': [category.to_dict() for category in categories]
    }), 200
