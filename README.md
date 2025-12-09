# AI Customer Support Bot

A production-grade AI-powered customer support bot leveraging **Google Gemini 2.5**, **FAISS** for RAG, and a responsive **React** frontend.

## 🎬 Project Demo

![Project Demo](assets/demo.webp)

> **Watch the full interaction:** The demo above showcases the Theme Toggle, Knowledge Base retrieval (RAG), and persistent session management.

---

## 🚀 Key Features

### 🧠 Intelligent RAG Engine
- **Knowledge Base**: Retrieves accurate answers from `data/sample_faqs.json` using FAISS vector similarity search.
- **Model**: Powered by **Gemini-2.5-Flash** for high-speed, low-latency responses.
- **Fallback Mechanism**: Robust error handling ensures the bot fails gracefully if the LLM is unreachable.

### 🎨 Modern UI/UX
- **Theme Toggle**: A creative, animated Sun/Moon toggle for seamless Light/Dark mode switching.
- **Responsive Design**: Built with Tailwind CSS to look great on all devices.
- **Real-time Streaming**: Simulates token-by-token streaming for a natural chat experience.

### ⚙️ Robust Backend
- **Session Management**: Persistent chat history stored in SQLite (Dev) / PostgreSQL (Prod).
- **Escalation Engine**: Detects user frustration or specific triggers to simulate ticket creation.
- **API Architecture**: Built on **FastAPI** with `uvicorn` for high-performance async processing.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3.10+, FastAPI | High-performance API |
| **LLM** | Google Gemini 2.5 Flash | Intelligent response generation |
| **Vector DB** | FAISS + SentenceTransformers | Semantic search & RAG |
| **Database** | SQLAlchemy (SQLite) | Session & Message storage |
| **Frontend** | React, Vite, Tailwind CSS | Responsive Chat UI |
| **Container** | Docker & Docker Compose | Containerized Deployment |

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Gemini API Key

### 1. clone & Setup
```bash
git clone <repository-url>
cd customer_support_bot
```

### 2. Backend Setup
```bash
# Create virtual env
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure Environment
cp .env.example .env
# Open .env and add your GEMINI_API_KEY
```

### 3. Initialize Data
```bash
# Create DB tables
python scripts/init_db.py

# Ingest FAQs into Vector DB
python scripts/ingest_data.py
```

### 4. Run Application
**Backend:**
```bash
python -m uvicorn src.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to chat!

---

## 🧪 Testing & Verification
- **Run Tests**: `pytest tests/`
- **Verify RAG**: `python scripts/verify_rag.py`
- **Debug Sessions**: `python scripts/debug_sessions.py`

---

*Verified Submission - December 2025*
