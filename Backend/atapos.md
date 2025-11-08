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

-   **Multi-Tenant Architecture**: Complete merchant isolation with per-tenant configuration and Midtrans credentials
-   **Dual Authentication System**: Passwordless customer auth (Magic Link/OTP) + Atlas SSO for staff with role-based access control
-   **Product Management**: Categories, pricing, tax/service charge configuration, and image uploads via Cloudinary (thumbnail + detail images)
-   **Order Management**: Complete order lifecycle with automatic customer creation, product snapshots, and tax/service charge calculation
-   **Payment Integration**:
    -   Midtrans Snap (QRIS, credit card, e-wallet, bank transfer)
    -   Cash payment processing with automatic change calculation
    -   Rounded amounts for easier cash handling
    -   Transaction management (cancel, expire, refund)
-   **Promotions**: Flexible promotion system with 3 discount types (percent, nominal, override price)
-   **Email Notifications**: Magic links, OTP codes, and payment receipts with HTML templates
-   **Table/Location Management**: Multi-location support for restaurant, barbershop, car wash, etc.
-   **Role-Based Access Control**: Admin (level 10) and Officer (level 100) with granular permissions

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

Request magic link for customer login via email. Link expires in 15 minutes.

**Request Body:**

```json
{
    "email": "customer@example.com"
}
```

**Response:** Always returns success (prevents email enumeration)

#### POST /api/v1/auth/customer/verify-magic-link

Verify magic link token and receive JWT access token.

**Request Body:**

```json
{
    "token": "uuid-token-from-email"
}
```

**Response:**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "customer": {
        "cu_id": 1,
        "cu_email": "customer@example.com",
        "cu_name": "John Doe"
    }
}
```

#### POST /api/v1/auth/customer/request-otp

Request 6-digit OTP code via email. OTP expires in 5 minutes.

**Request Body:**

```json
{
    "email": "customer@example.com"
}
```

**Response:** Always returns success (prevents email enumeration)

#### POST /api/v1/auth/customer/verify-otp

Verify OTP and get JWT token (valid for 7 days).

**Request Body:**

```json
{
    "email": "customer@example.com",
    "otp": "123456"
}
```

**Response:**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "customer": {
        "cu_id": 1,
        "cu_email": "customer@example.com",
        "cu_name": "John Doe"
    }
}
```

#### GET /api/v1/auth/customer/me

Get current customer information from JWT token.

**Authorization:** Required (Customer JWT token)

**Response:**

```json
{
    "cu_id": 1,
    "me_id": 1,
    "cu_email": "customer@example.com",
    "cu_name": "John Doe",
    "cu_phone": "081234567890",
    "created_at": "2025-01-01T00:00:00Z"
}
```

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

List all products for the authenticated merchant (public endpoint).

**Authorization:** None required

**Query Parameters:**

-   `search`: Filter by name or description (optional)
-   `pc_id`: Filter by category ID (optional)
-   `skip`: Offset pagination (default: 0)
-   `limit`: Records per page (1-1000, default: 100)

**Response:**

```json
[
    {
        "pr_id": 1,
        "pr_name": "Nasi Goreng",
        "pr_desc": "Delicious fried rice",
        "pr_type": "goods",
        "pr_base_price": 25000.0,
        "pr_tax_percent": 10.0,
        "pr_service_charge_percent": 5.0,
        "pr_is_available": true,
        "pr_is_active": true,
        "pc_id": 1,
        "pr_image_path": "https://res.cloudinary.com/.../thumbnail.jpg",
        "thumbnail": {
            "pa_id": 1,
            "pa_cloudinary_url": "https://res.cloudinary.com/.../thumbnail.jpg"
        },
        "detail_images": [
            {
                "pa_id": 2,
                "pa_cloudinary_url": "https://res.cloudinary.com/.../detail1.jpg",
                "pa_sort_order": 0
            }
        ]
    }
]
```

