---
title: Aventory - Inventory Management System
description: A comprehensive inventory management system built with FastAPI that handles warehouse operations, stock tracking, purchase orders, and item requests with complete audit trails
order: 16
category: Backend Application
tags: [inventory, fastapi, postgresql, warehouse, procurement, atlas-sso]
---

# Aventory - Inventory Management System

Aventory is a comprehensive inventory management system built with FastAPI that handles warehouse operations, stock tracking, purchase orders, and item requests with complete audit trails.

## Overview

Aventory provides end-to-end inventory management capabilities including:

-   Multi-warehouse stock management
-   Purchase order processing from suppliers
-   Internal item request and distribution
-   Stock adjustments and transfers
-   Real-time stock tracking
-   Complete transaction history

---

## Key Features

### 📦 Master Data Management

-   **Items**: Manage products with SKU, categories, and units of measurement
-   **Warehouses**: Multiple warehouse support with location tracking
-   **Suppliers**: Supplier database for procurement
-   **Categories & UOMs**: Organized classification and measurement units

### 🏭 Procurement Management

-   Create purchase orders for suppliers
-   Approval workflow for purchase orders
-   Receive goods and automatically update stock
-   Track purchase order history and status

### 📤 Distribution Management

-   Department-based item requests
-   Multi-level approval workflow
-   Issue items and automatically reduce stock
-   Track request status and history

### 📊 Stock Management

-   Real-time stock levels across all warehouses
-   Stock adjustments (IN/OUT transactions)
-   Stock transfers between warehouses (MOVE transactions)
-   Low stock alerts
-   Complete stock movement history

### 🔐 Security & Audit

-   ATAMS SSO integration for authentication
-   Role-based access control
-   Complete audit trail for all transactions
-   User tracking for all operations

---

## Business Flows

### Flow 1: Stock IN from Supplier (Purchase Order)

This is the main flow for receiving goods from suppliers and increasing warehouse stock.

```
Step 1: Create Purchase Order (PO)
  └─> POST /api/v1/purchase-orders/
  └─> Status: posted
  └─> Contains: supplier_id, warehouse_id, items with quantities and prices

Step 2: Approve Purchase Order
  └─> PUT /api/v1/purchase-orders/{po_id}/status
  └─> Body: {"po_status": "approved"}
  └─> Status: posted → approved
  └─> Only approved POs can be received

Step 3: Receive Goods (THIS IS WHERE STOCK INCREASES!)
  └─> PUT /api/v1/purchase-orders/{po_id}/receive
  └─> Status: approved → received
  └─> System automatically:
      ├─> Creates Stock Transaction (type: IN)
      ├─> Adds stock to specified warehouse
      └─> Records complete audit trail

Result: Stock INCREASED in warehouse! ✓
```

**Example Scenario:**

1. Procurement creates PO-2025-0001 for 100 pcs Mouse from Supplier A to Jakarta Warehouse
2. Manager approves the PO
3. Warehouse receives the goods and confirms in system
4. System creates stock transaction TX-PO-PO-2025-0001
5. Stock of Mouse in Jakarta Warehouse increases by 100 pcs

**Important Notes:**

-   PO must be in "approved" status before receiving
-   Receiving automatically confirms the stock transaction
-   Cannot receive the same PO twice
-   All items in PO are received together (partial receive not supported)

---

### Flow 2: Stock OUT to Department (Item Request)

This is the flow for departments to request items from warehouse and reduce stock.

```
Step 1: Create Item Request
  └─> POST /api/v1/item-requests/
  └─> Status: posted
  └─> Contains: department, warehouse_id, items with requested quantities
  └─> Note: Only the creator can see their own requests initially

Step 2: Submit for Approval
  └─> PUT /api/v1/item-requests/{rq_id}/submit
  └─> Status: posted → waiting_approval
  └─> Validation: Only request owner can submit
  └─> Now visible to approvers

Step 3: Approve or Reject Request
  └─> PUT /api/v1/item-requests/{rq_id}/approval
  └─> Body: {"rq_status": "approved"} or {"rq_status": "rejected"}
  └─> Status: waiting_approval → approved/rejected
  └─> Only approvers (role level 10) can approve/reject

Step 4: Issue Items (THIS IS WHERE STOCK DECREASES!)
  └─> PUT /api/v1/item-requests/{rq_id}/issue
  └─> Body: {"details": [{"rd_id": 1, "rd_qty_issued": 10}]}
  └─> Status: approved → issued
  └─> System automatically:
      ├─> Validates stock availability (CRITICAL!)
      ├─> Creates Stock Transaction (type: OUT)
      ├─> Reduces stock from warehouse
      └─> Records complete audit trail

Result: Stock DECREASED from warehouse! ✓
```

