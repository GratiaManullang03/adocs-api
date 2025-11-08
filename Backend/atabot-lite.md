---
title: ATABOT-Lite - Conversational Landing Page Bot
description: Conversational Landing Page Bot backend with hybrid search, multi-language support, and LLM integration optimized for business landing pages
order: 4
category: AI Service
tags: [atabot-lite, chatbot, nlp, hybrid-search, fastapi, poe-api]
---

# ATABOT Lite v3 - Conversational Landing Page Bot

A simple chatbot for company profiles that answers questions based on company data. This bot uses GPT-4o-mini via the POE API with context injection from `data.json`.

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
-   [Project Structure](#project-structure)
-   [Testing](#testing)
-   [Deployment](#deployment)
-   [Database Setup](#database-setup)
-   [Customization](#customization)
-   [Support](#support)
-   [License](#license)

## Key Features

-   **Context-Aware Responses**: Answers questions based solely on `data.json`; rejects out-of-context questions
-   **Session Memory**: Tracks conversation history per session for follow-up questions
-   **Conversation Recording**: Automatically records all conversations to PostgreSQL database for analytics
-   **Self-Introduction**: The bot can introduce itself when asked
-   **GPT-4o-mini Integration**: Uses the POE API to generate natural responses
-   **Company Profile Focus**: Specially designed to answer about Atams and its services
-   **Admin Analytics**: Retrieve conversation history by date range for monitoring and analysis
-   **Rate Limiting**: Protection from spam requests (built-in via ATAMS framework)

## Technology Stack

-   **Framework**: FastAPI (via ATAMS Toolkit)
-   **AI Model**: GPT-4o-mini (via POE API)
-   **API Client**: OpenAI Python SDK
-   **Database**: PostgreSQL (required for conversation recording)
-   **ORM**: SQLAlchemy
-   **Validation**: Pydantic
-   **Server**: Uvicorn
-   **Architecture**: AURA (ATAMS Universal Rest API)

## Prerequisites

-   Python 3.10+
-   PostgreSQL (required for conversation recording)
-   POE API Key for GPT-4o-mini
-   Virtual environment (recommended)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/GratiaManullang03/atabot-lite-v3
    cd atabot-lite-v3
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

Create a `.env` file in the project root directory with the following variables:

```env
# Application Settings
APP_NAME=atabot_lite_v3
APP_VERSION=1.0.0
DEBUG=true

# Database Configuration (REQUIRED for conversation recording)
DATABASE_URL=postgresql://user:password@localhost:5432/atabot_lite_v3

# Database Connection Pool
DB_POOL_SIZE=3
DB_MAX_OVERFLOW=5
DB_POOL_RECYCLE=3600
DB_POOL_TIMEOUT=30
DB_POOL_PRE_PING=true

# POE API Configuration (REQUIRED for chatbot)
POE_API_KEY=your_poe_api_key_here
POE_MODEL=GPT-4o-mini

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
CORS_ALLOW_CREDENTIALS=true
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*

# Logging
LOGGING_ENABLED=true
LOG_LEVEL=INFO
LOG_TO_FILE=false

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

**Important:** Make sure the `.env` file is not committed to the repository. Use `.env.example` as a template.

## Running the Application

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Access Points:**

-   API Documentation (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
-   API Documentation (ReDoc): [http://localhost:8000/redoc](http://localhost:8000/redoc)
-   Health Check: [http://localhost:8000/health](http://localhost:8000/health)
-   Chat Endpoint: [http://localhost:8000/api/v1/chat](http://localhost:8000/api/v1/chat)
-   Admin Endpoint: [http://localhost:8000/api/v1/admin](http://localhost:8000/api/v1/admin)

## API Endpoints

Base URL: `/api/v1`

### Chat

**Base Path:** `/api/v1/chat`

#### POST /api/v1/chat/

Send a message to the chatbot and receive a response based on company data.

**Authorization:** None (public endpoint)

**Request Body:**

```json
{
    "message": "What is Atams?",
    "session_id": "optional-session-id"
}
```

**Request Fields:**

-   `message` (required): User message/question (string, 1–2000 characters)
-   `session_id` (optional): Session ID to track the conversation (string)

**Response:**

```json
{
    "message": "Atams is an innovative Indonesian technology startup focused on providing all-in-one digital solutions for SMEs...",
    "session_id": "ce222231-792e-4d57-9747-bc1ec2aae1ce",
    "timestamp": "2025-10-24T14:36:31.308561"
}
```

**Response Fields:**

-   `message`: The bot’s answer
-   `session_id`: Session ID for conversation tracking
-   `timestamp`: Response time (UTC)

**Example Requests:**

1. **First question (without session_id):**

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, who are you?"}'
```

2. **Follow-up question (with session_id):**

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your main services?", "session_id": "your-session-id-here"}'
```

3. **Follow-up question (bot will remember previous context):**

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "How much does it cost?", "session_id": "same-session-id"}'
```

**Response Behavior:**

-   All conversations are automatically recorded to the database in the background
-   Recording happens asynchronously and does not block the chat response
-   Each conversation includes metadata: IP address, user agent, referer, and origin

### Admin

**Base Path:** `/api/v1/admin`

#### POST /api/v1/admin/conversations/by-date

Retrieve all conversations within a specified date range for analytics and monitoring purposes.

**Authorization:** None (consider adding authentication in production)

**Request Body:**

```json
{
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
}
```

**Request Fields:**

-   `start_date` (required): Start date in YYYY-MM-DD format (inclusive)
-   `end_date` (required): End date in YYYY-MM-DD format (inclusive)

**Validation:**

-   `end_date` must not be before `start_date`
-   Maximum date range is 365 days (1 year)

**Response:**

```json
{
    "total_sessions": 10,
    "total_conversations": 25,
    "sessions": [
        {
            "us_session_id": "abc-123-def-456",
            "us_user_id": null,
            "us_created_at": "2025-01-15T10:00:00",
            "us_updated_at": "2025-01-15T10:30:00",
            "conversations": [
                {
                    "uc_id": 1,
                    "uc_question": "Apa itu Atams?",
                    "uc_answer": "Atams adalah startup teknologi Indonesia...",
                    "uc_timestamp": "2025-01-15T10:00:00",
                    "uc_metadata": {
                        "ip_address": "127.0.0.1",
                        "user_agent": "Mozilla/5.0...",
                        "origin": "https://example.com"
                    }
                },
                {
                    "uc_id": 2,
                    "uc_question": "Berapa harganya?",
                    "uc_answer": "Untuk informasi harga...",
                    "uc_timestamp": "2025-01-15T10:05:00",
                    "uc_metadata": {
                        "ip_address": "127.0.0.1",
                        "user_agent": "Mozilla/5.0..."
                    }
                }
            ]
        }
    ]
}
```

**Response Fields:**

-   `total_sessions`: Total number of unique sessions in the date range
-   `total_conversations`: Total number of conversations (questions + answers)
-   `sessions`: Array of session objects, ordered by creation date (newest first)
    -   `us_session_id`: Unique session identifier
    -   `us_user_id`: User ID (nullable, for future authentication)
    -   `us_created_at`: Session creation timestamp
    -   `us_updated_at`: Last activity timestamp
    -   `conversations`: Array of conversation objects within this session
        -   `uc_id`: Conversation ID
        -   `uc_question`: User question
        -   `uc_answer`: Bot answer
        -   `uc_timestamp`: When the conversation occurred
        -   `uc_metadata`: Request metadata (IP, user agent, etc.)

**Example Request:**

```bash
curl -X POST http://localhost:8000/api/v1/admin/conversations/by-date \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  }'
```

**Error Responses:**

```json
{
    "detail": "end_date (2025-01-01) tidak boleh lebih kecil dari start_date (2025-01-15). Pastikan start_date <= end_date."
}
```

```json
{
    "detail": "Date range terlalu besar (400 hari). Maksimal range adalah 365 hari (1 tahun) untuk performa optimal."
}
```

### Health Check

#### GET /health

Check application status and database connection.

**Response:**

```json
{
    "status": "healthy",
    "version": "1.0.0",
    "database": "connected"
}
```

## Architecture

### Data Flow

```
User Message → Chat Endpoint → Chatbot Service → POE API (GPT-4o-mini)
                     ↓                 ↓
              Record Question    Load data.json
              (Background)       Build System Prompt
                                 Session Memory Check
                                      ↓
                              Process AI Response
                                      ↓
Bot Response ← Format Response ← Record Answer (Background)
```

### Layered Architecture

```
API Layer (endpoints/)       → Business Logic (services/)       → External API (POE)
     ↓                                  ↓                               ↓
  FastAPI                       ChatbotService                   OpenAI Client
  Request Validation            Context Injection                GPT-4o-mini
  Response Format               Session Memory
     ↓                                  ↓
Background Tasks          ConversationRecorder → Repository → Database (PostgreSQL)
                                                                      ↓
                                                              user_sessions
                                                              user_conversations
```

### Session Memory

Session memory is stored **in-memory** with the structure:

-   **Max messages per session**: 10 recent messages
-   **Session TTL**: 30 minutes since last activity
-   **Cleanup**: Automatically removes expired sessions

### Conversation Recording

All conversations are automatically recorded to PostgreSQL for analytics and monitoring:

**Database Schema:**

-   **user_sessions** (schema: `atabot_v3`):

    -   `us_id`: Primary key (auto-increment)
    -   `us_session_id`: Unique session identifier (indexed)
    -   `us_user_id`: Optional user identifier (for future authentication)
    -   `us_created_at`: Session creation timestamp
    -   `us_updated_at`: Last activity timestamp

-   **user_conversations** (schema: `atabot_v3`):
    -   `uc_id`: Primary key (auto-increment)
    -   `uc_us_session_id`: Foreign key to user_sessions
    -   `uc_question`: User question text
    -   `uc_answer`: Bot answer text
    -   `uc_metadata`: JSONB field with request metadata (IP, user agent, referer, origin)
    -   `uc_timestamp`: Conversation timestamp
    -   Indexes: session_id, timestamp, composite (session_id + timestamp)

**Recording Flow:**

1. User sends message to `/api/v1/chat`
2. Question is recorded to database (background task, non-blocking)
3. Bot generates response via POE API
4. Answer is updated in database (background task, non-blocking)
5. Response is returned to user immediately (no waiting for DB operations)

**Benefits:**

-   **Non-blocking**: Database operations run in background threads
-   **Analytics**: Track user behavior and popular questions
-   **Monitoring**: Identify issues or common user concerns
-   **Improvements**: Analyze conversations to improve bot responses

## Business Logic

### Context Injection

The chatbot uses **context injection** to ensure accurate answers:

1. **Load Company Data**: Reads `data.json` on service initialization
2. **Build System Prompt**: Composes a prompt containing:

    - Bot identity & personality
    - Company information (name, description, tagline)
    - Brand meaning (ATAMS)
    - Services (12 products)
    - Technology stack
    - FAQ
    - Contact info
    - Rules (bot behavior policies)

3. **Inject Context**: Sends system prompt + conversation history + user message to GPT-4o-mini
4. **Enforce Rules**: The bot is instructed to:

    - Only answer questions about Atams
    - Introduce itself when asked
    - Politely decline out-of-context questions

### Session Memory Management

```python
# Session structure
{
  "session_id": {
    "messages": [
      {"role": "user", "content": "..."},
      {"role": "assistant", "content": "..."}
    ],
    "last_activity": datetime
  }
}
```

**Process:**

1. User sends a message with/without session_id
2. If no session_id, generate a new one
3. Load conversation history from memory
4. Append user message to history
5. Send to POE API with full context
6. Save response to session memory
7. Return response + session_id

### Bot Personality & Rules

The bot is configured in `data.json` → `bot_config`:

```json
{
    "name": "Atabot",
    "personality": "friendly, professional, and helpful",
    "language": "Indonesian",
    "max_response_length": 500,
    "temperature": 0.7,
    "rules": [
        "Always use polite and professional language",
        "If you don’t know the answer, say it honestly",
        "Provide accurate information based on available data",
        "Do not give information outside the company context"
    ]
}
```

## Security

### Public API

The `/api/v1/chat` endpoint is a **public endpoint** with no authentication to simplify landing page integration.

### Admin Endpoints

The `/api/v1/admin/*` endpoints currently have **no authentication**. In production:

-   Add authentication middleware (API keys, JWT, or OAuth)
-   Implement role-based access control (RBAC)
-   Restrict access to authorized users only
-   Consider IP whitelisting for additional security

### Rate Limiting

The ATAMS framework provides built-in rate limiting:

-   **Default**: 100 requests per 60 seconds
-   **Configurable**: Via `.env` (`RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW`)

### Environment Variables Security

**Critical secrets that must NOT be committed:**

-   `POE_API_KEY`: POE API key
-   `DATABASE_URL`: Database connection string

Always use `.env.example` as a template and copy it to `.env` for development.

### Session Memory Security

-   Session data stored in-memory (non-persistent)
-   Expired sessions auto-cleaned on each request
-   No sensitive user data stored

### Database Security

-   All conversations stored in PostgreSQL with proper schema (`atabot_v3`)
-   Foreign key constraints ensure data integrity
-   Metadata stored as JSONB for flexible structure
-   Consider data retention policies (auto-delete old conversations)
-   Ensure database credentials are never committed to version control

## Project Structure

```
atabot-lite-v3/
├── app/
│   ├── core/
│   │   ├── config.py              # Configuration (POE_API_KEY, POE_MODEL)
│   │   └── __init__.py
│   ├── db/                        # Database setup
│   │   ├── session.py             # Database session management
│   │   └── __init__.py
│   ├── models/                    # SQLAlchemy database models
│   │   ├── conversation.py        # UserSession, UserConversation models
│   │   └── __init__.py
│   ├── schemas/                   # Pydantic schemas
│   │   ├── chat.py                # ChatRequest, ChatResponse
│   │   ├── conversation.py        # ConversationsByDateRequest/Response, SessionDetail
│   │   ├── common.py              # Shared response schemas
│   │   └── __init__.py
│   ├── services/                  # Business logic layer
│   │   ├── chatbot_service.py     # ChatbotService, SessionMemory
│   │   ├── conversation_recorder.py  # ConversationRecorder (async background recording)
│   │   └── __init__.py
│   ├── repositories/              # Data access layer
│   │   ├── conversation_repository.py  # ConversationRepository (DB operations)
│   │   └── __init__.py
│   ├── api/
│   │   ├── deps.py                # Dependencies
│   │   └── v1/
│   │       ├── api.py             # Router aggregation
│   │       └── endpoints/
│   │           ├── chat.py        # Chat endpoint (with background recording)
│   │           ├── admin.py       # Admin endpoints (conversations analytics)
│   │           └── __init__.py
│   └── main.py                    # FastAPI application entry point
├── tests/                         # Test files (not yet implemented)
├── data.json                      # Company data & bot configuration (CORE FILE)
├── .env                           # Environment variables (DO NOT COMMIT!)
├── .env.example                   # Environment template
├── .gitignore
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Key Files Explanation

### `data.json`

This file is the **main data source** for the chatbot. Structure:

```json
{
    "bot_config": {
        /* bot configuration */
    },
    "company_data": {
        "company_name": "...",
        "services": [
            /* array of services */
        ],
        "faq": [
            /* array of FAQs */
        ],
        "contacts": {
            /* contact info */
        },
        "additional_info": {
            /* extra info */
        }
    }
}
```

**How to update data:**

1. Edit `data.json` with the latest information
2. Restart the application (the service reloads the data)
3. Test the chatbot to ensure data is updated

### `app/services/chatbot_service.py`

Core chatbot logic:

-   `SessionMemory`: Class for managing conversation history
-   `ChatbotService`: Main service class with methods:

    -   `_load_company_data()`: Loads `data.json`
    -   `_build_system_prompt()`: Builds context injection prompt
    -   `get_response()`: Processes user message & returns bot response

### `app/api/v1/endpoints/chat.py`

FastAPI endpoint for chat with background conversation recording:

1. Receives `ChatRequest`
2. Extracts metadata from request (IP, user agent, etc.)
3. Calls `chatbot_service.get_response()` to get bot response
4. Records conversation in background (non-blocking via BackgroundTasks)
5. Returns `ChatResponse` immediately

### `app/api/v1/endpoints/admin.py`

Admin endpoints for conversation analytics:

-   `POST /conversations/by-date`: Retrieve conversations within a date range
-   Returns sessions with their conversations, metadata, and statistics

### `app/models/conversation.py`

SQLAlchemy database models:

-   `UserSession`: Stores unique chat sessions
-   `UserConversation`: Stores individual Q&A pairs with metadata

Both models use schema `atabot_v3`.

### `app/services/conversation_recorder.py`

Async service for recording conversations to database:

-   `record_question()`: Records user question (returns conversation_id)
-   `record_answer()`: Updates conversation with bot answer
-   Runs in background threads to avoid blocking responses
-   Handles errors gracefully (logs but doesn't fail chat requests)

### `app/repositories/conversation_repository.py`

Data access layer for conversation database operations:

-   `upsert_session()`: Create or update session
-   `insert_conversation()`: Insert new Q&A record
-   `update_conversation_answer()`: Update with bot answer
-   `get_session_conversations()`: Get all conversations for a session
-   `get_sessions_by_date_range()`: Get sessions within date range
-   `get_conversations_by_session_ids()`: Batch fetch conversations

## Testing

### Manual Testing

Use Swagger UI for interactive testing:

```
http://localhost:8000/docs
```

Or use curl:

```bash
# Test 1: Bot introduction
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, who are you?"}'

# Test 2: About company
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Atams?"}'

# Test 3: Out of context (should reject)
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I cook fried rice?"}'

# Test 4: Session memory (follow-up question)
SESSION_ID="test-123"
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What are Atams’ main services?\", \"session_id\": \"$SESSION_ID\"}"

curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"How much does it cost?\", \"session_id\": \"$SESSION_ID\"}"

# Test 5: Admin - Get conversations by date
curl -X POST http://localhost:8000/api/v1/admin/conversations/by-date \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  }'
```

### Expected Behavior

-   The bot should introduce itself as "Atabot, the virtual assistant from Atams"
-   The bot should accurately answer questions about Atams
-   The bot should politely reject out-of-context questions
-   The bot should remember conversation context within the same session
-   All conversations should be recorded to the database automatically
-   Admin endpoint should return conversations with session grouping and metadata

## Deployment

### Environment-Specific Configuration

**Development:**

-   `DEBUG=true`
-   `LOG_LEVEL=INFO`
-   CORS allows specific origins only

**Production:**

-   `DEBUG=false`
-   `LOG_LEVEL=WARNING`
-   CORS restricted to production domain
-   Use `--workers 4` or more for Uvicorn

### Deployment Checklist

1. Set all environment variables in production
2. Ensure `POE_API_KEY` is valid and not expired
3. Update `CORS_ORIGINS` with the production domain
4. Set `DEBUG=false`
5. Enable rate limiting (`RATE_LIMIT_ENABLED=true`)
6. Monitor `/health` endpoint for health checks
7. **Configure PostgreSQL database with schema `atabot_v3`**
8. **Run database migrations to create tables** (`user_sessions`, `user_conversations`)
9. **Add authentication to `/api/v1/admin/*` endpoints**
10. **Set up database backup and retention policies**
11. **Monitor database performance and connection pool**

## Database Setup

### Creating the Schema and Tables

Before running the application, you need to set up the PostgreSQL database:

1. **Create the database** (if not exists):

```sql
CREATE DATABASE atabot_lite_v3;
```

2. **Create the schema**:

```sql
CREATE SCHEMA IF NOT EXISTS atabot_v3;
```

3. **Create the tables**:

You can use the provided SQL migration file or create tables manually:

```sql
-- User Sessions Table
CREATE TABLE atabot_v3.user_sessions (
    us_id SERIAL PRIMARY KEY,
    us_session_id VARCHAR(255) NOT NULL UNIQUE,
    us_user_id VARCHAR(100),
    us_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    us_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_us_session_id ON atabot_v3.user_sessions(us_session_id);

-- User Conversations Table
CREATE TABLE atabot_v3.user_conversations (
    uc_id SERIAL PRIMARY KEY,
    uc_us_session_id VARCHAR(255) NOT NULL,
    uc_question TEXT NOT NULL,
    uc_answer TEXT,
    uc_metadata JSONB,
    uc_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_uc_session
        FOREIGN KEY (uc_us_session_id)
        REFERENCES atabot_v3.user_sessions(us_session_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE INDEX idx_uc_us_session_id ON atabot_v3.user_conversations(uc_us_session_id);
CREATE INDEX idx_uc_timestamp ON atabot_v3.user_conversations(uc_timestamp);
CREATE INDEX idx_uc_session_timestamp ON atabot_v3.user_conversations(uc_us_session_id, uc_timestamp);
```

### Database Migrations

For production environments, consider using a migration tool like Alembic:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic (if not already done)
alembic init alembic

# Create a new migration
alembic revision -m "create conversation tables"

# Run migrations
alembic upgrade head
```

### Verifying Database Setup

After creating the tables, verify the setup:

```sql
-- Check if schema exists
SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'atabot_v3';

-- List all tables in the schema
SELECT table_name FROM information_schema.tables WHERE table_schema = 'atabot_v3';

-- Check table structure
\d atabot_v3.user_sessions
\d atabot_v3.user_conversations
```

## Customization

### Update Company Data

Edit [data.json](data.json) to update:

-   Company information
-   List of services/products
-   FAQ
-   Contact info
-   Bot personality & rules

### Adjust Bot Behavior

In [data.json](data.json) → `bot_config`:

```json
{
  "temperature": 0.7,           // 0.0 = strict, 1.0 = creative
  "max_response_length": 500,   // Max tokens per response
  "personality": "...",          // Bot personality description
  "rules": [...]                 // Bot behavior rules
}
```

### Session Configuration

In [app/services/chatbot_service.py](app/services/chatbot_service.py) → `SessionMemory`:

```python
SessionMemory(
    max_messages_per_session=10,  # Number of messages stored
    session_ttl_minutes=30         # Session TTL (minutes)
)
```

## License

Proprietary – Atams Indonesia
