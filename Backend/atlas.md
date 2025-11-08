---
title: ATLAS - Authentication & Authorization Service
description: Robust multi-tenant authentication and authorization service with JWT, RBAC, email verification, and enterprise-grade security features
order: 1
category: API Service
tags: [atlas, auth, jwt, rbac, multi-tenant, fastapi, security]
---

# ATLAS - Authentication & Authorization Service

ATLAS is a robust, multi-tenant authentication and authorization service built with FastAPI. It provides a complete solution for managing users, applications, roles, and permissions in a scalable, tenant-based architecture with enterprise-grade security features.

## Key Features

### 🔐 Security & Authentication

-   **JWT-based Authentication**: Secure login/logout functionality using JSON Web Tokens (JWT) with support for access and refresh tokens
-   **Rate Limiting**: Built-in request rate limiting to prevent abuse and brute force attacks
-   **Response Encryption**: Optional AES-256 encryption for API responses with configurable keys
-   **CORS Protection**: Secure CORS configuration with customizable origins
-   **Email Verification**: User email verification system with secure token-based confirmation
-   **Password Reset**: Secure password reset flow with time-limited tokens

### 🏢 Multi-Tenant Architecture

-   **Schema Isolation**: Complete tenant separation using PostgreSQL schemas via `X-Tenant-Schema` header
-   **Tenant Management**: Administrative endpoints for creating and managing tenant schemas (can be disabled for production)
-   **Seed Data Protection**: Built-in protection against accidental deletion of seed data

### 👥 User & Access Management

-   **User Management**: Complete CRUD operations for managing users within each tenant
-   **Application Management**: Registration and management of different applications that use the authentication service
-   **Role-Based Access Control (RBAC)**: Define granular roles with permissions for each application
-   **User Role Assignment**: Flexible assignment and revocation of roles to/from users
-   **Permission System**: Fine-grained permission control per application and role

### 📧 Communication & Notifications

-   **Email System**: Built-in SMTP support for transactional emails (verification, password reset)
-   **HTML Email Templates**: Customizable email templates with Jinja2 templating
-   **Email Cooldown**: Anti-spam protection with configurable cooldown periods

### 🚀 Development & Deployment

-   **Database Seeding**: Automated initialization scripts for default tenants and sample data
-   **Docker Ready**: Fully containerized with Docker for easy setup, development, and deployment
-   **Environment-based Configuration**: Comprehensive configuration via environment variables
-   **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Technology Stack

-   **Backend**: Python, FastAPI
-   **Database**: PostgreSQL (with SQLAlchemy ORM)
-   **Security**: JWT tokens, AES-256 encryption, Rate limiting (slowapi)
-   **Email**: fastapi-mail with SMTP support
-   **Templates**: Jinja2 for email templates
-   **Containerization**: Docker, Docker Compose

## Project Structure

```
/app
|-- api/                # API endpoints and dependencies
|   |-- deps.py         # Dependencies for endpoints (auth, DB session, role checks)
|   |-- v1/             # API version 1
|       |-- api.py      # Main API router with conditional tenant management
|       |-- endpoints/  # Routers for each resource
|           |-- auth.py         # Authentication endpoints
|           |-- users.py        # User management
|           |-- roles.py        # Role management
|           |-- applications.py # Application management
|           |-- tenants.py      # Tenant management (conditional)
|           |-- health.py       # Health check
|-- core/               # Core components
|   |-- config.py       # Application configuration
|   |-- security.py     # JWT and security utilities
|   |-- encryption.py   # AES encryption for responses
|   |-- mailer.py       # Email service configuration
|-- db/                 # Database session management and base models
|-- models/             # SQLAlchemy ORM models
|-- repositories/       # Data access layer (interacts with the DB)
|-- schemas/            # Pydantic schemas for data validation
|-- services/           # Business logic layer
|-- templates/          # Jinja2 email templates
|-- utils/              # Utility scripts
|   |-- database_init.py    # Database initialization
|   |-- seed_protection.py  # Seed data protection
|   |-- email_cooldown.py   # Email rate limiting
|   |-- response_encryption.py # Response encryption utilities
|-- main.py             # Main FastAPI application entrypoint
```

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

-   Docker
-   Docker Compose

### 1. Clone the Repository

