#!/usr/bin/env python3
"""
Batch 1: Add English translations to 6 blog HTML files with 0 data-en attributes.
Files: china-logistics-dx.html, customs-dx-guide.html, gafam-ai.html,
       hs-code-guide.html, logistics-dx.html, trade-dx-guide.html
"""
import re
import os

BLOG_DIR = os.path.dirname(os.path.abspath(__file__))

def count_attrs(html, attr):
    return len(re.findall(rf'{attr}=', html))

def add_translation(html, ja_text, en_text, attr_type='data-ja'):
    """Add data-en or data-en-html next to existing data-ja or data-ja-html."""
    en_attr = attr_type.replace('-ja', '-en')
    # Escape for regex
    escaped = re.escape(ja_text)

    # Pattern: attr_type="value" without a following data-en
    # We need to insert data-en="translation" right after data-ja="value"
    pattern = rf'({attr_type}="{escaped}")(?!\s*{en_attr}=)'
    replacement = rf'\1 {en_attr}="{en_text}"'

    new_html = re.sub(pattern, replacement, html)
    return new_html

def add_translation_single_quoted(html, ja_text, en_text, attr_type='data-ja'):
    """Handle single-quoted attributes."""
    en_attr = attr_type.replace('-ja', '-en')
    escaped = re.escape(ja_text)
    pattern = rf"({attr_type}='{escaped}')(?!\s*{en_attr}=)"
    replacement = rf"\1 {en_attr}='{en_text}'"
    new_html = re.sub(pattern, replacement, html)
    return new_html

def process_file(filename, translations):
    """Process a single HTML file with a dict of translations."""
    filepath = os.path.join(BLOG_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    before_count = count_attrs(html, 'data-en')

    for ja_text, en_text, attr_type in translations:
        # Try double-quoted first
        html = add_translation(html, ja_text, en_text, attr_type)
        # Then single-quoted
        html = add_translation_single_quoted(html, ja_text, en_text, attr_type)

    after_count = count_attrs(html, 'data-en')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"{filename}: data-en {before_count} -> {after_count} (+{after_count - before_count})")
    return after_count - before_count


