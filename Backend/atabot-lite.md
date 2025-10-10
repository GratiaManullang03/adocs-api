---
title: ATABOT-Lite - Lightweight Adaptive Chatbot
description: Lightweight adaptive chatbot backend with hybrid search, multi-language support, and LLM integration optimized for business landing pages
order: 4
category: AI Service
tags: [atabot-lite, chatbot, nlp, hybrid-search, fastapi, poe-api]
---

# ATABOT-Lite

## 🎯 Overview

**ATABOT-Lite** is a lightweight, adaptive chatbot backend optimized for **company landing pages** and business websites. Built with FastAPI, it provides intelligent chat capabilities through **hybrid search technology** (keyword + semantic) and **multi-language support**, making it perfect for customer service and lead generation.

## ✨ Key Features

### 🤖 **Smart AI Integration**
- **LLM Integration**: Powered by Poe API for intelligent responses
- **Hybrid Search**: Combines keyword matching + semantic search for optimal performance
- **Enhanced NLP**: Advanced intent recognition and entity extraction
- **Multi-Language Support**: Indonesian, English, and mixed language detection

### 🚀 **Performance Optimized**
- **Lightweight**: < 400KB codebase, perfect for serverless deployment
- **Fast Response**: < 2 seconds for 90% of queries
- **Smart Caching**: Session-based conversation memory
- **Cost Efficient**: Minimal API calls through intelligent routing

### 🏗️ **Business Adaptive**
- **Universal Business Support**: Works for ANY industry (restaurant, healthcare, tech, retail, etc.)
- **Dynamic Data Structure**: Automatically adapts to different service categories
- **Flexible FAQ System**: Supports unlimited business-specific Q&A
- **Custom Bot Personality**: Configurable tone and behavior per company

### 🛡️ **Production Ready**
- **Rate Limiting**: Configurable request limits with headers
- **Security Middleware**: XSS protection and security headers
- **Error Handling**: Graceful degradation when APIs unavailable
- **Session Management**: Automatic cleanup and memory optimization

## 🏗️ Architecture

### **Clean Architecture Layers:**
```
┌─────────────────────────────────────┐
│           API Endpoints             │  ← FastAPI Routes
├─────────────────────────────────────┤
│          Middleware Layer           │  ← Security, Rate Limiting
├─────────────────────────────────────┤
│         Services Layer              │  ← Business Logic
│  • ChatbotService (Core Logic)      │
│  • NLPService (Language Processing) │
│  • LLMService (AI Integration)      │
│  • EmbeddingService (Vector Search) │
├─────────────────────────────────────┤
│         Core Layer                  │  ← Configuration, Utils
├─────────────────────────────────────┤
│    External APIs / Data Sources     │  ← Poe, Voyage, data.json
└─────────────────────────────────────┘
```

### **Hybrid Search Flow:**
```
User Query → NLP Processing → Intent Detection
     ↓
Keyword Search (Fast) → Results >= 3? → Return Results
     ↓ (if < 3 results)
Semantic Search (AI) → Combine & Deduplicate → Return Top Results
```

## 🛠️ Technologies

- **Backend**: FastAPI, Python 3.11+
- **AI**: Poe API (LLM), Voyage AI (Embeddings)
- **NLP**: Custom lightweight processing
- **Architecture**: Clean Architecture, Dependency Injection
- **Deployment**: Vercel, Docker, or traditional hosting

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone repository
git clone <your-repo-url>
cd atabot-lite

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configuration**
Create `.env` file:
```env
# Required for full functionality
POE_API_KEY=your_poe_api_key
VOYAGE_API_KEY=your_voyage_api_key  # Optional for semantic search

# Models (optional, has defaults)
POE_MODEL=ChatGPT-3.5-Turbo
VOYAGE_MODEL=voyage-3.5-lite
```

### 3. **Configure Your Business Data**
Edit `data.json` with your company information:

```json
{
  "bot_config": {
    "name": "YourBot",
    "personality": "professional and helpful",
    "language": "Indonesian",
    "max_response_length": 500,
    "temperature": 0.7,
    "rules": [
      "Always be polite and professional",
      "Only provide information based on company data",
      "If unsure, direct to customer service"
    ]
  },
  "company_data": {
    "company_name": "Your Company",
    "description": "Your company description",
    "services": [
      {
        "category": "Main Services",
        "name": "Service Name",
        "description": "Service description",
        "price": "Contact for pricing",
        "features": ["Feature 1", "Feature 2"]
      }
    ],
    "faq": [
      {
        "question": "Common customer question?",
        "answer": "Your helpful answer here."
      }
    ],
    "contacts": {
      "whatsapp": "+62-XXX-XXXX-XXXX",
      "email": "contact@yourcompany.com",
      "address": "Your business address"
    }
  }
}
```