```sh
git clone https://github.com/GratiaManullang03/atlas.git
cd atlas
```

### 2. Configure Environment Variables

The application uses a `.env` file for configuration. Copy the provided example and fill in your details.

```sh
cp .env.example .env
```

Now, edit the `.env` file with your specific configuration:

```env
# -------------------------------------
# APPLICATION SETTINGS
# -------------------------------------
APP_NAME=ATLAS
APP_VERSION=1.0.0
DEBUG=True

# -------------------------------------
# DATABASE CONNECTION
# -------------------------------------
# Contoh untuk PostgreSQL
DATABASE_URL=postgresql://atlas_user:atlas_password@localhost:5432/atlas_db

# -------------------------------------
# REDIS CONNECTION (OPSIONAL)
# -------------------------------------
# Kosongkan jika tidak digunakan
REDIS_URL=redis://localhost:6379/0

# -------------------------------------
# JWT & SECURITY
# -------------------------------------
# Ganti dengan key yang sangat rahasia, bisa generate online
SECRET_KEY=ganti_dengan_kunci_rahasia_yang_sangat_panjang_dan_acak
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000/api/v1

# -------------------------------------
# MULTI-TENANCY
# -------------------------------------
# Skema default jika X-Tenant-Schema tidak disediakan
DEFAULT_SCHEMA=public

# -------------------------------------
# SMTP EMAIL CONFIGURATION
# -------------------------------------
# Ganti dengan kredensial email Anda
MAIL_USERNAME=noreply@domainanda.com
MAIL_PASSWORD=password_email_anda
MAIL_FROM=noreply@domainanda.com
MAIL_FROM_NAME="ATLAS Service (No Reply)"
MAIL_SERVER=smtp.domainanda.com
MAIL_PORT=465

# --- Pengaturan Keamanan Email (Pilih salah satu) ---
# Untuk koneksi SSL/TLS (biasanya port 465)
MAIL_SSL_TLS=True
MAIL_STARTTLS=False

# Untuk koneksi STARTTLS (biasanya port 587)
# MAIL_SSL_TLS=False
# MAIL_STARTTLS=True

# -------------------------------------
# ENCRYPTION SETTINGS
# -------------------------------------
# Enable/disable response encryption
ENCRYPTION_RESPONSE=false
# 32-character encryption key for AES-256
ENCRYPTION_KEY=atlas_secure_key_2025_32chars!!
# 16-character initialization vector
ENCRYPTION_IV=atlas_iv_16char

# -------------------------------------
# DEVELOPMENT/ADMIN FEATURES
# -------------------------------------
# Enable tenant management endpoints (DISABLE for production/client deployment)
# Set to true only for development or admin maintenance
ENABLE_TENANT_MANAGEMENT=false
```

### ⚠️ Security Configuration

**Generate Secure Keys**: You must replace the following keys with secure, random values:

1. **SECRET_KEY** (for JWT tokens):

```sh
openssl rand -hex 64
```

2. **ENCRYPTION_KEY** (32 characters for AES-256):

```sh
openssl rand -hex 16
```

3. **ENCRYPTION_IV** (16 characters for AES):

```sh
openssl rand -hex 8
```

Copy the generated outputs and paste them into the `.env` file.

### 3. Build and Run with Docker

Use Docker Compose to build and run the application and its services:

```sh
docker-compose up --build -d
```

For development with hot-reloading, you can use the override file:

```sh
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build -d
```

### 4. Access the API

The API will be available at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

## API Usage

### Headers Required

When interacting with the API, you may need to provide the following headers:

-   **Authorization**: `Bearer <your_jwt_token>` for accessing protected endpoints
-   **X-Tenant-Schema**: The name of the tenant schema you want to operate on (e.g., `default_tenant`). If not provided, it will use the `DEFAULT_SCHEMA` from your configuration

### Error Codes & Responses

ATLAS uses standard HTTP status codes to indicate the success or failure of API requests. All error responses follow a consistent format:

```json
{
    "success": false,
    "message": "Error description",
    "data": null
}
```

#### Common Error Codes

