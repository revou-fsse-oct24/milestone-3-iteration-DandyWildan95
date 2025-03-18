<<<<<<< HEAD
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
=======
## REVOBANK PROJECT
=======
# Activity Diagrams Documentation

This README explains the purpose, key decisions, and processes represented in the **User Authentication** and **Transaction Handling** activity diagrams. These UML-compliant diagrams were created using draw.io to visualize workflows involving actors, decisions, and outcomes.

---

## **1. User Authentication Activity Diagram**

<img width="258" alt="User Authentication" src="https://github.com/user-attachments/assets/7aaffec4-fc75-4170-a125-c9e9e1342030" />



### **Purpose**
This diagram outlines the workflow for authenticating a user, including login, password verification, error handling, and token generation for successful logins.

### **Actors Involved**
- **User**: Initiates the login process.
- **Authentication Service**: Verifies credentials and manages token generation.

---

### **Key Processes**
1. **Login Initiation**: 
   - The user submits credentials (username/password).
2. **Password Verification**: 
   - The Authentication Service checks if the password matches stored records.
3. **Token Generation**: 
   - On success, a token is generated for session management.
4. **Error Handling**: 
   - Invalid credentials trigger an error message and retry logic.

### **Key Decisions**
- **Valid Password?**: 
  - If `Yes`, proceed to generate a token.
  - If `No`, display an error and prompt for retry.
- **Retry?**: 
  - If `Yes`, loop back to credential submission.
  - If `No`, terminate the process.

### **Outcomes**
- ✅ **Success**: User gains access (token generated).
- ❌ **Failure**: Process terminates after retry attempts.

---

## **2. Transaction Handling Activity Diagram**

<img width="204" alt="Transaction Authentication" src="https://github.com/user-attachments/assets/62fa8e31-0496-4aed-8fd0-67f9faceff52" />


### **Purpose**
This diagram visualizes the workflow for processing transactions, including balance verification, transaction completion, and history generation.

### **Actors Involved**
- **User**: Initiates the transaction.
- **Transaction Service**: Validates balances and processes transactions.

---

### **Key Processes**
1. **Transaction Initiation**: 
   - The user inputs transaction details (e.g., amount, recipient).
2. **Balance Verification**: 
   - The Transaction Service checks if the user’s account has sufficient funds.
3. **Transaction Completion**: 
   - On success, funds are transferred.
4. **History Generation**: 
   - A record is added to the transaction history.

### **Key Decisions**
- **Sufficient Balance?**: 
  - If `Yes`, complete the transaction.
  - If `No`, display an error and prompt for retry.
- **Retry?**: 
  - If `Yes`, loop back to transaction initiation.
  - If `No`, terminate the process.

### **Outcomes**
- ✅ **Success**: Transaction completed and history updated.
- ❌ **Failure**: Process terminates after retry attempts.

---

## **How to Use These Diagrams**
1. **System Design**: 
   - Clarify authentication and transaction logic during planning.
2. **Documentation**: 
   - Supplement technical specs for developers or stakeholders.
3. **Troubleshooting**: 
   - Identify failure points (e.g., invalid credentials, insufficient funds).
4. **Training**: 
   - Onboard teams on system workflows.

---

## **Key Takeaways**
- **Swimlanes**: Separate responsibilities between actors (User vs. Services).
- **Decision Nodes**: Represent critical branching logic (e.g., "Valid Password?").
- **Retry Loops**: Handle errors gracefully by allowing user retries.
- **UML Compliance**: Follows standards for clarity and interoperability.

---

## **Tools Used**
- **draw.io**: For creating UML-compliant diagrams with swimlanes and decision nodes.
- **Mermaid Syntax**: Optional text-based visualization (see [Mermaid Live Editor](https://mermaid.live)).

---

For feedback or updates, open an issue or contact the maintainers.  
>>>>>>> 0a797a6 (Initial commit)
>>>>>>> e85cba193e864b89fc47f0ce728ff1474623660e
