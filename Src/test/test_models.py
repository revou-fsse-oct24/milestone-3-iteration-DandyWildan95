from src.app import create_app
from src.models.base import db
from src.models.user import User
from src.models.account import Account
from src.models.transaction import Transaction

def test_create_user_with_account_and_transaction():
    app = create_app()
    
    with app.app_context():
        # Create a new user
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('testpassword')
        user.save()

        # Create an account for the user
        account = Account(
            user_id=user.id,
            account_number='1234567890',
            account_type='savings',
            balance=1000.00
        )
        account.save()

        # Create a transaction
        transaction = Transaction(
            account_id=account.id,
            transaction_type='deposit',
            amount=500.00,
            description='Initial deposit'
        )
        transaction.save()

        # Verify user
        print("User:", user.to_dict())
        
        # Verify account
        print("Account:", account.to_dict())
        
        # Verify transaction
        print("Transaction:", transaction.to_dict())

if __name__ == '__main__':
    test_create_user_with_account_and_transaction()