**Example Scenario:**

1. IT Department creates RQ-2025-0001 for 5 pcs Mouse from Jakarta Warehouse
2. Requester submits the request for approval
3. Manager approves the request
4. Warehouse staff issues the items
5. System validates stock: Jakarta has 100 pcs Mouse available
6. System creates stock transaction TX-RQ-RQ-2025-0001
7. Stock of Mouse in Jakarta Warehouse decreases by 5 pcs (100 → 95)

**Important Notes:**

-   Stock availability is validated before issuing
-   If insufficient stock, issue will fail with clear error message
-   Partial issue is supported (can issue less than requested)
-   Approvers can reject requests with reason
-   Only approved requests can be issued

---

### Flow 3: Stock MOVE Between Warehouses

Transfer stock from one warehouse to another.

```
Step 1: Create Stock Transaction (type: MOVE)
  └─> POST /api/v1/stock-transactions/
  └─> Body: {
        "tx_type": "MOVE",
        "tx_from_wh_id": 1,  // Source warehouse
        "tx_to_wh_id": 2,    // Destination warehouse
        "details": [...]
      }
  └─> Status: posted (not yet affecting stock)

Step 2: Confirm Transfer
  └─> PUT /api/v1/stock-transactions/{tx_id}/confirm
  └─> System automatically:
      ├─> Validates stock at source warehouse
      ├─> Decreases stock from source warehouse
      ├─> Increases stock at destination warehouse
      └─> Both operations are ATOMIC (all or nothing)

Result: Stock moved from Warehouse A to Warehouse B! ✓
```

**Example Scenario:**

1. Create transaction to move 20 pcs Mouse from Jakarta to Surabaya
2. System validates: Jakarta has 95 pcs Mouse available
3. Confirm transaction
4. Jakarta stock decreases: 95 → 75 pcs
5. Surabaya stock increases: 50 → 70 pcs
6. Transaction recorded as confirmed

**Important Notes:**

-   Source and destination warehouses must be different
-   Stock validated at confirmation time
-   If insufficient stock, confirmation fails
-   Both decrease and increase happen atomically
-   Cannot confirm the same transaction twice

---

### Flow 4: Stock Adjustment (Manual IN/OUT)

Manual stock adjustments for corrections, damage, loss, etc.

```
Step 1: Create Stock Transaction (type: IN or OUT)

  For Stock IN (add stock):
  └─> POST /api/v1/stock-transactions/
  └─> Body: {
        "tx_type": "IN",
        "tx_to_wh_id": 1,       // Destination warehouse
        "tx_from_wh_id": null,  // Must be null for IN
        "tx_note": "Stock opname correction",
        "details": [...]
      }

  For Stock OUT (remove stock):
  └─> POST /api/v1/stock-transactions/
  └─> Body: {
        "tx_type": "OUT",
        "tx_from_wh_id": 1,     // Source warehouse
        "tx_to_wh_id": null,    // Must be null for OUT
        "tx_note": "Damaged items",
        "details": [...]
      }

Step 2: Confirm Adjustment
  └─> PUT /api/v1/stock-transactions/{tx_id}/confirm
  └─> For IN: Stock increases at destination warehouse
  └─> For OUT: Stock decreases from source warehouse

Result: Stock adjusted! ✓
```

**Use Cases:**

-   **Stock IN**: Initial stock, stock corrections (increase), found items
-   **Stock OUT**: Damage, loss, theft, samples, write-offs

**Important Notes:**

-   Requires proper notes/reason for audit purposes
-   OUT transactions validate stock availability
-   All adjustments are logged with user and timestamp
-   Cannot be reversed once confirmed

---

## Stock Transaction Types Summary

| Type     | From Warehouse | To Warehouse | Effect            | Use Case                         |
| -------- | -------------- | ------------ | ----------------- | -------------------------------- |
| **IN**   | NULL           | Required     | ➕ Increase stock | PO receive, adjustments (add)    |
| **OUT**  | Required       | NULL         | ➖ Decrease stock | Item issue, adjustments (remove) |
| **MOVE** | Required       | Required     | ➕➖ Transfer     | Warehouse transfers              |

