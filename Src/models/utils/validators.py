import re
from email_validator import validate_email, EmailNotValidError

def validate_input(input_type, input_value):
    """
    Comprehensive input validator
    """
    validators = {
        'password': validate_password,
        'email': validate_email_address,
        'phone': validate_phone_number,
        'account_number': validate_account_number,
        'transaction_amount': validate_transaction_amount
    }

    if input_type not in validators:
        return False, "Invalid input type"

    return validators[input_type](input_value)

def validate_password(password):
    """
    Validate password strength:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is valid"

def validate_email_address(email):
    """
    Validate email address using email-validator library
    """
    try:
        validate_email(email)
        return True, "Email is valid"
    except EmailNotValidError as e:
        return False, str(e)

def validate_phone_number(phone):
    """
    Validate phone number format
    Supports international phone numbers
    """
    phone_regex = r'^\+?1?\d{9,15}$'
    if re.match(phone_regex, phone):
        return True, "Phone number is valid"
    return False, "Invalid phone number format"

def validate_account_number(account_number):
    """
    Validate bank account number
    - Must be numeric
    - Between 8 and 16 digits
    """
    if not account_number.isdigit():
        return False, "Account number must contain only digits"
    
    if len(account_number) < 8 or len(account_number) > 16:
        return False, "Account number must be between 8 and 16 digits"
    
    return True, "Account number is valid"

def validate_transaction_amount(amount):
    """
    Validate transaction amount
    - Must be a positive number
    - Cannot exceed a reasonable limit
    """
    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Transaction amount must be positive"
        
        if amount > 1_000_000:  # Configurable max transaction limit
            return False, "Transaction amount exceeds maximum limit"
        
        return True, "Transaction amount is valid"
    except ValueError:
        return False, "Invalid transaction amount"