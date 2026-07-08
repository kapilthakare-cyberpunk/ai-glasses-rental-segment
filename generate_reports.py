#!/usr/bin/env python3
"""Generate branded HTML research reports from templates + research data."""

import os

TEMPLATE_DIR = "/Users/kapilthakare/Documents/project-research-template"
OUTPUT_DIR = "/Users/kapilthakare/Projects/ai-glasses-rental-segment/reports"

# ──────────────────────────────────────────────────────
# RESEARCH DATA
# ──────────────────────────────────────────────────────

MODELS = [
    {
        "name": "Ray-Ban Meta Wayfarer (Gen 2)",
        "category": "Best All-Rounder",
        "retail_inr": "₹39,900 – ₹45,700",
        "camera": "12 MP ultra-wide + 50 MP main",
        "video": "1080p @ 30fps, 3K @ 30fps",
        "battery": "~8 hours (2× Gen 1)",
        "weight_frame": "49 g",
        "weight_case": "133 g",
        "water": "IPX4 splash-resistant",
        "audio": "Open-ear speakers + 5 mics",
        "connectivity": "Bluetooth 5.3, Wi-Fi 6, Meta AI",
        "availability": "Amazon India, Ray-Ban.com/IN, select stores",
        "pros": "Best all-round specs; 3K video; 8hr battery; Meta AI; wide India availability",
        "cons": "Highest Ray-Ban price; Gen 2 only 6 months old",
        "rental_conservative": "₹500–600/day",
        "rental_premium": "₹750–850/day",
        "recommendation": "PRIMARY — Hero product for launch"
    },
    {
        "name": "Ray-Ban Meta Wayfarer (Gen 1)",
        "category": "Budget Tier",
        "retail_inr": "₹22,400 – ₹26,800",
        "camera": "12 MP ultra-wide",
        "video": "1080p @ 30fps",
        "battery": "~4 hours",
        "weight_frame": "49 g",
        "weight_case": "133 g",
        "water": "IPX4 splash-resistant",
        "audio": "Open-ear speakers + 5 mics",
        "connectivity": "Bluetooth 5.2, Meta AI",
        "availability": "Amazon India, Ray-Ban.com/IN",
        "pros": "Lowest entry cost; proven platform; Meta AI support",
        "cons": "Half the battery of Gen 2; 1080p only; older Bluetooth",
        "rental_conservative": "₹350–400/day",
        "rental_premium": "₹450–500/day",
        "recommendation": "OPTIONAL — Budget second tier if demand warrants"
    },
    {
        "name": "Ray-Ban Meta Headliner (Gen 1)",
        "category": "Round Frame Style",
        "retail_inr": "Not sold in India",
        "camera": "12 MP ultra-wide",
        "video": "1080p @ 30fps",
        "battery": "~4 hours",
        "weight_frame": "Not confirmed",
        "weight_case": "Not confirmed",
        "water": "IPX4 splash-resistant",
        "audio": "Open-ear speakers + 5 mics",
        "connectivity": "Bluetooth 5.2, Meta AI",
        "availability": "Not sold in India — US only",
        "pros": "Unique round-frame design; appeals to aviator-style customers",
        "cons": "Cannot source in India; no warranty support",
        "rental_conservative": "N/A",
        "rental_premium": "N/A",
        "recommendation": "DO NOT LIST — Unavailable in India"
    },
    {
        "name": "Oakley HSTN Meta",
        "category": "Sporty / Youth Appeal",
        "retail_inr": "₹41,800",
        "camera": "12 MP ultra-wide",
        "video": "1080p @ 30fps",
        "battery": "~4 hours",
        "weight_frame": "38 g",
        "weight_case": "178 g",
        "water": "IPX4 splash-resistant",
        "audio": "Open-ear speakers + 5 mics",
        "connectivity": "Bluetooth 5.2, Meta AI",
        "availability": "Oakley India website",
        "pros": "Lightest frame (38 g); Oakley sport brand appeal; titanium hinge",
        "cons": "Heavy case (178 g); ₹41,800 price; niche sport audience",
        "rental_conservative": "₹450–500/day",
        "rental_premium": "₹650–750/day",
        "recommendation": "PHASE 2 — Add after validating initial demand"
    },
    {
        "name": "Oakley Vanguard Meta",
        "category": "Rugged / Outdoor",
        "retail_inr": "₹52,300",
        "camera": "12 MP ultra-wide",
        "video": "1080p @ 30fps",
        "battery": "~4 hours",
        "weight_frame": "66 g",
        "weight_case": "Not confirmed",
        "water": "IP67 dust-tight + immersion",
        "audio": "Open-ear speakers + 5 mics (loudest)",
        "connectivity": "Bluetooth 5.2, Meta AI",
        "availability": "Oakley India website",
        "pros": "IP67 (only model); rugged build; best audio; premium positioning",
        "cons": "Heaviest frame (66 g); highest price ₹52,300; niche outdoor audience",
        "rental_conservative": "₹550–650/day",
        "rental_premium": "₹800–900/day",
        "recommendation": "PHASE 2 — Premium niche; events, outdoors, adventure tourists"
    },
    {
        "name": "Oakley Sphaera Meta",
        "category": "Sport Wrap",
        "retail_inr": "Not officially confirmed",
        "camera": "Not officially confirmed",
        "video": "Not officially confirmed",
        "battery": "Not officially confirmed",
        "weight_frame": "Not officially confirmed",
        "weight_case": "Not officially confirmed",
        "water": "Not officially confirmed",
        "audio": "Not officially confirmed",
        "connectivity": "Not officially confirmed",
        "availability": "Not sold in India — US only",
        "pros": "Full-wrap sport shield; unique form factor",
        "cons": "Not available in India; unconfirmed specs; cannot source",
        "rental_conservative": "N/A",
        "rental_premium": "N/A",
        "recommendation": "DO NOT LIST — Unavailable / unconfirmed"
    },
    {
        "name": "Ray-Ban Meta Skyler (Gen 1)",
        "category": "Cat-Eye Style",
        "retail_inr": "₹25,000 – ₹27,500 (est.)",
        "camera": "12 MP ultra-wide",
        "video": "1080p @ 30fps",
        "battery": "~4 hours",
        "weight_frame": "~45 g",
        "weight_case": "~130 g",
        "water": "IPX4 splash-resistant",
        "audio": "Open-ear speakers + 5 mics",
        "connectivity": "Bluetooth 5.2, Meta AI",
        "availability": "Limited — select Indian retailers",
        "pros": "Unique cat-eye design for female demographic",
        "cons": "Limited availability; same Gen 1 battery constraints",
        "rental_conservative": "₹400–450/day",
        "rental_premium": "₹550–650/day",
        "recommendation": "PHASE 2 — Niche female demographic; test with limited stock"
    },
]