#### GET /api/v1/products/{pr_id}

Get single product details with images.

**Authorization:** None required

#### POST /api/v1/products

Create new product with optional image uploads.

**Authorization:** Admin (level >= 10)

**Request:** Multipart form-data

**Form Fields:**

-   `data` (JSON string): Product data
-   `thumbnail` (file, optional): Thumbnail image (JPG/JPEG/PNG, max 5MB)
-   `detail_images` (files, optional): Up to 3 detail images (JPG/JPEG/PNG, max 10MB each)

**Example `data` field:**

```json
{
    "pr_name": "Nasi Goreng",
    "pr_desc": "Delicious fried rice",
    "pr_type": "goods",
    "pr_base_price": 25000.0,
    "pr_tax_percent": 10.0,
    "pr_service_charge_percent": 5.0,
    "pr_is_available": true,
    "pr_is_active": true,
    "pc_id": 1
}
```

**Features:**

-   Automatic Cloudinary upload
-   Transaction rollback on upload failure
-   Sort order assigned automatically (0, 1, 2)

#### PUT /api/v1/products/{pr_id}

Update existing product.

**Authorization:** Admin (level >= 10)

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

**Base Path:** `/api/v1/products/{pr_id}`

#### POST /api/v1/products/{pr_id}/thumbnail

Upload or replace product thumbnail image.

**Authorization:** Admin (level >= 10)

**Request:** Multipart form-data with `file` field

**File Requirements:**

-   Format: JPG, JPEG, PNG
-   Max size: 5MB

**Response:**

```json
{
    "pa_id": 1,
    "pr_id": 1,
    "pa_type": "thumbnail",
    "pa_cloudinary_public_id": "atapos/products/1/thumbnail",
    "pa_cloudinary_url": "https://res.cloudinary.com/.../thumbnail.jpg"
}
```

#### DELETE /api/v1/products/{pr_id}/thumbnail

Delete product thumbnail image.

**Authorization:** Admin (level >= 10)

#### POST /api/v1/products/{pr_id}/detail-images

Upload product detail images (bulk upload, max 3).

**Authorization:** Admin (level >= 10)

**Request:** Multipart form-data with multiple `files` fields

**File Requirements:**

-   Format: JPG, JPEG, PNG
-   Max size per file: 10MB
-   Max files: 3 total (including existing)

**Response:**

```json
[
    {
        "pa_id": 2,
        "pa_type": "detail",
        "pa_cloudinary_url": "https://res.cloudinary.com/.../detail1.jpg",
        "pa_sort_order": 0
    },
    {
        "pa_id": 3,
        "pa_type": "detail",
        "pa_cloudinary_url": "https://res.cloudinary.com/.../detail2.jpg",
        "pa_sort_order": 1
    }
]
```

#### DELETE /api/v1/products/{pr_id}/detail-images

Delete product detail images (bulk delete).

**Authorization:** Admin (level >= 10)

**Request Body:**

```json
{
    "pa_ids": [2, 3]
}
```

---

### Promotions

**Base Path:** `/api/v1/promotions`

#### GET /api/v1/promotions

List all active promotions (public endpoint).

**Authorization:** None required

**Response:**

```json
[
    {
        "pm_id": 1,
        "pm_name": "Weekend 20% Off",
        "pm_discount_type": "percent",
        "pm_discount_value": 20.0,
        "pm_start_at": "2025-10-27T00:00:00Z",
        "pm_end_at": "2025-10-29T23:59:59Z",
        "pm_is_active": true,
        "products": [
            {
                "pr_id": 1,
                "pr_name": "Nasi Goreng",
                "pr_base_price": 25000.0
            }
        ]
    }
]
```

#### GET /api/v1/promotions/{pm_id}

Get single promotion details with products.

**Authorization:** None required

#### POST /api/v1/promotions

Create new promotion with product assignments.

**Authorization:** Admin (level >= 10)