| Status Code                   | Description              | Common Causes                                                                                                                     | Solution                                                    |
| ----------------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **400 Bad Request**           | Invalid request data     | - Username/email already exists<br>- Application code already exists<br>- Role code already exists<br>- Invalid data format       | Check request payload and ensure unique constraints are met |
| **401 Unauthorized**          | Authentication failed    | - Missing or invalid JWT token<br>- Token expired<br>- Invalid credentials<br>- Session fingerprint mismatch                      | Login again or refresh your access token                    |
| **403 Forbidden**             | Insufficient permissions | - Missing required permission<br>- No access to application<br>- Role level too low<br>- Attempting to modify protected seed data | Contact admin for proper role/permission assignment         |
| **404 Not Found**             | Resource not found       | - User not found<br>- Role not found<br>- Application not found<br>- Role assignment not found<br>- Tenant not found              | Verify resource ID exists in the system                     |
| **409 Conflict**              | Resource conflict        | - Tenant schema already exists                                                                                                    | Use a different name or remove existing resource            |
| **422 Unprocessable Entity**  | Token validation failed  | - Refresh token expired<br>- Refresh token invalid                                                                                | Login again to get new tokens                               |
| **429 Too Many Requests**     | Rate limit exceeded      | - Too many email verification requests<br>- Too many password reset requests<br>- Too many login attempts (5/minute)              | Wait for cooldown period before retrying                    |
| **500 Internal Server Error** | Server error             | - Database connection failed<br>- Tenant creation failed<br>- Encryption failed<br>- Unexpected server error                      | Check server logs and database connectivity                 |

#### Detailed Error Scenarios

##### Authentication Errors (401)

**Invalid Credentials**

```json
{
    "detail": "Invalid credentials or inactive account"
}
```

-   **Cause**: Wrong username/password or account is inactive
-   **Solution**: Verify credentials and account status

**Session Fingerprint Mismatch**

```json
{
    "detail": "Session fingerprint mismatch - token used from different device/location"
}
```

-   **Cause**: JWT token used from different device or IP address
-   **Solution**: Login again from current device

**Not Authenticated**

```json
{
    "detail": "Not authenticated"
}
```

-   **Cause**: No valid token provided
-   **Solution**: Include valid JWT token in Authorization header

##### Authorization Errors (403)

**Insufficient Permissions**

```json
{
    "detail": "Not enough permissions. Requires: users:read"
}
```

-   **Cause**: User doesn't have required permission
-   **Solution**: Contact admin to assign proper role with required permissions

**Application Access Denied**

```json
{
    "detail": "Not enough permissions. Requires access to application: APP_CODE"
}
```

-   **Cause**: User doesn't have role for the required application
-   **Solution**: Request access to the application from admin

**Role Level Insufficient**

```json
{
    "detail": "Forbidden. Required role level: 1, 2"
}
```

-   **Cause**: User's role level is too low
-   **Solution**: Request higher role level from admin

**Protected Seed Data**

```json
{
    "detail": "Cannot delete seed admin user. This user is protected."
}
```

-   **Cause**: Attempting to modify/delete protected seed data (ATLAS app, SUPER_ADMIN role, admin user)
-   **Solution**: Seed data cannot be modified to maintain system integrity

##### Token Errors (422)

**Refresh Token Expired**

```json
{
    "detail": "Refresh token expired, please login again"
}
```

-   **Cause**: Refresh token has expired (default: 30 days)
-   **Solution**: Perform full login to get new tokens

##### Rate Limiting Errors (429)

**Email Verification Cooldown**

```json
{
    "detail": "Verification email sudah dikirim. Mohon tunggu sebelum meminta lagi."
}
```

-   **Cause**: Verification email requested too frequently
-   **Solution**: Wait for cooldown period (default: 5 minutes)

**Password Reset Cooldown**

```json
{
    "detail": "Reset password email sudah dikirim. Mohon tunggu sebelum meminta lagi."
}
```

-   **Cause**: Password reset requested too frequently
-   **Solution**: Wait for cooldown period (default: 5 minutes)

**Login Rate Limit**

-   **Limit**: 5 requests per minute per IP
-   **Solution**: Wait before attempting more login requests

#### Error Response Examples

**Success Response:**

```json
{
    "success": true,
    "message": "User created successfully",
    "data": {
        "user_id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    }
}
```

**Error Response:**

```json
{
    "success": false,
    "message": "User not found",
    "data": null
}
```

**Validation Error (FastAPI automatic):**