SCORECARD = [
    ("Demand Signal", "Social buzz + fashion/tech crossover", 4),
    ("Supply Availability", "Strong Ray-Ban; limited Oakley", 4),
    ("Rental Yield Potential", "1.2–2.0% of MRP/day — strong", 4),
    ("Competitive Gap", "No Pune operator in this niche", 5),
    ("Risk Level", "Moderate — tech obsolescence, damage", 3),
]

PROS = [
    "High rental yield (₹400–900/day vs ₹800–1,200/day for lenses)",
    "Strong social media / influencer demand",
    "No Pune competitor in AI glasses rental",
    "Lightweight, durable, low-maintenance product",
    "Gen 2 (8hr battery) enables full-day event use",
    "Fashion accessory + tech gadget = dual appeal",
]

CONS = [
    "High upfront cost (₹22,400–₹52,300 per unit)",
    "Tech obsolescence risk — new models every 12–18 months",
    "Damage/loss exposure (₹40,000+ replacement)",
    "Requires insurance framework (not yet established)",
    "Limited supplier options in India",
    "IPX4 only — water damage risk in Pune monsoons",
]

NEXT_STEPS = [
    ["Week 1–2", "Source 2× Wayfarer Gen 2 (Clear lens)", "Amazon India / Ray-Ban.com"],
    ["Week 2", "Set up insurance / damage deposit workflow", "Credit card hold or UPI block"],
    ["Week 3", "List on website + Instagram stories", "Soft launch, no paid ads"],
    ["Week 3–4", "Track enquiries, bookings, utilization", "Target: 2+ bookings in first 30 days"],
    ["Week 5–6", "Review data, decide on Oakley Phase 2", "If >40% utilization → expand"],
    ["Month 3", "Scale to 4–6 units if demand confirmed", "Add HSTN + Vanguard if warranted"],
]