**Request Body:**

```json
{
    "pm_name": "Weekend 20% Off",
    "pm_discount_type": "percent",
    "pm_discount_value": 20.0,
    "pm_start_at": "2025-10-27T00:00:00Z",
    "pm_end_at": "2025-10-29T23:59:59Z",
    "pm_is_active": true,
    "product_ids": [1, 2, 3]
}
```

**Promotion Types:**

-   `percent`: Percentage discount (e.g., 20% off)
-   `nominal`: Fixed amount discount (e.g., Rp 10,000 off)
-   `override_price`: Set new fixed price (e.g., Rp 50,000)

#### PUT /api/v1/promotions/{pm_id}

Update existing promotion.

**Authorization:** Admin (level >= 10)

---

### Table Locations

**Base Path:** `/api/v1/table-locations`

#### GET /api/v1/table-locations

List all table locations (public endpoint). Used for restaurant tables, service stations, zones, etc.

**Authorization:** None required

**Response:**

```json
[
    {
        "tl_id": 1,
        "tl_number": "A1",
        "tl_name": "Table A1 - Window",
        "tl_capacity": 4,
        "tl_zone": "Indoor",
        "tl_is_active": true
    }
]
```

#### GET /api/v1/table-locations/{tl_id}

Get single table location details.

**Authorization:** None required

#### POST /api/v1/table-locations

Create new table location.

**Authorization:** Admin (level >= 10)

**Request Body:**

```json
{
    "tl_number": "A1",
    "tl_name": "Table A1 - Window",
    "tl_capacity": 4,
    "tl_zone": "Indoor",
    "tl_is_active": true
}
```

**Use Cases:**

-   Restaurant tables (dine-in)
-   Barbershop chairs
-   Car wash bays
-   Spa treatment rooms
-   Store zones/sections

#### PUT /api/v1/table-locations/{tl_id}

Update existing table location.

**Authorization:** Admin (level >= 10)

---

### Customers

**Base Path:** `/api/v1/customers`

#### GET /api/v1/customers

List all customers for the merchant.

**Authorization:** Officer + Admin (level >= 100)

**Query Parameters:**

-   `search`: Filter by name, email, or phone (optional)
-   `skip`: Offset pagination (default: 0)
-   `limit`: Records per page (1-1000, default: 100)

#### GET /api/v1/customers/{cu_id}

Get single customer details.

**Authorization:** Officer + Admin (level >= 100)

#### POST /api/v1/customers

Create new customer (public registration).

**Authorization:** None required

**Request Body:**

```json
{
    "cu_email": "customer@example.com",
    "cu_name": "John Doe",
    "cu_phone": "081234567890"
}
```

#### PUT /api/v1/customers/me

Update own customer profile.

**Authorization:** Customer JWT token

**Request Body:**

```json
{
    "cu_name": "John Doe",
    "cu_phone": "081234567890"
}
```

---

### Orders

**Base Path:** `/api/v1/orders`

#### GET /api/v1/orders

List all orders for the merchant (sorted by most recent first).

**Authorization:** Officer + Admin (level >= 100)

**Query Parameters:**

-   `skip`: Offset pagination (default: 0)
-   `limit`: Records per page (1-1000, default: 100)

**Response:**

```json
[
    {
        "oh_id": 123,
        "oh_order_number": "INV-20251108-0001",
        "oh_order_type": "dine_in",
        "oh_guest_count": 2,
        "oh_subtotal_amount": 50000.0,
        "oh_discount_amount": 5000.0,
        "oh_tax_amount": 4500.0,
        "oh_service_charge_amount": 2250.0,
        "oh_total_amount": 51750.0,
        "oh_rounded_amount": 51800.0,
        "oh_payment_status": "settlement",
        "oh_payment_type": "cash",
        "oh_paid_at": "2025-11-08T10:30:00Z",
        "customer": {
            "cu_id": 1,
            "cu_name": "John Doe"
        },
        "table_location": {
            "tl_id": 1,
            "tl_name": "Table A1"
        },
        "created_at": "2025-11-08T10:25:00Z"
    }
]
```

