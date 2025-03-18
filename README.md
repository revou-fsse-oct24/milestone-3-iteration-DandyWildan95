# RevoBank API

## Overview
RevoBank is a comprehensive RESTful API for banking operations, providing secure user, account, and transaction management.

## Features

### User Management
- User registration
- Profile retrieval and updates
- Secure JWT authentication

### Account Management
- Create, retrieve, update, and delete accounts
- Account balance tracking

### Transaction Management
- Deposit and withdrawal
- Account transfers
- Bill payments
- Investment transactions

## Technology Stack
- Flask
- SQLAlchemy
- Flask-RESTful
- JWT Authentication
- MySQL

## API Documentation
[View Postman Documentation](https://speeding-flare-28031.postman.co/workspace/My-Workspace~093f9620-066f-4483-8e19-81443a4b18ec/folder/43112813-6f6d170e-8a03-4bdc-bde4-108c105709d4?action=share&creator=43112813&ctx=documentation)

## Prerequisites
- Python 3.9+
- pip
- virtualenv
- MySQL
- UV (Universal Virtualenv) 0.6.6+

### Dependency Management
This project uses UV (Universal Virtualenv) for efficient dependency management and virtual environment setup. To install and manage dependencies:

```bash
# Install UV
pip install uv

# Create a virtual environment
uv venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate
# On Unix or MacOS
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

## Local Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/revobank-api.git
cd revobank-api
```

## Deployment to Render

### Prerequisites
- Render account
- GitHub repository with your project
- Environment variables prepared

### Deployment Strategy
This project is optimized for deployment on Render, a modern cloud platform that simplifies web service hosting.

### Deployment Steps
1. Push your code to GitHub repository
2. Log in to Render (https://render.com/)
3. Create a new Web Service
4. Connect your GitHub repository: 
   `https://github.com/revou-fsse-oct24/milestone-3-DandyWildan95`
5. Configure deployment settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Python Version: 3.9+

### Environment Configuration
Render requires specific environment variable setup:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Secure application secret
- `JWT_SECRET_KEY`: JWT token generation key
- `FLASK_ENV`: production

### Render-Specific Recommendations
- Use Render's PostgreSQL database service
- Leverage built-in environment variable management
- Enable automatic deployments from GitHub

### Environment Variables
Ensure the following environment variables are set in Render:
- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- Other sensitive configuration values

### Troubleshooting
- Verify all dependencies in `requirements.txt`
- Check `Procfile` for correct start command
- Ensure `wsgi.py` is correctly configured