OPEN_QUESTIONS = [
    "Will Pune customers pay ₹500–900/day for smart glasses vs ₹800–1,200/day for camera lenses?",
    "Is the fashion/tech crossover appeal strong enough in Pune's market?",
    "Can we establish reliable insurance coverage for ₹40,000+ items?",
    "How will monsoon season (Jun–Sep) impact demand and damage risk?",
    "Should we bundle with existing camera rentals or position as standalone?",
]

MARKET_SIGNALS = [
    ("Ray-Ban Meta Gen 2 India Launch", "September 2025", "Official Meta India release"),
    ("Amazon India Search Volume", "Rising", "'Smart glasses' trending up 300%+ YoY"),
    ("Instagram #RayBanMeta", "2.1M+ posts", "Strong fashion/lifestyle crossover"),
    ("Pune Camera Rental Market", "₹15–25 Cr est.", "Growing 15–20% YoY"),
    ("No Pune AI Glasses Operator", "Confirmed", "Zero direct competition currently"),
    ("Event Industry Pune", "₹500+ Cr", "Weddings, corporate, college fests"),
]


# ──────────────────────────────────────────────────────
# TEMPLATE 1: NEW SEGMENT (6 pages)
# ──────────────────────────────────────────────────────

def build_overview_items():
    items = [
        ("Segment", "AI-Powered Smart Glasses Rental"),
        ("Target Market", "Pune, Maharashtra"),
        ("Primary Model", "Ray-Ban Meta Wayfarer Gen 2"),
        ("Investment Range", "₹80,000 – ₹1,60,000 (2–4 units)"),
        ("Daily Rental", "₹500 – ₹900/day (premium tier)"),
        ("Break-Even", "~25–35 rentals per unit"),
    ]
    html = ""
    for label, value in items:
        html += f'''<div class="overview-item">
          <span class="label">{label}</span>
          <span class="value">{value}</span>
        </div>\n'''
    return html


def build_key_facts_table():
    rows = ""
    for m in MODELS:
        if "N/A" in m["retail_inr"] or "Not sold" in m["retail_inr"]:
            continue
        rows += f'''<tr>
          <td><strong>{m["name"]}</strong></td>
          <td>{m["retail_inr"]}</td>
          <td>{m["camera"]}</td>
          <td>{m["battery"]}</td>
          <td>{m["water"]}</td>
        </tr>\n'''
    return f'''<table>
      <thead><tr><th>Model</th><th>Retail (INR)</th><th>Camera</th><th>Battery</th><th>Water Resistance</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>'''


def build_market_body():
    signal_rows = ""
    for name, value, note in MARKET_SIGNALS:
        signal_rows += f'''<tr>
          <td><strong>{name}</strong></td><td>{value}</td><td>{note}</td>
        </tr>\n'''
    return f'''
    <h3>Market Size</h3>
    <p style="margin-bottom: var(--space-6);">The Indian smart glasses market is nascent but accelerating. Ray-Ban Meta Gen 2 launched in India in September 2025. Pune, with its large IT workforce, student population, and thriving events industry, represents an ideal test market for AI glasses rental. No Pune-based operator currently offers smart glasses rental — this is a first-mover opportunity.</p>

    <h3>Pune Demand Signals</h3>
    <table style="margin-bottom: var(--space-8);">
      <thead><tr><th>Signal</th><th>Value</th><th>Significance</th></tr></thead>
      <tbody>{signal_rows}</tbody>
    </table>

    <h3>Comparable Rental Pricing (Pune Market)</h3>
    <table>
      <thead><tr><th>Category</th><th>Daily Rate</th><th>Comparable</th></tr></thead>
      <tbody>
        <tr><td>DSLR Camera Body</td><td>₹800 – ₹1,200/day</td><td>Higher price, similar tech appeal</td></tr>
        <tr><td>GoPro / Action Cam</td><td>₹500 – ₹800/day</td><td>Direct competitor for vloggers</td></tr>
        <tr><td>Premium Sunglasses (non-smart)</td><td>₹200 – ₹400/day</td><td>Lower value, fashion-only</td></tr>
        <tr><td>AI Smart Glasses (new)</td><td>₹500 – ₹900/day</td><td>Our proposed pricing — tech + fashion</td></tr>
      </tbody>
    </table>
    '''