#### GET /api/v1/orders/my-orders

Get order history for authenticated customer.

**Authorization:** Customer JWT

**Query Parameters:**

-   `skip`: Offset pagination (default: 0)
-   `limit`: Records per page (1-1000, default: 100)
-   `oh_payment_status`: Filter by payment status (optional: pending, settlement, cancel, etc.)

#### GET /api/v1/orders/{oh_id}

Get single order by ID with all items and details.

**Authorization:** Officer + Admin (level >= 100) or Customer (own order only)

**Response:**

```json
{
    "oh_id": 123,
    "oh_order_number": "INV-20251108-0001",
    "oh_order_type": "dine_in",
    "oh_guest_count": 2,
    "oh_subtotal_amount": 50000.0,
    "oh_discount_amount": 5000.0,
    "oh_tax_amount": 4500.0,
    "oh_service_charge_amount": 2250.0,
    "oh_total_amount": 51750.0,
    "oh_rounded_amount": 51800.0,
    "oh_payment_status": "settlement",
    "oh_payment_type": "qris",
    "oh_midtrans_order_id": "INV-20251108-0001",
    "oh_midtrans_transaction_id": "abc123-def456",
    "oh_qris_string": "00020101021126...",
    "oh_qris_acquirer": "gopay",
    "oh_paid_at": "2025-11-08T10:30:00Z",
    "oh_notes": "Window seat please",
    "customer": {
        "cu_id": 1,
        "cu_email": "customer@example.com",
        "cu_name": "John Doe",
        "cu_phone": "081234567890"
    },
    "table_location": {
        "tl_id": 1,
        "tl_number": "A1",
        "tl_name": "Table A1 - Window"
    },
    "items": [
        {
            "oi_id": 1,
            "pr_id": 1,
            "oi_product_name_snapshot": "Nasi Goreng",
            "oi_product_type": "goods",
            "oi_qty": 2,
            "oi_base_price": 25000.0,
            "oi_final_price": 22500.0,
            "oi_line_subtotal": 45000.0,
            "oi_notes": "Extra spicy"
        }
    ],
    "created_at": "2025-11-08T10:25:00Z"
}
```

#### POST /api/v1/orders

Create new order with items. Supports both customer self-ordering and staff-assisted ordering.

**Authorization:** Officer + Admin (level >= 100) or Customer JWT

**For Customer Self-Ordering:**

```json
{
    "oh_order_type": "dine_in",
    "tl_id": 1,
    "oh_guest_count": 2,
    "oh_notes": "Window seat please",
    "items": [
        {
            "pr_id": 1,
            "oi_qty": 2,
            "oi_notes": "Extra spicy"
        }
    ]
}
```

**For Staff (can specify customer via email or ID):**

```json
{
    "cu_email": "customer@example.com",
    "cu_name": "John Doe",
    "cu_phone": "081234567890",
    "oh_order_type": "dine_in",
    "tl_id": 1,
    "oh_guest_count": 2,
    "items": [
        {
            "pr_id": 1,
            "oi_qty": 2,
            "oi_notes": "Extra spicy"
        }
    ]
}
```

**Order Types:**

-   `dine_in`: Restaurant/cafe table service
-   `takeaway`: Order for pickup
-   `delivery`: Order for delivery
-   `service_job`: Service-based businesses (barbershop, car wash, etc.)
-   `walk_in`: Quick retail purchase

**Features:**

-   Auto-creates customer if email provided
-   Applies active promotions automatically
-   Calculates tax and service charge per item
-   Stores product snapshots for historical pricing
-   Generates unique order number: `INV-YYYYMMDD-XXXX`
-   **NEW:** Calculates rounded amount for easier cash handling

#### POST /api/v1/orders/{oh_id}/create-payment

