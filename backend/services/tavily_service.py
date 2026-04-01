# Backwards compatibility — use services.data_sources.tavily_source directly
from services.data_sources.tavily_source import search_company

__all__ = ["search_company"]
