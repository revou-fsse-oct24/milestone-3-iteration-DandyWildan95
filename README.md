# RevoBank - Modern Banking Application

## Overview
RevoBank is a comprehensive banking application that provides users with a range of financial management features. The application offers core banking functionality as well as advanced financial tools to help users manage their finances effectively.

## Features

### Core Banking
- User account creation and management
- Multiple bank accounts per user
- Transaction history and tracking
- Secure authentication with JWT

### Advanced Financial Management
- **Budget Tracking**: Create and manage budgets for different spending categories
- **Bill Payments**: Schedule and manage bill payments to various billers
- **Transaction Categorization**: Categorize transactions for better financial insights

## Technical Stack
- **Backend**: Python with Flask and Flask-RESTful
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens) with Flask-JWT-Extended
- **Containerization**: Docker

## Installation & Setup

### Prerequisites
- Python 3.9+
- MySQL Server
- Docker and Docker Compose (optional)

### Database Setup
1. Create a MySQL database:
   ```sql
   CREATE DATABASE revobank;
   CREATE USER 'revobank_user'@'localhost' IDENTIFIED BY 'Bangsat1';
   GRANT ALL PRIVILEGES ON revobank.* TO 'revobank_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Using Docker
1. Clone the repository:
   ```
   git clone https://github.com/revou-fsse-oct24/milestone-3-DandyWildan95.git
   cd milestone-3-DandyWildan95
   ```

2. Make sure Docker Desktop is running

3. Build and start the Docker container:
   ```
   docker-compose build
   docker-compose up -d
   ```

4. The application will be available at `http://localhost:5000`

### Without Docker
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. For MySQL support, install system dependencies:
   ```
   # Ubuntu/Debian
   sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
   
   # macOS
   brew install mysql-client
   ```

3. Run the application:
   ```
   export FLASK_APP=src/app.py
   flask run
   ```

## API Documentation

### Authentication
- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Login and get JWT token

### Accounts
- `GET /api/accounts`: Get all accounts for the authenticated user
- `POST /api/accounts`: Create a new account
- `GET /api/accounts/:id`: Get account details by ID
- `GET /api/accounts/:id/transactions`: Get transactions for an account

### Budgets
- `POST /api/budgets`: Create a new budget
- `GET /api/budgets`: Get all budgets for the authenticated user
- `PUT /api/budgets/:id`: Update a budget

### Transaction Categories
- `GET /api/transactions/categories`: Get all transaction categories

### Bill Payments
- `POST /api/bills`: Schedule a new bill payment
- `GET /api/bills`: Get all scheduled bill payments
- `PUT /api/bills/:id`: Update a scheduled bill payment
- `DELETE /api/bills/:id`: Cancel a scheduled bill payment

## Testing

Run the automated tests with:

```bash
docker-compose exec web python test.py
```

For testing MySQL connectivity:
```
python src
