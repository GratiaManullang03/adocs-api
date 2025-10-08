---
title: AURA - Location Autocomplete API
description: Lightweight asynchronous location autocomplete API powered by Geoapify with real-time city suggestions
order: 11
category: Utility Service
tags: [autocomplete, location, geoapify, fastapi, async]
---

# AURA - Location Autocomplete API

AURA is a lightweight, asynchronous API built with FastAPI that provides location autocomplete suggestions. It leverages an external geolocation service (Geoapify) to deliver fast and relevant city search results, making it ideal for applications requiring a location search feature.

## Features

  - **Fast Autocomplete**: Provides real-time city suggestions as the user types.
  - **Asynchronous**: Built on FastAPI and `httpx` for high-performance, non-blocking I/O.
  - **External Service Integration**: Uses the Geoapify Geocoding API to fetch location data.
  - **Clean Architecture**: Organized into logical layers (API, services, schemas) for better maintainability.
  - **Configuration Management**: Centralized configuration using Pydantic's `BaseSettings`.
  - **Health Check**: Includes a `/health` endpoint to monitor the status of the API and its database connection.

## Project Structure

The project follows a clean and scalable structure:

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── location.py  # Autocomplete endpoint logic
│   │   │   └── health.py    # Health check endpoint
│   │   └── api.py           # Main v1 API router
│   └── deps.py              # Dependencies (e.g., auth, DB session)
├── core/
│   ├── config.py            # Application settings
│   ├── http_client.py       # Async HTTP client for external APIs
│   └── exceptions.py        # Custom exception classes
├── db/
│   ├── base.py              # Declarative base for models
│   └── session.py           # Database session management
├── schemas/
│   ├── location.py          # Pydantic schemas for location data
│   └── common.py            # Common response schemas
├── services/
│   └── location.py          # Business logic for location features
└── main.py                  # Main application entrypoint
```

## API Endpoints

### Health Check

  - **GET `/api/v1/health/`**
      - Checks the health of the application, including database and Redis connectivity.
      - **Response:**
        ```json
        {
          "success": true,
          "message": "Database: healthy, Redis: not configured"
        }
        ```

### Location Autocomplete

  - **GET `/api/v1/locations/autocomplete`**
      - Provides a list of city suggestions based on the query string.
      - **Query Parameters:**
          - `q` (str): The search query (minimum 2 characters).
          - `limit` (int, optional): The maximum number of results to return. Defaults to 5, max 20.
      - **Response:**
        ```json
        {
          "success": true,
          "message": "Autocomplete results retrieved",
          "data": [
            {
              "formatted": "Liverpool, England, United Kingdom",
              "city": "Liverpool",
              "state": "England",
              "country": "United Kingdom",
              "country_code": "gb"
            }
          ],
          "total": 1
        }
        ```

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**
    Create a `.env` file in the root directory and add the necessary environment variables. See the Configuration section below.

4.  **Run the application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    The application will be available at `http://127.0.0.1:8000`.

## Configuration

The application requires the following environment variables, which should be placed in a `.env` file in the root directory:

```ini
# .env file

# Application
APP_NAME=ATAMS Backend
APP_VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/atabot

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# JWT (akan disesuaikan per client)
SECRET_KEY=your-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# External APIs
GEOAPIFY_API_KEY=your-geoapify-api-key
GEOAPIFY_BASE_URL=https://api.geoapify.com/v1
```