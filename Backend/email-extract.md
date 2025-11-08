---
title: Email Extractor
description: Simple FastAPI application that automatically extracts email addresses from any webpage using Beautiful Soup
order: 10
category: Utility Service
tags: [email-extractor, web-scraping, beautifulsoup, fastapi, utility]
---

# Email Extractor

Email Extractor is a **FastAPI** application that extracts email addresses from a web page. Simply provide a URL, and the application will scan the page for email addresses and return them to you.

---

## Features

-   **Email Extraction:** Automatically extracts email addresses from any given webpage.
-   **Simple API:** An easy-to-use **API** endpoint to integrate with other applications.
-   **Results Storage:** Saves the scraping results for future reference.

---

## Technology Stack

-   [**FastAPI**](https://fastapi.tiangolo.com/): A modern, high-performance web framework for building APIs with Python.
-   [**Beautiful Soup**](https://www.crummy.com/software/BeautifulSoup/): A Python library for pulling data out of HTML and XML files.
-   [**SQLAlchemy**](https://www.sqlalchemy.org/): The Python SQL Toolkit and Object Relational Mapper.
-   [**Pydantic**](https://pydantic-docs.helpmanual.io/): Data validation and settings management using Python type annotations.

---

## Getting Started

### Prerequisites

-   Python 3.10+
-   Pip

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/GratiaManullang03/email-extract.git
    cd email-extract
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Start the Uvicorn server:**

    ```bash
    uvicorn app.main:app --reload
    ```

2.  **Open your browser and navigate to [http://127.0.0.1:8000](https://www.google.com/search?q=http://127.0.0.1:8000)**

---

## API Usage

### Extract Emails

-   **URL:** `/api/v1/extract-emails/`
-   **Method:** `POST`
-   **Request Body:**
    ```json
    {
        "url": "https://example.com"
    }
    ```
-   **Success Response:**
    ```json
    {
        "emails": ["email1@example.com", "email2@example.com"]
    }
    ```

### Get Health Status

-   **URL:** `/api/v1/health/`
-   **Method:** `GET`
-   **Success Response:**
    ```json
    {
        "status": "ok"
    }
    ```
