---
title: ATAPOS - Point of Sale System
description: A comprehensive Point of Sale (POS) API system built with FastAPI, featuring multi-tenant architecture, integrated payment gateway (Midtrans), customer authentication, and real-time order management for restaurants, retail stores, and service businesses
order: 15
category: Backend Application
tags: [pos, fastapi, postgresql, midtrans, multi-tenant, atlas-sso, cloudinary]
---

# ATAPOS - Point of Sale System

A comprehensive Point of Sale (POS) API system built with FastAPI, featuring multi-tenant architecture, integrated payment gateway (Midtrans), customer authentication, and real-time order management for restaurants, retail stores, and service businesses.

## Table of Contents

-   [Key Features](#key-features)
-   [Technology Stack](#technology-stack)
-   [Prerequisites](#prerequisites)
-   [Installation](#installation)
-   [Configuration](#configuration)
-   [Running the Application](#running-the-application)
-   [API Endpoints](#api-endpoints)
-   [Architecture](#architecture)
-   [Business Logic](#business-logic)
-   [Security](#security)
-   [Testing](#testing)
-   [Deployment](#deployment)
-   [Project Structure](#project-structure)

## Key Features

-   **Multi-Tenant Architecture**: Complete merchant isolation with per-tenant configuration
-   **Product Management**: Categories, variants, pricing, and inventory tracking with image attachments via Cloudinary
-   **Order Management**: Complete order lifecycle from creation to payment with order items and customer details
-   **Payment Integration**: Midtrans payment gateway integration with transaction logging
-   **Promotions**: Flexible promotion system with product-specific discounts
-   **Customer Authentication**: Magic link and OTP-based authentication for customers via email
-   **Table Management**: Location-based ordering for restaurant/cafe businesses
-   **Atlas SSO Integration**: Enterprise authentication via ATAMS (Atlas Microservices)
-   **Role-Based Access Control**: Admin (level 100) and Officer (level 10) roles

## Technology Stack

-   **Framework**: FastAPI 0.115+
-   **Database**: PostgreSQL (Cloud-hosted via Aiven/similar)
-   **ORM**: SQLAlchemy with connection pooling
-   **Authentication**: Atlas SSO (ATAMS) + JWT for customers
-   **Validation**: Pydantic v2
-   **Server**: Uvicorn
-   **Storage**: Cloudinary for product images
-   **Payment Gateway**: Midtrans
-   **Email Service**: SMTP (FastAPI-Mail)
-   **ATAMS Toolkit**: Code generation and utilities

## Prerequisites

-   Python 3.10+
-   PostgreSQL database (cloud-hosted recommended)
-   Cloudinary account for image storage
-   Midtrans account for payment processing
-   Atlas SSO credentials (ATAMS)
-   SMTP server for email notifications

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/[username]/atapos.git
    cd atapos
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - Linux/Mac:
        ```bash
        source venv/bin/activate
        ```
    - Windows:
        ```bash
        venv\Scripts\activate
        ```

4. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the project root directory with the following variables (see `.env.example` for reference):

```env
# Application Settings
APP_NAME=ATAPOS - Point of Sale System
APP_VERSION=1.0.0
DEBUG=true

# Role Levels Configuration
# ADMIN (Owner) = 100 - Full access to all merchant data and operations
# OFFICER (Staff) = 10 - Limited access to daily operations

# Database Configuration
DATABASE_URL=postgresql://user:password@host:port/database

# Database Connection Pool Settings
# IMPORTANT: Tune based on your database connection limit!
# For Aiven free tier (20 connections): DB_POOL_SIZE=3, DB_MAX_OVERFLOW=5 (max 8 per app)
# Formula: Total Connections = (DB_POOL_SIZE + DB_MAX_OVERFLOW) × Number of App Instances
DB_POOL_SIZE=3
DB_MAX_OVERFLOW=5
DB_POOL_RECYCLE=3600
DB_POOL_TIMEOUT=30
DB_POOL_PRE_PING=true

# Atlas SSO Configuration
ATLAS_SSO_URL=https://api.atlas-microapi.atamsindonesia.com/api/v1
ATLAS_APP_CODE=ATAPOS
ATLAS_ENCRYPTION_KEY=[32-char-key]
ATLAS_ENCRYPTION_IV=[16-char-iv]

# Response Encryption (for GET endpoints)
# Generate secure keys using:
#   Key (32 chars): openssl rand -hex 16
#   IV (16 chars):  openssl rand -hex 8
ENCRYPTION_ENABLED=false
ENCRYPTION_KEY=change_me_32_characters_long!!
ENCRYPTION_IV=change_me_16char

# CORS Configuration
CORS_ORIGINS=["*.atamsindonesia.com"]

# Logging
LOGGING_ENABLED=true
LOG_LEVEL=INFO
LOG_TO_FILE=false

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Merchant Configuration
DEFAULT_MERCHANT_ID=1

# Midtrans Payment Gateway
# Note: Merchant-specific credentials are stored in database (merchant table)
# These are fallback/default values for testing
MIDTRANS_IS_PRODUCTION=false
MIDTRANS_DEFAULT_CURRENCY=IDR

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=YOUR_CLOUD_NAME
CLOUDINARY_API_KEY=YOUR_API_KEY
CLOUDINARY_API_SECRET=YOUR_API_SECRET
CLOUDINARY_FOLDER=YOUR_FOLDER_NAME

# JWT Configuration (for Customer Authentication)
# Generate a strong secret key using: openssl rand -hex 32
JWT_SECRET_KEY=change-this-to-random-secret-key-in-production-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=168

# Customer Authentication Configuration
MAGIC_LINK_EXPIRE_MINUTES=15
OTP_EXPIRE_MINUTES=5
OTP_LENGTH=6

# Application Configuration
# Frontend URL for magic links and redirects
APP_URL=http://localhost:3000

# SMTP Email Configuration
MAIL_USERNAME=noreply@yourdomain.com
MAIL_PASSWORD=your_email_password
MAIL_FROM=noreply@yourdomain.com
MAIL_FROM_NAME="ATLAS Service (No Reply)"
MAIL_SERVER=smtp.yourdomain.com
MAIL_PORT=465
MAIL_SSL_TLS=True
MAIL_STARTTLS=False
```

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down
```

**Access Points:**

-   API Documentation (Swagger): http://localhost:8000/docs
-   API Documentation (ReDoc): http://localhost:8000/redoc
-   Health Check: http://localhost:8000/health

**Demo Pages (Development):**

-   Customer Authentication Demo: http://localhost:8000/demo/customer-auth
-   Snap Payment Demo: http://localhost:8000/demo/snap-embedded
-   Order History Demo: http://localhost:8000/demo/order-history

## Demo Pages

ATAPOS includes interactive demo pages for testing and demonstrating key features:

### Customer Authentication Demo

**URL:** `/demo/customer-auth`

Test passwordless customer authentication with Magic Link and OTP methods:

-   Request magic link via email
-   Verify magic link token and receive JWT
-   Request OTP code via email
-   Verify OTP and receive JWT
-   Test JWT token with `/auth/customer/me` endpoint

**Features:**

-   Real-time event logging
-   JWT token display and copy
-   Token testing interface
-   Works with actual email delivery

### Snap Payment Demo

**URL:** `/demo/snap-embedded`

Interactive Midtrans Snap payment integration demo:

-   Automatic order creation (cu_id: 1, pr_id: 1, qty: 2)
-   Snap token generation
-   Embedded payment modal (credit card, QRIS, e-wallet, etc.)
-   Payment status callbacks
-   Requires valid JWT token and Midtrans client key

**Payment Flow:**

1. Enter JWT token (from customer auth demo)
2. Enter Midtrans client key (from sandbox)
3. Click "Create Test Order & Pay"
4. System creates order and generates Snap token
5. Payment modal opens automatically
6. Complete payment with test credentials
7. View payment result and status

### Order History Demo

**URL:** `/demo/order-history`

View customer order history with filtering:

-   List all orders for authenticated customer
-   Filter by payment status
-   View order details with items
-   Real-time order updates
-   Requires valid customer JWT token

---

## API Endpoints

Base URL: `/api/v1`

For detailed technical documentation including authentication requirements, validation rules, error codes, and complete flow diagrams, see [ATAMS.md](ATAMS.md).

### Authentication

**Base Path:** `/api/v1/auth/customer`

Customer authentication uses passwordless methods (Magic Link & OTP). For staff authentication, use Atlas SSO directly.

#### POST /api/v1/auth/customer/request-magic-link

Request magic link for customer login via email.

**Request Body:**

```json
{
    "email": "customer@example.com"
}
```

#### POST /api/v1/auth/customer/verify-magic-link

Verify magic link token and receive JWT.

**Request Body:**

```json
{
    "token": "uuid-token-from-email"
}
```

#### POST /api/v1/auth/customer/request-otp

Request 6-digit OTP code via email.

**Request Body:**

```json
{
    "email": "customer@example.com"
}
```

#### POST /api/v1/auth/customer/verify-otp

Verify OTP and get JWT token.

**Request Body:**

```json
{
    "email": "customer@example.com",
    "otp": "123456"
}
```

#### GET /api/v1/auth/customer/me

Get current customer information from JWT token.

**Authorization:** Required (Customer JWT token)

---

### Merchants

**Base Path:** `/api/v1/merchants`

#### GET /api/v1/merchants

List all merchants with pagination.

**Authorization:** Admin (level >= 100)

**Query Parameters:**

-   `search`: Filter by name or business type (optional)
-   `skip`: Offset pagination (default: 0)
-   `limit`: Records per page (1-1000, default: 100)

#### GET /api/v1/merchants/{id}

Get single merchant by ID.

**Authorization:** Admin (level >= 100)

#### POST /api/v1/merchants

Create new merchant.

**Authorization:** Admin (level >= 100)

**Request Body:**

```json
{
    "me_name": "My Store",
    "me_business_type": "fnb",
    "me_pos_mode": "centralized",
    "me_is_active": true,
    "me_midtrans_server_key": "optional",
    "me_midtrans_client_key": "optional",
    "me_midtrans_is_production": false
}
```

#### PUT /api/v1/merchants/{id}

Update existing merchant.

**Authorization:** Admin (level >= 100)

#### DELETE /api/v1/merchants/{id}

Delete merchant.

**Authorization:** Admin (level >= 100)

---

### Products

**Base Path:** `/api/v1/products`

#### GET /api/v1/products

List all products for the authenticated merchant.

**Authorization:** Staff (level >= 10)

**Query Parameters:**

-   `search`: Filter by name or description (optional)
-   `category_id`: Filter by category (optional)
-   `skip`: Offset pagination (default: 0)
-   `limit`: Records per page (1-1000, default: 100)

#### POST /api/v1/products

Create new product.

**Authorization:** Admin (level >= 100)

**Request Body:**

```json
{
    "pr_name": "Product Name",
    "pr_description": "Product description",
    "pr_price": 50000,
    "pr_stock": 100,
    "pc_id": 1,
    "pr_is_available": true
}
```

---

### Product Categories

**Base Path:** `/api/v1/product-categories`

#### GET /api/v1/product-categories

List all product categories.

**Authorization:** Staff (level >= 10)

#### POST /api/v1/product-categories

Create new category.

**Authorization:** Admin (level >= 100)

---

### Product Attachments

**Base Path:** `/api/v1/product-attachments`

#### POST /api/v1/product-attachments

Upload product image to Cloudinary.

**Authorization:** Admin (level >= 100)

**Request:** Multipart form data with image file

---

### Promotions

**Base Path:** `/api/v1/promotions`

#### GET /api/v1/promotions

List all promotions.

**Authorization:** Staff (level >= 10)

#### POST /api/v1/promotions

Create new promotion with items.

**Authorization:** Admin (level >= 100)

**Request Body:**

```json
{
    "pm_name": "Weekend Special",
    "pm_description": "50% off selected items",
    "pm_start_date": "2025-01-01T00:00:00Z",
    "pm_end_date": "2025-01-31T23:59:59Z",
    "pm_is_active": true,
    "items": [
        {
            "pr_id": 1,
            "pmi_discount_amount": 25000
        }
    ]
}
```

---

### Table Locations

**Base Path:** `/api/v1/table-locations`

#### GET /api/v1/table-locations

List all table locations for restaurant/cafe.

**Authorization:** Staff (level >= 10)

#### POST /api/v1/table-locations

Create new table location.

**Authorization:** Admin (level >= 100)

---

### Customers

**Base Path:** `/api/v1/customers`

#### GET /api/v1/customers

List all customers for the merchant.

**Authorization:** Staff (level >= 10)

#### POST /api/v1/customers

Create new customer.

**Authorization:** Staff (level >= 10)

---

### Orders

**Base Path:** `/api/v1/orders`

#### GET /api/v1/orders

List all orders for the merchant.

**Authorization:** Staff (level >= 10)

**Query Parameters:**

-   `skip`: Offset pagination (default: 0)
-   `limit`: Records per page (1-1000, default: 100)

#### GET /api/v1/orders/my-orders

Get order history for authenticated customer.

**Authorization:** Customer JWT

**Query Parameters:**

-   `skip`: Offset pagination (default: 0)
-   `limit`: Records per page (1-1000, default: 100)
-   `status`: Filter by payment status (optional)

#### GET /api/v1/orders/{oh_id}

Get single order by ID with all items.

**Authorization:** Staff (level >= 10) or Customer (own order only)

#### POST /api/v1/orders

Create new order with items.

**Authorization:** Staff (level >= 10) or Customer JWT

**For Customers:**

```json
{
    "oh_order_type": "dine_in",
    "tl_id": 1,
    "oh_notes": "Optional notes",
    "items": [
        {
            "pr_id": 1,
            "oi_qty": 2,
            "oi_notes": "Extra spicy"
        }
    ]
}
```

**For Staff (can specify customer):**

```json
{
    "oh_order_type": "dine_in",
    "cu_email": "customer@example.com",
    "cu_name": "John Doe",
    "items": [...]
}
```

#### POST /api/v1/orders/{oh_id}/create-payment

Generate Midtrans Snap token for payment.

**Authorization:** Staff (level >= 10) or Customer (own order only)

Returns `token` and `redirect_url` for payment processing.

#### POST /api/v1/orders/{oh_id}/check-status

Check payment status from Midtrans.

**Authorization:** Staff (level >= 10) or Customer (own order only)

Returns current payment status and Midtrans transaction details.

## Architecture

### Database Schema

**Schema:** `atapos`

**Tables:**

1. **merchant** - Merchant/tenant configuration

    - `me_id` (PK): Merchant ID
    - `me_name`: Business name
    - `me_business_type`: fnb, retail, service, other
    - `me_pos_mode`: centralized, distributed, hybrid
    - `me_midtrans_server_key`: Midtrans credentials
    - **Multi-tenancy root**: All other tables reference this

2. **product_category** - Product categories

    - `pc_id` (PK): Category ID
    - `me_id` (FK): Merchant reference
    - `pc_name`: Category name

3. **product** - Products/menu items

    - `pr_id` (PK): Product ID
    - `me_id` (FK): Merchant reference
    - `pc_id` (FK): Category reference
    - `pr_name`, `pr_price`, `pr_stock`: Product details

4. **product_attachment** - Product images (Cloudinary URLs)

    - `pa_id` (PK): Attachment ID
    - `pr_id` (FK): Product reference
    - `pa_url`: Cloudinary image URL

5. **promotion** - Promotional campaigns

    - `pm_id` (PK): Promotion ID
    - `me_id` (FK): Merchant reference
    - `pm_start_date`, `pm_end_date`: Validity period

6. **promotion_item** - Products in promotions

    - `pmi_id` (PK): Promotion item ID
    - `pm_id` (FK): Promotion reference
    - `pr_id` (FK): Product reference
    - `pmi_discount_amount`: Discount value

7. **table_location** - Physical tables/locations

    - `tl_id` (PK): Table ID
    - `me_id` (FK): Merchant reference
    - `tl_name`: Table identifier

8. **customer** - Customer registry

    - `cu_id` (PK): Customer ID
    - `me_id` (FK): Merchant reference
    - `cu_email`, `cu_name`, `cu_phone`: Contact info

9. **order_header** - Order master records

    - `oh_id` (PK): Order ID
    - `me_id` (FK): Merchant reference
    - `tl_id` (FK): Table reference
    - `cu_id` (FK): Customer reference
    - `oh_status`: pending, confirmed, completed, cancelled
    - `oh_total_amount`: Order total
    - `oh_payment_status`: pending, paid, failed

10. **order_item** - Order line items

    - `oi_id` (PK): Order item ID
    - `oh_id` (FK): Order header reference
    - `pr_id` (FK): Product reference
    - `oi_quantity`, `oi_price`: Item details

11. **payment_log** - Payment transaction logs
    - `pl_id` (PK): Payment log ID
    - `oh_id` (FK): Order reference
    - `pl_midtrans_order_id`: Midtrans transaction ID
    - `pl_status`: pending, success, failed
    - `pl_response_json`: Full Midtrans response

### Layered Architecture

```
API Layer (endpoints/)       → Business Logic (services/)       → Data Access (repositories/)       → Database
     ↓                                  ↓                                  ↓
  FastAPI                          Validation                         SQLAlchemy
  Authorization                    Business Rules                     ORM Queries
  Response Format                  Orchestration                      Transactions
```

### Data Flow

```
Request → Middleware → Endpoint → Service → Repository → Database
                           ↓
                    Atlas SSO (staff auth)
                    JWT (customer auth)
                    Midtrans (payments)
                    Cloudinary (images)
                    SMTP (emails)
```

## Business Logic

### Multi-Tenancy

All data is isolated per merchant (`me_id`). Staff users authenticated via Atlas SSO have their `me_id` extracted from the token and used to filter all queries automatically.

### Order Workflow

1. Customer places order (pending status)
2. Staff confirms order (confirmed status)
3. Payment processed via Midtrans
4. On successful payment, order marked as paid
5. Order completed when fulfilled

### Promotion Application

Promotions are time-bound and product-specific. Discounts are applied at order creation time by checking active promotions for the selected products.

### Customer Authentication

1. Customer requests login with email
2. System sends magic link OR OTP via email
3. Customer clicks link or enters OTP
4. System issues JWT token with 7-day expiry
5. Token used for customer-facing endpoints

## Security

### Authentication & Authorization

**Atlas SSO (ATAMS):**

-   Staff/admin authentication via Atlas microservices
-   Token validation with AES encryption
-   User information includes `user_id`, `role_level`, `me_id`

**JWT (Customer):**

-   Customer authentication via magic link or OTP
-   JWT tokens issued with HS256 algorithm
-   7-day token expiry (configurable)

**Authorization Levels:**

-   **Level 10** (>= 10): Officer/Staff - daily operations access
-   **Level 100** (>= 100): Admin/Owner - full merchant management

**Usage in Endpoints:**

```python
from app.api.deps import require_auth, require_min_role_level, require_customer_auth

# Staff auth (any level >= 1)
@router.get("/endpoint", dependencies=[Depends(require_auth)])

# Admin-only auth
@router.get("/admin", dependencies=[Depends(require_min_role_level(100))])

# Customer auth
@router.get("/customer-endpoint", dependencies=[Depends(require_customer_auth)])
```

### Response Encryption

Optional AES encryption for GET endpoints configured via `ENCRYPTION_ENABLED` environment variable.

### Environment Variables

**Critical secrets that must not be committed:**

-   `DATABASE_URL`: Database connection string
-   `ATLAS_ENCRYPTION_KEY`, `ATLAS_ENCRYPTION_IV`: Atlas SSO keys
-   `JWT_SECRET_KEY`: JWT signing key
-   `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`: Cloudinary credentials
-   `MAIL_PASSWORD`: SMTP password
-   Midtrans keys stored in database per merchant

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_orders.py

# Run specific test
pytest tests/test_orders.py::test_create_order
```

### Test Structure

```
tests/
├── conftest.py           # Test fixtures
├── test_endpoints/       # API endpoint tests
├── test_services/        # Service layer tests
└── test_repositories/    # Repository layer tests
```

## Deployment

### Environment-Specific Configuration

**Development:**

-   `DEBUG=true`
-   Detailed logging
-   Local SMTP testing

**Production:**

-   `DEBUG=false`
-   Error logging only
-   Secure SMTP with SSL/TLS
-   Connection pooling optimized for cloud database limits
-   CORS restricted to production domains

### Docker Deployment

See [docker-compose.yml](docker-compose.yml) for complete configuration.

```bash
docker-compose up -d
```

### Database Connection Pooling

**IMPORTANT:** Tune `DB_POOL_SIZE` and `DB_MAX_OVERFLOW` based on your database connection limit:

-   **Aiven Free Tier** (20 connections): `DB_POOL_SIZE=3`, `DB_MAX_OVERFLOW=5` (max 8 per instance)
-   **Production** (100+ connections): Scale accordingly
-   **Formula**: Total Connections = (DB_POOL_SIZE + DB_MAX_OVERFLOW) × Number of App Instances

## Project Structure

```
atapos/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration and settings
│   │   └── security.py        # Security utilities
│   ├── db/
│   │   └── session.py         # Database session management
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── merchant.py
│   │   ├── product.py
│   │   ├── product_category.py
│   │   ├── product_attachment.py
│   │   ├── promotion.py
│   │   ├── promotion_item.py
│   │   ├── table_location.py
│   │   ├── customer.py
│   │   ├── order_header.py
│   │   ├── order_item.py
│   │   └── payment_log.py
│   ├── schemas/               # Pydantic schemas
│   │   ├── common.py          # Shared response schemas
│   │   ├── merchant.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── ...
│   ├── repositories/          # Data access layer
│   │   ├── merchant_repository.py
│   │   ├── product_repository.py
│   │   ├── order_repository.py
│   │   └── ...
│   ├── services/              # Business logic layer
│   │   ├── merchant_service.py
│   │   ├── product_service.py
│   │   ├── order_service.py
│   │   ├── payment_service.py
│   │   └── ...
│   ├── api/
│   │   ├── deps.py            # Dependencies (auth, db)
│   │   └── v1/
│   │       ├── api.py         # Router aggregation
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── merchants.py
│   │           ├── products.py
│   │           ├── product_categories.py
│   │           ├── product_attachments.py
│   │           ├── promotions.py
│   │           ├── table_locations.py
│   │           ├── customers.py
│   │           └── orders.py
│   ├── utils/                 # Utility functions
│   └── main.py                # FastAPI application entry point
├── tests/                     # Test files
│   ├── conftest.py
│   └── test_*/
├── .env.example               # Environment variables template
├── .gitignore
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose configuration
├── WARP.md                    # Development guide for Warp
└── README.md                  # This file
```

## Code Generation (ATAMS)

Using ATAMS toolkit for rapid development:

```bash
# Generate complete CRUD resource
atams generate [resource_name]
```

This creates:

-   Model in `app/models/`
-   Schema in `app/schemas/`
-   Repository in `app/repositories/`
-   Service in `app/services/`
-   Router in `app/api/v1/endpoints/`
