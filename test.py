import secrets
import unittest
import json
import datetime
from src.app import create_app
from src.models.base import db
from src.models.user import User
from src.models.account import Account
from src.models.transaction import Transaction
from src.models.budget import Budget
from src.models.transaction_category import TransactionCategory
from src.models.bill import Bill

# Generate secure keys
print("FLASK_ENV: production")
print("SECRET_KEY:", secrets.token_hex(32))
print("JWT_SECRET_KEY:", secrets.token_hex(32))

class FinancialFeaturesTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create database tables
        db.create_all()
        
        # Set up test data
        self.setup_test_data()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def setup_test_data(self):
        # Create test user
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('Test1234!')
        user.save()
        self.user_id = user.id
        
        # Create test account
        account = Account(
            user_id=user.id,
            account_number='1234567890',
            account_type='savings',
            balance=5000.00
        )
        account.save()
        self.account_id = account.id
        
        # Create transaction categories
        categories = [
            TransactionCategory(name='Housing'),
            TransactionCategory(name='Food'),
            TransactionCategory(name='Transportation'),
            TransactionCategory(name='Utilities'),
            TransactionCategory(name='Entertainment')
        ]
        for category in categories:
            category.save()
        
        # Get auth token
        response = self.client.post('/api/auth/login',
            json={'username': 'testuser', 'password': 'Test1234!'}
        )
        data = json.loads(response.data)
        self.access_token = data['access_token']
        self.headers = {'Authorization': f'Bearer {self.access_token}'}
    
    def test_budget_endpoints(self):
        # Test POST /budgets
        budget_data = {
            'name': 'Monthly Food',
            'amount': 500.00,
            'start_date': (datetime.datetime.now()).strftime('%Y-%m-%d'),
            'end_date': (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
        }
        
        response = self.client.post('/api/budgets', 
            json=budget_data, 
            headers=self.headers
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['budget']['name'], 'Monthly Food')
        budget_id = data['budget']['id']
        
        # Test GET /budgets
        response = self.client.get('/api/budgets', headers=self.headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['budgets']), 1)
        
        # Test PUT /budgets/:id
        update_data = {
            'amount': 600.00
        }
        
        response = self.client.put(f'/api/budgets/{budget_id}', 
            json=update_data, 
            headers=self.headers
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['budget']['amount'], 600.00)
    
    def test_transaction_categories_endpoint(self):
        # Test GET /transactions/categories
        response = self.client.get('/api/transactions/categories', headers=self.headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['categories']), 5)  # We added 5 categories in setup
    
    def test_bill_endpoints(self):
        # Test POST /bills
        bill_data = {
            'biller_name': 'Electricity Company',
            'due_date': (datetime.datetime.now() + datetime.timedelta(days=15)).strftime('%Y-%m-%d'),
            'amount': 150.00,
            'account_id': self.account_id
        }
        
        response = self.client.post('/api/bills', 
            json=bill_data, 
            headers=self.headers
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['bill']['biller_name'], 'Electricity Company')
        bill_id = data['bill']['id']
        
        # Test GET /bills
        response = self.client.get('/api/bills', headers=self.headers)
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['bills']), 1)
        
        # Test PUT /bills/:id
        update_data = {
            'amount': 160.00
        }
        
        response = self.client.put(f'/api/bills/{bill_id}', 
            json=update_data, 
            headers=self.headers
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['bill']['amount'], 160.00)
        
        # Test DELETE /bills/:id (which actually just cancels it)
        response = self.client.delete(f'/api/bills/{bill_id}', headers=self.headers)
        
        self.assertEqual(response.status_code, 200)
        
        # Verify bill is now cancelled
        response = self.client.get('/api/bills', headers=self.headers)
        data = json.loads(response.data)
        
        self.assertEqual(data['bills'][0]['status'], 'cancelled')
    
    def test_validation_errors(self):
        # Test invalid budget data
        invalid_budget = {
            'name': 'Invalid Budget',
            'amount': -100.00,  # Invalid negative amount
            'start_date': '2023-01-01',
            'end_date': '2023-01-01'  # Same as start date - invalid
        }
        
        response = self.client.post('/api/budgets', 
            json=invalid_budget, 
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)
        
        # Test invalid bill data - insufficient balance
        invalid_bill = {
            'biller_name': 'Big Expense',
            'due_date': '2023-12-31',
            'amount': 10000.00,  # More than account balance
            'account_id': self.account_id
        }
        
        response = self.client.post('/api/bills', 
            json=invalid_bill, 
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()

