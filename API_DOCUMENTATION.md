# API Documentation

## Authentication Endpoints

<!-- ### POST /api/auth/login
- **Description**: User login endpoint
- **Parameters**: 
  - `username` (string): User's username
  - `password` (string): User's password
- **Response**: JWT token and user information -->

### POST /api/auth/register
- **Description**: User registration endpoint
- **Parameters**:
  - `email` (string): User's email address
  - `password` (string): User's password
  - `username` (string): Desired username
- **Response**: Success message and user ID

## User Management

### GET /api/users/profile
- **Description**: Get user profile information
- **Headers**: Authorization: Bearer {token}
- **Response**: User profile data

### PUT /api/users/profile
- **Description**: Update user profile
- **Headers**: Authorization: Bearer {token}
- **Parameters**: Profile update data
- **Response**: Updated profile information
