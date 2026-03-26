import json
import re
from openai import OpenAI
from groq import Groq


def call_llm(provider: str, model: str, api_key: str, prompt: str) -> dict:
    """
    Call LLM and return parsed JSON response.
    Supports OpenAI and Groq providers.
    Retries once on JSON parse failure.
    """
    for attempt in range(2):
        raw = _call_provider(provider, model, api_key, prompt)
        parsed = _parse_json(raw)
        if parsed is not None:
            return parsed

    raise ValueError(f"LLM returned invalid JSON after 2 attempts. Raw response: {raw}")


def _call_provider(provider: str, model: str, api_key: str, prompt: str) -> str:
    """Call the appropriate LLM provider and return raw text response."""
    if provider == "openai":
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return response.choices[0].message.content

    elif provider == "groq":
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


def _parse_json(text: str) -> dict | None:
    """Try to parse JSON from LLM response. Handles markdown code blocks."""
    if not text:
        return None

    text = text.strip()

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code block
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try finding first { ... } block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return None
