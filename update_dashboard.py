#!/usr/bin/env python3
"""
Sales Dashboard Auto-Updater
Run: python update_dashboard.py
Downloads the latest data from Google Sheets, updates the dashboard, and pushes to GitHub.
"""
import urllib.request
import urllib.error
import json
import re
import subprocess
import sys
import os
import shutil
from datetime import datetime

SHEET_ID       = '1kDStST-tcRZqB8OXfjtuoNqcTtYVv6W5ew0w0eZaPsI'
APPS_SCRIPT_URL = ('https://script.google.com/macros/s/'
                   'AKfycbwEGFMhe8R_nKAo8M0_oDRPXSPkRh7lZHA8LQI43yW9P-xHyBLZ5QgLh0WVANZr8e14/exec')
EXPORT_URL     = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=xlsx'

WORKDIR    = r'd:\Sales insights'
EXCEL      = os.path.join(WORKDIR, 'Sales Ledger 2026.xlsx')
DASHBOARD  = os.path.join(WORKDIR, 'Sales_Dashboard.html')

# Maps scorecard element ID → data key
SCORECARD_IDS = {
    'sc-total-revenue':   ('totalRevenue',),
    'sc-collected':       ('collected',),
    'sc-outstanding':     ('outstanding',),
    'sc-total-orders':    ('totalOrders',),
    'sc-aov':             ('aov',),
    'sc-active-cust':     ('activeCust',),
    'sc-fulfillment':     ('fulfRate',),
    'sc-pay-invoiced':    ('totalRevenue',),
    'sc-pay-collected':   ('collected',),
    'sc-pay-outstanding': ('outstanding',),
}

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def try_download_excel():
    print('Downloading latest Excel from Google Sheets...')
    try:
        data = fetch(EXPORT_URL)
        if os.path.exists(EXCEL):
            shutil.copy2(EXCEL, EXCEL + '.bak')
        with open(EXCEL, 'wb') as f:
            f.write(data)
        size_kb = len(data) // 1024
        print(f'  Downloaded {size_kb} KB — saved to Sales Ledger 2026.xlsx')
        return True
    except Exception as e:
        print(f'  Could not auto-download (sheet may need public access): {e}')
        print('  Using existing local Excel file instead.')
        return False

def try_apps_script():
    print('Fetching live data from Apps Script...')
    try:
        raw = fetch(APPS_SCRIPT_URL)
        d = json.loads(raw.decode('utf-8'))
        if 'error' in d:
            print(f'  Apps Script error: {d["error"]}')
            return None
        months = d.get('monthly', {}).get('labels', [])
        print(f'  Apps Script returned {len(months)} months: {months}')
        return d
    except Exception as e:
        print(f'  Apps Script fetch failed: {e}')
        return None