Generate Midtrans Snap payment token and redirect URL.

**Authorization:** Officer + Admin (level >= 100) or Customer (own order only)

**Response:**

```json
{
    "token": "66e4fa55-fdac-4ef9-91b5-733b97d1b862",
    "redirect_url": "https://app.sandbox.midtrans.com/snap/v2/vtweb/66e4fa55-fdac-4ef9-91b5-733b97d1b862"
}
```

**Payment Methods Available:**

-   QRIS (GoPay, OVO, DANA, ShopeePay, LinkAja)
-   Credit/Debit Card
-   Bank Transfer (BCA, Mandiri, BNI, BRI, Permata)
-   E-wallet direct (GoPay, ShopeePay)
-   Alfamart/Indomaret
-   Kredivo, Akulaku

#### POST /api/v1/orders/{oh_id}/pay-cash

Process cash payment (staff-only). **NEW FEATURE**

**Authorization:** Officer + Admin (level >= 100)

**Request Body:**

```json
{
    "amount_paid": 60000.0
}
```

**Response:**

```json
{
    "oh_id": 123,
    "oh_order_number": "INV-20251108-0001",
    "oh_total_amount": 51750.0,
    "oh_rounded_amount": 51800.0,
    "amount_paid": 60000.0,
    "change_amount": 8200.0,
    "oh_payment_status": "settlement",
    "oh_paid_at": "2025-11-08T10:30:00Z"
}
```

**Features:**

-   Uses rounded amount (nearest Rp 100) for easier cash handling
-   Automatic change calculation
-   Validates sufficient payment
-   Updates order status to settlement
-   Creates payment log with audit trail

#### POST /api/v1/orders/{oh_id}/check-status

Check current payment status from Midtrans.

**Authorization:** Officer + Admin (level >= 100) or Customer (own order only)

**Response:**

```json
{
    "oh_payment_status": "settlement",
    "oh_midtrans_transaction_id": "abc123-def456",
    "oh_payment_type": "qris",
    "oh_paid_at": "2025-11-08T10:30:00Z",
    "midtrans_response": {
        "status_code": "200",
        "transaction_status": "settlement",
        "fraud_status": "accept"
    }
}
```

#### POST /api/v1/orders/{oh_id}/cancel

Cancel pending payment (before payment is made).

**Authorization:** Officer + Admin (level >= 100) or Customer (own order only)

**Requirements:**

-   Order payment status must be `pending`
-   Cannot cancel already paid orders

#### POST /api/v1/orders/{oh_id}/expire

Manually expire pending payment (staff-only).

**Authorization:** Officer + Admin (level >= 100)

**Requirements:**

-   Order payment status must be `pending`

#### POST /api/v1/orders/{oh_id}/refund

Refund settled payment (admin-only).

**Authorization:** Admin (level >= 10)

**Request Body:**

```json
{
    "amount": 51750.0,
    "reason": "Customer request"
}
```

**Refund Types:**

-   Full refund: Omit `amount` or use full order total
-   Partial refund: Specify `amount`

#### POST /api/v1/orders/webhooks/midtrans

Midtrans payment webhook notification (public endpoint for Midtrans servers).

**Authorization:** None (verified via SHA512 signature)

**Features:**

-   Verifies Midtrans signature
-   Updates order payment status
-   Sends receipt email on successful payment
-   Logs all notifications for audit trail
-   Handles all payment methods (QRIS, card, bank transfer, etc.)

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
    - `me_id` (FK): Merchant reference
    - `pa_type`: thumbnail, detail
    - `pa_cloudinary_public_id`: Cloudinary public ID for deletion
    - `pa_cloudinary_url`: Full Cloudinary image URL
    - `pa_sort_order`: 0, 1, 2 (for detail images)

