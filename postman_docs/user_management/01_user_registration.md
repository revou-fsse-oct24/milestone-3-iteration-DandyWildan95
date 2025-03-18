# User Registration Endpoint Documentation

## Endpoint Details
- **Method:** POST
- **URL:** `/users`
- **Authentication:** Not Required

## Request Specification

### Request Headers
| Header        | Value             | Description                     |
|---------------|-------------------|--------------------------------|
| Content-Type  | application/json  | Indicates JSON payload         |

### Request Body Parameters
| Parameter     | Type   | Required | Description                       | Constraints                                                     |
|--------------|--------|----------|-----------------------------------|----------------------------------------------------------------|
| username     | String | Yes      | Unique username for the account   | 3-50 characters, alphanumeric and underscores                  |
| email        | String | Yes      | User's email address              | Must be a valid email format                                   |
| password     | String | Yes      | Password for the account          | Minimum 12 characters, must include uppercase, lowercase, number, and special character |
| first_name   | String | No       | User's first name                 | Maximum 50 characters                                          |
| last_name    | String | No       | User's last name                  | Maximum 50 characters                                          |
| phone_number | String | No       | User's phone number               | 9-15 digits, optional international format                     |

### Example Request Payload
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "StrongPass123!@#",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "+1234567890"
}
mkdir -p "c:\Tugas Revou\Module-3-Dandy\postman_docs"
cat > "c:\Tugas Revou\Module-3-Dandy\postman_docs\01_user_management_overview.md" << 'EOL'
# RevoBank User Management API Documentation

## Overview
The User Management API provides endpoints for user-related operations in the RevoBank application. These endpoints handle user registration, authentication, profile management, and user-specific interactions.

## Endpoints
1. **User Registration:** `/users` (POST)
   - Create a new user account
   - No authentication required

2. **User Login:** `/login` (POST)
   - Authenticate user and generate access token
   - No authentication required

3. **Get User Profile:** `/users/me` (GET)
   - Retrieve current user's profile information
   - Requires JWT authentication

4. **Update User Profile:** `/users/me` (PUT)
   - Update current user's profile details
   - Requires JWT authentication

## Authentication
- Uses JWT (JSON Web Token) for secure authentication
- Tokens are generated upon successful login
- Include token in `Authorization` header for protected endpoints

## Security Considerations
- Passwords are hashed before storage
- Unique constraints on username and email
- Minimum password complexity requirements
- Token-based authentication with expiration

## Error Handling
- Consistent error response format
- Descriptive error messages
- Appropriate HTTP status codes

## Versioning
- Current API version: v1
- Base URL: `/api/v1/`

## Rate Limiting
- Implemented to prevent abuse
- Specific limits may vary based on endpoint

## Compliance
- GDPR and data protection considerations
- Secure handling of personal information
