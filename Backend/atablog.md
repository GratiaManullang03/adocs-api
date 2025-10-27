---
title: Atablog - Blog Management System
description: A comprehensive blog management system built with FastAPI and PostgreSQL, featuring AI-powered content generation, media management with Cloudinary, and Atlas SSO integration
order: 14
category: Backend Application
tags: [blog, fastapi, postgresql, ai-generation, cloudinary, atlas-sso]
---

# Atablog - Blog Management System

A comprehensive blog management system built with FastAPI and PostgreSQL, featuring AI-powered content generation, media management with Cloudinary, and Atlas SSO integration.

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
-   [Deployment](#deployment)
-   [Project Structure](#project-structure)

## Key Features

-   **AI Blog Generator** 🤖: Generate blog posts using POE API (GPT-4o-mini) with Jina AI for web search and content fetching
-   **Cloudinary Integration** ☁️: Secure media storage with signed URLs and automatic cleanup
-   **View Counter** 👁️: IP-based rate limiting (15 minutes) with automatic cleanup after 24 hours
-   **Status Transitions** 🔄: Strict workflow management (Draft → Published → Archived → Deleted)
-   **Edit Protection** 🔒: Only Draft and Archived posts can be edited
-   **Featured Posts** ⭐: Maximum 5 featured posts (only Published posts)
-   **Cross-Schema Support** 🔗: Join with external schemas (Atlas SSO users)
-   **Media Auto-Cleanup** 🧹: Automatic deletion from Cloudinary and relation cleanup

## Technology Stack

-   **Framework**: FastAPI 0.115+
-   **Database**: PostgreSQL (with custom schema `atablog`)
-   **ORM**: SQLAlchemy
-   **Authentication**: Atlas SSO (ATAMS)
-   **Validation**: Pydantic
-   **Server**: Uvicorn
-   **Storage**: Cloudinary
-   **AI Services**: POE API (OpenAI compatible) + Jina AI
-   **Connection Pool**: Optimized for cloud databases (Aiven compatible)

## Prerequisites

-   Python 3.10+
-   PostgreSQL 12+
-   Cloudinary Account (for media storage)
-   POE API Key (for AI blog generation)
-   Jina AI API Key (for web search & content fetching)
-   Atlas SSO access (for authentication)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/GratiaManullang03/atablog.git
    cd atablog
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

Create a `.env` file in the project root directory based on `.env.example`:

```env
# Application Settings
APP_NAME=atablog
APP_VERSION=1.0.0
DEBUG=true

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/atablog

# Database Connection Pool Settings
# For Aiven free tier (20 connections): DB_POOL_SIZE=3, DB_MAX_OVERFLOW=5
DB_POOL_SIZE=3
DB_MAX_OVERFLOW=5
DB_POOL_RECYCLE=3600
DB_POOL_TIMEOUT=30
DB_POOL_PRE_PING=true

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
CLOUDINARY_FOLDER=atablog

# POE API (OpenAI compatible)
POE_API_KEY=your_poe_key
LLM_MODEL=GPT-4o-mini
LLM_MAX_TOKENS=500
LLM_TEMPERATURE=0.7
LLM_TIMEOUT=60

# Jina AI
JINA_API_KEY=your_jina_key

# Atlas SSO Configuration
ATLAS_SSO_URL=https://api.atlas-microapi.atamsindonesia.com/api/v1
ATLAS_APP_CODE=ATABLOG
ATLAS_ENCRYPTION_KEY=7c5f7132ba1a6e566bccc56416039bea
ATLAS_ENCRYPTION_IV=ce84582d0e6d2591

# Response Encryption (Optional)
ENCRYPTION_ENABLED=false
ENCRYPTION_KEY=change_me_32_characters_long!!
ENCRYPTION_IV=change_me_16char

# CORS Configuration
# CORS_ORIGINS=["*"]  # Default: *.atamsindonesia.com

# Logging
LOGGING_ENABLED=true
LOG_LEVEL=INFO
LOG_TO_FILE=false

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
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
# Build and run
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

## API Endpoints

Base URL: `/api/v1`

### Master Data (Admin)

#### Master Status (Read-only)

-   `GET /api/v1/master-status` - List all statuses

#### Categories

-   `GET /api/v1/categories` - List categories with post count
-   `POST /api/v1/categories` - Create category (auto-generates slug)
-   `PUT /api/v1/categories/{id}` - Update category
-   `DELETE /api/v1/categories/{id}` - Delete (checks FK constraints)

#### Tags

-   `GET /api/v1/tags` - List tags with usage count
-   `POST /api/v1/tags` - Create tag (auto-generates slug)
-   `PUT /api/v1/tags/{id}` - Update tag
-   `DELETE /api/v1/tags/{id}` - Delete (CASCADE)

### Blog Management (Admin)

**Authorization Required:** Atlas SSO token with minimum role level 50

#### Blog Posts

-   `GET /api/v1/blog` - List all posts with filters (status, category, author, search)
-   `GET /api/v1/blog/{id}` - Get post detail with relations
-   `POST /api/v1/blog` - Create post (Draft status)
-   `POST /api/v1/blog/generate` - **AI Generate** post from topic or URLs
-   `PUT /api/v1/blog/{id}` - Update post (Draft/Archived only)
-   `PUT /api/v1/blog/{id}/status` - Change post status
-   `PUT /api/v1/blog/{id}/featured` - Toggle featured (max 5)
-   `DELETE /api/v1/blog/{id}` - Soft delete post

### Media Management (Admin)

-   `GET /api/v1/media` - List media with signed URLs (15min expiry)
-   `POST /api/v1/media/upload` - Upload to Cloudinary
-   `DELETE /api/v1/media/{id}` - Delete from Cloudinary + cleanup relations

**Supported Formats:** JPG, PNG, WebP (max 5MB)

### Public Endpoints

**No Authorization Required**

-   `GET /api/v1/posts` - List published posts with filters
-   `GET /api/v1/posts/{slug}` - Get post by slug + increment view counter

View counter has 15-minute rate limit per IP (hashed with SHA256).

## Architecture

### Database Schema

**Schema:** `atablog`

**Tables:**

1. **master_status** - Post statuses (1=Draft, 2=Published, 3=Scheduled, 4=Archived, 5=Deleted)
2. **master_category** - Blog categories with slug
3. **master_tag** - Blog tags with slug
4. **media_file** - Media files metadata (Cloudinary paths)
5. **blog_post** - Blog posts
    - FK → `atablog.master_category`
    - FK → `atablog.master_status`
    - Cross-schema join → `pt_atams_indonesia.users` (author)
6. **post_tag** - Many-to-many: posts ↔ tags
    - FK → `atablog.blog_post` (CASCADE)
    - FK → `atablog.master_tag` (CASCADE)
7. **post_media** - Post media attachments
    - FK → `atablog.blog_post` (CASCADE)
    - FK → `atablog.media_file` (CASCADE)
8. **blog_view_tracking** - View counter rate limiting (24h retention)

### Layered Architecture

```
API Layer (endpoints/)       → Business Logic (services/)       → Data Access (repositories/)       → Database
     ↓                                  ↓                                  ↓
  FastAPI                          Validation                         SQLAlchemy
  Authorization                    Business Rules                     ORM + Raw SQL
  Response Format                  Orchestration                      Transactions
                                        ↓
                                  External APIs
                                  (POE, Jina, Cloudinary)
```

### Data Flow

```
Request → Atlas SSO Auth → Endpoint → Service → Repository → Database (atablog schema)
                                         ↓
                                   External APIs:
                                   - POE (AI generation)
                                   - Jina (web search/fetch)
                                   - Cloudinary (media storage)
```

## Business Logic

### AI Blog Generation

**Endpoint:** `POST /api/v1/blog/generate`

**Two Modes:**

1. **Web Search Mode** (no URLs provided):

    - Jina AI searches top 3 results
    - Fetches and extracts content
    - POE generates blog post

2. **Reference Mode** (URLs provided, max 3):
    - Jina AI fetches URLs directly
    - POE generates from references

**Auto-calculation:**

-   Read time (based on word count)
-   Excerpt (first 200 chars)
-   Status: Draft (requires manual review)

### Status Transition Rules

**Strict Workflow:**

```
Draft (1) → Published (2), Scheduled (3), Archived (4), Deleted (5)
Published (2) → Archived (4), Deleted (5)
Archived (4) → Draft (1), Published (2), Deleted (5)
Scheduled (3) → Published (2), Archived (4), Deleted (5)
Deleted (5) → [Terminal state]
```

**Edit Protection:**

-   Can edit: Draft (1), Archived (4)
-   Cannot edit: Published (2), Scheduled (3), Deleted (5)
-   Exception: `ForbiddenException` with message

### Featured Posts Limit

**Business Rule:**

-   Maximum 5 featured posts allowed
-   Only Published (2) posts can be featured
-   Validation at service layer

### View Counter Rate Limiting

**Implementation:**

-   Hash IP with SHA256 (privacy)
-   Store: `blog_view_tracking` table
-   Rate limit: 15 minutes per IP per post
-   Auto cleanup: Records > 24 hours deleted automatically

### Media Delete - Auto Cleanup

**Cascade Flow:**

1. Delete from Cloudinary
2. Set `bp_featured_image = NULL` in posts using it
3. Delete `post_media` relations (CASCADE)
4. Delete from `media_file` table

## Security

### Authentication & Authorization

**Atlas SSO (ATAMS):**

-   Token validation via Atlas API
-   User information from `pt_atams_indonesia.users`
-   Cross-schema join for author details

**Authorization Levels:**

-   **Public endpoints** (>= 1): View published posts
-   **Admin endpoints** (>= 50): Full CRUD operations

**Usage:**

```python
from atams.auth import require_min_role_level

# Admin only
@router.post("/blog", dependencies=[Depends(require_min_role_level(50))])
```

### Response Encryption

Optional AES encryption for GET endpoints (configurable via `ENCRYPTION_ENABLED`).

### Environment Variables

**Critical secrets (NEVER commit to Git):**

-   `DATABASE_URL`: Database connection
-   `POE_API_KEY`: AI generation
-   `JINA_API_KEY`: Web search
-   `CLOUDINARY_API_SECRET`: Media storage
-   `ATLAS_ENCRYPTION_KEY`, `ATLAS_ENCRYPTION_IV`: SSO encryption

## Deployment

### Environment Configuration

**Development:**

-   `DEBUG=true`
-   `DB_POOL_SIZE=3`, `DB_MAX_OVERFLOW=5`

**Production:**

-   `DEBUG=false`
-   Adjust pool size based on connection limits
-   CORS restricted to specific domains

### Docker Deployment

```bash
# Build image
docker-compose build

# Run in production
docker-compose up -d
```

## Project Structure

```
atablog/
├── app/
│   ├── core/
│   │   └── config.py              # Settings
│   ├── db/
│   │   ├── session.py             # DB session
│   ├── models/                    # SQLAlchemy models
│   │   ├── blog_post.py
│   │   ├── blog_view_tracking.py
│   │   ├── master_category.py
│   │   ├── master_status.py
│   │   ├── master_tag.py
│   │   ├── media_file.py
│   │   ├── post_media.py
│   │   └── post_tag.py
│   ├── schemas/                   # Pydantic schemas
│   │   ├── common.py              # Base response schemas
│   │   ├── blog.py
│   │   ├── category.py
│   │   ├── tag.py
│   │   └── media.py
│   ├── repositories/              # Data access layer
│   │   ├── blog_repository.py
│   │   ├── category_repository.py
│   │   └── ...
│   ├── services/                  # Business logic
│   │   ├── blog_service.py
│   │   ├── ai_service.py          # POE + Jina integration
│   │   ├── media_service.py       # Cloudinary
│   │   └── ...
│   ├── api/
│   │   ├── deps.py                # Auth dependencies
│   │   └── v1/
│   │       ├── api.py             # Router aggregation
│   │       └── endpoints/
│   │           ├── blog.py
│   │           ├── categories.py
│   │           ├── tags.py
│   │           ├── media.py
│   │           └── public.py
│   ├── utils/
│   │   └── slug.py                # Slug generation
│   └── main.py                    # FastAPI app
├── tests/
│   ├── conftest.py
│   └── test_*/
├── docs/                          # Documentation
│   ├── BLOG ENDPOINTS.md
│   ├── BLOG DDL.md
│   └── cloudinary/
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Support

For questions or issues, please refer to the documentation files or create an issue in the repository.
