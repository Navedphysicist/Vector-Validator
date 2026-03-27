import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from routers import settings, analyze, algorithm, feedback


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


# On Vercel, routes are served under /api via serverless function
root_path = "/api" if os.getenv("VERCEL") else ""

app = FastAPI(title="Vector Validator API", lifespan=lifespan, root_path=root_path)

allowed_origins = [
    "http://localhost:5173",
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
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(settings.router)
app.include_router(analyze.router)
app.include_router(algorithm.router)
app.include_router(feedback.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
