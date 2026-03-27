# Vector Priority Algorithm

## What It Does

Given a **company** and a **role**, determine the priority order of three vectors:
- **Business Model** — How the company makes money
- **Industry** — Sector / vertical
- **Transaction Platform** — How customers interact

---

## The Rule

**Two factors decide priority:**

1. **Role family** sets the default order
2. **If the company has a Unique attribute**, it gets promoted to #1

---

## Role Family Defaults

| Role Family | P1 | P2 | P3 | Why P1 matters most for this role |
|---|---|---|---|---|
| Marketing / Brand | Industry | Platform | Model | Marketers must understand the customer, product claims, regulatory landscape of their specific industry |
| Finance / Accounting | Platform | Model | Industry | Finance leaders need to understand how money flows — revenue recognition, unit economics, and financial operations depend on the transaction platform |
| Sales / Revenue | Model | Industry | Platform | The business model defines the entire sales motion — subscription retention vs ad-hoc conversion vs marketplace growth are fundamentally different |
| Operations / General Mgmt | Platform | Model | Industry | Operations leaders manage the platform complexity — multi-unit stores, warehouses, digital fulfillment, or field services |
| People / HR | Industry | Model | Platform | HR needs to understand the industry talent pool — where to recruit, compensation benchmarks, and culture norms differ by industry |
| Technology / Engineering | Platform | Industry | Model | Tech leaders build and maintain the platform — DTC tech stack vs POS systems vs marketplace infrastructure require different expertise |
| Product | Platform | Industry | Model | Product leaders shape the customer experience which is defined by the transaction platform — mobile app, physical store, or omnichannel |
| Supply Chain / Logistics | Model | Platform | Industry | Business model dictates supply chain design — subscription = predictable demand, ad-hoc = variable, marketplace = no inventory |
| Legal / Compliance | Industry | Model | Platform | Legal and compliance landscape is heavily industry-specific — food safety vs fintech regulations vs healthcare HIPAA |
| Data / Analytics | Platform | Model | Industry | Data leaders need platform context — DTC generates different data patterns than four-wall retail or marketplace |

---

## Common vs Unique

Every attribute value is either **Common** or **Unique**.

- **Common** — Widely seen across many companies. No promotion.
- **Unique** — Highly specialized, hard to find experience in. Promotes to P1.

Examples:

**Business Models:**

| Common | Unique |
|---|---|
| Subscription | POC (% Completion) — partial payment on long-running contracts (construction, restoration) |
| E-Commerce | Value-based Care — healthcare reimbursement tied to patient outcomes |
| SaaS | iBuying — company buys inventory (homes, cars) and resells directly |
| Retail | Rental / Resale — asset ownership with depreciation + utilization economics |
| Wholesale | BNPL (Buy Now Pay Later) — deferred payment with merchant-funded credit |
| Ad Hoc Commerce | Brokerage — commission on transactions without owning inventory |
| Franchise | Concession / Licensing — revenue from IP or territorial rights |
| Marketplace | Revenue Share (embedded) — monetizing third-party activity on your platform |
| Revenue Share | |
| Freemium | |
| Membership | |
| Direct Sales | |

**Industries:**

| Common | Unique |
|---|---|
| Food & Beverage | Disaster Recovery / Restoration — emergency cleanup and remediation services |
| Fashion / Apparel | Non-Alcoholic Beer / Spirits — emerging category requiring new market creation |
| Technology | Connected Fitness Hardware — physical devices with digital subscription (Peloton, Tonal) |
| Healthcare | Proptech — real estate technology disrupting traditional brokerage |
| Financial Services | Space Technology — satellite, launch, orbital services |
| Pet Food / Pet Products | Cannabis / CBD — federally complex regulatory landscape |
| Activewear | Vertical Farming — controlled environment agriculture at commercial scale |
| EdTech | Nuclear Energy (SMR) — small modular reactor technology |
| Beauty / Cosmetics | |
| Fitness / Wellness | |
| Personal Care / Grooming | |
| Construction | |
| QSR / Fast Casual | |
| Home Services | |
| Insurance / InsurTech | |

**Transaction Platforms:**

| Common | Unique |
|---|---|
| Digital DTC | B2B Project-based — large contracts with milestone billing (construction, consulting) |
| Multi-unit Four-wall | Telehealth — remote medical delivery via video/app |
| E-Commerce | Blockchain Settlement — crypto/DeFi transactions on-chain |
| Omnichannel | Embedded (API-based) — product delivered inside another company's platform |
| Digital Platform | Auction / Bidding — price determined by competitive bidding |
| Mobile-first | Peer-to-peer Network — users transact directly with each other (lending, energy) |
| B2B Field Services | |
| B2C Field Services | |
| Marketplace (Two-sided) | |
| Retail (Physical) | |
| Streaming | |

