---
title: Compro Assets API
description: Company profile assets management API with Atlas SSO authentication, role-based access control, and response encryption
order: 9
category: API Service
tags: [compro-assets, crud, atlas-sso, fastapi, postgresql]
---

# Compro Assets API

API to manage company profile assets with authentication features using Atlas SSO.

## Features

* **CRUD Operations** for Company Profile Assets
* **Atlas SSO Integration** for authentication & authorization
* **Role-based Access Control** with role level validation
* **Public Endpoints** for GET operations (no auth)
* **Protected Endpoints** for Create/Update/Delete (role_level >= 10)
* **Response Encryption** for GET endpoints (optional)
* **Database Auditing** with created_by, created_at, updated_by, updated_at

## Tech Stack

* **FastAPI** - Modern Python web framework
* **PostgreSQL** - Database with `compro` schema
* **SQLAlchemy** - ORM
* **ATAMS Toolkit** - Internal toolkit for authentication & utilities
* **Atlas SSO** - Single Sign-On service
* **Docker & Docker Compose** - Containerization

## Project Structure

```
compro_assets/
├── app/
│   ├── api/
│   │   ├── deps.py                    # Dependencies (auth)
│   │   └── v1/
│   │       ├── api.py                 # Router registration
│   │       └── endpoints/
│   │           ├── compro_assets.py   # Assets endpoints
│   │           └── users.py           # User endpoints (example)
│   ├── core/
│   │   └── config.py                  # Settings
│   ├── db/
│   │   └── session.py                 # Database session
│   ├── models/
│   │   └── compro_asset.py            # SQLAlchemy models
│   ├── repositories/
│   │   └── compro_asset_repository.py # Data access layer
│   ├── schemas/
│   │   └── compro_asset.py            # Pydantic schemas
│   ├── services/
│   │   └── compro_asset_service.py    # Business logic
│   └── main.py                        # Application entry point
├── venv/                              # Virtual environment
├── .env                               # Environment variables (gitignored)
├── .env.example                       # Example environment variables
├── docker-compose.yml                 # Docker compose config
├── docker-compose.override.yml        # Docker override for development
├── Dockerfile                         # Docker image
├── requirements.txt                   # Python dependencies
├── ddl.md                             # Database schema documentation
├── todo.md                            # API specification
└── README.md                          # This file
```

## API Endpoints

### Assets Management

| Method   | Endpoint                 | Auth Required     | Description                      |
| -------- | ------------------------ | ----------------- | -------------------------------- |
| `GET`    | `/api/v1/assets`         | No                | Get all assets (simplified list) |
| `GET`    | `/api/v1/assets/{ca_id}` | No                | Get asset detail by ID           |
| `POST`   | `/api/v1/assets`         | Yes (level >= 10) | Create new asset                 |
| `PUT`    | `/api/v1/assets/{ca_id}` | Yes (level >= 10) | Update existing asset            |
| `DELETE` | `/api/v1/assets/{ca_id}` | Yes (level >= 10) | Delete asset                     |

### Authentication

Authentication uses **Atlas SSO** with a Bearer token or cookie (`ATLASTOKEN`).

**Authorization Rules:**

* **GET endpoints**: Public access (no authentication required)
* **POST/PUT/DELETE**: Requires `role_level >= 10` for app `COMPRO_ASSETS`

## Database Schema

```sql
CREATE SCHEMA IF NOT EXISTS compro;

CREATE TABLE IF NOT EXISTS compro.compro_assets (
  ca_id              BIGSERIAL PRIMARY KEY,
  ca_title           TEXT,
  ca_tagline         TEXT,
  ca_image           TEXT,
  ca_image_carousel  TEXT[]      DEFAULT '{}',
  ca_subtitle        TEXT,
  ca_link            TEXT,
  created_at         TIMESTAMP   NOT NULL DEFAULT NOW(),
  created_by         TEXT        NOT NULL,
  updated_at         TIMESTAMP,
  updated_by         TEXT
);

CREATE INDEX IF NOT EXISTS idx_compro_assets_title ON compro.compro_assets (ca_title);
```

## Setup & Installation

### Prerequisites

* Python 3.11+
* PostgreSQL 14+
* Docker & Docker Compose (optional)

### 1. Clone Repository

```bash
git clone <repository-url>
cd compro_assets
```

### 2. Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Application
APP_NAME=compro_assets
APP_VERSION=1.0.0
DEBUG=true

# Database
DATABASE_URL=postgresql://user:password@localhost/compro_assets

# Atlas SSO
ATLAS_SSO_URL=https://api.atlas-microapi.atamsindonesia.com/api/v1
ATLAS_APP_CODE=COMPRO_ASSETS
ATLAS_ENCRYPTION_KEY=7c5f7132ba1a6e566bccc56416039bea
ATLAS_ENCRYPTION_IV=ce84582d0e6d2591