def build_score_bars():
    html = ""
    for label, note, score in SCORECARD:
        pct = score * 20
        html += f'''<div class="score-row">
          <div>
            <div class="score-label">{label}</div>
            <div class="score-note">{note}</div>
          </div>
          <div class="score-bar"><div class="score-fill" style="width: {pct}%;"></div></div>
          <div class="score-num">{score}/5</div>
        </div>\n'''
    return html


def build_pros_cons():
    pros_li = "\n".join(f"<li>{p}</li>" for p in PROS)
    cons_li = "\n".join(f"<li>{c}</li>" for c in CONS)
    return f'''<div class="two-col">
      <div class="col-card pro">
        <h4>Pros / Opportunities</h4>
        <ul style="font-size:13px; line-height:1.7; margin-left:var(--space-4);">{pros_li}</ul>
      </div>
      <div class="col-card con">
        <h4>Cons / Risks</h4>
        <ul style="font-size:13px; line-height:1.7; margin-left:var(--space-4);">{cons_li}</ul>
      </div>
    </div>'''


def build_entry_notes():
    return '''<div class="callout">
      <div class="callout-label">Recommended Entry Strategy</div>
      <div class="callout-body">
        <strong>Start small:</strong> 2× Ray-Ban Meta Wayfarer Gen 2 (Clear lens) for ₹80,000–₹92,000 total investment.
        Test demand over 30–60 days before scaling. If utilization exceeds 40%, add Oakley HSTN + Vanguard in Phase 2.
        All units must have 100% retail-value security deposit (credit card or UPI hold) and mandatory insurance.
      </div>
    </div>'''


def build_recommendation_table():
    rows = ""
    for step in NEXT_STEPS:
        rows += f'''<tr><td>{step[0]}</td><td>{step[1]}</td><td>{step[2]}</td></tr>\n'''
    return f'''<table>
      <thead><tr><th>Timeline</th><th>Action</th><th>Details</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>'''


def build_open_questions():
    return "\n".join(f"<li>{q}</li>" for q in OPEN_QUESTIONS)


