---
title: Atablog - Blog Management System
description: A comprehensive blog management system built with FastAPI and PostgreSQL, featuring AI-powered content generation, media management with Cloudinary, and Atlas SSO integration
order: 14
category: Backend Application
tags:
    [
        blog,
        cms,
        fastapi,
        postgresql,
        ai-generation,
        poe-api,
        jina-ai,
        cloudinary,
        wysiwyg,
        media-management,
        atlas-sso,
        sqlalchemy,
    ]
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
-   [Validation Rules Summary](#validation-rules-summary)
-   [Error Handling](#error-handling)
-   [Performance Optimizations](#performance-optimizations)
-   [API Interactive Documentation](#api-interactive-documentation)
-   [Support](#support)

## Key Features

-   **AI Blog Generator** 🤖: Generate blog posts using POE API (GPT-4o-mini) with Jina AI for web search and content fetching
-   **WYSIWYG Editor Support** ✍️: Full support for WYSIWYG editors (Tiptap) with images embedded in HTML content
-   **Featured Image Upload** 📷: Separate thumbnail/featured image management with dedicated endpoints
-   **Cloudinary Integration** ☁️: Secure media storage with signed URLs (15-min expiry) and automatic cleanup
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

-   `GET /api/v1/blog` - List all posts with filters and pagination
    -   **Query Parameters:** `status_id`, `category_id`, `author_id`, `search`, `sort` (created_at|published_at|view_count), `order` (asc|desc), `page` (default: 1), `size` (1-100, default: 20)
    -   Returns posts with `featured_image_url`, author info, category, tags, view count
-   `GET /api/v1/blog/{id}` - Get post detail with full relations
    -   Returns complete post data including content, metadata, reference URLs, media tracking
-   `POST /api/v1/blog` - Create post (always Draft status, auto-extracts media from HTML)
    -   **Validation:** Title (1-255 chars), content (required), max 10 tags per post
    -   **Auto-calculation:** Slug, read time, excerpt (if not provided)
    -   **Media tracking:** Auto-extracts `data-media-id` from HTML content
-   `POST /api/v1/blog/generate` - **AI Generate** post from topic or URLs (max 3 URLs)
    -   **Target lengths:** short (500-800 words), medium (1200-1800 words), long (2500-3500 words)
    -   **Two modes:** Web search (no URLs) or Reference (URLs provided)
    -   Uses POE API (GPT-4o-mini) + Jina AI for content fetching
    -   Always creates with Draft status, stores reference URLs
-   `PUT /api/v1/blog/{id}` - Update post (Draft/Archived only)
    -   **Edit protection:** Cannot edit Published, Scheduled, or Deleted posts
    -   **Auto-recalculation:** Slug (if title changes), read time, excerpt
    -   **Media tracking:** Re-extracts media IDs if content changes
-   `PUT /api/v1/blog/{id}/status` - Change post status with strict transition rules
    -   **Scheduled posts:** Require future `published_at` date
    -   **Published posts:** Auto-set `published_at` to now() if not already set
    -   Validates allowed transitions before updating
-   `PUT /api/v1/blog/{id}/featured` - Toggle featured (max 5, Published posts only)
    -   **Validation:** Only Published posts can be featured, max 5 featured posts allowed
-   `POST /api/v1/blog/{id}/featured-image` - Upload featured image (PNG/JPG/JPEG, max 5MB)
    -   Uploads to Cloudinary folder: `atablog/posts/{id}/featured/`
    -   Deletes old featured image automatically
-   `DELETE /api/v1/blog/{id}/featured-image` - Delete featured image from Cloudinary and database
-   `DELETE /api/v1/blog/{id}` - Soft delete post (changes status to Deleted)

### Media Management (Admin)

-   `POST /api/v1/media/upload` - Upload image to Cloudinary (for WYSIWYG editor)
-   `DELETE /api/v1/media/{id}` - Delete from Cloudinary + cleanup relations

**Supported Formats:** JPG, PNG, WebP (max 5MB)

**WYSIWYG Integration:**

-   Images are embedded directly in `bp_content` HTML using `data-media-id` attribute
-   Backend auto-parses HTML to track media usage in `post_media` table
-   Example: `<img src="cloudinary-url" data-media-id="123" alt="description">`

### Public Endpoints

**No Authorization Required**

-   `GET /api/v1/posts` - List published posts (status=Published only)
    -   **Query Parameters:** `category` (slug), `tag` (slug), `search`, `sort` (latest|popular|featured), `featured` (boolean), `page` (default: 1), `size` (1-100, default: 20)
    -   **Sort options:** latest (published_at DESC), popular (view_count DESC), featured (featured first)
    -   Returns posts with `featured_image_url`, author name, category, tags
-   `GET /api/v1/posts/{slug}` - Get post by slug with related posts
    -   **Features:** Auto-increments view counter with rate limiting, returns related posts (same category, limit 5)
    -   **View tracking:** IP-based (SHA256 hashed for privacy), 15-minute cooldown per IP per post
    -   **Auto-cleanup:** Deletes view tracking records older than 24 hours

**Rate Limiting Details:**

-   IP addresses hashed with SHA256 for privacy
-   15-minute cooldown between views from same IP per post
-   Tracking records automatically cleaned up after 24 hours

## Architecture

### Database Schema

**Schema:** `atablog`

**Tables:**

1. **master_status** - Post statuses (1=Draft, 2=Published, 3=Scheduled, 4=Archived, 5=Deleted)
2. **master_category** - Blog categories with slug
3. **master_tag** - Blog tags with slug
4. **media_file** - Media files metadata (Cloudinary paths)
5. **blog_post** - Blog posts (main table)
    - Contains: title, slug, content (HTML), excerpt, featured_image, read_time, view_count, is_featured, metadata
    - FK → `atablog.master_category` (RESTRICT)
    - FK → `atablog.master_status` (RESTRICT)
    - Cross-schema join → `pt_atams_indonesia.users` (author info)
    - Column `bp_reference_urls`: JSON array of source URLs (for AI-generated posts)
6. **post_tag** - Many-to-many junction: posts ↔ tags
    - FK → `atablog.blog_post` (CASCADE)
    - FK → `atablog.master_tag` (CASCADE)
    - Unique constraint on (post_id, tag_id)
    - Max 10 tags per post (validated in service layer)
7. **post_media** - Media tracking junction: posts ↔ media files
    - FK → `atablog.blog_post` (CASCADE)
    - FK → `atablog.media_file` (RESTRICT)
    - Tracks which media is used in which posts
    - No position/placement/caption data (all in HTML)
    - Media IDs extracted from `data-media-id` attributes in HTML
8. **blog_view_tracking** - View counter rate limiting
    - Stores: post_id, ip_hash (SHA256), viewed_at
    - 15-minute rate limit per IP per post
    - Records older than 24 hours auto-deleted

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

**Request Parameters:**

-   `topic`: string (1-500 chars, required) - Main topic or title
-   `reference_urls`: array of string (max 3, optional) - Source URLs
-   `keywords`: array of string (max 10, optional) - Keywords to include
-   `target_length`: enum (short|medium|long, default: medium)
-   `category_id`: int (required) - Blog category
-   `custom_instructions`: string (optional) - Additional instructions for AI

**Target Length Mapping:**

-   `short`: 500-800 words
-   `medium`: 1200-1800 words (default)
-   `long`: 2500-3500 words

**Two Generation Modes:**

1. **Reference Mode** (URLs provided):

    - Fetches content from provided URLs (max 3)
    - Uses Jina Reader to extract clean markdown
    - Limits each source to 5000 characters
    - Tracks used URLs in `bp_reference_urls`

2. **Web Search Mode** (no URLs):
    - Searches web using Jina Search API
    - Gets top 3 relevant results
    - Fetches content from each result URL
    - Tracks searched URLs in `bp_reference_urls`

**AI Generation Process:**

1. Gather source content (via Reference or Search mode)
2. Build system prompt with target word count, HTML formatting requirements, keywords
3. Send to POE API (GPT-4o-mini) for generation
4. Extract title from generated content (first line or h1)
5. Generate unique slug from title (adds timestamp if duplicate)
6. Calculate read time (200 words/minute for technical content)
7. Extract excerpt (first 200 characters)
8. **Always saves with Draft status** (requires manual review before publishing)
9. Store reference URLs as JSON array

**Configuration (from .env):**

-   `POE_API_KEY`: POE API key
-   `LLM_MODEL`: Model name (default: GPT-4o-mini)
-   `LLM_MAX_TOKENS`: Max response tokens (default: 500)
-   `LLM_TEMPERATURE`: Creativity level 0-1 (default: 0.7)
-   `LLM_TIMEOUT`: Request timeout in seconds (default: 60)
-   `JINA_API_KEY`: Jina AI API key for search and content fetching

### Status Transition Rules

**Strict Workflow:**

```
Draft (1) → Published (2), Scheduled (3), Archived (4), Deleted (5)
Published (2) → Archived (4), Deleted (5)
Scheduled (3) → Published (2), Archived (4), Deleted (5)
Archived (4) → Draft (1), Published (2), Deleted (5)
Deleted (5) → [Terminal state - cannot be restored]
```

**Status-Specific Behavior:**

1. **Publishing (status_id = 2):**

    - Auto-sets `published_at` to now() if not already set
    - Do NOT send `published_at` in request body (will be ignored)

2. **Scheduling (status_id = 3):**

    - `published_at` is **REQUIRED** in request body
    - Must be a future date
    - Validation fails if date is in past

3. **Other statuses:**
    - `published_at` parameter is ignored

**Transition Validation:**

-   System checks if transition is allowed before updating
-   Throws `BadRequestException` with details if invalid transition attempted
-   Error includes current status, target status, and list of allowed transitions

**Edit Protection:**

-   **Can edit:** Draft (1), Archived (4) only
-   **Cannot edit:** Published (2), Scheduled (3), Deleted (5)
-   Attempting to edit protected post throws `ForbiddenException` with status name
-   Exception message: "Cannot edit post with status '{status}'. Only 'Draft' or 'Archived' posts can be edited."

### Featured Posts Limit

**Business Rules:**

-   Maximum 5 featured posts allowed at any time
-   **Only Published (status_id = 2) posts can be featured**
-   Draft/Scheduled/Archived/Deleted posts cannot be featured

**Validation Process:**

1. Check if post exists
2. Verify post status is Published (2)
    - If not Published: throws `BadRequestException` with status info
3. If setting featured = true: check current featured count
    - If count >= 5: throws `BadRequestException` with current count
4. Update featured status

**Error Messages:**

-   "Only Published posts can be featured. Current status: {status_name}"
-   "Maximum 5 featured posts allowed. You currently have {count}."

### View Counter Rate Limiting

**Implementation Details:**

-   **IP Hashing:** SHA256 for privacy protection (original IP not stored)
-   **Storage:** `blog_view_tracking` table
-   **Rate Limit:** 15 minutes cooldown per IP per post
-   **Auto Cleanup:** Records older than 24 hours automatically deleted

**Flow:**

1. User visits post via `GET /api/v1/posts/{slug}`
2. System hashes IP address with SHA256
3. Checks if IP viewed this post in last 15 minutes
4. If no recent view:
    - Increment `bp_view_count` by 1
    - Record view in `blog_view_tracking` table
5. If recent view exists: skip increment
6. After successful view tracking, cleanup old records (> 24 hours)

**Privacy Features:**

-   Original IP addresses never stored in database
-   Only SHA256 hashes stored (irreversible)
-   View tracking records automatically expire after 24 hours

### WYSIWYG Image Management

**Frontend Integration Flow (Tiptap):**

1. User inserts image in WYSIWYG editor
2. Frontend uploads image to `POST /api/v1/media/upload`
    - **Allowed formats:** JPG, PNG, WebP
    - **Max size:** 5MB
3. Backend uploads to Cloudinary folder: `atablog/media/`
4. Response contains `mf_id` and signed URL (15-min expiry)
5. Frontend inserts image in HTML with tracking attribute:
    ```html
    <img
        src="https://cloudinary-signed-url"
        data-media-id="123"
        alt="description" />
    ```
6. When post is created/updated, backend automatically:
    - Parses HTML content
    - Extracts all `data-media-id` attributes using regex pattern
    - Tracks media usage in `post_media` junction table

**Media Tracking:**

-   `post_media` table tracks which media files are used in which posts
-   All positioning, sizing, styling, and captions controlled by HTML/CSS in frontend
-   Images embedded directly in `bp_content` HTML (no separate media array in response)
-   Media tracking is for cleanup purposes (prevent deleting in-use media)

**HTML Parser:**

-   Pattern: `data-media-id=["']?(\d+)["']?`
-   Extracts unique media IDs from HTML content
-   Handles both quoted and unquoted attribute values
-   Automatically called on post create and update

### Featured Image Management

**Separate from Content Images:**

Featured images serve as post thumbnails and are managed separately from content images.

| Feature               | Featured Image                                    | Content Images (WYSIWYG)          |
| --------------------- | ------------------------------------------------- | --------------------------------- |
| **Purpose**           | Post thumbnail/preview                            | Embedded in content               |
| **Storage**           | `bp_featured_image` column (Cloudinary public_id) | HTML `<img>` tags in `bp_content` |
| **Upload Endpoint**   | `POST /api/v1/blog/{id}/featured-image`           | `POST /api/v1/media/upload`       |
| **Delete Endpoint**   | `DELETE /api/v1/blog/{id}/featured-image`         | `DELETE /api/v1/media/{id}`       |
| **Allowed Types**     | PNG, JPG, JPEG                                    | JPG, PNG, WebP                    |
| **Max Size**          | 5MB                                               | 5MB                               |
| **Tracking**          | Direct column reference                           | `post_media` junction table       |
| **Cloudinary Folder** | `atablog/posts/{post_id}/featured/`               | `atablog/media/`                  |
| **Filename Format**   | `featured-{uuid}`                                 | `{uuid}`                          |

**Upload Process:**

1. Validate file type (PNG/JPG/JPEG only) and size (max 5MB)
2. Delete old featured image from Cloudinary (if exists)
3. Generate unique filename: `featured-{uuid}`
4. Upload to Cloudinary: `atablog/posts/{post_id}/featured/`
5. Store Cloudinary `public_id` in `bp_featured_image` column
6. Return response with signed URL (15-min expiry)

**Response in All GET Endpoints:**

```json
{
    "bp_featured_image": "atablog/posts/123/featured/featured-abc123",
    "featured_image_url": "https://res.cloudinary.com/.../signed-url-15min"
}
```

**Delete Process:**

1. Check if featured image exists
2. Delete from Cloudinary
3. Set `bp_featured_image = NULL` in database
4. Continue even if Cloudinary deletion fails (log error)

### Media Delete - Auto Cleanup

**Endpoint:** `DELETE /api/v1/media/{media_id}`

**Automatic Cleanup Flow:**

1. **Delete from Cloudinary:**

    - Remove physical file from Cloudinary storage
    - Continue cleanup even if Cloudinary deletion fails
    - Error logged but doesn't stop database cleanup

2. **Cleanup Featured Image References:**

    - Find all posts using this media as featured image
    - Set `bp_featured_image = NULL` for those posts
    - Ensures no broken references in database

3. **Delete Media Relations (CASCADE):**

    - `post_media` junction table records automatically deleted
    - Database CASCADE constraint handles this
    - Removes all tracking records for this media

4. **Delete Media Record:**
    - Remove from `media_file` table
    - Final cleanup of media metadata

**No Usage Check:**

-   Media can be deleted even if in use
-   All references automatically cleaned up
-   Frontend may show broken images until content is updated
-   Recommended: Check media usage before deletion in frontend

## Security

### Authentication & Authorization

**Atlas SSO (ATAMS):**

-   Token validation via Atlas API
-   User information from `pt_atams_indonesia.users`
-   Cross-schema join for author details

**Authorization Levels:**

| Level | Access            | Endpoints                                                                     |
| ----- | ----------------- | ----------------------------------------------------------------------------- |
| None  | Public access     | `/api/v1/posts/*` - Published posts only                                      |
| 10+   | Read master data  | `/api/v1/master-status/*` - Read-only                                         |
| 50+   | Full admin access | `/api/v1/blog/*`, `/api/v1/categories/*`, `/api/v1/tags/*`, `/api/v1/media/*` |

**Endpoints by Authorization:**

1. **Public (No Auth):**

    - `GET /api/v1/posts` - List published posts
    - `GET /api/v1/posts/{slug}` - Get post detail

2. **Level 10+ (Read):**

    - `GET /api/v1/master-status` - List statuses
    - `GET /api/v1/master-status/{id}` - Get status detail

3. **Level 50+ (Admin):**
    - All blog CRUD operations
    - AI blog generation
    - Category and tag management
    - Media upload and delete
    - Featured image management
    - Status transitions

**Implementation:**

```python
from atams.sso import create_atlas_client, create_auth_dependencies

# Initialize Atlas SSO client
atlas_client = create_atlas_client(settings)

# Create auth dependencies
get_current_user, require_auth, require_min_role_level, require_role_level = create_auth_dependencies(atlas_client)

# Usage in router
api_router.include_router(
    blog_admin.router,
    prefix="/blog",
    tags=["Blog - Admin"],
    dependencies=[Depends(require_min_role_level(50))]
)
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
│   │   ├── blog_post.py           # Blog schemas
│   │   ├── master_category.py     # Category schemas
│   │   ├── master_tag.py          # Tag schemas
│   │   ├── master_status.py       # Status schemas
│   │   └── media_file.py          # Media schemas
│   ├── repositories/              # Data access layer
│   │   ├── blog_repository.py
│   │   ├── category_repository.py
│   │   └── ...
│   ├── services/                  # Business logic
│   │   ├── blog_service.py        # Blog CRUD + featured image + status transitions
│   │   ├── blog_list_service.py   # Blog list with pagination + batch tag loading
│   │   ├── ai_blog_service.py     # AI blog generation (POE + Jina)
│   │   ├── media_service.py       # Media upload/delete + Cloudinary integration
│   │   ├── master_category_service.py  # Category CRUD
│   │   ├── master_tag_service.py       # Tag CRUD
│   │   └── master_status_service.py    # Status list (read-only)
│   ├── api/
│   │   ├── deps.py                # Auth dependencies
│   │   └── v1/
│   │       ├── api.py             # Router aggregation
│   │       └── endpoints/
│   │           ├── blog_admin.py      # Blog admin endpoints
│   │           ├── blog_public.py     # Blog public endpoints
│   │           ├── master_category.py # Category endpoints
│   │           ├── master_tag.py      # Tag endpoints
│   │           ├── master_status.py   # Status endpoints
│   │           └── media.py           # Media upload/delete
│   ├── utils/
│   │   ├── slug.py                # Slug generation with uniqueness check
│   │   ├── read_time.py           # Read time calculation (200 wpm) + excerpt extraction
│   │   ├── security.py            # IP hashing (SHA256) for view tracking
│   │   ├── cloudinary_helper.py   # Cloudinary upload/delete + signed URL generation
│   │   ├── jina_helper.py         # Jina AI search + URL content fetching
│   │   └── html_parser.py         # Extract media IDs from HTML data-media-id attributes
│   └── main.py                    # FastAPI app
├── tests/
│   ├── conftest.py
│   └── test_*/
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Validation Rules Summary

### Blog Post Validation

| Field          | Rule                              | Error Message                          |
| -------------- | --------------------------------- | -------------------------------------- |
| `bp_title`     | 1-255 characters (required)       | "Title is required" / "Title too long" |
| `bp_content`   | Minimum 1 character (required)    | "Content is required"                  |
| `bp_excerpt`   | Maximum 500 characters (optional) | "Excerpt too long"                     |
| `tag_ids`      | Maximum 10 tags per post          | "Maximum 10 tags per post"             |
| `bp_slug`      | Auto-generated, must be unique    | Auto-adds timestamp if duplicate       |
| `bp_status_id` | Must follow transition rules      | "Invalid status transition"            |

### Media Validation

| Field              | Rule                | Error Message                                |
| ------------------ | ------------------- | -------------------------------------------- |
| **Featured Image** | PNG, JPG, JPEG only | "Invalid file type. Allowed: PNG, JPG, JPEG" |
| **Content Image**  | JPG, PNG, WebP only | "Invalid file type. Allowed: JPG, PNG, WebP" |
| **File Size**      | Maximum 5MB         | "File too large. Maximum size: 5MB"          |

### AI Generation Validation

| Field            | Rule                        | Error Message              |
| ---------------- | --------------------------- | -------------------------- |
| `topic`          | 1-500 characters (required) | "Topic is required"        |
| `reference_urls` | Maximum 3 URLs              | "Maximum 3 reference URLs" |
| `keywords`       | Maximum 10 keywords         | "Maximum 10 keywords"      |
| `target_length`  | Enum: short, medium, long   | "Invalid target length"    |

### Category & Tag Validation

| Field                 | Rule                     | Error Message         |
| --------------------- | ------------------------ | --------------------- |
| `mc_name` / `mt_name` | Required, must be unique | "Name already exists" |
| `mc_slug` / `mt_slug` | Auto-generated from name | N/A                   |

## Error Handling

### Error Response Format

All errors return consistent JSON format:

```json
{
    "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Code | Exception             | When It Occurs                              | Example                              |
| ---- | --------------------- | ------------------------------------------- | ------------------------------------ |
| 400  | `BadRequestException` | Validation failed or business rule violated | "Maximum 5 featured posts allowed"   |
| 403  | `ForbiddenException`  | Action not allowed due to state             | "Cannot edit Published post"         |
| 404  | `NotFoundException`   | Resource not found                          | "Blog post not found"                |
| 401  | `Unauthorized`        | Invalid or missing auth token               | "Invalid authentication credentials" |
| 422  | `ValidationError`     | Request body validation failed              | "Field required" (Pydantic)          |

### Business Logic Errors

**Status Transition Errors:**

```json
{
    "detail": "Invalid status transition from 'Published' to 'Draft'. Allowed transitions: Archived, Deleted"
}
```

**Edit Protection Errors:**

```json
{
    "detail": "Cannot edit post with status 'Published'. Only 'Draft' or 'Archived' posts can be edited."
}
```

**Featured Post Limit Errors:**

```json
{
    "detail": "Maximum 5 featured posts allowed. You currently have 5."
}
```

**Featured Post Status Errors:**

```json
{
    "detail": "Only Published posts can be featured. Current status: Draft"
}
```

**Scheduled Post Validation Errors:**

```json
{
    "detail": "published_at is required for scheduled posts and must be a future date"
}
```

### Validation Errors (422)

Pydantic validation errors return detailed field-level information:

```json
{
    "detail": [
        {
            "loc": ["body", "bp_title"],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": ["body", "tag_ids"],
            "msg": "ensure this value has at most 10 items",
            "type": "value_error.list.max_items"
        }
    ]
}
```

## Performance Optimizations

### N+1 Query Prevention

**Problem:** Loading tags for multiple posts causes N+1 queries (1 query for posts + N queries for tags)

**Solution:** Batch loading in `blog_list_service.py`

```python
# Get all post IDs
post_ids = [post["bp_id"] for post in results]

# Single query to load all tags for all posts
tags_results = self.blog_repo.get_tags_for_posts(db, post_ids)

# Group tags by post_id in memory
tags_by_post = {}
for tag_row in tags_results:
    post_id = tag_row["pt_post_id"]
    if post_id not in tags_by_post:
        tags_by_post[post_id] = []
    tags_by_post[post_id].append(tag_row)
```

**Result:** O(1) queries instead of O(N+1)

### Cloudinary Signed URLs

-   **Expiry:** 15 minutes (configurable)
-   **Purpose:** Prevent unauthorized access to media files
-   **Generation:** On-demand for each request
-   **Caching:** Not cached (generated fresh each time for security)

### View Counter Optimization

-   **Rate Limiting:** Prevents multiple increments from same IP
-   **Auto Cleanup:** Removes records older than 24 hours to keep table small
-   **Hashed IPs:** SHA256 hashing for privacy (irreversible)

## API Interactive Documentation

FastAPI provides interactive API documentation with live testing:

-   **Swagger UI:** http://localhost:8000/docs
-   **ReDoc:** http://localhost:8000/redoc

### OpenAPI Examples

The API includes detailed request examples for complex endpoints:

**Status Update Examples (5 scenarios):**

1. Publish post (auto-set published_at)
2. Schedule post (require future published_at)
3. Archive post
4. Set to Draft (only from Archived)
5. Delete post (terminal state)

**Try it out in Swagger UI:**

-   Select endpoint
-   Choose example from dropdown
-   Click "Try it out"
-   Execute request with pre-filled data

## Support

For questions or issues, please refer to the documentation files or create an issue in the repository.
