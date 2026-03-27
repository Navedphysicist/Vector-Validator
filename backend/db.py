import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS validation_results (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            company TEXT NOT NULL,
            industry TEXT NOT NULL,
            business_model TEXT NOT NULL,
            transaction_platform TEXT NOT NULL,
            role TEXT NOT NULL,
            role_family TEXT NOT NULL,
            p1 TEXT NOT NULL,
            p2 TEXT NOT NULL,
            p3 TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL,
            comment TEXT,
            user_name TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS user_settings (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_name TEXT UNIQUE NOT NULL,
            llm_provider TEXT DEFAULT 'openai',
            llm_model TEXT DEFAULT 'gpt-4o',
            llm_api_key TEXT,
            tavily_api_key TEXT,
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def insert_feedback(data: dict) -> dict:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO validation_results
            (company, industry, business_model, transaction_platform, role,
             role_family, p1, p2, p3, is_correct, comment, user_name)
        VALUES (%(company)s, %(industry)s, %(business_model)s, %(transaction_platform)s,
                %(role)s, %(role_family)s, %(p1)s, %(p2)s, %(p3)s,
                %(is_correct)s, %(comment)s, %(user_name)s)
        RETURNING *
    """, data)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(row)


def get_feedback(limit: int = 100) -> list[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM validation_results ORDER BY created_at DESC LIMIT %s",
        (limit,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]


def upsert_settings(user_name: str, settings: dict):
    conn = get_connection()
    cur = conn.cursor()
    # Only update API keys if a new value is provided (not None/empty)
    # This prevents overwriting saved keys when the user doesn't re-enter them
    cur.execute("""
        INSERT INTO user_settings (user_name, llm_provider, llm_model, llm_api_key, tavily_api_key, updated_at)
        VALUES (%(user_name)s, %(llm_provider)s, %(llm_model)s, %(llm_api_key)s, %(tavily_api_key)s, NOW())
        ON CONFLICT (user_name) DO UPDATE SET
            llm_provider = EXCLUDED.llm_provider,
            llm_model = EXCLUDED.llm_model,
            llm_api_key = CASE WHEN EXCLUDED.llm_api_key IS NOT NULL THEN EXCLUDED.llm_api_key ELSE user_settings.llm_api_key END,
            tavily_api_key = CASE WHEN EXCLUDED.tavily_api_key IS NOT NULL THEN EXCLUDED.tavily_api_key ELSE user_settings.tavily_api_key END,
            updated_at = NOW()
    """, {**settings, "user_name": user_name})
    conn.commit()
    cur.close()
    conn.close()


def get_settings(user_name: str) -> dict | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_settings WHERE user_name = %s", (user_name,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return dict(row) if row else None
