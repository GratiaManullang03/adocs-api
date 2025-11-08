---
title: Email Blast API
description: Powerful email campaign management system with bulk sending, click tracking, campaign statistics, and background processing
order: 5
category: API Service
tags: [email-blast, smtp, campaign, tracking, fastapi, sqlalchemy]
---

# Email Blast API

## Overview

This is a powerful and scalable Email Blast API built with **FastAPI** and **SQLAlchemy**. It's designed to manage email campaigns, send bulk and single emails, and track email engagement with features like click tracking. This API is ideal for applications that require robust email functionalities, such as newsletters, notifications, and marketing campaigns.

---

## Features

-   **📨 Bulk Email Campaigns:** Send thousands of emails in the background without blocking the API.
-   **📧 Single Email Sending:** Easily send customized single emails.
-   **📈 Campaign Statistics:** Track the performance of your email campaigns with detailed statistics, including total emails sent, failed, and clicked.
-   **🖱️ Click Tracking:** Monitor user engagement by tracking clicks on the links in your emails.
-   **📋 All Campaigns List:** Get a paginated list of all your email campaigns.
-   **ጤ Health Check Endpoint:** A health check endpoint to monitor the status of the database and Redis connections.

---

## Prerequisites

-   **Python 3.10+**
-   **Docker and Docker Compose**
-   **PostgreSQL Database**
-   **Redis** (Optional, for caching and background tasks)

---

## Getting Started

### 1. Clone the repository:

```bash
git clone https://github.com/GratiaManullang03/email-blast.git
cd email-blast
```

### 2\. Create and configure the .env file:

Create a `.env` file in the root of the project and add the following environment variables:

```env
# Application
APP_NAME=EMAIL_BLAST
APP_VERSION=1.0.0
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@db:5432/atabot

# Redis (optional)
REDIS_URL=redis://redis:6379/0

# JWT (will be adjusted per client)
SECRET_KEY=your-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration
MAIL_USERNAME=noreply@atamsindonesia.com
MAIL_PASSWORD=n0r3ply
MAIL_FROM=noreply@atamsindonesia.com
MAIL_FROM_NAME=Atams Indonesia (Do Not Reply)
MAIL_PORT=465
MAIL_SERVER=rumahweb.net
MAIL_USE_TLS=False
MAIL_USE_SSL=True

# Frontend URL for tracking links
FRONTEND_URL=http://localhost:3000
```

### 3\. Build and run with Docker Compose:

```bash
docker-compose up -d --build
```

### 4\. The API will be available at http://localhost:8000.

---

## API Endpoints

### Health

-   `GET /health`: Checks the health of the database and Redis connections.

### Emails

-   `POST /emails/bulk`: Sends a bulk email campaign to multiple recipients.
-   `POST /emails/single`: Sends a single customized email.
-   `GET /emails/track/{tracking_id}`: Tracks an email click and redirects to a landing page.
-   `POST /emails/track/{tracking_id}`: API endpoint to track an email click.
-   `GET /emails/campaigns`: Gets a list of email campaigns with pagination.
-   `GET /emails/campaigns/{campaign_id}/stats`: Gets statistics for a specific campaign.
-   `GET /emails/stats/overview`: Gets an overview of all email statistics.

### Interactive API Documentation

Once the application is running, you can access the interactive API documentation at:

-   **Swagger UI:** `http://localhost:8000/docs`
-   **ReDoc:** `http://localhost:8000/redoc`
