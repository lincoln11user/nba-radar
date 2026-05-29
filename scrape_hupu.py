"""
Scrape Hupu NBA stats pages and output players.json for the radar chart.
Hupu pages are server-rendered HTML tables — no API key needed.

Stats from 8 categories:
  pts (得分), asts (助攻), reb (篮板), stl (抢断), blk (盖帽),
  fgp (投篮%), tpp (三分%), ftp (罚球%)

Run: python scrape_hupu.py
Output: players.json (minified) and players_pretty.json (readable)
"""
import urllib.request
import urllib.error
import re
import json
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = "https://nba.hupu.com/stats/players"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# ── helpers ──────────────────────────────────────────────
def fetch(url, timeout=15):
    """Fetch URL, return decoded HTML or '' on failure."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  WARN: {url} → {e}")
        return ""

def parse_table(html):
    """Parse the first <table> in html into a list of dicts keyed by header row."""
    # Find table
    m = re.search(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
    if not m:
        return []
    table = m.group(1)
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL)
    result = []
    headers = []
    for row in rows:
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.DOTALL)
        clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
        if not clean:
            continue
        if not headers:
            headers = clean
        else:
            result.append(dict(zip(headers, clean)))
    return result, headers

# ── per-category parsers ─────────────────────────────────
def scrape_category(cat):
    """Scrape one stat category, return {player_name: {fields}}."""
    url = f"{BASE}/{cat}"
    print(f"  Fetching {url} ...")
    html = fetch(url)
    if not html:
        return {}
    rows, headers = parse_table(html)
    data = {}
    for r in rows:
        name = r.get('球员', '')
        if not name:
            continue
        # Parse numeric values where possible
        parsed = {}
        for k, v in r.items():
            if k == '排名':
                continue
            # Try to extract number from strings like "47.6%" or "10.80-22.80"
            v_clean = v.replace('%', '').strip()
            try:
                parsed[k] = float(v_clean)
            except ValueError:
                # Could be a ranged stat like "10.80-22.80" — keep both
                if '-' in v_clean and v_clean.count('-') == 1:
                    parts = v_clean.split('-')
                    try:
                        parsed[k] = [float(parts[0]), float(parts[1])]
                    except ValueError:
                        parsed[k] = v
                else:
                    parsed[k] = v
        data[name] = parsed
    print(f"    → {len(data)} players")
    return data

# ── merge helpers ────────────────────────────────────────
def safe_float(v, default=0.0):
    """Unwrap value: float, list→first element, or default."""
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, list) and len(v) > 0:
        return float(v[0])
    try:
        return float(v)
    except (ValueError, TypeError):
        return default

# ── main ─────────────────────────────────────────────────
def main():
    print("Scraping Hupu NBA stats (8 categories)...\n")

    categories = ['pts', 'asts', 'reb', 'stl', 'blk', 'fgp', 'tpp', 'ftp']
    cat_data = {}
    for cat in categories:
        cat_data[cat] = scrape_category(cat)
        time.sleep(0.5)  # be polite

    # ── merge all categories by player name ──
    print("\nMerging categories by player name...")
    # Collect all player names
    all_names = set()
    for cat in categories:
        all_names.update(cat_data[cat].keys())
    print(f"  Total unique players: {len(all_names)}")

    # Build merged dict
    merged = {}
    for name in all_names:
        p = {'name': name, 'team': '', 'gp': 0, 'mpg': 0.0}
        # Merge from each category
        for cat in categories:
            if name in cat_data[cat]:
                d = cat_data[cat][name]
                # Extract team and gp (appear in most categories)
                if d.get('球队'):
                    p['team'] = d['球队']
                gp = safe_float(d.get('场次', 0))
                if gp > 0:
                    p['gp'] = int(gp)
                mpg = safe_float(d.get('上场时间', d.get('时间', 0)))
                if mpg > 0:
                    p['mpg'] = mpg
                # Merge stats
                for k, v in d.items():
                    if k in ('球员', '球队', '场次', '排名'):
                        continue
                    # Prefer the first value we see, but if already exists, keep existing
                    if k not in p:
                        p[k] = v

        # Extract key derived stats
        raw = cat_data['pts'].get(name, {})
        p['pts'] = safe_float(raw.get('得分', 0))
        p['fgm'] = safe_float(raw.get('命中', 0)) if '命中' in raw else 0
        p['fga'] = 0
        if '命中-出手' in raw and isinstance(raw['命中-出手'], list):
            p['fgm'] = raw['命中-出手'][0]
            p['fga'] = raw['命中-出手'][1]
        p['fg_pct'] = safe_float(raw.get('命中率', 0))

        p['tpm'] = 0
        p['tpa'] = 0
        if '命中-三分' in raw and isinstance(raw['命中-三分'], list):
            p['tpm'] = raw['命中-三分'][0]
            p['tpa'] = raw['命中-三分'][1]
        p['tp_pct'] = safe_float(raw.get('三分命中率', 0))

        p['ftm'] = 0
        p['fta'] = 0
        if '命中-罚球' in raw and isinstance(raw['命中-罚球'], list):
            p['ftm'] = raw['命中-罚球'][0]
            p['fta'] = raw['命中-罚球'][1]
        p['ft_pct'] = safe_float(raw.get('罚球命中率', 0))

        # From other categories — use the actual Chinese headers from Hupu
        ast_data = cat_data['asts'].get(name, {})
        p['ast'] = safe_float(ast_data.get('助攻数', 0))

        reb_data = cat_data['reb'].get(name, {})
        p['reb'] = safe_float(reb_data.get('篮板数', 0))
        p['oreb'] = safe_float(reb_data.get('进攻篮板', 0))
        p['dreb'] = safe_float(reb_data.get('防守篮板', 0))

        stl_data = cat_data['stl'].get(name, {})
        p['stl'] = safe_float(stl_data.get('抢断数', 0))

        blk_data = cat_data['blk'].get(name, {})
        p['blk'] = safe_float(blk_data.get('盖帽数', 0))

        merged[name] = p

    # ── filter: only players with reasonable GP (>= 20) ──
    qualified = {n: p for n, p in merged.items() if p['gp'] >= 20 and p['mpg'] >= 10}
    print(f"  Qualified (GP>=20, MPG>=10): {len(qualified)}")

    # ── sort by PTS descending ──
    sorted_players = sorted(qualified.values(), key=lambda x: x['pts'], reverse=True)

    # ── output ──
    print(f"\nWriting {len(sorted_players)} players to players.json ...")
    with open('players_raw.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_players, f, ensure_ascii=False, indent=2)
    print("Done → players_raw.json")

    # Show top 10
    print("\nTop 10 by PTS:")
    for i, p in enumerate(sorted_players[:10]):
        print(f"  {i+1}. {p['name']} ({p['team']}) "
              f"PTS:{p['pts']:.1f} AST:{p['ast']:.1f} REB:{p['reb']:.1f} "
              f"FG%:{p['fg_pct']:.1f} 3P%:{p['tp_pct']:.1f} "
              f"STL:{p['stl']:.1f} BLK:{p['blk']:.1f}")

if __name__ == '__main__':
    main()
