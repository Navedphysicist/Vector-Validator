ROLE_FAMILIES = [
    {
        "name": "Marketing / Brand",
        "keywords": ["marketing", "brand", "growth", "demand gen", "content", "communications", "cmo", "digital marketing", "brand manager", "creative"],
        "default_order": ["Industry", "Platform", "Model"],
        "reasoning": "Marketers must understand the customer, product claims, regulatory landscape of their specific industry",
    },
    {
        "name": "Finance / Accounting",
        "keywords": ["finance", "controller", "fp&a", "treasury", "accounting", "audit", "cfo", "financial", "comptroller", "tax"],
        "default_order": ["Platform", "Model", "Industry"],
        "reasoning": "Finance leaders need to understand how money flows — revenue recognition, unit economics depend on the transaction platform",
    },
    {
        "name": "Sales / Revenue",
        "keywords": ["sales", "revenue", "partnerships", "business development", "commercial", "cro", "account executive", "account management", "bd"],
        "default_order": ["Model", "Industry", "Platform"],
        "reasoning": "The business model defines the entire sales motion — subscription retention vs ad-hoc conversion vs marketplace growth",
    },
    {
        "name": "Operations / General Mgmt",
        "keywords": ["operations", "president", "gm", "chief of staff", "coo", "ceo", "general manager", "managing director"],
        "default_order": ["Platform", "Model", "Industry"],
        "reasoning": "Operations leaders manage the platform complexity — multi-unit stores, warehouses, digital fulfillment, or field services",
    },
    {
        "name": "People / HR",
        "keywords": ["people", "hr", "human resources", "talent", "recruiting", "culture", "chro", "talent acquisition", "organizational development"],
        "default_order": ["Industry", "Model", "Platform"],
        "reasoning": "HR needs to understand the industry talent pool — where to recruit, comp benchmarks, and culture norms differ by industry",
    },
    {
        "name": "Technology / Engineering",
        "keywords": ["engineering", "cto", "it", "infrastructure", "architect", "software", "technology", "devops", "platform engineering", "security"],
        "default_order": ["Platform", "Industry", "Model"],
        "reasoning": "Tech leaders build and maintain the platform — DTC stack vs POS systems vs marketplace infrastructure require different expertise",
    },
    {
        "name": "Product",
        "keywords": ["product", "cpo", "product management", "product manager", "product design", "ux", "product strategy"],
        "default_order": ["Platform", "Industry", "Model"],
        "reasoning": "Product leaders shape the customer experience defined by the transaction platform — mobile app, physical store, or omnichannel",
    },
    {
        "name": "Supply Chain / Logistics",
        "keywords": ["supply chain", "logistics", "procurement", "manufacturing", "warehouse", "distribution", "fulfillment", "inventory"],
        "default_order": ["Model", "Platform", "Industry"],
        "reasoning": "Business model dictates supply chain design — subscription = predictable demand, ad-hoc = variable, marketplace = no inventory",
    },
    {
        "name": "Legal / Compliance",
        "keywords": ["legal", "counsel", "compliance", "regulatory", "governance", "clo", "attorney", "privacy", "risk"],
        "default_order": ["Industry", "Model", "Platform"],
        "reasoning": "Legal/compliance landscape is heavily industry-specific — food safety vs fintech regulations vs healthcare HIPAA",
    },
    {
        "name": "Data / Analytics",
        "keywords": ["data", "analytics", "bi", "data science", "cdo", "business intelligence", "machine learning", "ai", "data engineering"],
        "default_order": ["Platform", "Model", "Industry"],
        "reasoning": "Data leaders need platform context — DTC generates different data patterns than four-wall retail or marketplace",
    },
]


def classify_role(role_title: str) -> dict | None:
    """Match role title to a family using keyword matching. Returns None if no match."""
    role_lower = role_title.lower()
    for family in ROLE_FAMILIES:
        for keyword in family["keywords"]:
            if keyword in role_lower:
                return family
    return None
