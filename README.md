- **Database**: PostgreSQL (Production), SQLite (Dev)
- **Vector DB**: FAISS
- **Frontend**: React, Vite, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose

## ⚡ Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL & Redis (or use Docker)
- Google Gemini API Key

### Backend Setup
1. **Clone & Install**
   ```bash
   git clone <repo>
   cd customer_support_bot
   pip install -r requirements.txt
   ```

2. **Environment**
   Copy `.env.example` to `.env` and add your keys:
   ```bash
   cp .env.example .env
   # Edit .env with GEMINI_API_KEY
   ```

3. **Initialize DB**
   ```bash
   python scripts/init_db.py
   ```

4. **Run Server**
   ```bash
   python -m uvicorn src.main:app --reload
   ```

### Frontend Setup
1. **Install & Run**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   Access UI at `http://localhost:5173`.

## 🐳 Docker Deployment

Build and run everything with Docker Compose:

```bash
docker-compose up --build
```
- **Frontend/Backend**: http://localhost:8000
- **Database**: Port 5432
- **Redis**: Port 6379

## 🧪 Testing

Run backend integration tests:
```bash
pytest tests/ -v
```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
