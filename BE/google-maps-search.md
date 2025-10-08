---
title: Google Maps Search API
description: Find businesses on Google Maps with no website, high reviews, and phone contact using SerpAPI integration with advanced filtering
order: 7
category: API Service
tags: [google-maps, serpapi, business-search, fastapi, lead-generation]
---

# Google Maps Search API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SerpAPI](https://img.shields.io/badge/SerpAPI-Integration-blue)](https://serpapi.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://docs.docker.com/compose/)

A **Google Maps Search API** to find businesses/SMEs on Google Maps that **have no website**, with **high reviews** and **phone contact**.

Built with **FastAPI**, **SerpAPI**, and **Clean Architecture** principles.

---

## 📑 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
  - [Setup with Docker](#setup-with-docker)
  - [Manual Setup (Development)](#manual-setup-development)
- [API Documentation](#-api-documentation)
- [API Endpoints](#-api-endpoints)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Example Usage](#-example-usage)

---

## ✨ Features

- 🔍 **Google Maps Search** via SerpAPI
- 🚫 **Filter businesses without website** - only capture businesses with no website
- ⭐ **High reviews filter** - only businesses with more than 100 reviews
- 📞 **Phone contact required** - only businesses with phone numbers
- ⚡ **Async & Parallel Processing** - searches performed in parallel for optimal performance
- 📦 **Bulk Search Support** - search multiple locations/keywords at once (max 10)
- 🎯 **Clean Architecture** - maintainable and scalable

---

## 🚀 Quick Start

### Prerequisites
- Python **3.11+**
- SerpAPI API Key ([Get it here](https://serpapi.com/))
- Docker & Docker Compose (optional)

---

### Setup with Docker

1. Clone repository
```bash
git clone https://github.com/GratiaManullang03/google-maps-search.git
cd google-maps-search
```

2. Copy environment variables
```bash
cp .env.example .env
# Edit .env and add your SERPAPI_API_KEY
```

3. Run with Docker Compose
```bash
docker compose up -d
```

👉 API will be available at **[http://localhost:8000](http://localhost:8000)**

---

### Manual Setup (Development)

1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Setup environment variables

Create `.env` file:
```env
APP_NAME="Google Maps Search API"
APP_VERSION="1.0.0"
DEBUG=True

SERPAPI_API_KEY=your-serpapi-key-here
```

4. Run the app
```bash
uvicorn app.main:app --reload --port 8000
```

---

## 📚 API Documentation

* Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔌 API Endpoints

### 1. Single Search

**POST** `/api/v1/gmaps/search`

Search businesses on Google Maps without website, with reviews > 100, and with phone contact.

**Request Body:**
```json
{
  "query": "restaurant",
  "location": "Jakarta, Indonesia",
  "num_results": 20
}
```

**Response:**
```json
{
  "success": true,
  "message": "Google Maps search completed successfully",
  "data": {
    "query": "restaurant",
    "location": "Jakarta, Indonesia",
    "total_results": 5,
    "results": [
      {
        "title": "Warung Makan Bu Tini",
        "address": "Jl. Sudirman No. 123, Jakarta",
        "phone": "+62812345678",
        "rating": 4.5,
        "reviews": 120,
        "type": "Restaurant"
      }
    ]
  }
}
```

---

### 2. Bulk Search

**POST** `/api/v1/gmaps/bulk-search`

Perform multiple searches in parallel (max 10 searches).

**Request Body:**
```json
{
  "searches": [
    {
      "query": "restaurant",
      "location": "Jakarta, Indonesia",
      "num_results": 20
    },
    {
      "query": "hotel",
      "location": "Bali, Indonesia",
      "num_results": 20
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Completed 2 Google Maps searches",
  "data": [
    {
      "query": "restaurant",
      "location": "Jakarta, Indonesia",
      "total_results": 5,
      "results": [...]
    },
    {
      "query": "hotel",
      "location": "Bali, Indonesia",
      "total_results": 3,
      "results": [...]
    }
  ]
}
```

---

### 3. Health Check

**GET** `/api/v1/health`

Check if the API is running.

**Response:**
```json
{
  "success": true,
  "message": "Service is healthy"
}
```

---

## 🔧 Configuration

### SerpAPI Setup

1. Sign up at [https://serpapi.com/](https://serpapi.com/)
2. Get your API key from dashboard
3. Add to `.env`:
```env
SERPAPI_API_KEY=your_api_key_here
```

### Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | string | required | Search query (e.g., "restaurant", "hotel") |
| location | string | required | Location (e.g., "Jakarta, Indonesia") |
| num_results | integer | 20 | Number of results (10-100) |

---

## 📁 Project Structure

```
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── health.py      # Health check endpoint
│       │   └── gmaps.py       # Google Maps endpoints
│       └── api.py             # Router aggregator
├── core/
│   └── config.py              # Configuration & settings
├── schemas/
│   ├── common.py              # Common schemas
│   └── gmaps.py               # Google Maps schemas
├── services/
│   └── gmaps.py               # Google Maps business logic
└── main.py                    # Application entry point
```

---

## 🔄 How It Works

1. **Client sends request** with query and location
2. **API calls SerpAPI** for Google Maps search
3. **Filter results** - only businesses without website, reviews > 100, and with phone
4. **Return filtered results** with contact information

### Filter Logic:
```python
# Only businesses WITHOUT website, WITH phone, and reviews > 100
filtered_results = [
    place for place in local_results
    if not place.get("website")
    and place.get("reviews", 0) > 100
    and place.get("phone")
]
```

---

## 💡 Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/v1/gmaps/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "restaurant",
    "location": "Jakarta, Indonesia",
    "num_results": 20
  }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/api/v1/gmaps/search"
payload = {
    "query": "restaurant",
    "location": "Jakarta, Indonesia",
    "num_results": 20
}

response = requests.post(url, json=payload)
print(response.json())
```

### Using JavaScript fetch

```javascript
fetch('http://localhost:8000/api/v1/gmaps/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    query: 'restaurant',
    location: 'Jakarta, Indonesia',
    num_results: 20
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 🚢 Deployment

### Production with Docker

```bash
docker compose up -d --build
```

### Environment Variables (Production)

```env
APP_NAME="Google Maps Search API"
APP_VERSION="1.0.0"
DEBUG=False

SERPAPI_API_KEY=your-serpapi-key
```

---

## 📝 Notes

- ⚡ **Async processing** for optimal performance
- 🚫 **Auto-filter** businesses with website
- ⭐ Only returns businesses with **reviews > 100**
- 📞 Only returns businesses with **phone contact**
- ⏱️ Request timeout: 30 seconds per search
- 📊 Bulk search: maximum 10 searches per request

---

## 🔐 Security Notes

- Never commit `.env` file to repository
- Protect `SERPAPI_API_KEY` - don't expose to public
- Implement rate limiting for production

---

## 📄 License

This project is proprietary and confidential.

---

🔥 Ready to find businesses without website, high reviews, and phone contacts!
