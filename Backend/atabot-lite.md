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

* [Key Features](#key-features)
* [Technology Stack](#technology-stack)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Configuration](#configuration)
* [Running the Application](#running-the-application)
* [API Endpoints](#api-endpoints)
* [Architecture](#architecture)
* [Business Logic](#business-logic)
* [Security](#security)
* [Project Structure](#project-structure)

## Key Features

* **Context-Aware Responses**: Answers questions based solely on `data.json`; rejects out-of-context questions
* **Session Memory**: Tracks conversation history per session for follow-up questions
* **Self-Introduction**: The bot can introduce itself when asked
* **GPT-4o-mini Integration**: Uses the POE API to generate natural responses
* **Company Profile Focus**: Specially designed to answer about Atams and its services
* **Rate Limiting**: Protection from spam requests (built-in via ATAMS framework)

## Technology Stack

* **Framework**: FastAPI (via ATAMS Toolkit)
* **AI Model**: GPT-4o-mini (via POE API)
* **API Client**: OpenAI Python SDK
* **Database**: PostgreSQL (optional, for framework)
* **Validation**: Pydantic
* **Server**: Uvicorn
* **Architecture**: AURA (ATAMS Universal Rest API)

## Prerequisites

* Python 3.10+
* PostgreSQL (optional, for other ATAMS features)
* POE API Key for GPT-4o-mini
* Virtual environment (recommended)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/[username]/atabot-lite-v3.git
   cd atabot-lite-v3
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   * Linux/Mac:

     ```bash
     source venv/bin/activate
     ```
   * Windows:

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

# Database Configuration (required by ATAMS framework)
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

* API Documentation (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)
* API Documentation (ReDoc): [http://localhost:8000/redoc](http://localhost:8000/redoc)
* Health Check: [http://localhost:8000/health](http://localhost:8000/health)
* Chat Endpoint: [http://localhost:8000/api/v1/chat](http://localhost:8000/api/v1/chat)

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

* `message` (required): User message/question (string, 1–2000 characters)
* `session_id` (optional): Session ID to track the conversation (string)

**Response:**

```json
{
  "message": "Atams is an innovative Indonesian technology startup focused on providing all-in-one digital solutions for SMEs...",
  "session_id": "ce222231-792e-4d57-9747-bc1ec2aae1ce",
  "timestamp": "2025-10-24T14:36:31.308561"
}
```

**Response Fields:**

* `message`: The bot’s answer
* `session_id`: Session ID for conversation tracking
* `timestamp`: Response time (UTC)

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
                                      ↓
                               Load data.json
                               Build System Prompt
                               Session Memory Check
                                      ↓
Bot Response ← Format Response ← Process AI Response
```

### Layered Architecture

```
API Layer (endpoints/)       → Business Logic (services/)       → External API (POE)
     ↓                                  ↓
  FastAPI                       ChatbotService                   OpenAI Client
  Request Validation            Context Injection                GPT-4o-mini
  Response Format               Session Memory
```

### Session Memory

Session memory is stored **in-memory** with the structure:

* **Max messages per session**: 10 recent messages
* **Session TTL**: 30 minutes since last activity
* **Cleanup**: Automatically removes expired sessions

## Business Logic

### Context Injection

The chatbot uses **context injection** to ensure accurate answers:

1. **Load Company Data**: Reads `data.json` on service initialization
2. **Build System Prompt**: Composes a prompt containing:

   * Bot identity & personality
   * Company information (name, description, tagline)
   * Brand meaning (ATAMS)
   * Services (12 products)
   * Technology stack
   * FAQ
   * Contact info
   * Rules (bot behavior policies)
3. **Inject Context**: Sends system prompt + conversation history + user message to GPT-4o-mini
4. **Enforce Rules**: The bot is instructed to:

   * Only answer questions about Atams
   * Introduce itself when asked
   * Politely decline out-of-context questions

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

### Rate Limiting

The ATAMS framework provides built-in rate limiting:

* **Default**: 100 requests per 60 seconds
* **Configurable**: Via `.env` (`RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW`)

### Environment Variables Security

**Critical secrets that must NOT be committed:**

* `POE_API_KEY`: POE API key
* `DATABASE_URL`: Database connection string

Always use `.env.example` as a template and copy it to `.env` for development.

### Session Memory Security

* Session data stored in-memory (non-persistent)
* Expired sessions auto-cleaned on each request
* No sensitive user data stored

## Project Structure

```
atabot-lite-v3/
├── app/
│   ├── core/
│   │   ├── config.py              # Configuration (added: POE_API_KEY, POE_MODEL)
│   │   └── __init__.py
│   ├── db/                        # Database setup (from ATAMS framework)
│   │   ├── session.py
│   │   └── __init__.py
│   ├── models/                    # (empty – no DB models for chatbot)
│   │   └── __init__.py
│   ├── schemas/                   # Pydantic schemas
│   │   ├── chat.py                # ChatRequest, ChatResponse
│   │   ├── common.py              # Shared response schemas
│   │   └── __init__.py
│   ├── services/                  # Business logic layer
│   │   ├── chatbot_service.py     # ChatbotService, SessionMemory
│   │   └── __init__.py
│   ├── api/
│   │   ├── deps.py                # Dependencies (from ATAMS)
│   │   └── v1/
│   │       ├── api.py             # Router aggregation
│   │       └── endpoints/
│   │           ├── chat.py        # Chat endpoint
│   │           └── __init__.py
│   ├── repositories/              # (empty – no data access layer needed)
│   │   └── __init__.py
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
  "bot_config": { /* bot configuration */ },
  "company_data": {
    "company_name": "...",
    "services": [ /* array of services */ ],
    "faq": [ /* array of FAQs */ ],
    "contacts": { /* contact info */ },
    "additional_info": { /* extra info */ }
  }
}
```

**How to update data:**

1. Edit `data.json` with the latest information
2. Restart the application (the service reloads the data)
3. Test the chatbot to ensure data is updated

### `app/services/chatbot_service.py`

Core chatbot logic:

* `SessionMemory`: Class for managing conversation history
* `ChatbotService`: Main service class with methods:

  * `_load_company_data()`: Loads `data.json`
  * `_build_system_prompt()`: Builds context injection prompt
  * `get_response()`: Processes user message & returns bot response

### `app/api/v1/endpoints/chat.py`

FastAPI endpoint for chat. Simple POST endpoint that:

1. Receives `ChatRequest`
2. Calls `chatbot_service.get_response()`
3. Returns `ChatResponse`

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
```

### Expected Behavior

* The bot should introduce itself as “Atabot, the virtual assistant from Atams”
* The bot should accurately answer questions about Atams
* The bot should politely reject out-of-context questions
* The bot should remember conversation context within the same session

## Deployment

### Environment-Specific Configuration

**Development:**

* `DEBUG=true`
* `LOG_LEVEL=INFO`
* CORS allows specific origins only

**Production:**

* `DEBUG=false`
* `LOG_LEVEL=WARNING`
* CORS restricted to production domain
* Use `--workers 4` or more for Uvicorn

### Deployment Checklist

1. Set all environment variables in production
2. Ensure `POE_API_KEY` is valid and not expired
3. Update `CORS_ORIGINS` with the production domain
4. Set `DEBUG=false`
5. Enable rate limiting (`RATE_LIMIT_ENABLED=true`)
6. Monitor `/health` endpoint for health checks

## Customization

### Update Company Data

Edit [data.json](data.json) to update:

* Company information
* List of services/products
* FAQ
* Contact info
* Bot personality & rules

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

## Support

For questions or issues:

* Email: [info@atamsindonesia.com](mailto:info@atamsindonesia.com)
* Documentation: [ATAMS Docs](https://docs.atamsindonesia.com)
* Company Website: [https://atamsindonesia.com](https://atamsindonesia.com)

## License

Proprietary – Atams Indonesia