### 4. **Run Application**
```bash
# Development
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Access at: `http://localhost:8000`

## 📚 API Documentation

### **Core Endpoints**

#### **💬 Chat API**
- `POST /api/v1/chat/message` - Send message, get complete response
- `POST /api/v1/chat/message/stream` - Get streaming response (SSE)
- `GET /api/v1/chat/session/create` - Create new chat session
- `GET /api/v1/chat/history/{session_id}` - Get conversation history
- `DELETE /api/v1/chat/session/{session_id}` - Clear session

#### **❤️ System Health**
- `GET /api/v1/health` - Health check
- `GET /docs` - Swagger documentation
- `GET /` - Demo widget page

### **Request/Response Examples**

**Send Message:**
```bash
curl -X POST "http://localhost:8000/api/v1/chat/message" \
     -H "Content-Type: application/json" \
     -d '{
       "message": "Halo, apa layanan yang tersedia?",
       "session_id": "session123"
     }'
```

**Response:**
```json
{
  "success": true,
  "message": "Message processed successfully",
  "data": {
    "response": "Halo! Kami menyediakan berbagai layanan...",
    "session_id": "session123",
    "timestamp": "2024-01-01T12:00:00Z"
  }
}
```

## 🎨 Business Examples

The system automatically adapts to ANY business type. See `/examples/` folder for:

- **Restaurant** (`restaurant_data.json`) - Menu, prices, delivery info
- **Healthcare** (`healthcare_data.json`) - Services, doctors, BPJS info
- **Tech Services** (`tech_services_data.json`) - Development, pricing, timelines

Simply replace `data.json` with your business data structure!

## 🚀 Deployment

### **Vercel (Recommended for Serverless)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### **Docker**
```bash
# Build image
docker build -t atabot-lite .

# Run container
docker run -p 8000:8000 --env-file .env atabot-lite
```

### **Traditional Hosting**
```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🔧 Configuration Options

### **Environment Variables**
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `POE_API_KEY` | Poe API key for LLM | Optional* | None |
| `POE_MODEL` | LLM model to use | No | "ChatGPT-3.5-Turbo" |
| `VOYAGE_API_KEY` | Voyage AI for embeddings | Optional | None |
| `VOYAGE_MODEL` | Embedding model | No | "voyage-3.5-lite" |

*Without API keys, bot will show configuration messages

### **Performance Tuning**
```json
// In data.json bot_config
{
  "temperature": 0.7,           // Creativity (0.0-1.0)
  "max_response_length": 500,   // Response limit
  "language": "Indonesian"      // Primary language
}
```

## 🎯 Multi-Language Support

### **Supported Languages**
- **Indonesian**: Full support with slang detection
- **English**: Complete language support
- **Mixed Languages**: Smart detection and context switching
- **Regional Languages**: AI-powered understanding
- **Slang/Abbreviations**: Automatic normalization

### **Smart Language Routing**
```
Simple queries (Indonesian/English) → Fast keyword search
Complex queries (mixed/regional) → AI-powered processing
```

## 🛡️ Security Features

- **Rate Limiting**: Configurable per IP (default: 20 req/min)
- **Input Validation**: XSS and injection protection
- **Security Headers**: X-Frame-Options, CSP, etc.
- **API Key Protection**: Graceful degradation when missing
- **Session Isolation**: Secure conversation separation

## 📊 Performance Metrics

| Metric | Target | Achieved |
|--------|---------|----------|
| Response Time (P90) | < 2s | ✅ ~1.5s |
| Memory Usage | < 100MB | ✅ ~80MB |
| Docker Image Size | < 500MB | ✅ ~380MB |
| Code Lines | < 1500 | ✅ ~1200 |
| API Calls (per query) | Minimal | ✅ 0-1 calls |

## 🔍 Troubleshooting

### **Common Issues**

1. **"API key tidak tersedia"**
   - Add `POE_API_KEY` to `.env` file
   - Bot works in demo mode without API keys

2. **Slow responses**
   - Check internet connection
   - Verify API key validity
   - Consider using keyword search only

3. **Memory issues**
   - Clear old sessions: `DELETE /api/v1/chat/session/{id}`
   - Restart application periodically

4. **Language not understood**
   - System falls back to AI processing automatically
   - Add common terms to `data.json` FAQ section

### **Debug Mode**
```bash
# Enable debug logging
export DEBUG=true
uvicorn app.main:app --reload --log-level debug
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## 💡 Need Help?

- 📖 **Full Documentation**: Check `/docs` endpoint when running
- 🎬 **Demo**: Visit root URL (`/`) for interactive widget
- 🐛 **Issues**: Report bugs via GitHub Issues
- 💬 **Support**: Create discussion for questions

**Built with ❤️ for Indonesian UMKM and businesses worldwide**