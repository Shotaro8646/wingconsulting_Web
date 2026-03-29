#!/usr/bin/env python3
"""Discover all data-ja/data-ja-html values across all 23 files that need translation."""
import re, os, json, sys

sys.stdout.reconfigure(encoding='utf-8')

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = [
    # 0 data-en
    "china-logistics-dx.html", "customs-dx-guide.html", "gafam-ai.html",
    "hs-code-guide.html", "logistics-dx.html", "trade-dx-guide.html",
    # 1 data-en
    "dx-consulting-guide.html", "global-it-organization-model.html", "pfas-global-regulation-2026.html",
    # 4 data-en
    "chemical-import-automation.html", "dark-funnel-b2b.html", "exhibition-lead-ma.html",
    "first-party-data-b2b.html", "geo-aeo-ai-search-b2b.html", "gtm-engineer-b2b-japan.html",
    "ma-tool-data-foundation.html", "poc-death-dx-consulting.html", "supply-chain-resilience-ai.html",
    "trade-dx-complete-guide.html", "trade-dx-success-failure.html", "trade-operations-overview.html",
    "vibe-marketing-b2b.html",
    # 25 data-en
    "b2b-saas-kpi-intent-data.html",
]

for filename in FILES:
    filepath = os.path.join(BLOG_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    data_ja_count = len(re.findall(r'data-ja=', html))
    data_ja_html_count = len(re.findall(r'data-ja-html=', html))
    data_en_count = len(re.findall(r'data-en=', html))
    data_en_html_count = len(re.findall(r'data-en-html=', html))

    total_ja = data_ja_count + data_ja_html_count
    total_en = data_en_count + data_en_html_count
    need = total_ja - total_en

    print(f"{filename}: ja={data_ja_count}+{data_ja_html_count}={total_ja}, en={data_en_count}+{data_en_html_count}={total_en}, need={need}")
