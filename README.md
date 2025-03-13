# RevoBank API

## Overview
RevoBank is a comprehensive banking API that provides secure and efficient financial management services. Built with Flask and SQLAlchemy, it offers robust user, account, and transaction management.

## Features
- User Registration and Authentication
- Account Management
- Transaction Processing
- Secure JWT-based Authorization
- Role-based Access Control

## Technology Stack
- Python 3.9+
- Flask
- SQLAlchemy
- JWT Authentication
- PostgreSQL

## Installation

### Prerequisites
- Python 3.9+
- pip
- Virtual Environment

### Setup Steps
1. Clone the repository
```bash
git clone https://github.com/yourusername/revobank.git
cd revobank
```

2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Set Environment Variables
Create a `.env` file with:
```
FLASK_APP=src/app.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/revobank
JWT_SECRET_KEY=your_secret_key
```

5. Initialize Database
```bash
flask db upgrade
```

## API Endpoints

### Authentication
- `POST /auth/register`: Create new user
- `POST /auth/login`: User login
- `POST /auth/refresh`: Refresh access token

### User Management
- `GET /users/me`: Get current user profile
- `PUT /users/me`: Update user profile

### Account Management
- `GET /accounts`: List user accounts
- `GET /accounts/<id>`: Get specific account details
- `POST /accounts`: Create new account
- `PUT /accounts/<id>`: Update account
- `DELETE /accounts/<id>`: Delete account

### Transaction Management
- `GET /transactions`: List transactions
- `GET /transactions/<id>`: Get transaction details
- `POST /transactions`: Create new transaction

## Postman Documentation
[Postman API Documentation](https://documenter.getpostman.com/view/your-postman-link)

## Testing
Run tests using:
```bash
python -m pytest
```

## Deployment
Deployed on Heroku: [RevoBank API](https://revobank-api.herokuapp.com)

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
MIT License