5. **promotion** - Promotional campaigns

    - `pm_id` (PK): Promotion ID
    - `me_id` (FK): Merchant reference
    - `pm_name`: Promotion name
    - `pm_discount_type`: percent, nominal, override_price
    - `pm_discount_value`: Discount value
    - `pm_start_at`, `pm_end_at`: Validity period
    - `pm_is_active`: Active flag

6. **promotion_item** - Products in promotions

    - `pi_id` (PK): Promotion item ID
    - `pm_id` (FK): Promotion reference
    - `pr_id` (FK): Product reference

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
    - `u_id`: Staff user ID (nullable)
    - `cu_id` (FK): Customer reference (nullable)
    - `tl_id` (FK): Table reference (nullable)
    - `oh_order_number`: Unique order number (INV-YYYYMMDD-XXXX)
    - `oh_order_type`: dine_in, takeaway, delivery, service_job, walk_in
    - `oh_guest_count`: Number of guests
    - `oh_subtotal_amount`: Subtotal before discounts/taxes
    - `oh_discount_amount`: Total discounts applied
    - `oh_tax_amount`: Total tax
    - `oh_service_charge_amount`: Total service charge
    - `oh_total_amount`: Final total amount
    - **`oh_rounded_amount`**: Rounded total (nearest Rp 100) **NEW**
    - `oh_payment_status`: pending, settlement, cancel, deny, expire, failure, refund
    - `oh_fraud_status`: Midtrans fraud status
    - `oh_payment_type`: Payment method (qris, gopay, credit_card, cash, etc.)
    - `oh_midtrans_order_id`: Midtrans order ID
    - `oh_midtrans_transaction_id`: Midtrans transaction ID
    - `oh_midtrans_transaction_time`: Midtrans transaction time
    - `oh_midtrans_transaction_status`: Midtrans status
    - `oh_qris_string`: QRIS string (if QRIS payment)
    - `oh_qris_acquirer`: QRIS acquirer (gopay, linkaja, etc.)
    - `oh_qris_actions`: JSONB with QRIS actions
    - `oh_expired_at`: Payment expiration time
    - `oh_paid_at`: Payment completion time
    - `oh_notes`: Order notes

10. **order_item** - Order line items

    - `oi_id` (PK): Order item ID
    - `oh_id` (FK): Order header reference
    - `pr_id` (FK): Product reference
    - `oi_product_name_snapshot`: Product name at time of order
    - `oi_product_type`: goods, service
    - `oi_qty`: Quantity
    - `oi_base_price`: Original product price
    - `oi_final_price`: Price after promotions
    - `oi_line_subtotal`: Final price × quantity
    - `oi_notes`: Item notes

11. **payment_log** - Payment transaction audit logs
    - `py_id` (PK): Payment log ID
    - `oh_id` (FK): Order reference
    - `me_id` (FK): Merchant reference
    - `py_event_type`: charge, notification, status_check, refund, cancel, expire, **cash** **NEW**
    - `py_order_id`: Midtrans order ID
    - `py_transaction_id`: Midtrans transaction ID
    - `py_transaction_status`: Transaction status
    - `py_fraud_status`: Fraud detection status
    - `py_payment_type`: Payment method
    - `py_gross_amount`: Payment amount
    - `py_signature_key`: Midtrans signature (for verification)
    - `py_raw_payload`: JSONB with full Midtrans response

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

**Digital Payment Flow (Midtrans Snap):**

1. Customer/staff creates order → Status: `pending`
2. Generate Snap payment token via `/create-payment`
3. Customer pays via Snap (QRIS, card, e-wallet, bank transfer, etc.)
4. Midtrans sends webhook notification
5. System updates status → `settlement`
6. Receipt email sent automatically

**Cash Payment Flow (NEW):**

1. Customer/staff creates order → Status: `pending`
2. Staff processes cash payment via `/pay-cash`
3. System validates amount ≥ rounded amount
4. System calculates change
5. System updates status → `settlement`
6. Receipt displayed (change amount shown)

**Payment Status States:**