---

## Status Transitions

### Purchase Order Status

```
posted → approved → received
posted → cancel
```

### Item Request Status

```
posted → waiting_approval → approved → issued
posted → waiting_approval → rejected
```

### Stock Transaction Status

```
posted → confirmed
```

**Note**: Stock transactions don't have a visible status field. They have `tx_confirmed_at` timestamp:

-   `tx_confirmed_at = NULL`: Posted (not yet affecting stock)
-   `tx_confirmed_at != NULL`: Confirmed (stock updated)

---

## API Endpoints Overview

### Master Data

-   `GET /api/v1/items/` - List all items
-   `GET /api/v1/items/{id}` - Get item details
-   `POST /api/v1/items/` - Create new item
-   `PUT /api/v1/items/{id}` - Update item
-   `DELETE /api/v1/items/{id}` - Delete item

Similar endpoints exist for:

-   `/api/v1/warehouses/`
-   `/api/v1/suppliers/`
-   `/api/v1/item-categories/`
-   `/api/v1/uoms/`

### Stock Management

-   `GET /api/v1/stocks/` - View stock levels (read-only)
    -   Filter by warehouse, item, low stock
-   `GET /api/v1/stocks/{id}` - Get stock details

### Purchase Orders

-   `POST /api/v1/purchase-orders/` - Create PO
-   `GET /api/v1/purchase-orders/` - List POs
-   `GET /api/v1/purchase-orders/{id}` - Get PO details
-   `PUT /api/v1/purchase-orders/{id}/status` - Approve/Cancel PO
-   `PUT /api/v1/purchase-orders/{id}/receive` - Receive goods (stock IN)

### Item Requests

-   `POST /api/v1/item-requests/` - Create request
-   `GET /api/v1/item-requests/` - List requests
-   `GET /api/v1/item-requests/{id}` - Get request details
-   `PUT /api/v1/item-requests/{id}/submit` - Submit for approval
-   `PUT /api/v1/item-requests/{id}/approval` - Approve/Reject request
-   `PUT /api/v1/item-requests/{id}/issue` - Issue items (stock OUT)

### Stock Transactions

-   `POST /api/v1/stock-transactions/` - Create transaction (IN/OUT/MOVE)
-   `GET /api/v1/stock-transactions/` - List transactions
-   `GET /api/v1/stock-transactions/{id}` - Get transaction details
-   `PUT /api/v1/stock-transactions/{id}/confirm` - Confirm and update stock

---

## Authentication & Authorization

### Authentication

