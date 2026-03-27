# Vector Validator

An AI-powered priority ranking tool for executive search. Given a company and a role, it determines which business attributes (Business Model, Industry, or Transaction Platform) matter most when sourcing candidates.

Built for executive search professionals to validate and refine a Vector Priority Algorithm through structured feedback.

## How It Works

```
Company + Role  -->  Web Search  -->  Extract 3 Vectors  -->  Classify Common/Unique  -->  Priority Ranking
                     (Tavily)         (LLM)                   (LLM + Taxonomy)            (Deterministic)
```

1. **Analyze** -- Searches the web for company info, extracts three business vectors using an LLM
2. **Classify** -- Each vector is classified as Common or Unique against a curated taxonomy of ~110 values
3. **Prioritize** -- A deterministic algorithm ranks the vectors (P1 > P2 > P3) based on the role family and uniqueness
4. **Validate** -- Users submit feedback, stored in PostgreSQL for algorithm refinement

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL database (or [Neon](https://neon.tech) serverless Postgres)
- API keys: [OpenAI](https://platform.openai.com) (or [Groq](https://console.groq.com)) + [Tavily](https://tavily.com)

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
```

Start the server:

```bash
uvicorn main:app --reload
```

Runs at `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Runs at `http://localhost:5173`

### Configure API Keys

1. Open `http://localhost:5173`
2. Enter your name
3. Click the **Settings** gear icon
4. Add your **LLM API Key** and **Tavily API Key**
5. Save -- you're ready to go

## Features

- **AI-Powered Analysis** -- Tavily web search + LLM extraction of business vectors
- **Editable Vectors** -- Review and correct AI-extracted vectors before running the algorithm
- **10 Role Families** -- Automatic role classification with keyword matching + LLM fallback
- **Common/Unique Classification** -- Curated taxonomy with ~110 values, leans toward Unique when uncertain
- **Deterministic Priority Algorithm** -- Validated against 97 test cases
- **Feedback Collection** -- "Looks Good" / "Needs Adjustment" with optional comments
- **Validation History** -- Sidebar with cached data and notification badge for new entries
- **Multi-Provider LLM** -- OpenAI (gpt-4o, gpt-4o-mini, gpt-4-turbo) and Groq (llama-4-scout, llama-3.3-70b, mixtral-8x7b)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, TypeScript, Tailwind CSS 4, Vite |
| Backend | FastAPI, Python |
| Database | PostgreSQL (Neon) |
| LLM | OpenAI or Groq |
| Web Search | Tavily API |

## Documentation

- [Architecture and Features](docs/architecture-and-features.md) -- Detailed documentation of how the algorithm works, all features, project structure, database schema, and API endpoints
- [Priority Algorithm Spec](matching-engine/priority-algorithm.md) -- The original algorithm specification
- [Validation Test Cases](matching-engine/vector-priority-validation.xlsx) -- 97 company/role test cases used to validate the algorithm

## License

Private -- For internal use by Talent Studios.
