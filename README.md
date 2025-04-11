
# RevoBank Backend

## Project Overview
RevoBank is a comprehensive financial management application designed to help users track their finances, manage transactions, and gain insights into their spending habits.

## Features
- User Authentication
- User Profile Management
- Account Management
- Transaction Tracking
- Budget Planning
- Bill Management

## Authentication Routes
### Auth Routes (`/auth`)
- `POST /auth/register`: User registration
  - Validates email format
  - Enforces password strength requirements
- `POST /auth/login`: User login
- `POST /auth/logout`: User logout
- `GET /auth/profile`: Retrieve user profile information

## User Management Routes (`/user`)
- `PUT /user/update_profile`: Update user profile
  - Change username
  - Change email
- `PUT /user/change_password`: Change user password
- `DELETE /user/delete_account`: Delete user account

## Account Management Routes (`/account`)
- `POST /account/create`: Create a new bank account
- `GET /account/list`: List all user accounts
- `GET /account/<account_id>`: Get specific account details

## Technology Stack
- Backend: Flask
- Authentication: Flask-Login
- Database: SQLAlchemy
- API: Flask-RESTful
- JWT: Flask-JWT-Extended

## Prerequisites
- Python 3.8+
- pip
- Virtual Environment

## Installation
1. Clone the repository
2. Create a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables
5. Initialize the database
   ```
   flask db upgrade
   ```

## Running the Application
```
flask run
```

## Testing
```
python -m pytest
```

## Security Features
- Password hashing
- Email validation
- Login attempt protection
- Secure user sessions

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Contact
Repository: [milestone-3-iteration-DandyWildan95](https://github.com/revou-fsse-oct24/milestone-3-iteration-DandyWildan95.git)
=======
