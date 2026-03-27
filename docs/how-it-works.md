# How Vector Validator Works

## Overview

Vector Validator helps executive search firms determine which company attributes matter most when sourcing candidates for a given role. It answers: **"For this role at this company, should we prioritize Business Model experience, Industry experience, or Transaction Platform experience?"**

## The Three Business Vectors

Every company is described by three vectors:

| Vector | Question It Answers | Example |
|--------|---------------------|---------|
| **Business Model** | How does the company make money? | Subscription, SaaS, Marketplace, Franchise |
| **Industry** | What sector does the company operate in? | Healthcare, Food & Beverage, Fintech |
| **Transaction Platform** | How do customers interact with the company? | Digital DTC, Multi-unit Four-wall, Telehealth |

## Common vs Unique Classification

Each vector is classified as **Common** or **Unique**:

- **Common**: Widely seen across 10+ well-known companies. Executives with this experience are easy to find. Examples: Subscription, E-Commerce, SaaS.
- **Unique**: Highly specialized. A recruiter would struggle to name 10 companies with this attribute. Examples: POC (% Completion), Vertical Farming, Telehealth.

The classification uses a curated taxonomy of ~110 values (located in `backend/services/tier_taxonomy.py`) as reference. The LLM classifies each vector against this taxonomy. When uncertain, the system leans toward Unique to avoid missing specialized characteristics.

## The 10 Role Families

Roles are grouped into 10 families, each with a default priority order:

| Role Family | Default Order (P1 > P2 > P3) | Example Roles |
|-------------|-------------------------------|---------------|
| Marketing / Brand | Industry > Platform > Model | CMO, VP Marketing, Growth Lead |
| Finance / Accounting | Platform > Model > Industry | CFO, Controller, FP&A |
| Sales / Revenue | Model > Industry > Platform | CRO, VP Sales, Account Executive |
| Operations / General Mgmt | Platform > Model > Industry | COO, CEO, Chief of Staff |
| People / HR | Industry > Model > Platform | CHRO, VP Talent, Head of People |
| Technology / Engineering | Platform > Industry > Model | CTO, VP Engineering, DevOps |
| Product | Platform > Industry > Model | CPO, VP Product, UX Lead |
| Supply Chain / Logistics | Model > Platform > Industry | VP Supply Chain, Procurement |
| Legal / Compliance | Industry > Model > Platform | CLO, General Counsel |
| Data / Analytics | Platform > Model > Industry | CDO, VP Data Science |

Role classification uses keyword matching first, with LLM fallback for ambiguous titles.

## The Priority Algorithm

The algorithm determines the final P1 > P2 > P3 order through three steps:

### Step 1: Classify the Role
Map the role title to one of 10 role families. This gives us the **default priority order**.

### Step 2: Classify the Vectors
Determine if each vector is **Common** or **Unique** using the taxonomy + LLM.

### Step 3: Calculate Final Priority
Pure deterministic logic:

1. Start with the role family's default order
2. Find all Unique vectors
3. If no Unique vectors: use the default order as-is
4. If P1 is already Unique: no change needed
5. Otherwise: promote the highest-ranked Unique vector to P1, keep the rest in default order

### Example

**Company:** ATI Restoration | **Role:** CFO

- Role Family: Finance / Accounting
- Default order: Platform > Model > Industry
- Business Model: POC (% Completion) = **Unique**
- Industry: Disaster Recovery = **Unique**
- Transaction Platform: B2B Field Services = **Common**

The highest Unique in the default order is Model (P2 position). Promote it to P1:

**Result:** Model > Platform > Industry

This tells the recruiter: prioritize finding a CFO who understands % completion accounting, then platform experience, then industry.

## Application Flow

```
User enters Company + Role
         |
         v
   [Tavily Web Search]
   Searches "{company} company business model industry overview"
   Returns top 5 results
         |
         v
   [LLM Vector Extraction]
   Extracts: Business Model, Industry, Transaction Platform
   Uses taxonomy as reference vocabulary
         |
         v
   User reviews/edits vectors
         |
         v
   [Role Classification]
   Keyword match -> LLM fallback -> default to Operations
         |
         v
   [Tier Classification]
   LLM classifies each vector as Common or Unique
   Using taxonomy + definitions
         |
         v
   [Priority Algorithm]
   Deterministic: promotes Unique vectors up the priority order
         |
         v
   User sees: Role Family, Unique Vectors, Final Prioritization
         |
         v
   User submits feedback (Looks Good / Needs Adjustment)
         |
         v
   Stored in PostgreSQL for algorithm refinement
```

## Project Structure

```
backend/
  main.py                  -- FastAPI app entry point
  models.py                -- Pydantic request/response schemas
  db.py                    -- PostgreSQL connection and queries
  routers/
    analyze.py             -- POST /analyze (web search + vector extraction)
    algorithm.py           -- POST /run-algorithm (classification + priority)
    feedback.py            -- GET/POST /feedback
    settings.py            -- GET/POST /settings
  services/
    algorithm_service.py   -- Priority calculation (pure logic)
    role_families.py       -- 10 role families with keywords and default orders
    tier_taxonomy.py       -- Common/Unique value definitions (~110 values)
    tavily_service.py      -- Tavily web search integration
    llm_service.py         -- OpenAI/Groq unified client
    prompts.py             -- LLM prompt templates

frontend/
  src/
    App.tsx                -- Main app orchestrating the multi-step workflow
    components/
      CompanyRoleInput.tsx -- Step 1: Company + Role input form
      VectorDisplay.tsx    -- Step 2: Editable vector display
      AlgorithmResult.tsx  -- Step 3: Role Family, Unique Vectors, Final Prioritization
      FeedbackForm.tsx     -- Step 4: Feedback submission
      FeedbackSidebar.tsx  -- Validation history table
      SettingsModal.tsx    -- API key configuration
    lib/
      api.ts               -- Backend API client
      types.ts             -- TypeScript interfaces

matching-engine/           -- Design specs and algorithm documentation
```

## Database Tables

### validation_results
Stores user feedback on algorithm results for future refinement.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| company | TEXT | Company name |
| business_model | TEXT | Extracted business model |
| industry | TEXT | Extracted industry |
| transaction_platform | TEXT | Extracted transaction platform |
| role | TEXT | Role title |
| role_family | TEXT | Classified role family |
| p1, p2, p3 | TEXT | Priority order result |
| is_correct | BOOLEAN | User's validation |
| comment | TEXT | Optional user comment |
| user_name | TEXT | Who submitted |
| created_at | TIMESTAMPTZ | Timestamp |

### user_settings
Stores per-user API key configuration.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_name | TEXT | Unique user identifier |
| llm_provider | TEXT | "openai" or "groq" |
| llm_model | TEXT | Model name (e.g., "gpt-4o") |
| llm_api_key | TEXT | LLM API key |
| tavily_api_key | TEXT | Tavily API key |
| updated_at | TIMESTAMPTZ | Last updated |

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | /analyze | Search company + extract vectors via LLM |
| POST | /run-algorithm | Classify role + tiers + calculate priority |
| POST | /feedback | Submit validation feedback |
| GET | /feedback?limit=100 | Retrieve feedback history |
| POST | /settings | Save user API keys |
| GET | /settings/{user_name} | Get user settings (keys masked) |
| GET | /health | Health check |
