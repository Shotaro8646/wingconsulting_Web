#!/usr/bin/env python3
"""Extract all unique data-ja and data-ja-html values from each file for translation."""
import re, os, sys, json

sys.stdout.reconfigure(encoding='utf-8')

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = [
    "china-logistics-dx.html", "customs-dx-guide.html", "gafam-ai.html",
    "hs-code-guide.html", "logistics-dx.html", "trade-dx-guide.html",
    "dx-consulting-guide.html", "global-it-organization-model.html", "pfas-global-regulation-2026.html",
    "chemical-import-automation.html", "dark-funnel-b2b.html", "exhibition-lead-ma.html",
    "first-party-data-b2b.html", "geo-aeo-ai-search-b2b.html", "gtm-engineer-b2b-japan.html",
    "ma-tool-data-foundation.html", "poc-death-dx-consulting.html", "supply-chain-resilience-ai.html",
    "trade-dx-complete-guide.html", "trade-dx-success-failure.html", "trade-operations-overview.html",
    "vibe-marketing-b2b.html", "b2b-saas-kpi-intent-data.html",
]

for filename in FILES:
    filepath = os.path.join(BLOG_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Find all data-ja="..." without following data-en="..."
    # Double-quoted
    ja_vals = set()
    for m in re.finditer(r'data-ja="([^"]*)"', html):
        # Check if data-en follows
        after = html[m.end():m.end()+100]
        if not re.match(r'\s*data-en=', after):
            ja_vals.add(m.group(1))

    ja_html_vals = set()
    for m in re.finditer(r'data-ja-html="([^"]*)"', html):
        after = html[m.end():m.end()+100]
        if not re.match(r'\s*data-en-html=', after):
            ja_html_vals.add(m.group(1))

    # Single-quoted
    for m in re.finditer(r"data-ja='([^']*)'", html):
        after = html[m.end():m.end()+100]
        if not re.match(r"\s*data-en=", after):
            ja_vals.add(m.group(1))

    for m in re.finditer(r"data-ja-html='([^']*)'", html):
        after = html[m.end():m.end()+100]
        if not re.match(r"\s*data-en-html=", after):
            ja_html_vals.add(m.group(1))

    if ja_vals or ja_html_vals:
        print(f"\n=== {filename} ===")
        print(f"  data-ja needing translation: {len(ja_vals)}")
        print(f"  data-ja-html needing translation: {len(ja_html_vals)}")
        # Print short vals (< 50 chars) - these are labels, headers, short text
        short_ja = sorted([v for v in ja_vals if len(v) < 60])
        if short_ja:
            print(f"  Short data-ja values ({len(short_ja)}):")
            for v in short_ja[:10]:
                print(f"    - {v}")
            if len(short_ja) > 10:
                print(f"    ... and {len(short_ja)-10} more")
