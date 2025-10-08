---
title: Google Search API Service
description: High-performance asynchronous SerpAPI wrapper with aggregated search results, deduplication, and bulk operations support
order: 6
category: API Service
tags: [google-search, serpapi, search, fastapi, async]
---

# Google Search API Service

This project is a high-performance, asynchronous FastAPI application that serves as a robust wrapper around the SerpApi Google Search service. It is designed to provide aggregated and deduplicated search results by intelligently querying multiple variations of a search term.

## Features

  - **Fast & Asynchronous**: Built with FastAPI and `asyncio` for high-performance, non-blocking I/O.
  - **Aggregated Search Results**: Automatically performs searches on multiple query variations (e.g., "item in location", "item suppliers in location") to gather a comprehensive list of results.
  - **Deduplication**: Intelligently removes duplicate results based on their URL, providing a clean and unique list.
  - **Dynamic Configuration**: Easily configure the application, including API keys and database connections, using a `.env` file.
  - **Scalable Architecture**: Organized into a clean and scalable project structure with services, schemas, and repositories.
  - **Bulk Operations**: Includes a `/bulk-search` endpoint to perform multiple search operations in a single API call.
  - **Health Check**: A `/health` endpoint to monitor the status of the database and other connected services.

## Prerequisites

  - Python 3.10+
  - PostgreSQL Database
  - An API Key from [SerpApi](https://serpapi.com/)

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/GratiaManullang03/google-search.git
    cd google-search
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The application is configured using environment variables. Create a file named `.env` in the root directory of the project and add the following variables:

```env
# Application Settings
APP_NAME="Google Search API"
APP_VERSION="1.0.0"
DEBUG=True

# Database URL
# Example: postgresql+psycopg2://user:password@host:port/dbname
DATABASE_URL="postgresql+psycopg2://your_db_user:your_db_password@localhost:5432/your_db_name"

# External API Keys
SERPAPI_API_KEY="your_serpapi_api_key_here"

# JWT Configuration (if authentication is needed)
SECRET_KEY="your_super_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

To run the application, use `uvicorn`. From the root directory:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload
```

The API will be available at `http://localhost:8081`. You can access the interactive documentation at `http://localhost:8081/docs`.

## API Endpoints

### Health Check

  - **GET** `/api/v1/health`
  - **Description**: Checks the connection status of the database and Redis (if configured).
  - **Response**:
    ```json
    {
      "success": true,
      "message": "Database: healthy, Redis: not configured"
    }
    ```

---

### Perform a Search

  - **POST** `/api/v1/serpapi/search`
  - **Description**: Performs a search using multiple query variations, aggregates the results, and returns a unique list.
  - **Request Body**:
    ```json
    {
      "item": "clove",
      "location": "Mumbai, Maharashtra, India",
      "num_results": 100,
      "search_variations": true
    }
    ```
  - **Parameters**:
      - `item` (str): The product or item to search for.
      - `location` (str): The geographical location for the search.
      - `num_results` (int, optional): The desired number of results per query variation. Min: 10, Max: 100. Defaults to 10.
      - `search_variations` (bool, optional): If `true`, the service will query multiple variations of the search term. Defaults to `true`.
  - **Success Response** (`200 OK`):
    ```json
    {
      "success": true,
      "message": "Search completed successfully",
      "data": {
        "query": "clove in Mumbai, Maharashtra, India",
        "location": "Mumbai, Maharashtra, India",
        "total_results": 50,
        "results": [
          {
            "title": "Top Clove Wholesalers in Mumbai near me",
            "link": "https://www.justdial.com/Mumbai/Clove-Wholesalers/nct-11301685",
            "snippet": "Popular Clove Wholesalers in Mumbai · A1 Dry Fruit · Shah Gabhrubhai Uttamchand..."
          }
          // ... more results
        ]
      }
    }
    ```

---

### Perform a Bulk Search

  - **POST** `/api/v1/serpapi/bulk-search`
  - **Description**: Executes multiple search requests in parallel.
  - **Request Body**:
    ```json
    {
      "searches": [
        {
          "item": "rice",
          "location": "Hanoi, Vietnam",
          "num_results": 20
        },
        {
          "item": "coffee",
          "location": "Jakarta, Indonesia",
          "num_results": 20
        }
      ]
    }
    ```
  - **Success Response** (`200 OK`):
    ```json
    {
        "success": true,
        "message": "Completed 2 searches",
        "data": [
            {
                "query": "rice in Hanoi, Vietnam",
                "location": "Hanoi, Vietnam",
                "total_results": 18,
                "results": [
                    // ... rice search results
                ]
            },
            {
                "query": "coffee in Jakarta, Indonesia",
                "location": "Jakarta, Indonesia",
                "total_results": 20,
                "results": [
                    // ... coffee search results
                ]
            }
        ]
    }
    ```