**How to tell if something is Unique**: If you'd struggle to name 10+ well-known companies with that attribute, it's probably Unique. If a recruiter would need to search across different industries to find experienced executives, it's Unique.

**If a value isn't in the list**: Do NOT default to Common. First, use LLM to classify it (ask: "Is this business model / industry / platform widely seen across many companies, or is it highly specialized?"). If the LLM is uncertain, flag it for human review before proceeding.

---

## The Algorithm (3 steps)

```
1. Identify the role family → get default order [P1, P2, P3]
2. Is any vector Unique?
   - No  → use the default order, done
   - Yes → promote the highest-ranking Unique vector to P1
           (if two are Unique, promote whichever is already
            higher in the default order)
           remaining two keep their default relative order
3. User can override by drag-reorder in the UI
```

---

## Examples (step-by-step walkthrough)

### Example 1: Ollie Pet — CFO (no Unique → default holds)

```
Company:  Model = Subscription (Common)
          Industry = Pet Food (Common)
          Platform = Digital DTC (Common)
Role:     CFO → Finance family
Default:  Platform > Model > Industry

Any Unique? No
→ Final:  Platform > Model > Industry
```

**Why**: For a CFO at a DTC pet food company, understanding the digital DTC platform (paid media finance, inventory planning, no retail intermediary) matters most. Pet food industry experience is not critical for finance.

---

### Example 2: ATI Restoration — CFO (Unique promotes to P1, rest keeps default order)

```
Company:  Model = POC / % Completion (Unique)
          Industry = Disaster Recovery (Unique)
          Platform = B2B Field Services (Common)
Role:     CFO → Finance family
Default:  Platform > Model > Industry

Any Unique? Yes — Model and Industry are both Unique
Highest Unique in default = Model (P2)
→ Promote Model to P1, remaining keep default order: Platform > Industry

Final:  Model > Platform > Industry
```

**Why**: POC accounting is so specialized that finding a CFO with percentage-of-completion experience matters more than anything. After that, Platform still matters more than Industry for a finance role — understanding B2B field services economics is more relevant to the CFO's daily work than disaster recovery industry knowledge.

---

### Example 3: ATI Restoration — CMO (P1 already Unique → no change)

```
Company:  Model = POC / % Completion (Unique)
          Industry = Disaster Recovery (Unique)
          Platform = B2B Field Services (Common)
Role:     CMO → Marketing family
Default:  Industry > Platform > Model

Any Unique? Yes — Model and Industry are both Unique
Is P1 (Industry) Unique? Yes → no change needed

Final:  Industry > Platform > Model
```

**Why**: For marketing, understanding the disaster recovery audience is critical. Industry is already P1 and it's Unique — no promotion needed. After that, Platform (how you reach customers) matters more than Model (POC is irrelevant to marketing).

---

## All Validated Examples (from Jeremy)

| # | Company | Role | Business Model | Industry | Transaction Platform | Final Priority |
|---|---------|------|---------------|----------|---------------------|---------------|
| 1 | Ollie Pet | CFO | Subscription (C) | Pet Food (C) | Digital DTC (C) | Platform > Model > Industry |
| 2 | Ollie Pet | CMO | Subscription (C) | Pet Food (C) | Digital DTC (C) | Industry > Platform > Model |
| 3 | ATI Restoration | CMO | POC (U) | Disaster Recovery (U) | B2B Field Services (C) | Industry > Platform > Model |
| 4 | ATI Restoration | CFO | POC (U) | Disaster Recovery (U) | B2B Field Services (C) | Model > Platform > Industry |
| 5 | Coffee Cafe Chain | CFO | Ad Hoc Commerce (C) | F&B / QSR (C) | Multi-unit Four-wall (C) | Platform > Model > Industry |

*C = Common, U = Unique. Algorithm produces the correct result for all 5.*

---

## Edge Cases

| Situation | What Happens |
|---|---|
| No Unique vectors | Role default order as-is |
| One Unique, not P1 | Promote it to P1, remaining two keep default relative order |
| One Unique, already P1 | No change |
| Two Unique, one is P1 | No change — P1 is already Unique |
| Two Unique, neither is P1 | Promote the higher-ranked Unique to P1, remaining keep default order |
| All three Unique | No change — P1 is already Unique |
| Unknown role title | Use AI to classify into a family. If that fails, default to Operations / General Mgmt |
| Unknown attribute value | Use LLM to classify. If uncertain, flag for human review. |
| User manually reorders | Their order wins, always |
