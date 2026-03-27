import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from routers import settings, analyze, algorithm, feedback

is_vercel = bool(os.getenv("VERCEL"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Vector Validator API", lifespan=lifespan)

allowed_origins = [
    "http://localhost:5173",
    "https://*.vercel.app",
]

# Add Vercel deployment URL if set
vercel_url = os.getenv("VERCEL_URL")
if vercel_url:
    allowed_origins.append(f"https://{vercel_url}")

# Add custom domain if set
production_url = os.getenv("PRODUCTION_URL")
if production_url:
    allowed_origins.append(production_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if is_vercel else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# On Vercel, requests arrive as /api/analyze, /api/settings, etc.
# Locally (via Vite proxy), requests arrive as /analyze, /settings, etc.
prefix = "/api" if is_vercel else ""

app.include_router(settings.router, prefix=prefix)
app.include_router(analyze.router, prefix=prefix)
app.include_router(algorithm.router, prefix=prefix)
app.include_router(feedback.router, prefix=prefix)


@app.get(f"{prefix}/health")
async def health():
    return {"status": "ok"}
