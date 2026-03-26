TAXONOMY = {
    "business_model": {
        "common": [
            {"name": "Subscription", "description": "Recurring revenue from regular payments — Netflix, Spotify, SaaS products, meal kits, pet food delivery"},
            {"name": "E-Commerce", "description": "Online buying and selling of goods — Amazon, Shopify stores, branded DTC sites"},
            {"name": "SaaS", "description": "Software as a service, recurring cloud-based license — Salesforce, Slack, HubSpot"},
            {"name": "Retail", "description": "Physical store sales to consumers — Walmart, Target, Sephora, Apple Store"},
            {"name": "Wholesale", "description": "Bulk sales to retailers or distributors — Sysco, CPG brands selling to grocery chains"},
            {"name": "Ad Hoc Commerce", "description": "Walk-in, one-time transactions — QSR, coffee shops, convenience stores, fast casual"},
            {"name": "Franchise", "description": "License-based expansion through independent operators — McDonald's, 7-Eleven, Orangetheory"},
            {"name": "Marketplace", "description": "Platform connecting buyers and sellers, takes a cut — eBay, Etsy, Airbnb, Uber"},
            {"name": "Revenue Share", "description": "Split revenue with partners or content creators — YouTube, app stores, affiliate programs"},
            {"name": "Freemium", "description": "Free base tier with paid premium upgrades — Spotify, Dropbox, LinkedIn"},
            {"name": "Membership", "description": "Fee-based access to services or products — Costco, Amazon Prime, gym memberships"},
            {"name": "Direct Sales", "description": "Selling directly to end customer without intermediary — door-to-door, catalog, direct response"},
            {"name": "Advertising", "description": "Revenue from displaying ads to users — Google, Meta, media companies, free apps"},
            {"name": "Licensing", "description": "Revenue from licensing IP, patents, technology, or brand — Disney, Qualcomm, ARM"},
            {"name": "Transaction Fee", "description": "Fee per transaction processed — Stripe, PayPal, Square, Visa"},
            {"name": "Commission", "description": "Percentage taken on each sale facilitated — real estate agents, insurance brokers"},
            {"name": "Consulting / Professional Services", "description": "Revenue from expert advice and project-based work — McKinsey, Accenture, law firms"},
            {"name": "Hardware + Software", "description": "Physical product with software/subscription component — Apple, Peloton, Ring"},
            {"name": "Managed Services", "description": "Outsourced ongoing service management — IT managed services, HR outsourcing"},
            {"name": "Usage-based / Pay-per-use", "description": "Charges based on consumption — AWS, utilities, API call pricing, cloud storage"},
            {"name": "Bundled / Tiered Pricing", "description": "Multiple product tiers at different price points — cable packages, insurance plans"},
            {"name": "Razor-and-Blade", "description": "Cheap hardware, expensive consumables — printers/ink, Keurig/pods, Gillette"},
            {"name": "Affiliate / Referral", "description": "Revenue from driving customers to other businesses — comparison sites, influencer marketing"},
            {"name": "Contract / Retainer", "description": "Fixed recurring fee for ongoing services — legal retainers, PR agencies, security services"},
            {"name": "Donations / Nonprofit", "description": "Revenue from donations, grants, fundraising — charities, foundations, public media"},
            {"name": "Insurance Premium", "description": "Regular payments for risk coverage — health, auto, property, life insurance"},
            {"name": "Tuition / Education Fee", "description": "Payment for educational programs — universities, bootcamps, online courses"},
            {"name": "Real Estate / Lease", "description": "Revenue from property ownership and leasing — REITs, landlords, co-working spaces"},
            {"name": "White Label / Private Label", "description": "Manufacturing products sold under another brand — store brands, contract manufacturing"},
            {"name": "Dropshipping", "description": "Selling products without holding inventory — fulfilled by third-party supplier"},
        ],
        "unique": [
            {"name": "POC (% Completion)", "description": "Partial payment on long-running contracts — construction, restoration, large consulting. Revenue recognized as work progresses over months/years."},
            {"name": "Value-based Care", "description": "Healthcare reimbursement tied to patient outcomes, not volume of services delivered. Requires completely different financial modeling."},
            {"name": "iBuying", "description": "Company buys inventory (homes, cars) and resells directly — heavy balance sheet risk, requires real estate or automotive finance expertise (Opendoor, Carvana)"},
            {"name": "Rental / Resale", "description": "Asset ownership with depreciation, utilization rates, and reverse logistics — clothing rental, equipment leasing (Rent the Runway, Hertz)"},
            {"name": "BNPL (Buy Now Pay Later)", "description": "Deferred payment with merchant-funded consumer credit — requires credit risk expertise, merchant integration (Affirm, Klarna, Afterpay)"},
            {"name": "Brokerage (Principal)", "description": "Commission on transactions without owning inventory but with principal risk — stock brokers, freight brokers, energy traders"},
            {"name": "Concession / Licensing (Venue)", "description": "Revenue from IP rights or territorial licenses at physical venues — sports venues, airport concessions, casino operations"},
            {"name": "Revenue Share (Embedded)", "description": "Monetizing third-party activity running inside your platform via embedded services — embedded finance, insurance, identity verification"},
            {"name": "Tolling / Processing", "description": "Fee for processing raw materials owned by the customer — oil refining, metal processing, chemical manufacturing"},
            {"name": "Capitation", "description": "Fixed per-member payment regardless of services used — healthcare managed care, HMOs. Inverts the incentive from fee-for-service."},
            {"name": "Royalty Streaming", "description": "Upfront payment for ongoing royalty rights — mining royalties, music royalties, pharmaceutical royalties (Franco-Nevada, Hipgnosis)"},
            {"name": "Carbon Credit Trading", "description": "Buying and selling carbon offset credits — environmental markets, voluntary carbon markets, compliance credits"},
            {"name": "Data Monetization (Primary)", "description": "Primary revenue from selling proprietary data or insights — Bloomberg, Nielsen, CoreSignal, credit bureaus"},
            {"name": "Government Contract (IDIQ)", "description": "Indefinite delivery/indefinite quantity government contracts — defense, infrastructure, complex procurement cycles"},
            {"name": "Cooperative / Mutual", "description": "Member-owned structure where profits distributed to members — credit unions, agricultural co-ops, mutual insurance"},
            {"name": "Auction-based Revenue", "description": "Revenue from auction mechanics — ad auctions (Google), spectrum auctions, art houses (Christie's, Sotheby's)"},
            {"name": "Outcome-based Pricing", "description": "Payment tied to achieving specific measurable outcomes — performance marketing, success-fee consulting, pay-for-performance pharma"},
            {"name": "Build-Operate-Transfer (BOT)", "description": "Build an asset, operate it for a period, then transfer ownership — infrastructure, offshore development centers"},
        ],
    },
    "industry": {
        "common": [
            {"name": "Food & Beverage", "description": "CPG food, beverages, restaurants, food service, snacks, dairy, confectionery"},
            {"name": "Fashion / Apparel", "description": "Clothing, footwear, accessories, luxury goods, fast fashion, sustainable fashion"},
            {"name": "Technology", "description": "Software, hardware, IT services, cloud computing, cybersecurity, enterprise tech"},
            {"name": "Healthcare", "description": "Hospitals, pharma, medical devices, health services, digital health, clinical research"},
            {"name": "Financial Services", "description": "Banking, insurance, investment management, wealth management, payments, lending"},
            {"name": "Pet Food / Pet Products", "description": "Pet nutrition, supplies, services, veterinary, pet insurance, pet tech"},
            {"name": "Activewear", "description": "Athletic and performance clothing, sportswear, athleisure, outdoor apparel"},
            {"name": "EdTech", "description": "Education technology, online learning platforms, LMS, tutoring, upskilling"},
            {"name": "Beauty / Cosmetics", "description": "Skincare, makeup, fragrance, personal care, clean beauty, cosmeceuticals"},
            {"name": "Fitness / Wellness", "description": "Gyms, health clubs, wellness apps, mental health, meditation, nutrition coaching"},
            {"name": "Personal Care / Grooming", "description": "Grooming, hygiene, oral care, men's grooming, shaving, body care"},
            {"name": "Construction", "description": "Building, contracting, infrastructure development, civil engineering, specialty trades"},
            {"name": "QSR / Fast Casual", "description": "Quick-service and fast casual restaurants, pizza chains, coffee chains, juice bars"},
            {"name": "Home Services", "description": "HVAC, plumbing, cleaning, pest control, lawn care, roofing, painting, moving"},
            {"name": "Insurance / InsurTech", "description": "Insurance products, digital distribution, claims tech, underwriting platforms"},
            {"name": "Automotive", "description": "Vehicle manufacturing, dealerships, auto parts, mobility, EV, fleet management"},
            {"name": "Travel & Hospitality", "description": "Hotels, airlines, travel agencies, tourism, cruise lines, vacation rentals"},
            {"name": "Real Estate", "description": "Property development, management, brokerage, commercial real estate, REITs"},
            {"name": "Media & Entertainment", "description": "Film, TV, streaming, gaming, publishing, podcasting, live events"},
            {"name": "Retail (General)", "description": "General merchandise, department stores, specialty retail, discount retail"},
            {"name": "Consumer Electronics", "description": "Phones, computers, smart home, wearables, audio equipment, cameras"},
            {"name": "Logistics & Transportation", "description": "Freight, shipping, warehousing, last-mile delivery, trucking, rail"},
            {"name": "Energy & Utilities", "description": "Oil & gas, electric utilities, renewable energy, solar, wind, grid infrastructure"},
            {"name": "Telecommunications", "description": "Mobile carriers, ISPs, fiber, 5G infrastructure, unified communications"},
            {"name": "Pharmaceuticals", "description": "Drug development, manufacturing, distribution, generics, biotech"},
            {"name": "Agriculture / AgTech", "description": "Farming, crop sciences, animal health, precision agriculture, food supply"},
            {"name": "Manufacturing", "description": "Industrial manufacturing, consumer goods production, contract manufacturing"},
            {"name": "Professional Services", "description": "Consulting, legal, accounting, staffing, engineering services"},
            {"name": "Ecommerce / Online Retail", "description": "Pure-play online retailers, marketplaces, flash sales, social commerce"},
            {"name": "Restaurants / Food Service", "description": "Full-service restaurants, catering, ghost kitchens, food trucks, meal delivery"},
        ],
        "unique": [
            {"name": "Disaster Recovery / Restoration", "description": "Emergency cleanup, mold remediation, water damage, fire restoration — very specialized audience and service delivery model"},
            {"name": "Non-Alcoholic Beer / Spirits", "description": "Emerging category requiring new market creation, not replacing existing habits — regulatory gray area, novel consumer education"},
            {"name": "Connected Fitness Hardware", "description": "Physical devices with digital subscription — Peloton, Tonal, Mirror — hardware + content hybrid requiring both manufacturing and digital expertise"},
            {"name": "Proptech", "description": "Real estate technology disrupting traditional brokerage and property management — regulatory complexity, slow-moving industry"},
            {"name": "Space Technology", "description": "Satellite, launch, orbital services — extremely niche regulatory (FAA/FCC), long development cycles, government/defense customers"},
            {"name": "Cannabis / CBD", "description": "Federally complex regulatory landscape, state-by-state compliance, banking restrictions, evolving legal framework"},
            {"name": "Vertical Farming", "description": "Controlled environment agriculture at commercial scale — deep tech + agriculture hybrid, energy-intensive, novel supply chain"},
            {"name": "Nuclear Energy (SMR)", "description": "Small modular reactor technology — deep regulatory (NRC), decades-long permitting, public perception challenges"},
            {"name": "Psychedelics Therapy", "description": "FDA-regulated psychedelic-assisted therapy — intersection of pharma, mental health, and evolving drug regulation"},
            {"name": "Lab-grown Meat / Cultured Protein", "description": "Cell-cultured protein production — FDA/USDA dual regulation, food science frontier, consumer acceptance challenges"},
            {"name": "Quantum Computing", "description": "Quantum hardware and software — extremely early-stage, deeply technical, limited commercial applications today"},
            {"name": "Autonomous Vehicles / Robotics", "description": "Self-driving technology, delivery robots — heavy regulatory, safety certification, liability frameworks"},
            {"name": "Digital Therapeutics", "description": "FDA-approved software-based treatments — intersection of tech, pharma, and clinical trials, requires clinical evidence"},
            {"name": "Rare Disease / Orphan Drug", "description": "Treatments for diseases affecting very small populations — specialized FDA pathways, ultra-niche patient populations"},
            {"name": "Satellite Internet", "description": "LEO satellite broadband (Starlink, Kuiper) — space + telecom + international regulatory hybrid"},
            {"name": "Synthetic Biology", "description": "Engineering biological systems for industrial use — gene editing, biomanufacturing, biosecurity concerns"},
            {"name": "Carbon Capture / Climate Tech", "description": "Direct air capture, carbon sequestration — nascent market, regulatory credits-dependent, deep engineering"},
            {"name": "Longevity / Anti-aging", "description": "Science-backed life extension — unregulated supplements vs FDA-regulated therapeutics, credibility challenges"},
        ],
    },
    "transaction_platform": {
        "common": [
            {"name": "Digital DTC", "description": "Direct-to-consumer via owned website/app — brand controls the entire customer experience, owns the data"},
            {"name": "Multi-unit Four-wall", "description": "Physical store locations — retail chains, restaurant chains, gym chains, clinic networks"},
            {"name": "E-Commerce", "description": "Online marketplace or storefront — Amazon seller, Shopify store, branded online store"},
            {"name": "Omnichannel", "description": "Combination of digital + physical channels — buy online pick up in store, endless aisle, unified inventory"},
            {"name": "Digital Platform", "description": "Software platform (web/mobile) — SaaS dashboards, social media, productivity tools, banking apps"},
            {"name": "Mobile-first", "description": "Primary interaction through mobile app — Uber, DoorDash, banking apps, dating apps, fitness trackers"},
            {"name": "B2B Field Services", "description": "Service teams deployed to business client sites — IT services, facilities management, commercial cleaning"},
            {"name": "B2C Field Services", "description": "Service teams deployed to consumer homes — plumbing, HVAC, pest control, lawn care, home cleaning"},
            {"name": "Marketplace (Two-sided)", "description": "Platform connecting buyers and sellers — Airbnb, Uber, Etsy, StockX, Poshmark"},
            {"name": "Retail (Physical)", "description": "Traditional brick-and-mortar retail — department stores, specialty shops, pop-up stores"},
            {"name": "Streaming", "description": "Content delivered via streaming platform — Netflix, Spotify, Disney+, Twitch, podcasting"},
            {"name": "Wholesale / Distribution", "description": "B2B bulk sales through distribution channels — Sysco, US Foods, UNFI, McLane"},
            {"name": "Contact Center / Inside Sales", "description": "Sales and service through phone/chat/email — insurance sales, telecom support, SaaS sales"},
            {"name": "Events / Venues", "description": "In-person experiences at physical venues — concerts, sports, conferences, trade shows"},
            {"name": "Kiosk / Self-service", "description": "Automated self-service points — ATMs, vending machines, airport check-in, self-checkout"},
            {"name": "Social Commerce", "description": "Shopping directly within social media platforms — TikTok Shop, Instagram Shopping, live selling"},
            {"name": "Franchise Network", "description": "Distributed operations through franchise partners — each location independently operated"},
            {"name": "Call / Appointment-based", "description": "Service scheduled by appointment — salons, clinics, financial advisors, tutoring"},
            {"name": "Catalog / Direct Mail", "description": "Orders placed via physical or digital catalog — legacy but still significant in some verticals"},
        ],
        "unique": [
            {"name": "B2B Project-based", "description": "Large contracts with milestone billing — construction, consulting, enterprise IT implementations, multi-year engagements"},
            {"name": "Telehealth", "description": "Remote medical delivery via video/app — HIPAA compliance, multi-state licensing, regulatory complexity per jurisdiction"},
            {"name": "Blockchain Settlement", "description": "Crypto/DeFi transactions settled on-chain — smart contracts, gas fees, wallet infrastructure, regulatory uncertainty"},
            {"name": "Embedded (API-based)", "description": "Product delivered inside another company's platform via API — embedded finance, insurance, identity verification, payments"},
            {"name": "Auction / Bidding", "description": "Price determined by competitive bidding — art (Christie's), commodities, spectrum auctions, government procurement"},
            {"name": "Peer-to-peer Network", "description": "Users transact directly with each other — P2P lending, energy trading, file sharing, decentralized exchanges"},
            {"name": "Satellite / Remote Delivery", "description": "Service delivered via satellite or remote infrastructure — satellite internet, remote sensing, space-based imaging"},
            {"name": "Drone / Autonomous Delivery", "description": "Goods delivered by autonomous vehicles or drones — last-mile innovation, regulatory FAA framework"},
            {"name": "Virtual Reality / Metaverse", "description": "Transactions inside virtual environments — gaming economies, virtual real estate, digital goods, VR experiences"},
            {"name": "Clinical Trial Network", "description": "Multi-site patient recruitment and trial management — pharma/biotech, IRB approvals, patient data handling"},
            {"name": "Dark Store / Ghost Kitchen", "description": "Fulfillment-only locations not open to public — delivery-only restaurants, rapid grocery delivery warehouses"},
            {"name": "Government Portal / GovTech", "description": "Services delivered through government digital infrastructure — permits, benefits, compliance filing, procurement"},
        ],
    },
}


def get_taxonomy_for_prompt() -> str:
    """Format the entire taxonomy as a string for embedding in LLM prompts."""
    sections = []

    for vector_name, tiers in TAXONOMY.items():
        display_name = vector_name.replace("_", " ").title()
        sections.append(f"=== {display_name} ===\n")

        sections.append("COMMON (widely seen, 10+ well-known companies have this):")
        for item in tiers["common"]:
            sections.append(f"  - {item['name']}: {item['description']}")

        sections.append("\nUNIQUE (highly specialized, hard to find executives with this experience):")
        for item in tiers["unique"]:
            sections.append(f"  - {item['name']}: {item['description']}")

        sections.append("")

    return "\n".join(sections)


def get_common_values(vector: str) -> list[str]:
    """Get list of common value names for a vector."""
    return [item["name"] for item in TAXONOMY[vector]["common"]]


def get_unique_values(vector: str) -> list[str]:
    """Get list of unique value names for a vector."""
    return [item["name"] for item in TAXONOMY[vector]["unique"]]