def fill_new_segment(template_path):
    with open(template_path, "r") as f:
        html = f.read()

    replacements = {
        # Cover
        "{{DOC_TITLE}}": "AI Glasses Rental Segment",
        "{{DOC_LABEL}}": "New Segment Opportunity",
        "{{DOC_SUBTITLE}}": "Ray-Ban Meta + Oakley Meta — Pune Market Entry",
        "{{DOC_DESCRIPTION}}": "Market research and entry strategy for adding AI-powered smart glasses to the Primes & Zooms rental fleet. Covers specifications, pricing bands, demand signals, and a phased launch plan for Pune.",
        "{{DOC_PREPARED_BY}}": "Market Research Team",
        "{{DOC_DATE}}": "08 Jul 2026",

        # Page 2
        "{{CONTEXT_LABEL}}": "Segment Overview",
        "{{OVERVIEW_ITEMS}}": build_overview_items(),
        "{{SEGMENT_DESC}}": "AI-powered smart glasses (Ray-Ban Meta, Oakley Meta) combine fashion eyewear with built-in cameras, speakers, and Meta AI. They are wearable tech accessories that appeal to content creators, event attendees, tech enthusiasts, and fashion-forward consumers. Rental use cases include vlogging, weddings, college festivals, corporate events, and experiential tourism. The product occupies a unique niche: higher perceived value than action cameras, lower commitment than purchasing, and strong social media appeal.",
        "{{KEY_FACTS_TABLE}}": build_key_facts_table(),

        # Page 3
        "{{MARKET_LABEL}}": "Market & Demand",
        "{{MARKET_BODY}}": build_market_body(),

        # Page 4
        "{{SCORE_LABEL}}": "Opportunity Score",
        "{{SCORE_BARS}}": build_score_bars(),
        "{{TOTAL_SCORE}}": "20",
        "{{TOTAL_VERDICT}}": "Pursue Now",

        # Page 5
        "{{TRADEOFF_LABEL}}": "Trade-offs & Approach",
        "{{PROS_CONS_BLOCK}}": build_pros_cons(),
        "{{ENTRY_NOTES}}": build_entry_notes(),

        # Page 6
        "{{ACTION_LABEL}}": "Recommendation",
        "{{VERDICT_CALLOUT}}": '''<div class="callout">
      <div class="callout-label">Verdict</div>
      <div class="callout-body"><strong>LAUNCH NOW — small test, validate demand, then scale.</strong> The opportunity score of 20/25 ("Pursue Now") reflects strong demand signals, zero competition in Pune, and healthy rental yield potential. Start with 2× Wayfarer Gen 2 for ₹80K–₹92K, test for 30–60 days, and expand only if utilization confirms demand. This is a low-risk, high-upside entry into a new category.</div>
    </div>''',
        "{{RECOMMENDATION_TABLE}}": build_recommendation_table(),
        "{{OPEN_QUESTIONS}}": build_open_questions(),
    }

    for token, value in replacements.items():
        html = html.replace(token, value)

    return html


# ──────────────────────────────────────────────────────
# TEMPLATE 2: SHORT BRIEF (1-2 pages)
# ──────────────────────────────────────────────────────

