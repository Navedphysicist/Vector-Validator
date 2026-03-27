# Vector Validator

An AI-powered tool that determines hiring priority tiers (P1, P2, P3) for executive search by analyzing company business vectors.

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL database (or [Neon](https://neon.tech) serverless Postgres)
- API keys: OpenAI (or Groq) + [Tavily](https://tavily.com)

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:

```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

Start the server:

```bash
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

### 3. Configure API Keys

1. Open `http://localhost:5173` in your browser
2. Enter your name to get started
3. Open **Settings** (gear icon in the navbar)
4. Add your **LLM API Key** (OpenAI or Groq) and **Tavily API Key**
5. Save

You're ready to go.

## Usage

1. Enter a **Company Name** and **Role** (e.g., "Sweetgreen", "CFO")
2. Click **Analyze** -- the app searches the web and extracts three business vectors
3. Review and optionally edit the vectors, then click **Run Algorithm**
4. See the **Role Family**, **Unique Vectors**, and **Final Prioritization** (P1 > P2 > P3)
5. Submit feedback on whether the ranking looks correct
6. View all past validations in the **History** sidebar

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, TypeScript, Tailwind CSS 4, Vite |
| Backend | FastAPI, Python |
| Database | PostgreSQL (Neon) |
| LLM | OpenAI (gpt-4o) or Groq |
| Web Search | Tavily API |