```json
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "value is not a valid email address",
            "type": "value_error.email"
        }
    ]
}
```

### Available Endpoints

#### Authentication (`/api/v1/auth`)

-   `POST /login` - User login with username/email and password
-   `POST /refresh` - Refresh access token using refresh token
-   `POST /logout` - Logout and invalidate tokens
-   `GET /me` - Get current user information
-   `POST /request-verification` - Request email verification
-   `GET /verify-email` - Verify email with token
-   `POST /forgot-password` - Request password reset
-   `GET /reset-password` - Password reset form
-   `POST /reset-password` - Submit new password

#### Users (`/api/v1/users`)

-   `GET /` - List all users (with pagination)
-   `GET /{user_id}` - Get specific user
-   `POST /` - Create new user
-   `PUT /{user_id}` - Update user
-   `DELETE /{user_id}` - Delete user
-   `POST /{user_id}/roles` - Assign roles to user
-   `GET /{user_id}/roles` - Get user roles
-   `DELETE /{user_id}/roles/{role_id}` - Remove role from user

#### Applications (`/api/v1/applications`)

-   `GET /` - List all applications
-   `GET /{app_id}` - Get specific application with roles
-   `POST /` - Create new application
-   `PUT /{app_id}` - Update application
-   `DELETE /{app_id}` - Delete application

#### Roles (`/api/v1/roles`)

-   `GET /` - List all roles
-   `GET /{role_id}` - Get specific role
-   `POST /` - Create new role
-   `PUT /{role_id}` - Update role
-   `DELETE /{role_id}` - Delete role
-   `PUT /{role_id}/permissions` - Update role permissions

#### Tenant Management (`/api/v1/tenants`) \*

-   `POST /` - Create new tenant schema
-   `GET /` - List all tenants
-   `GET /{schema_name}` - Get specific tenant info
-   `DELETE /{schema_name}` - Delete tenant schema

_Note: Tenant management endpoints are only available when `ENABLE_TENANT_MANAGEMENT=true`_

#### Health Check (`/api/v1/health`)

-   `GET /` - Application health status

## Configuration Options

### Security Features

1. **Response Encryption**: Set `ENCRYPTION_RESPONSE=true` to enable AES-256 encryption of all API responses
2. **Rate Limiting**: Built-in rate limiting (5 requests/minute for login endpoint)
3. **CORS**: Configurable CORS origins via `FRONTEND_URL`

### Email Configuration

Configure SMTP settings for email notifications:

-   Email verification for new users
-   Password reset functionality
-   Customizable HTML templates in `app/templates/`

### Tenant Management Security

For production deployments to clients:

-   Set `ENABLE_TENANT_MANAGEMENT=false` to completely disable tenant management endpoints
-   This prevents clients from accidentally or maliciously manipulating tenant data
-   Only enable for development or administrative maintenance

### Multi-Tenant Usage

1. **Default Tenant**: Requests without `X-Tenant-Schema` header use `DEFAULT_SCHEMA`
2. **Tenant Isolation**: Each tenant has its own PostgreSQL schema with complete data isolation
3. **Tenant Creation**: Use tenant management endpoints to create new schemas

## Development

### Running Tests

```sh
# Run tests inside the container
docker-compose exec app pytest

# Or run specific test file
docker-compose exec app pytest tests/test_auth.py
```

### Database Migrations

```sh
# Generate new migration
docker-compose exec app alembic revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec app alembic upgrade head
```

### Logs

```sh
# View application logs
docker-compose logs -f app

# View database logs
docker-compose logs -f db
```

## Production Deployment

### Security Checklist

-   [ ] Set `DEBUG=false`
-   [ ] Generate secure `SECRET_KEY`, `ENCRYPTION_KEY`, and `ENCRYPTION_IV`
-   [ ] Configure proper SMTP settings
-   [ ] Set `ENABLE_TENANT_MANAGEMENT=false` for client deployments
-   [ ] Configure proper `FRONTEND_URL` for CORS
-   [ ] Use strong database credentials
-   [ ] Enable HTTPS in production
-   [ ] Configure proper logging

### Environment Variables for Production

```env
DEBUG=false
ENABLE_TENANT_MANAGEMENT=false
ENCRYPTION_RESPONSE=true
# Use production database URL
# Use production email credentials
# Use secure generated keys
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