-   **Method**: JWT Bearer Token
-   **Provider**: ATAMS SSO (http://localhost:8080)
-   **Header**: `Authorization: Bearer <token>`

### Authorization Levels

-   **Role Level 1**: Admin - Full access to all operations
-   **Role Level 10**: Manager/Supervisor - Can approve, receive, issue
-   **Role Level 100**: Staff/User - Can create requests, view data

### Access Control

-   Item requests follow ownership model:
    -   Creators can only see/edit their own requests (when posted)
    -   After submission, approvers can see all pending requests
    -   Approvers can approve/reject any request
-   Purchase orders and stock transactions are visible to all authorized users

---

## Installation & Setup

### Prerequisites

-   Python 3.8+
-   PostgreSQL 12+
-   ATAMS SSO running on http://localhost:8080

### Installation Steps

1. **Clone the repository**

```bash
git clone https://github.com/GratiaManullang03/aventory
cd aventory
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env and set:
# - DATABASE_URL=postgresql://user:pass@localhost:5432/aventory
# - ATAMS_SSO_URL=http://localhost:8080
# - Other configurations
```

5. **Run database migrations**

```bash
# Database migrations are handled by ATAMS framework
# Ensure your database schema is up to date
```

6. **Seed master data (optional)**

```bash
python faker/seed_data.py
```

7. **Seed transaction data (optional)**

```bash
# Update AUTH_TOKEN in faker/seed_transactions.py first
python faker/seed_transactions.py
```

---

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8081 --env-file .env --reload
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8081 --env-file .env --workers 4
```

The API will be available at `http://localhost:8081`

### API Documentation

-   **Swagger UI**: http://localhost:8081/docs
-   **ReDoc**: http://localhost:8081/redoc

---

## Common Use Cases

### Use Case 1: New Stock Arrival from Supplier

1. Procurement creates PO with items and quantities
2. Manager approves the PO
3. When goods arrive, warehouse staff clicks "Receive"
4. System automatically creates stock IN transaction
5. Stock is immediately available for requests

### Use Case 2: Department Needs Items

1. Department staff creates item request
2. Staff submits request to manager
3. Manager reviews and approves
4. Warehouse validates stock availability
5. Warehouse issues items
6. System automatically reduces stock

### Use Case 3: Warehouse Rebalancing

1. Check stock levels across warehouses
2. Create MOVE transaction from high-stock to low-stock warehouse
3. Confirm transaction
4. Stock automatically adjusted in both warehouses

### Use Case 4: Stock Correction

1. Physical stock count reveals discrepancy
2. Create IN transaction to add missing stock (or OUT to remove excess)
3. Add note explaining the correction
4. Confirm transaction
5. Stock updated to match physical count

---

## Data Validation & Business Rules

### Purchase Orders

-   ✓ Must have at least one item
-   ✓ All items must exist in system
-   ✓ Quantities must be positive
-   ✓ Warehouse must exist and be active
-   ✓ Supplier must exist and be active
-   ✓ Can only receive approved POs
-   ✓ Cannot receive the same PO twice

### Item Requests

-   ✓ Must have at least one item
-   ✓ All items must exist in system
-   ✓ Quantities must be positive
-   ✓ Warehouse must exist
-   ✓ Only owner can submit their request
-   ✓ Stock availability validated when issuing
-   ✓ Can issue partial quantities (less than requested)

### Stock Transactions

-   ✓ Must have at least one item
-   ✓ Transaction code must be unique
-   ✓ Type-specific validations:
    -   IN: `tx_from_wh_id` must be NULL
    -   OUT: `tx_to_wh_id` must be NULL
    -   MOVE: Both warehouses required and must be different
-   ✓ OUT and MOVE validate sufficient stock
-   ✓ Cannot confirm the same transaction twice

---

## Error Handling

The system provides clear error messages for common scenarios:

### Stock Errors

```json
{
    "detail": "Insufficient stock for item 'Mouse' (SKU: IT-001) in warehouse 'Jakarta'. Available: 5 pcs, Required: 10 pcs."
}
```

### Validation Errors

```json
{
    "detail": "Purchase order must have at least 1 detail line. Please add items to the purchase order."
}
```

### Authorization Errors

```json
{
    "detail": "You can only submit your own requests"
}
```

### Status Errors

```json
{
    "detail": "Can only receive purchase order with status approved. Current status: posted"
}
```

---

## Troubleshooting

### Issue: Stock not updating after PO receive

**Solution**: Check that:

1. PO status is "approved" before receiving
2. No errors in API response
3. Check stock transactions table for corresponding TX record

### Issue: Cannot issue item request

**Possible Causes**:

1. Request not in "approved" status → Ensure request is approved first
2. Insufficient stock → Check stock levels, receive more stock if needed
3. User doesn't have permission → Verify user has role level 10 or higher

### Issue: 401 Unauthorized

**Solution**:

1. Token expired → Get new token from ATAMS SSO
2. Invalid token → Verify token format
3. ATAMS SSO not running → Start ATAMS SSO service

---

## Performance Considerations

-   **Pagination**: All list endpoints support pagination (default limit: 100)
-   **Filters**: Use query parameters to filter large datasets
-   **Indexes**: Database indexes on frequently queried fields (codes, status, dates)
-   **Transactions**: Stock updates use database transactions for data integrity

---

## Database Schema

### Key Tables

-   `aventory.item` - Item master data
-   `aventory.warehouse` - Warehouse master data
-   `aventory.stock` - Current stock levels (wh_id + it_id unique)
-   `aventory.purchase_order` + `purchase_order_detail` - PO data
-   `aventory.item_request` + `item_request_detail` - Request data
-   `aventory.stock_tx` + `stock_tx_detail` - Stock transaction history

### Important Constraints

-   Stock table has unique constraint on (wh_id, it_id)
-   Transaction codes are unique
-   All operations maintain referential integrity

---

## Contributing

1. Follow the existing code structure
2. Add proper validation and error messages
3. Update documentation for new features
4. Test all business flows before committing
