import sys
import os
from pathlib import Path

# Add backend directory to Python path so imports work
backend_dir = str(Path(__file__).resolve().parent.parent / "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Set dotenv path explicitly for Vercel (backend/.env won't exist, but just in case)
os.environ.setdefault("DOTENV_PATH", os.path.join(backend_dir, ".env"))

from main import app  # noqa: E402