def run_extraction():
    print('Extracting data from Excel...')
    result = subprocess.run(
        [sys.executable, 'extract_data.py'],
        cwd=WORKDIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        print('  Extraction failed:', result.stderr[:300])
        return None
    try:
        d = json.loads(result.stdout)
        months = d.get('monthly', {}).get('labels', [])
        print(f'  Extracted {len(months)} months: {months}')
        return d
    except Exception as e:
        print(f'  JSON parse error: {e}')
        return None

def update_html(data):
    print('Updating Sales_Dashboard.html...')
    with open(DASHBOARD, encoding='utf-8') as f:
        html = f.read()

    # ── 1. Replace STATIC_DATA ──────────────────────────────────────
    marker = 'const STATIC_DATA = '
    pos = html.find(marker)
    if pos == -1:
        print('  ERROR: STATIC_DATA marker not found')
        return False
    pos += len(marker)
    depth = 0
    end = pos
    for i, ch in enumerate(html[pos:], pos):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    html = html[:pos] + json.dumps(data, separators=(',', ':')) + html[end:]

    # ── 2. Update date chip ─────────────────────────────────────────
    months = data['monthly']['labels']
    if months:
        chip_text = f"{months[0][:3]} – {months[-1]} 2026"
        html = re.sub(
            r'(id="date-chip"[^>]*>)[^<]*(</)',
            rf'\g<1>{chip_text}\g<2>',
            html
        )

    # ── 3. Update scorecard data-count values ───────────────────────
    sc = data['scorecards']
    for elem_id, (key,) in SCORECARD_IDS.items():
        val = sc.get(key, 0)
        html = re.sub(
            rf'(id="{elem_id}"[^>]*data-count=")[^"]+(")',
            rf'\g<1>{val}\g<2>',
            html
        )

    # ── 4. Rebuild monthly revenue scorecards ───────────────────────
    html = rebuild_monthly_scorecards(html, data)

    with open(DASHBOARD, 'w', encoding='utf-8') as f:
        f.write(html)
    print('  HTML updated.')
    return True


def rebuild_monthly_scorecards(html, data):
    month_labels   = data['monthly']['labels']
    month_revenues = data['monthly']['revenue']
    if not month_labels:
        return html

    COLORS = ['#6c63ff','#00d4aa','#ff9f43','#ff6b6b','#a29bfe',
              '#74b9ff','#fd79a8','#55efc4','#fdcb6e','#e17055','#81ecec','#dfe6e9']

    current_month = datetime.now().month
    month_name_to_num = {
        'January':1,'February':2,'March':3,'April':4,'May':5,'June':6,
        'July':7,'August':8,'September':9,'October':10,'November':11,'December':12
    }

    cards_html = []
    for i, (label, rev) in enumerate(zip(month_labels, month_revenues)):
        color = COLORS[i % len(COLORS)]
        short = label[:3]
        mnum  = month_name_to_num.get(label, i+1)

        # Growth label
        if i == 0:
            pct_text = ''
        else:
            prev = month_revenues[i-1]
            pct  = (rev - prev) / prev * 100 if prev else 0
            sign = '+' if pct >= 0 else ''
            pct_text = f'({sign}{pct:.1f}%)'

        # Is this the current in-progress month?
        in_progress = (mnum == current_month)
        sub_text    = 'Month in progress' if in_progress else 'Monthly total'
        if not in_progress and not pct_text:
            sub_text = 'Opening month'

        label_inner = (f'{short} Revenue '
                       f'<span class="sc-pct">'
                       f'{"in progress" if in_progress else pct_text}'
                       f'</span>')

        cards_html.append(
            f'<div class="scorecard" style="--card-color:{color}">\n'
            f' <div class="sc-label">{label_inner}</div>\n'
            f' <div class="sc-value" data-count="{rev}" data-prefix="GHS " data-format="currency">GHS 0</div>\n'
            f' <div class="sc-sub">{sub_text}</div>\n'
            f' </div>'
        )

    new_block = '\n '.join(cards_html)

    # Replace the existing monthly scorecard block (from first "Jan Revenue" card to last closing </div>)
    old = re.search(
        r'<div class="scorecard"[^>]*>\s*<div class="sc-label">Jan Revenue.*?'
        r'<div class="sc-sub">[^<]*</div>\s*</div>\s*</div>',
        html, re.DOTALL
    )
    if old:
        html = html[:old.start()] + new_block + '\n </div>' + html[old.end():]
        print(f'  Monthly scorecards rebuilt: {len(month_labels)} months')
    else:
        print('  WARNING: could not locate monthly scorecard block — values patched instead')
        for i, (label, rev) in enumerate(zip(month_labels, month_revenues)):
            short = label[:3]
            html = re.sub(
                rf'(<div class="sc-label">{short} Revenue.*?data-count=")[^"]+(")',
                rf'\g<1>{rev}\g<2>',
                html, flags=re.DOTALL
            )
    return html

def git_push(months):
    last = months[-1] if months else 'latest'
    msg  = f'Auto-update: data through {last} 2026 [{datetime.now().strftime("%d %b %Y")}]'
    print(f'Pushing to GitHub — "{msg}"')
    for cmd in [
        ['git', 'add', 'Sales_Dashboard.html'],
        ['git', 'commit', '-m', msg],
        ['git', 'push'],
    ]:
        r = subprocess.run(cmd, cwd=WORKDIR, capture_output=True, text=True)
        label = ' '.join(cmd[:2])
        if r.returncode == 0 or 'nothing to commit' in (r.stdout + r.stderr):
            out = (r.stdout + r.stderr).strip().splitlines()
            print(f'  {label}: {out[-1] if out else "OK"}')
        else:
            print(f'  {label} ERROR: {r.stderr.strip()[:200]}')

if __name__ == '__main__':
    print('=' * 58)
    print('  Sales Dashboard Auto-Updater')
    print(f'  {datetime.now().strftime("%d %B %Y  %H:%M")}')
    print('=' * 58)

    # 1. Try to download fresh Excel from Google Sheets
    try_download_excel()

    # 2. Get data from Apps Script (live Google Sheets)
    live = try_apps_script()

    # 3. Extract from Excel (always done — catches any offline changes too)
    excel = run_extraction()

    # 4. Pick the most complete / up-to-date source
    live_m  = len(live['monthly']['labels'])  if live  else 0
    excel_m = len(excel['monthly']['labels']) if excel else 0

    if excel_m >= live_m and excel:
        print(f'\nBest source: Excel ({excel_m} months)')
        best = excel
    elif live:
        print(f'\nBest source: Apps Script ({live_m} months)')
        best = live
    else:
        print('\nNo data available. Aborting.')
        sys.exit(1)

    # 5. Update dashboard HTML
    if not update_html(best):
        sys.exit(1)

    # 6. Push to GitHub Pages
    git_push(best['monthly']['labels'])

    print()
    print('All done! Dashboard is live at:')
    print('  https://emehub.github.io/Sales-analysis/Sales_Dashboard.html')