# Response Encryption (optional)
ENCRYPTION_ENABLED=false
ENCRYPTION_KEY=change_me_32_characters_long!!
ENCRYPTION_IV=change_me_16char
```

### 3. Database Setup

Create database and schema:

```sql
CREATE DATABASE compro_assets;
\c compro_assets
CREATE SCHEMA compro;
```

Run DDL from [ddl.md](ddl.md):

```bash
psql -U user -d compro_assets -f ddl.sql
```

### 4. Installation

#### Option A: Docker (Recommended)

```bash
# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f app
```

The API will run at `http://localhost:8000`

#### Option B: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access API

* **API Documentation (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Alternative Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
* **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

## Usage Examples

### 1. Get All Assets (Public)

```bash
curl -X GET "http://localhost:8000/api/v1/assets"
```

### 2. Get Asset by ID (Public)

```bash
curl -X GET "http://localhost:8000/api/v1/assets/1"
```

### 3. Create Asset (Authenticated)

```bash
curl -X POST "http://localhost:8000/api/v1/assets" \
  -H "Authorization: Bearer <your-atlas-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ca_title": "Nexgen Gaming",
    "ca_tagline": null,
    "ca_image": "/portofolio/gaming.png",
    "ca_image_carousel": [],
    "ca_subtitle": "",
    "ca_link": ""
  }'
```

### 4. Update Asset (Authenticated)

```bash
curl -X PUT "http://localhost:8000/api/v1/assets/1" \
  -H "Authorization: Bearer <your-atlas-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ca_title": "Updated Title",
    "ca_tagline": "Updated Tagline",
    "ca_image": "/updated/image.png",
    "ca_image_carousel": ["/carousel/1.png"],
    "ca_subtitle": "Updated subtitle",
    "ca_link": "https://example.com"
  }'
```

### 5. Delete Asset (Authenticated)

```bash
curl -X DELETE "http://localhost:8000/api/v1/assets/1" \
  -H "Authorization: Bearer <your-atlas-token>"
```

## Authentication Flow

1. User logs in via Atlas SSO
2. Atlas returns an access token (JWT)
3. The client stores the token in:

   * **Header**: `Authorization: Bearer <token>`
   * **Cookie**: `ATLASTOKEN=<token>`
4. Every request to a protected endpoint will validate:

   * Is the token valid?
   * Does the user have access to the `COMPRO_ASSETS` app?
   * Is role level >= 10?

## Development

### Hot Reload

Docker Compose is configured with volume mounting for hot reload:

```yaml
volumes:
  - ./app:/app/app
```

Changes in the `app/` folder will automatically reload without restarting the container.

### Running Tests

```bash
# In container
docker-compose exec app pytest

# Local
pytest
```

### Code Structure Pattern

This project uses **Clean Architecture**:

1. **API Layer** (`endpoints/`) - Handles HTTP requests
2. **Service Layer** (`services/`) - Business logic & validation
3. **Repository Layer** (`repositories/`) - Data access
4. **Model Layer** (`models/`) - Database entities
5. **Schema Layer** (`schemas/`) - Request/Response validation

## Generate CRUD

Using ATAMS CLI to generate CRUD boilerplate:

```bash
atams generate <resource_name>
```

Example:

```bash
atams generate department
```

## Docker Commands

```bash
# Build
docker-compose build

# Start
docker-compose up

# Stop
docker-compose down

# View logs
docker-compose logs -f app

# Execute command in container
docker-compose exec app <command>

# Rebuild and restart
docker-compose up --build --force-recreate
```

## Troubleshooting

### Database Connection Error

Ensure the DATABASE_URL is correct and the database has been created:

```bash
psql -U user -c "CREATE DATABASE compro_assets;"
```

### Atlas SSO Connection Error

Check:

1. `ATLAS_SSO_URL` is correct
2. `ATLAS_APP_CODE` matches what’s registered in Atlas
3. The network can access Atlas SSO

### Permission Denied Error

Ensure the user in Atlas has a role with:

* `app_code = "COMPRO_ASSETS"`
* `role_level >= 10`

## Example Endpoints (from template)

This project also includes an example CRUD for Users demonstrating:

* Complete CRUD operations (GET, POST, PUT, DELETE)
* Two-level authorization (Route + Service)
* Atlas SSO authentication
* Response encryption for GET endpoints
* ORM and Native SQL examples in BaseRepository
* Proper commit/rollback handling
* Proper error handling

**Available endpoints:**

* GET /api/v1/users - List all users (requires role level >= 50)
* GET /api/v1/users/{id} - Get single user (requires role level >= 10)
* POST /api/v1/users - Create user (requires role level >= 50)
* PUT /api/v1/users/{id} - Update user (requires role level >= 10)
* DELETE /api/v1/users/{id} - Delete user (requires role level >= 50)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Internal ATAMS Project

## Contact

* **Developer**: ATAMS Team
* **Project**: Compro Assets API
* **Documentation**: [API Docs](http://localhost:8000/docs)