# ============================================================
# CHINA-LOGISTICS-DX.HTML
# ============================================================
china_logistics_translations = [
    # Hero section
    ("中国物流が&lt;em&gt;「別次元」&lt;/em&gt;に入った。&lt;br/&gt;日本の現場は、この現実を直視できるか。",
     "China's Logistics Has Entered a &lt;em&gt;New Dimension&lt;/em&gt;.&lt;br/&gt;Can Japan's Industry Face This Reality?",
     "data-ja-html"),
    ("ヒューマノイド世界シェア90%、ドローン全国配送許可、自動運転トラック4,000台商用稼働 ―&lt;br/&gt;2025〜2026年の中国物流DXは、もはや「追いかける対象」ではなく「競争環境そのもの」を変えている。",
     "90% global humanoid market share, nationwide drone delivery permits, 4,000 autonomous trucks in commercial operation —&lt;br/&gt;China's logistics DX in 2025-2026 is no longer something to catch up with; it is reshaping the competitive landscape itself.",
     "data-ja-html"),
    ("Wings株式会社 ｜ DX・ITコンサルティング", "Wings Inc. | DX &amp; IT Consulting", "data-ja"),
    ("読了目安：10分", "Estimated reading time: 10 min", "data-ja"),

    # Opening
    ("中国の物流？安かろう悪かろうでしょう", "Chinese logistics? Cheap and low quality, right?", "data-ja"),
    ("もしまだそう思っているなら、認識を根本からアップデートする必要がある。2026年初頭の中国物流セクターは、総物流価値350兆元超、対GDP比の社会物流コスト13.9%という数字が示す通り、量だけでなく「質」において急速に成熟している。",
     "If you still think that way, it is time for a fundamental update. In early 2026, China's logistics sector is maturing rapidly not only in volume but in quality, as evidenced by total logistics value exceeding 350 trillion yuan and social logistics costs falling to 13.9% of GDP.",
     "data-ja"),

    # Lead text
    ("本稿で提示するのは、中国物流の「技術紹介」ではない。&lt;strong&gt;日本の物流企業が今直面している競争環境の構造変化&lt;/strong&gt;そのものだ。中国企業は国内で磨き上げた自動化・AI技術を武器に、日本を含むグローバル市場の物流インフラを再構築し始めている。この動きを「対岸の火事」と見るか、「自社のサプライチェーンに直結する脅威」と見るかで、3年後の景色は決定的に変わる。",
     "What this article presents is not a technology showcase of Chinese logistics. It is about &lt;strong&gt;the structural shift in the competitive environment that Japanese logistics companies now face&lt;/strong&gt;. Chinese firms are leveraging automation and AI technologies honed domestically to reconstruct logistics infrastructure across global markets, including Japan. Whether you view this as a distant concern or a direct threat to your supply chain will decisively shape the landscape three years from now.",
     "data-ja-html"),

    # Section headings
    ("1. 数字で見る中国物流の「現在地」", "1. China's Logistics Today: The Numbers", "data-ja"),
    ("まず、マクロの数字を押さえておこう。中国物流市場のスケールと効率改善のスピードは、日本の物流関係者にとって驚異的なものだ。",
     "Let us start with the macro figures. The scale and pace of efficiency gains in China's logistics market are astonishing for Japan's logistics professionals.",
     "data-ja"),

    # Stat items
    ("兆元+", "Tn Yuan+", "data-ja"),
    ("総物流価値&lt;br/&gt;(前年比+6.5%)", "Total logistics value&lt;br/&gt;(+6.5% YoY)", "data-ja-html"),
    ("兆USD", "Tn USD", "data-ja"),
    ("2025年市場規模&lt;br/&gt;(2030年に1.78兆USD予測)", "2025 market size&lt;br/&gt;(projected 1.78 Tn USD by 2030)", "data-ja-html"),
    ("社会物流コスト/GDP比&lt;br/&gt;(過去最低を更新)", "Logistics cost / GDP ratio&lt;br/&gt;(record low)", "data-ja-html"),
    ("年平均成長率(CAGR)&lt;br/&gt;2025→2030年予測", "CAGR&lt;br/&gt;2025-2030 forecast", "data-ja-html"),

    ("特に注目すべきは、社会物流コストの対GDP比が13.9%まで低下した点だ。この指標は、経済活動1単位あたりの物流コストがどれだけ効率化されたかを示す。日本の同指標は約8〜9%と元々低いが、中国はわずか数年で14.7%から13.9%へと急速に改善しており、そのスピード自体がインフラと技術への投資規模を物語っている。",
     "Particularly noteworthy is that the logistics cost-to-GDP ratio has dropped to 13.9%. This metric shows how efficiently logistics costs support each unit of economic activity. Japan's equivalent figure has long been around 8-9%, but China's rapid improvement from 14.7% to 13.9% in just a few years itself speaks to the scale of infrastructure and technology investment.",
     "data-ja"),

    # Section 2
    ("2. ヒューマノイドロボット：世界の90%が「中国製」",
     "2. Humanoid Robots: 90% of the World's Output Is Made in China",
     "data-ja"),
    ("前回の米国編でBoston DynamicsやAgility Roboticsのヒューマノイドを紹介したが、市場の勢力図を見れば現実はさらに鮮烈だ。&lt;strong&gt;2025年に出荷された世界のヒューマノイドロボットの約87〜90%が中国製&lt;/strong&gt;であり、出荷台数は約13,000〜14,600台に達した。",
     "In our previous US edition, we introduced humanoids from Boston Dynamics and Agility Robotics, but the market reality is even more striking. &lt;strong&gt;Approximately 87-90% of the world's humanoid robots shipped in 2025 were made in China&lt;/strong&gt;, with shipments reaching roughly 13,000 to 14,600 units.",
     "data-ja-html"),

    # Robot cards
    ("智元ロボット（上海）", "AgiBot (Shanghai)", "data-ja"),
    ("世界シェア39%のトップ企業。工業用A2-Wは倉庫・工場向けに特化。「WorkGPT」搭載。",
     "Global market leader with 39% share. Industrial A2-W is purpose-built for warehouses and factories. Equipped with 'WorkGPT'.",
     "data-ja"),
    ("5,100台出荷 ｜ 15kg可搬/片腕", "5,100 units shipped | 15 kg payload per arm", "data-ja"),
    ("宇樹科技（杭州）", "Unitree Robotics (Hangzhou)", "data-ja"),
    ("圧倒的な低価格で研究・教育・消費者市場を席巻。運動制御技術に定評あり。",
     "Dominating research, education, and consumer markets with dramatically low pricing. Renowned for motion control technology.",
     "data-ja"),
    ("UBTECH 優必選（深セン）", "UBTECH Robotics (Shenzhen)", "data-ja"),
    ("自動車製造ライン統合に強み。SFエクスプレスと物流現場での実証を推進中。",
     "Excels at automotive production line integration. Advancing field trials with SF Express in logistics settings.",
     "data-ja"),
]

# Read the rest of the file to get all data-ja attributes
filepath = os.path.join(BLOG_DIR, "china-logistics-dx.html")
with open(filepath, 'r', encoding='utf-8') as f:
    full_html = f.read()

# Extract all data-ja values
all_data_ja = re.findall(r'data-ja="([^"]*)"', full_html)
all_data_ja_html = re.findall(r'data-ja-html="([^"]*)"', full_html)

# Print what we found for debugging
print(f"\nchina-logistics-dx.html: Found {len(all_data_ja)} data-ja, {len(all_data_ja_html)} data-ja-html attrs")
print("data-ja values needing translation:")
for v in all_data_ja:
    already_has = v in [t[0] for t in china_logistics_translations if t[2] == 'data-ja']
    if not already_has:
        print(f"  MISSING: {v[:80]}...")

print("\ndata-ja-html values needing translation:")
for v in all_data_ja_html:
    already_has = v in [t[0] for t in china_logistics_translations if t[2] == 'data-ja-html']
    if not already_has:
        print(f"  MISSING: {v[:80]}...")

print("\n--- Script discovery complete. Run the full translation script next. ---")