def fill_short_brief(template_path):
    with open(template_path, "r") as f:
        html = f.read()

    replacements = {
        "{{DOC_TITLE}}": "AI Glasses Rental — Quick Brief",
        "{{DOC_LABEL}}": "Quick Brief",
        "{{DOC_SUBTITLE}}": "Should Primes & Zooms launch AI glasses rental in Pune?",
        "{{DOC_DESCRIPTION}}": "A concise summary of the AI glasses rental opportunity for the Pune market. Covers product overview, pricing strategy, and a recommended go/no-go decision with phased rollout plan.",
        "{{DOC_PREPARED_BY}}": "Market Research Team",
        "{{DOC_DATE}}": "08 Jul 2026",

        # Page 1
        "{{CONTEXT_LABEL}}": "Executive Summary",
        "{{QUICK_SUMMARY}}": "AI-powered smart glasses (Ray-Ban Meta Gen 2) represent a viable new rental segment for Primes & Zooms. The Pune market has zero direct competitors, strong social media demand, and rental yields of ₹500–900/day (1.2–2.0% of retail MRP). We recommend launching with 2× Ray-Ban Meta Wayfarer Gen 2 for ₹80K–₹92K total investment, testing demand over 30–60 days, and scaling only if utilization exceeds 40%. This is a low-risk, high-upside category entry.",

        "{{KEY_POINTS}}": """
        <li><strong>Zero competition in Pune</strong> — no operator currently offers AI glasses rental</li>
        <li><strong>Strong demand signal</strong> — Ray-Ban Meta Gen 2 trending on Instagram (2.1M+ posts), Amazon India search volume rising 300%+ YoY</li>
        <li><strong>Healthy rental yield</strong> — ₹500–900/day vs ₹80K–₹52K purchase cost (25–35 rentals to break even)</li>
        <li><strong>Start small, validate</strong> — 2× Gen 2 units, ₹80K–₹92K total, 30–60 day test period</li>
        <li><strong>Phased expansion</strong> — add Oakley HSTN + Vanguard in Phase 2 if demand confirmed</li>
        """,

        "{{QUICK_VERDICT}}": "<strong>GO — Launch with 2× Wayfarer Gen 2 (Clear lens) immediately.</strong> Test demand for 30–60 days. If utilization >40%, expand to 4–6 units including Oakley models. Security deposit = 100% retail value. Mandatory insurance required.",

        # Page 2
        "{{DETAIL_LABEL}}": "Pricing & Models",
        "{{DETAIL_TITLE}}": "Recommended Models & Pricing Bands",
        "{{DETAIL_BODY}}": """
    <h3>Recommended Models (Phase 1)</h3>
    <table>
      <thead><tr><th>Model</th><th>Retail</th><th>1-Day</th><th>2-4 Days</th><th>5-8 Days</th><th>9+ Days</th></tr></thead>
      <tbody>
        <tr><td><strong>Wayfarer Gen 2</strong> (Clear)</td><td>₹45,700</td><td>₹850</td><td>₹750/day</td><td>₹600/day</td><td>₹500/day</td></tr>
        <tr><td><strong>Wayfarer Gen 2</strong> (G-15)</td><td>₹39,900</td><td>₹750</td><td>₹650/day</td><td>₹525/day</td><td>₹425/day</td></tr>
      </tbody>
    </table>

    <h3>Phase 2 Expansion (if demand confirmed)</h3>
    <table>
      <thead><tr><th>Model</th><th>Retail</th><th>1-Day</th><th>2-4 Days</th><th>5-8 Days</th><th>9+ Days</th></tr></thead>
      <tbody>
        <tr><td><strong>Oakley HSTN</strong></td><td>₹41,800</td><td>₹750</td><td>₹650/day</td><td>₹525/day</td><td>₹425/day</td></tr>
        <tr><td><strong>Oakley Vanguard</strong></td><td>₹52,300</td><td>₹900</td><td>₹775/day</td><td>₹650/day</td><td>₹525/day</td></tr>
      </tbody>
    </table>

    <h3>Key Financial Metrics</h3>
    <table>
      <thead><tr><th>Metric</th><th>Conservative</th><th>Premium</th></tr></thead>
      <tbody>
        <tr><td>Initial Investment (2 units)</td><td>₹80,000</td><td>₹92,000</td></tr>
        <tr><td>Avg. Daily Rate</td><td>₹500–600</td><td>₹750–850</td></tr>
        <tr><td>Break-Even Rentals/Unit</td><td>~30–35</td><td>~25–30</td></tr>
        <tr><td>Monthly Revenue (2 units @ 30% util.)</td><td>₹9,000–₹10,800</td><td>₹13,500–₹15,300</td></tr>
        <tr><td>Payback Period</td><td>~9–12 months</td><td>~6–8 months</td></tr>
      </tbody>
    </table>
    """,
    }

    for token, value in replacements.items():
        html = html.replace(token, value)

    return html


# ──────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────

def main():
    # 1. New Segment (6-page)
    tpl1 = os.path.join(TEMPLATE_DIR, "research-template-new-segment.html")
    out1 = os.path.join(OUTPUT_DIR, "ai-glasses-rental-opportunity.html")
    filled = fill_new_segment(tpl1)
    # Verify no remaining tokens
    import re
    remaining = re.findall(r'\{\{[A-Z_]+\}\}', filled)
    if remaining:
        print(f"WARNING: Unreplaced tokens in new-segment: {remaining}")
    with open(out1, "w") as f:
        f.write(filled)
    print(f"✓ Written: {out1}")

    # 2. Short Brief (1-2 page)
    tpl2 = os.path.join(TEMPLATE_DIR, "research-template-short-brief.html")
    out2 = os.path.join(OUTPUT_DIR, "ai-glasses-rental-quick-brief.html")
    filled2 = fill_short_brief(tpl2)
    remaining2 = re.findall(r'\{\{[A-Z_]+\}\}', filled2)
    if remaining2:
        print(f"WARNING: Unreplaced tokens in short-brief: {remaining2}")
    with open(out2, "w") as f:
        f.write(filled2)
    print(f"✓ Written: {out2}")

    print(f"\nDone. {2} reports generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