-   `pending`: Awaiting payment
-   `settlement`: Paid successfully
-   `cancel`: Cancelled by user
-   `deny`: Denied by fraud detection
-   `expire`: Payment timeout
-   `failure`: Payment failed
-   `refund`: Refunded

### Order Calculation Logic

**Price Calculation (per item):**

1. Base price from product
2. Apply promotion (if active):
    - `percent`: `base_price × (1 - discount_value / 100)`
    - `nominal`: `base_price - discount_value`
    - `override_price`: `discount_value`
3. Final price = promotional price or base price
4. Line subtotal = `final_price × quantity`

**Order Total Calculation:**

1. Subtotal = sum of all line subtotals
2. Tax = sum of `(line_subtotal × tax_percent / 100)` per item
3. Service charge = sum of `(line_subtotal × service_charge_percent / 100)` per item
4. Discount = subtotal - sum of line subtotals with promotions
5. Total amount = `subtotal - discount + tax + service_charge`
6. **Rounded amount (NEW)** = Total rounded to nearest Rp 100

**Example:**

```
Item 1: Nasi Goreng × 2
  Base price: Rp 25,000
  Promotion: 10% off → Final price: Rp 22,500
  Line subtotal: Rp 45,000
  Tax (10%): Rp 4,500
  Service (5%): Rp 2,250

Order Summary:
  Subtotal: Rp 45,000
  Discount: Rp 5,000
  Tax: Rp 4,500
  Service: Rp 2,250
  Total: Rp 46,750
  Rounded: Rp 46,800 (for cash payment)
```

### Promotion Application

Promotions are automatically applied at order creation time:

-   Checks promotion validity (start/end dates)
-   Checks `pm_is_active` flag
-   Applies best available discount per product
-   Stores original and final prices for audit trail

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

-   **Level 10** (>= 10): Admin/Owner - full merchant management (create/update products, categories, promotions, tables, refunds)
-   **Level 100** (>= 100): Officer/Staff - daily operations access (view orders, process cash payments, cancel/expire payments)

**Usage in Endpoints:**

```python
from app.api.deps import get_auth_context, get_customer_auth_context

# Dual auth (accepts both customer JWT and staff SSO)
auth: AuthContext = Depends(get_auth_context())

# Customer-only auth
auth: AuthContext = Depends(get_customer_auth_context())

# In endpoint logic:
if auth.is_customer():
    # Customer-specific logic
    auth.require_ownership(order.cu_id)  # Validate ownership
elif auth.is_staff():
    # Staff-specific logic
    if auth.is_admin():  # Level >= 10
        # Admin operations
    elif auth.is_officer():  # Level >= 100
        # Officer operations
```

**AuthContext Methods:**

```python
auth.is_customer() -> bool  # True if authenticated via customer JWT
auth.is_staff() -> bool  # True if authenticated via Atlas SSO
auth.is_admin() -> bool  # True if role_level >= 10
auth.is_officer() -> bool  # True if role_level >= 100
auth.require_staff()  # Raises 403 if not staff
auth.require_customer()  # Raises 403 if not customer
auth.require_ownership(cu_id)  # Raises 403 if customer doesn't own resource
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
│   │           ├── customer_auth.py
│   │           ├── merchants.py
│   │           ├── customers.py
│   │           ├── products.py
│   │           ├── product_categories.py
│   │           ├── promotions.py
│   │           ├── table_locations.py
│   │           └── orders.py
│   ├── utils/                 # Utility functions
│   │   ├── cloudinary.py      # Cloudinary integration
│   │   └── email.py           # Email service
│   ├── templates/             # Email templates
│   │   └── email/
│   │       ├── magic_link.html
│   │       ├── otp.html
│   │       └── receipt.html
│   ├── demo/                  # Demo HTML pages
│   │   ├── customer_auth.py
│   │   ├── snap_embedded.py
│   │   └── order_history.py
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
