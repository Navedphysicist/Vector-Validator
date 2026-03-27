from services.tier_taxonomy import get_taxonomy_for_prompt


def vector_extraction_prompt(company_name: str, tavily_results: str) -> str:
    taxonomy = get_taxonomy_for_prompt()

    return f"""You are an expert business analyst specializing in executive search and company analysis.

Given the following information about a company, identify its three core business vectors.

Company: {company_name}

Research data:
{tavily_results}

Identify exactly three things:
1. Business Model — How the company primarily makes money
2. Industry — The sector/vertical the company operates in
3. Transaction Platform — How customers interact with or buy from the company

Use the following taxonomy as your reference. Pick the closest matching value from these lists, or create a concise new term if nothing fits:

{taxonomy}

IMPORTANT:
- Pick the SINGLE most dominant business model, not a combination
- Pick the most specific industry, not a broad category
- Pick the primary transaction platform, not all channels
- If the company has multiple models (e.g., subscription + retail), pick the one that drives the majority of revenue

Return ONLY valid JSON with no other text:
{{"businessModel": "...", "industry": "...", "transactionPlatform": "..."}}"""


def tier_classification_prompt(business_model: str, industry: str, transaction_platform: str) -> str:
    taxonomy = get_taxonomy_for_prompt()

    return f"""You are classifying business attributes as Common or Unique for an executive search matching algorithm.

Definitions:
- Common: Widely seen across many companies. You can easily name 10+ well-known companies with this attribute. Executives with this experience are relatively easy to find.
- Unique: Highly specialized. A recruiter would struggle to name 10 companies with this attribute. Finding executives with this specific experience requires searching across different industries.

Here is the full reference taxonomy:

{taxonomy}

Now classify these three values:
- Business Model: {business_model}
- Industry: {industry}
- Transaction Platform: {transaction_platform}

Rules:
- If a value exactly matches or closely matches a known Common value, classify as Common
- If a value exactly matches or closely matches a known Unique value, classify as Unique
- If a value is NOT in either list, use your judgment based on the definitions above and your training data
- When uncertain, lean toward Unique — it is safer to treat an attribute as specialized than to miss a genuinely unique characteristic

Return ONLY valid JSON with no other text:
{{"businessModel": "Common" or "Unique", "industry": "Common" or "Unique", "transactionPlatform": "Common" or "Unique", "reasoning": "One sentence explaining each classification"}}"""


def role_classification_prompt(role_title: str) -> str:
    return f"""Classify this job role into exactly one of these 10 role families:

1. Marketing / Brand
2. Finance / Accounting
3. Sales / Revenue
4. Operations / General Mgmt
5. People / HR
6. Technology / Engineering
7. Product
8. Supply Chain / Logistics
9. Legal / Compliance
10. Data / Analytics

Role title: {role_title}

Consider the primary function of this role. For example:
- "Chief Commercial Officer" → Sales / Revenue (drives revenue)
- "VP Growth" → Marketing / Brand (drives customer acquisition)
- "Head of Strategy" → Operations / General Mgmt (general management)

Return ONLY valid JSON with no other text:
{{"roleFamily": "exact family name from the list above"}}"""
