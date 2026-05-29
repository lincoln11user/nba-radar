"""
Scrape Hupu NBA stats → players.json (12-axis format for radar chart).
Run: python build_players.py
Output: players.json
"""
import urllib.request
import re
import json
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = "https://nba.hupu.com/stats/players"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
CATEGORIES = ['pts', 'asts', 'reb', 'stl', 'blk']

# ── position map (extensive) ─────────────────────────────
POSITIONS = {
    # PG
    '卢卡-东契奇': 'PG', '斯蒂芬-库里': 'PG', '贾-莫兰特': 'PG',
    '达龙-福克斯': 'PG', '特雷-杨': 'PG', '泰雷斯-哈利伯顿': 'PG',
    '詹姆斯-哈登': 'PG', '凯里-欧文': 'PG', '达米安-利拉德': 'PG',
    '拉梅洛-鲍尔': 'PG', '贾马尔-默里': 'PG', '弗雷德-范弗利特': 'PG',
    '凯德-坎宁安': 'PG', '约什-吉迪': 'PG', '克里斯-保罗': 'PG',
    '杰伦-布伦森': 'PG', '达里厄斯-加兰': 'PG', '德章泰-默里': 'PG',
    '拉塞尔-威斯布鲁克': 'PG', '马库斯-斯马特': 'PG', 'TJ-麦康奈尔': 'PG',
    '科比-怀特': 'PG', '丹尼斯-施罗德': 'PG', '斯库特-亨德森': 'PG',
    '马克尔-富尔茨': 'PG', '特里-罗齐尔': 'PG', '迈克-康利': 'PG',
    '安芬尼-西蒙斯': 'PG', '科尔-安东尼': 'PG', '杰伦-萨格斯': 'PG',

    # SG
    '谢伊-吉尔杰斯-亚历山大': 'SG', '安东尼-爱德华兹': 'SG',
    '多诺万-米切尔': 'SG', '德文-布克': 'SG', '德斯蒙德-贝恩': 'SG',
    '泰雷斯-马克西': 'SG', '杰伦-威廉姆斯': 'SG', '扎克-拉文': 'SG',
    '泰勒-希罗': 'SG', '奥斯汀-里夫斯': 'SG', '布拉德利-比尔': 'SG',
    '乔丹-普尔': 'SG', 'CJ-麦科勒姆': 'SG', '马利克-蒙克': 'SG',
    '巴迪-希尔德': 'SG', '小加里-特伦特': 'SG', '安芬尼-西蒙斯': 'SG',
    '杰伦-格林': 'SG', '卡姆-托马斯': 'SG', '诺曼-鲍威尔': 'SG',
    '德马尔-德罗赞': 'SG',

    # SF
    '杰森-塔图姆': 'SF', '杰伦-布朗': 'SF', '科怀-伦纳德': 'SF',
    '勒布朗-詹姆斯': 'SF', '吉米-巴特勒': 'SF', '保罗-乔治': 'SF',
    '弗朗茨-瓦格纳': 'SF', '布兰登-英格拉姆': 'SF', '米卡尔-布里奇斯': 'SF',
    'OG-阿奴诺比': 'SF', '德马尔-德罗赞': 'SF', '约什-哈特': 'SF',
    '赫伯特-琼斯': 'SF', '狄龙-布鲁克斯': 'SF', '凯尔-库兹马': 'SF',
    '托拜厄斯-哈里斯': 'SF', '八村垒': 'SF', '杰登-麦克丹尼尔斯': 'SF',
    'RJ-巴雷特': 'SF', '哈里森-巴恩斯': 'SF',

    # PF
    '扬尼斯-阿德托昆博': 'PF', '凯文-杜兰特': 'PF', '杰森-塔特姆': 'PF',
    '帕斯卡尔-西亚卡姆': 'PF', '保罗-班切罗': 'PF', '埃文-莫布利': 'PF',
    '小贾伦-杰克逊': 'PF', '朱利叶斯-兰德尔': 'PF', '劳里-马尔卡宁': 'PF',
    '蔡恩-威廉森': 'PF', '切特-霍姆格伦': 'PF', '德雷蒙德-格林': 'PF',
    '阿隆-戈登': 'PF', '杰拉米-格兰特': 'PF', '约翰-科林斯': 'PF',
    '小贾巴里-史密斯': 'PF', '基根-默里': 'PF', 'PJ-华盛顿': 'PF',
    '奥比-托平': 'PF', '迈尔斯-布里奇斯': 'PF', '杰伦-约翰逊': 'PF',
    '德尼-阿夫迪亚': 'PF',

    # C
    '尼古拉-约基奇': 'C', '乔尔-恩比德': 'C', '安东尼-戴维斯': 'C',
    '巴姆-阿德巴约': 'C', '鲁迪-戈贝尔': 'C', '卡尔-安东尼-唐斯': 'C',
    '维克托-文班亚马': 'C', '多曼塔斯-萨博尼斯': 'C', '伊维察-祖巴茨': 'C',
    '布鲁克-洛佩斯': 'C', '迈尔斯-特纳': 'C', '贾勒特-阿伦': 'C',
    '尼古拉-武切维奇': 'C', '克林特-卡佩拉': 'C', '约纳斯-瓦兰丘纳斯': 'C',
    '艾尔佩伦-申京': 'C', '优素福-努尔基奇': 'C', '雅各布-珀尔特尔': 'C',
    '德安德烈-艾顿': 'C', '史蒂文-亚当斯': 'C', '纳兹-里德': 'C',
    '丹尼尔-加福德': 'C', '沃克-凯斯勒': 'C',
}

# Handle both · and - separators
def match_position(name):
    if name in POSITIONS:
        return POSITIONS[name]
    # Try replacing · with -
    alt = name.replace('·', '-')
    if alt in POSITIONS:
        return POSITIONS[alt]
    return ''


# ── helpers ──────────────────────────────────────────────
def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  WARN: {url} → {e}")
        return ""

def parse_table(html):
    m = re.search(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
    if not m:
        return []
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', m.group(1), re.DOTALL)
    headers = []
    result = []
    for row in rows:
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.DOTALL)
        clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
        if not clean:
            continue
        if not headers:
            headers = clean
        elif len(clean) >= 3:
            result.append(dict(zip(headers, clean)))
    return result

def sf(v, default=0.0):
    """Safe float conversion."""
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, list):
        return float(v[0]) if v else default
    if isinstance(v, str):
        v = v.replace('%', '').strip()
        if '-' in v and v.count('-') == 1:
            return float(v.split('-')[0])
        try: return float(v)
        except ValueError: return default
    return default


# ── main ─────────────────────────────────────────────────
def main():
    print("Scraping Hupu NBA stats...\n")
    cat_data = {}
    for cat in CATEGORIES:
        url = f"{BASE}/{cat}"
        print(f"  {cat} ...", end=" ", flush=True)
        rows = parse_table(fetch(url))
        cat_data[cat] = {r['球员']: r for r in rows}
        print(f"{len(rows)} players")
        time.sleep(0.5)

    # ── merge ──
    all_names = set()
    for cat in CATEGORIES:
        all_names.update(cat_data[cat].keys())

    merged = {}
    for name in all_names:
        cat_count = sum(1 for cat in CATEGORIES if name in cat_data[cat])
        if name not in cat_data['pts'] or cat_count < 2:
            continue

        p = {'name': name, 'position': match_position(name), 'categories': cat_count}
        pts = cat_data['pts'][name]

        p['gp'] = int(sf(pts.get('场次', 0)))
        p['mpg'] = max(sf(pts.get('上场时间', 0)), 1)
        p['pts'] = sf(pts.get('得分', 0))
        p['fg_pct'] = sf(pts.get('命中率', 0))
        p['tp_pct'] = sf(pts.get('三分命中率', 0))
        p['ft_pct'] = sf(pts.get('罚球命中率', 0))

        for key, tag in [('命中-出手', 'fg'), ('命中-三分', 'tp'), ('命中-罚球', 'ft')]:
            raw = pts.get(key, '0-0')
            parts = str(raw).split('-')
            p[f'{tag}m'] = sf(parts[0])
            p[f'{tag}a'] = sf(parts[1])

        p['ast'] = sf(cat_data['asts'][name]['助攻数']) if name in cat_data['asts'] else 0
        p['tov'] = sf(cat_data['asts'][name]['失误数']) if name in cat_data['asts'] else 0

        if name in cat_data['reb']:
            r = cat_data['reb'][name]
            p['reb'] = sf(r.get('篮板数', 0))
            p['oreb'] = sf(r.get('进攻篮板', 0))
            p['dreb'] = sf(r.get('防守篮板', 0))
        else:
            p['reb'] = p['oreb'] = p['dreb'] = 0

        p['stl'] = sf(cat_data['stl'][name]['抢断数']) if name in cat_data['stl'] else 0
        p['blk'] = sf(cat_data['blk'][name]['盖帽数']) if name in cat_data['blk'] else 0

        merged[name] = p

    players = list(merged.values())
    print(f"\nQualified: {len(players)} players")

    # ── percentiles (GLOBAL — across all qualified players) ──
    def pctile(values, v):
        if not values or max(values) == min(values):
            return 50
        rank = sum(1 for x in values if x <= v)
        return round((rank / len(values)) * 99)

    all_pts   = [p['pts'] for p in players]
    all_tpp   = [p['tp_pct'] for p in players]
    all_ftp   = [p['ft_pct'] for p in players]
    all_ast   = [p['ast'] for p in players]
    all_reb   = [p['reb'] for p in players]
    all_stl   = [p['stl'] for p in players]
    all_blk   = [p['blk'] for p in players]
    all_tov   = [p['tov'] for p in players]
    all_fga   = [p.get('fga', 0) for p in players]
    all_fgm   = [p.get('fgm', 0) for p in players]

    for p in players:
        d = {
            'threePT':    pctile(all_tpp, p['tp_pct']),
            'midRange':   pctile(all_fgm, p['fgm']),
            'rimFin':     int(pctile(all_fga, p.get('fga', 0)) * 0.5 + pctile(all_ftp, p['ft_pct']) * 0.5),
            'FT':         pctile(all_ftp, p['ft_pct']),
            'perimD':     int(pctile(all_stl, p['stl']) * 0.5 + 25),
            'rimProt':    pctile(all_blk, p['blk']),
            'helpSwitch': int((pctile(all_stl, p['stl']) + pctile(all_blk, p['blk'])) / 2),
            'steals':     pctile(all_stl, p['stl']),
            'playmaking': pctile(all_ast, p['ast']),
            'ballHandle': pctile(all_tov, -p['tov']),  # negative: fewer TOV = higher
            'rebounding': pctile(all_reb, p['reb']),
            'athleticism': 50,
        }
        p['data'] = d

        # scout = data for now (will be manually tuned)
        p['scout'] = dict(d)

        # Weighted blend
        w = {
            'threePT': 0.75, 'midRange': 0.4, 'rimFin': 0.4, 'FT': 0.75,
            'perimD': 0.35, 'rimProt': 0.4, 'helpSwitch': 0.25, 'steals': 0.5,
            'playmaking': 0.65, 'ballHandle': 0.4, 'rebounding': 0.55, 'athleticism': 0.15,
        }
        p['attrs'] = {}
        for axis in d:
            wd = w.get(axis, 0.5)
            score = round(wd * d[axis] + (1 - wd) * p['scout'][axis])
            p['attrs'][axis] = max(1, min(99, score))

    # ── manual scout overrides for well-known stars ──
    overrides = {
        '斯蒂芬-库里': {
            'threePT': 99, 'midRange': 90, 'rimFin': 60, 'FT': 95,
            'playmaking': 92, 'ballHandle': 97, 'perimD': 60, 'rimProt': 10,
            'helpSwitch': 55, 'steals': 70, 'rebounding': 45, 'athleticism': 75,
        },
        '尼古拉-约基奇': {
            'threePT': 78, 'midRange': 95, 'rimFin': 95, 'FT': 85,
            'playmaking': 99, 'ballHandle': 90, 'perimD': 60, 'rimProt': 78,
            'helpSwitch': 72, 'steals': 65, 'rebounding': 95, 'athleticism': 68,
        },
        '扬尼斯-阿德托昆博': {
            'threePT': 30, 'midRange': 55, 'rimFin': 99, 'FT': 50,
            'playmaking': 82, 'ballHandle': 84, 'perimD': 88, 'rimProt': 95,
            'helpSwitch': 85, 'steals': 72, 'rebounding': 90, 'athleticism': 99,
        },
        '卢卡-东契奇': {
            'threePT': 82, 'midRange': 88, 'rimFin': 85, 'FT': 78,
            'playmaking': 95, 'ballHandle': 94, 'perimD': 68, 'rimProt': 40,
            'helpSwitch': 60, 'steals': 70, 'rebounding': 72, 'athleticism': 72,
        },
        '凯文-杜兰特': {
            'threePT': 90, 'midRange': 97, 'rimFin': 85, 'FT': 88,
            'playmaking': 82, 'ballHandle': 86, 'perimD': 80, 'rimProt': 82,
            'helpSwitch': 78, 'steals': 68, 'rebounding': 72, 'athleticism': 78,
        },
        '杰森-塔图姆': {
            'threePT': 85, 'midRange': 84, 'rimFin': 82, 'FT': 82,
            'playmaking': 78, 'ballHandle': 84, 'perimD': 86, 'rimProt': 78,
            'helpSwitch': 80, 'steals': 72, 'rebounding': 76, 'athleticism': 88,
        },
        '谢伊-吉尔杰斯-亚历山大': {
            'threePT': 78, 'midRange': 92, 'rimFin': 88, 'FT': 90,
            'playmaking': 86, 'ballHandle': 92, 'perimD': 88, 'rimProt': 55,
            'helpSwitch': 72, 'steals': 85, 'rebounding': 60, 'athleticism': 86,
        },
        '安东尼-爱德华兹': {
            'threePT': 88, 'midRange': 80, 'rimFin': 90, 'FT': 82,
            'playmaking': 72, 'ballHandle': 84, 'perimD': 82, 'rimProt': 55,
            'helpSwitch': 68, 'steals': 72, 'rebounding': 65, 'athleticism': 96,
        },
        '科怀-伦纳德': {
            'threePT': 84, 'midRange': 94, 'rimFin': 82, 'FT': 88,
            'playmaking': 70, 'ballHandle': 82, 'perimD': 94, 'rimProt': 68,
            'helpSwitch': 80, 'steals': 88, 'rebounding': 68, 'athleticism': 82,
        },
        '维克托-文班亚马': {
            'threePT': 72, 'midRange': 65, 'rimFin': 88, 'FT': 80,
            'playmaking': 60, 'ballHandle': 68, 'perimD': 78, 'rimProt': 98,
            'helpSwitch': 90, 'steals': 70, 'rebounding': 90, 'athleticism': 95,
        },
        '乔尔-恩比德': {
            'threePT': 74, 'midRange': 88, 'rimFin': 92, 'FT': 88,
            'playmaking': 72, 'ballHandle': 68, 'perimD': 84, 'rimProt': 94,
            'helpSwitch': 76, 'steals': 65, 'rebounding': 85, 'athleticism': 78,
        },
        '勒布朗-詹姆斯': {
            'threePT': 78, 'midRange': 82, 'rimFin': 94, 'FT': 72,
            'playmaking': 94, 'ballHandle': 88, 'perimD': 78, 'rimProt': 72,
            'helpSwitch': 82, 'steals': 68, 'rebounding': 78, 'athleticism': 85,
        },
        '贾-莫兰特': {
            'threePT': 68, 'midRange': 72, 'rimFin': 92, 'FT': 78,
            'playmaking': 88, 'ballHandle': 92, 'perimD': 60, 'rimProt': 25,
            'helpSwitch': 50, 'steals': 65, 'rebounding': 48, 'athleticism': 96,
        },
        '多诺万-米切尔': {
            'threePT': 84, 'midRange': 82, 'rimFin': 78, 'FT': 86,
            'playmaking': 76, 'ballHandle': 86, 'perimD': 78, 'rimProt': 35,
            'helpSwitch': 60, 'steals': 75, 'rebounding': 50, 'athleticism': 90,
        },
        '泰雷斯-马克西': {
            'threePT': 82, 'midRange': 75, 'rimFin': 72, 'FT': 88,
            'playmaking': 70, 'ballHandle': 84, 'perimD': 60, 'rimProt': 20,
            'helpSwitch': 48, 'steals': 65, 'rebounding': 40, 'athleticism': 88,
        },
        '凯德-坎宁安': {
            'threePT': 74, 'midRange': 78, 'rimFin': 72, 'FT': 85,
            'playmaking': 82, 'ballHandle': 80, 'perimD': 68, 'rimProt': 45,
            'helpSwitch': 62, 'steals': 65, 'rebounding': 65, 'athleticism': 74,
        },
        '保罗-班切罗': {
            'threePT': 65, 'midRange': 78, 'rimFin': 84, 'FT': 72,
            'playmaking': 72, 'ballHandle': 76, 'perimD': 65, 'rimProt': 58,
            'helpSwitch': 60, 'steals': 58, 'rebounding': 72, 'athleticism': 84,
        },
        '帕斯卡尔-西亚卡姆': {
            'threePT': 68, 'midRange': 80, 'rimFin': 82, 'FT': 76,
            'playmaking': 68, 'ballHandle': 72, 'perimD': 74, 'rimProt': 60,
            'helpSwitch': 68, 'steals': 62, 'rebounding': 72, 'athleticism': 80,
        },
        '杰伦-布朗': {
            'threePT': 72, 'midRange': 78, 'rimFin': 85, 'FT': 75,
            'playmaking': 62, 'ballHandle': 78, 'perimD': 80, 'rimProt': 45,
            'helpSwitch': 65, 'steals': 70, 'rebounding': 60, 'athleticism': 92,
        },
    }

    def match_override(name):
        if name in overrides:
            return overrides[name]
        alt = name.replace('·', '-')
        if alt in overrides:
            return overrides[alt]
        return None

    for p in players:
        ov = match_override(p['name'])
        if ov:
            p['attrs'] = ov
            for axis, val in ov.items():
                p['scout'][axis] = val
        else:
            # For non-star players, fix obvious stat issues
            a = p['attrs']
            # If ballHandle is broken (no TOV data), use fg_pct proxy
            if a['ballHandle'] < 10:
                a['ballHandle'] = 50
            # If no position assigned, guess from available stats
            if not p['position']:
                if p['blk'] >= 1.5:
                    p['position'] = 'C'
                elif p['ast'] >= 5:
                    p['position'] = 'PG' if p['reb'] < 7 else 'SF'
                elif p['reb'] >= 10:
                    p['position'] = 'PF'
                else:
                    p['position'] = 'SF'

    # ── team colors ──
    TEAM_COLORS = {
        '勇士': '#FDB927', '掘金': '#FEC524', '雄鹿': '#00471B',
        '湖人': '#552583', '火箭': '#CE1141', '雷霆': '#007AC1',
        '凯尔特人': '#007A33', '76人': '#006BB6', '快船': '#C8102E',
        '太阳': '#E56020', '独行侠': '#00538C', '马刺': '#000000',
        '骑士': '#860038', '森林狼': '#0C2340', '尼克斯': '#F58426',
        '灰熊': '#5D76A9', '国王': '#5A2D81', '老鹰': '#E03A3E',
        '篮网': '#000000', '黄蜂': '#1D1160', '热火': '#98002E',
        '魔术': '#0077C0', '猛龙': '#CE1141', '步行者': '#FDBB30',
        '活塞': '#C8102E', '开拓者': '#E03A3E', '爵士': '#002B5C',
        '奇才': '#002B5C', '公牛': '#CE1141', '鹈鹕': '#0C2340',
    }

    # Get team from pts page
    for p in players:
        name = p['name']
        p['team'] = cat_data['pts'][name].get('球队', '') if name in cat_data['pts'] else ''
        p['color'] = TEAM_COLORS.get(p['team'], '#3b82f6')

    # ── LEGENDS: historical greats (hand-curated, multi-season) ──
    LEGENDS = [
        # ===== PG =====
        {
            "id": "magic-87", "name": "魔术师约翰逊 (87)", "position": "PG",
            "team": "湖人", "color": "#552583", "season": "1986-87",
            "attrs": {'threePT':30,'midRange':78,'rimFin':88,'FT':85,'playmaking':99,'ballHandle':96,'perimD':70,'rimProt':40,'helpSwitch':75,'steals':78,'rebounding':75,'athleticism':88},
            "stats": {"pts":23.9,"ast":12.2,"reb":6.3,"stl":1.7,"blk":0.5,"fg_pct":52.2,"tp_pct":20.5,"ft_pct":84.8,"gp":80,"mpg":36.3}
        },
        {
            "id": "stockton-95", "name": "约翰·斯托克顿 (95)", "position": "PG",
            "team": "爵士", "color": "#002B5C", "season": "1994-95",
            "attrs": {'threePT':78,'midRange':82,'rimFin':58,'FT':88,'playmaking':99,'ballHandle':94,'perimD':88,'rimProt':15,'helpSwitch':82,'steals':95,'rebounding':38,'athleticism':62},
            "stats": {"pts":14.7,"ast":12.3,"reb":3.1,"stl":2.4,"blk":0.3,"fg_pct":54.2,"tp_pct":44.9,"ft_pct":80.4,"gp":82,"mpg":35.0}
        },
        {
            "id": "nash-06", "name": "史蒂夫·纳什 (06)", "position": "PG",
            "team": "太阳", "color": "#E56020", "season": "2005-06",
            "attrs": {'threePT':90,'midRange':92,'rimFin':60,'FT':94,'playmaking':98,'ballHandle':94,'perimD':35,'rimProt':10,'helpSwitch':40,'steals':45,'rebounding':40,'athleticism':68},
            "stats": {"pts":18.8,"ast":10.5,"reb":4.2,"stl":0.8,"blk":0.2,"fg_pct":51.2,"tp_pct":43.9,"ft_pct":92.1,"gp":79,"mpg":35.4}
        },
        {
            "id": "cp3-09", "name": "克里斯·保罗 (09)", "position": "PG",
            "team": "黄蜂", "color": "#1D1160", "season": "2008-09",
            "attrs": {'threePT':78,'midRange':88,'rimFin':65,'FT':88,'playmaking':96,'ballHandle':95,'perimD':94,'rimProt':15,'helpSwitch':88,'steals':96,'rebounding':45,'athleticism':80},
            "stats": {"pts":22.8,"ast":11.0,"reb":5.5,"stl":2.8,"blk":0.1,"fg_pct":50.3,"tp_pct":36.4,"ft_pct":86.8,"gp":78,"mpg":38.5}
        },
        {
            "id": "westbrook-17", "name": "威斯布鲁克 (17)", "position": "PG",
            "team": "雷霆", "color": "#007AC1", "season": "2016-17",
            "attrs": {'threePT':65,'midRange':72,'rimFin':88,'FT':82,'playmaking':94,'ballHandle':88,'perimD':78,'rimProt':30,'helpSwitch':68,'steals':75,'rebounding':88,'athleticism':98},
            "stats": {"pts":31.6,"ast":10.4,"reb":10.7,"stl":1.6,"blk":0.4,"fg_pct":42.5,"tp_pct":34.3,"ft_pct":84.5,"gp":81,"mpg":34.6}
        },
        {
            "id": "rose-11", "name": "德里克·罗斯 (11)", "position": "PG",
            "team": "公牛", "color": "#CE1141", "season": "2010-11",
            "attrs": {'threePT':62,'midRange':78,'rimFin':94,'FT':82,'playmaking':82,'ballHandle':90,'perimD':72,'rimProt':35,'helpSwitch':65,'steals':68,'rebounding':42,'athleticism':98},
            "stats": {"pts":25.0,"ast":7.7,"reb":4.1,"stl":1.0,"blk":0.6,"fg_pct":44.5,"tp_pct":33.2,"ft_pct":85.8,"gp":81,"mpg":37.4}
        },
        {
            "id": "kidd-03", "name": "贾森·基德 (03)", "position": "PG",
            "team": "篮网", "color": "#000000", "season": "2002-03",
            "attrs": {'threePT':68,'midRange':62,'rimFin':55,'FT':82,'playmaking':96,'ballHandle':88,'perimD':92,'rimProt':25,'helpSwitch':88,'steals':85,'rebounding':72,'athleticism':78},
            "stats": {"pts":18.7,"ast":8.9,"reb":6.3,"stl":2.2,"blk":0.3,"fg_pct":41.4,"tp_pct":34.1,"ft_pct":84.1,"gp":80,"mpg":37.4}
        },

        # ===== SG =====
        {
            "id": "jordan-96", "name": "迈克尔·乔丹 (96)", "position": "SG",
            "team": "公牛", "color": "#CE1141", "season": "1995-96",
            "attrs": {'threePT':78,'midRange':99,'rimFin':98,'FT':85,'playmaking':82,'ballHandle':94,'perimD':99,'rimProt':55,'helpSwitch':92,'steals':94,'rebounding':65,'athleticism':98},
            "stats": {"pts":30.4,"ast":4.3,"reb":6.6,"stl":2.2,"blk":0.5,"fg_pct":49.5,"tp_pct":42.7,"ft_pct":83.4,"gp":82,"mpg":37.7}
        },
        {
            "id": "jordan-91", "name": "迈克尔·乔丹 (91)", "position": "SG",
            "team": "公牛", "color": "#CE1141", "season": "1990-91",
            "attrs": {'threePT':60,'midRange':97,'rimFin':99,'FT':84,'playmaking':78,'ballHandle':94,'perimD':98,'rimProt':58,'helpSwitch':90,'steals':96,'rebounding':62,'athleticism':99},
            "stats": {"pts":31.5,"ast":5.5,"reb":6.0,"stl":2.7,"blk":1.0,"fg_pct":53.9,"tp_pct":31.2,"ft_pct":85.1,"gp":82,"mpg":37.0}
        },
        {
            "id": "kobe-06", "name": "科比·布莱恩特 (06)", "position": "SG",
            "team": "湖人", "color": "#552583", "season": "2005-06",
            "attrs": {'threePT':82,'midRange':97,'rimFin':94,'FT':86,'playmaking':75,'ballHandle':92,'perimD':95,'rimProt':40,'helpSwitch':85,'steals':82,'rebounding':55,'athleticism':94},
            "stats": {"pts":35.4,"ast":4.5,"reb":5.3,"stl":1.8,"blk":0.4,"fg_pct":45.0,"tp_pct":34.7,"ft_pct":85.0,"gp":80,"mpg":41.0}
        },
        {
            "id": "kobe-10", "name": "科比·布莱恩特 (10)", "position": "SG",
            "team": "湖人", "color": "#552583", "season": "2009-10",
            "attrs": {'threePT':75,'midRange':95,'rimFin':88,'FT':84,'playmaking':78,'ballHandle':90,'perimD':92,'rimProt':35,'helpSwitch':82,'steals':78,'rebounding':52,'athleticism':88},
            "stats": {"pts":27.0,"ast":5.0,"reb":5.4,"stl":1.5,"blk":0.3,"fg_pct":45.6,"tp_pct":32.9,"ft_pct":81.1,"gp":73,"mpg":38.8}
        },
        {
            "id": "wade-09", "name": "德维恩·韦德 (09)", "position": "SG",
            "team": "热火", "color": "#98002E", "season": "2008-09",
            "attrs": {'threePT':60,'midRange':85,'rimFin':96,'FT':78,'playmaking':82,'ballHandle':88,'perimD':94,'rimProt':72,'helpSwitch':88,'steals':88,'rebounding':50,'athleticism':95},
            "stats": {"pts":30.2,"ast":7.5,"reb":5.0,"stl":2.2,"blk":1.3,"fg_pct":49.1,"tp_pct":31.7,"ft_pct":76.5,"gp":79,"mpg":38.6}
        },
        {
            "id": "iverson-01", "name": "阿伦·艾弗森 (01)", "position": "SG",
            "team": "76人", "color": "#006BB6", "season": "2000-01",
            "attrs": {'threePT':68,'midRange':85,'rimFin':88,'FT':80,'playmaking':78,'ballHandle':96,'perimD':82,'rimProt':10,'helpSwitch':68,'steals':92,'rebounding':35,'athleticism':94},
            "stats": {"pts":31.1,"ast":4.6,"reb":3.8,"stl":2.5,"blk":0.3,"fg_pct":42.0,"tp_pct":32.0,"ft_pct":81.4,"gp":71,"mpg":42.0}
        },
        {
            "id": "harden-18", "name": "詹姆斯·哈登 (18)", "position": "SG",
            "team": "火箭", "color": "#CE1141", "season": "2017-18",
            "attrs": {'threePT':88,'midRange':85,'rimFin':88,'FT':90,'playmaking':92,'ballHandle':92,'perimD':65,'rimProt':35,'helpSwitch':55,'steals':78,'rebounding':52,'athleticism':78},
            "stats": {"pts":30.4,"ast":8.8,"reb":5.4,"stl":1.8,"blk":0.7,"fg_pct":44.9,"tp_pct":36.7,"ft_pct":85.8,"gp":72,"mpg":35.4}
        },
        {
            "id": "tmac-03", "name": "特雷西·麦迪 (03)", "position": "SG",
            "team": "魔术", "color": "#0077C0", "season": "2002-03",
            "attrs": {'threePT':82,'midRange':92,'rimFin':88,'FT':78,'playmaking':78,'ballHandle':88,'perimD':78,'rimProt':55,'helpSwitch':72,'steals':75,'rebounding':62,'athleticism':92},
            "stats": {"pts":32.1,"ast":5.5,"reb":6.5,"stl":1.7,"blk":0.8,"fg_pct":45.7,"tp_pct":38.6,"ft_pct":79.3,"gp":75,"mpg":39.4}
        },

        # ===== SF =====
        {
            "id": "lebron-13", "name": "勒布朗·詹姆斯 (13)", "position": "SF",
            "team": "热火", "color": "#98002E", "season": "2012-13",
            "attrs": {'threePT':78,'midRange':85,'rimFin':98,'FT':72,'playmaking':90,'ballHandle':90,'perimD':94,'rimProt':78,'helpSwitch':92,'steals':78,'rebounding':75,'athleticism':98},
            "stats": {"pts":26.8,"ast":7.3,"reb":8.0,"stl":1.7,"blk":0.9,"fg_pct":56.5,"tp_pct":40.6,"ft_pct":75.3,"gp":76,"mpg":37.9}
        },
        {
            "id": "lebron-18", "name": "勒布朗·詹姆斯 (18)", "position": "SF",
            "team": "骑士", "color": "#860038", "season": "2017-18",
            "attrs": {'threePT':78,'midRange':82,'rimFin':96,'FT':70,'playmaking':94,'ballHandle':90,'perimD':85,'rimProt':72,'helpSwitch':85,'steals':72,'rebounding':78,'athleticism':94},
            "stats": {"pts":27.5,"ast":9.1,"reb":8.6,"stl":1.4,"blk":0.9,"fg_pct":54.2,"tp_pct":36.7,"ft_pct":73.1,"gp":82,"mpg":36.9}
        },
        {
            "id": "bird-86", "name": "拉里·伯德 (86)", "position": "SF",
            "team": "凯尔特人", "color": "#007A33", "season": "1985-86",
            "attrs": {'threePT':88,'midRange':98,'rimFin':82,'FT':92,'playmaking':88,'ballHandle':84,'perimD':78,'rimProt':55,'helpSwitch':82,'steals':75,'rebounding':88,'athleticism':72},
            "stats": {"pts":25.8,"ast":6.8,"reb":9.8,"stl":2.0,"blk":0.6,"fg_pct":49.6,"tp_pct":42.3,"ft_pct":89.6,"gp":82,"mpg":38.0}
        },
        {
            "id": "pippen-94", "name": "斯科蒂·皮蓬 (94)", "position": "SF",
            "team": "公牛", "color": "#CE1141", "season": "1993-94",
            "attrs": {'threePT':62,'midRange':75,'rimFin':78,'FT':68,'playmaking':82,'ballHandle':82,'perimD':98,'rimProt':65,'helpSwitch':96,'steals':90,'rebounding':72,'athleticism':92},
            "stats": {"pts":22.0,"ast":5.6,"reb":8.7,"stl":2.9,"blk":0.8,"fg_pct":49.1,"tp_pct":32.0,"ft_pct":66.0,"gp":72,"mpg":38.3}
        },
        {
            "id": "kawhi-19", "name": "科怀·伦纳德 (19)", "position": "SF",
            "team": "猛龙", "color": "#CE1141", "season": "2018-19",
            "attrs": {'threePT':82,'midRange':94,'rimFin':85,'FT':86,'playmaking':68,'ballHandle':82,'perimD':98,'rimProt':62,'helpSwitch':88,'steals':90,'rebounding':68,'athleticism':88},
            "stats": {"pts":26.6,"ast":3.3,"reb":7.3,"stl":1.8,"blk":0.4,"fg_pct":49.6,"tp_pct":37.1,"ft_pct":85.4,"gp":60,"mpg":34.0}
        },

        # ===== PF =====
        {
            "id": "duncan-03", "name": "蒂姆·邓肯 (03)", "position": "PF",
            "team": "马刺", "color": "#000000", "season": "2002-03",
            "attrs": {'threePT':10,'midRange':88,'rimFin':94,'FT':68,'playmaking':68,'ballHandle':68,'perimD':94,'rimProt':98,'helpSwitch':94,'steals':65,'rebounding':92,'athleticism':78},
            "stats": {"pts":23.3,"ast":3.9,"reb":12.9,"stl":0.7,"blk":2.9,"fg_pct":51.3,"tp_pct":27.3,"ft_pct":71.0,"gp":81,"mpg":39.3}
        },
        {
            "id": "malone-97", "name": "卡尔·马龙 (97)", "position": "PF",
            "team": "爵士", "color": "#002B5C", "season": "1996-97",
            "attrs": {'threePT':15,'midRange':88,'rimFin':92,'FT':75,'playmaking':62,'ballHandle':65,'perimD':82,'rimProt':75,'helpSwitch':75,'steals':72,'rebounding':92,'athleticism':85},
            "stats": {"pts":27.4,"ast":4.5,"reb":9.9,"stl":1.4,"blk":0.6,"fg_pct":55.0,"tp_pct":0.0,"ft_pct":75.5,"gp":82,"mpg":36.6}
        },
        {
            "id": "kg-04", "name": "凯文·加内特 (04)", "position": "PF",
            "team": "森林狼", "color": "#0C2340", "season": "2003-04",
            "attrs": {'threePT':55,'midRange':88,'rimFin':82,'FT':78,'playmaking':78,'ballHandle':72,'perimD':94,'rimProt':88,'helpSwitch':94,'steals':78,'rebounding':94,'athleticism':90},
            "stats": {"pts":24.2,"ast":5.0,"reb":13.9,"stl":1.5,"blk":2.2,"fg_pct":49.9,"tp_pct":25.6,"ft_pct":79.1,"gp":82,"mpg":39.4}
        },
        {
            "id": "dirk-07", "name": "德克·诺维茨基 (07)", "position": "PF",
            "team": "独行侠", "color": "#00538C", "season": "2006-07",
            "attrs": {'threePT':88,'midRange':98,'rimFin':78,'FT':92,'playmaking':65,'ballHandle':70,'perimD':55,'rimProt':60,'helpSwitch':55,'steals':48,'rebounding':82,'athleticism':68},
            "stats": {"pts":24.6,"ast":3.4,"reb":8.9,"stl":0.7,"blk":0.8,"fg_pct":50.2,"tp_pct":41.6,"ft_pct":90.4,"gp":78,"mpg":36.2}
        },
        {
            "id": "barkley-93", "name": "查尔斯·巴克利 (93)", "position": "PF",
            "team": "太阳", "color": "#E56020", "season": "1992-93",
            "attrs": {'threePT':50,'midRange':82,'rimFin':92,'FT':72,'playmaking':72,'ballHandle':70,'perimD':72,'rimProt':62,'helpSwitch':65,'steals':72,'rebounding':92,'athleticism':88},
            "stats": {"pts":25.6,"ast":5.1,"reb":12.2,"stl":1.6,"blk":1.0,"fg_pct":52.0,"tp_pct":30.5,"ft_pct":76.5,"gp":76,"mpg":37.6}
        },

        # ===== C =====
        {
            "id": "shaq-00", "name": "沙奎尔·奥尼尔 (00)", "position": "C",
            "team": "湖人", "color": "#552583", "season": "1999-00",
            "attrs": {'threePT':5,'midRange':45,'rimFin':99,'FT':40,'playmaking':55,'ballHandle':50,'perimD':55,'rimProt':96,'helpSwitch':72,'steals':35,'rebounding':95,'athleticism':95},
            "stats": {"pts":29.7,"ast":3.8,"reb":13.6,"stl":0.5,"blk":3.0,"fg_pct":57.4,"tp_pct":0.0,"ft_pct":52.4,"gp":79,"mpg":40.0}
        },
        {
            "id": "hakeem-94", "name": "哈基姆·奥拉朱旺 (94)", "position": "C",
            "team": "火箭", "color": "#CE1141", "season": "1993-94",
            "attrs": {'threePT':20,'midRange':82,'rimFin':98,'FT':70,'playmaking':65,'ballHandle':62,'perimD':88,'rimProt':99,'helpSwitch':92,'steals':82,'rebounding':90,'athleticism':92},
            "stats": {"pts":27.3,"ast":3.6,"reb":11.9,"stl":1.6,"blk":3.7,"fg_pct":52.8,"tp_pct":42.1,"ft_pct":71.6,"gp":80,"mpg":41.0}
        },
        {
            "id": "kareem-72", "name": "卡里姆·贾巴尔 (72)", "position": "C",
            "team": "雄鹿", "color": "#00471B", "season": "1971-72",
            "attrs": {'threePT':5,'midRange':75,'rimFin':99,'FT':68,'playmaking':55,'ballHandle':50,'perimD':78,'rimProt':96,'helpSwitch':75,'steals':45,'rebounding':94,'athleticism':85},
            "stats": {"pts":34.8,"ast":4.6,"reb":16.6,"stl":0,"blk":0,"fg_pct":57.4,"tp_pct":0,"ft_pct":68.9,"gp":81,"mpg":44.2}
        },
        {
            "id": "wilt-62", "name": "威尔特·张伯伦 (62)", "position": "C",
            "team": "勇士", "color": "#FDB927", "season": "1961-62",
            "attrs": {'threePT':5,'midRange':50,'rimFin':99,'FT':30,'playmaking':48,'ballHandle':40,'perimD':70,'rimProt':98,'helpSwitch':65,'steals':30,'rebounding':99,'athleticism':98},
            "stats": {"pts":50.4,"ast":2.4,"reb":25.7,"stl":0,"blk":0,"fg_pct":50.6,"tp_pct":0,"ft_pct":61.3,"gp":80,"mpg":48.5}
        },
        {
            "id": "russell-62", "name": "比尔·拉塞尔 (62)", "position": "C",
            "team": "凯尔特人", "color": "#007A33", "season": "1961-62",
            "attrs": {'threePT':5,'midRange':45,'rimFin':78,'FT':55,'playmaking':62,'ballHandle':45,'perimD':98,'rimProt':99,'helpSwitch':98,'steals':65,'rebounding':99,'athleticism':94},
            "stats": {"pts":18.9,"ast":4.5,"reb":23.6,"stl":0,"blk":0,"fg_pct":45.7,"tp_pct":0,"ft_pct":59.5,"gp":76,"mpg":45.2}
        },
        {
            "id": "admiral-95", "name": "大卫·罗宾逊 (95)", "position": "C",
            "team": "马刺", "color": "#000000", "season": "1994-95",
            "attrs": {'threePT':20,'midRange':72,'rimFin':92,'FT':75,'playmaking':55,'ballHandle':55,'perimD':88,'rimProt':96,'helpSwitch':88,'steals':70,'rebounding':90,'athleticism':96},
            "stats": {"pts":27.6,"ast":2.9,"reb":10.8,"stl":1.7,"blk":3.2,"fg_pct":53.0,"tp_pct":30.0,"ft_pct":77.4,"gp":81,"mpg":38.0}
        },
        {
            "id": "dwight-11", "name": "德怀特·霍华德 (11)", "position": "C",
            "team": "魔术", "color": "#0077C0", "season": "2010-11",
            "attrs": {'threePT':5,'midRange':35,'rimFin':92,'FT':45,'playmaking':38,'ballHandle':42,'perimD':78,'rimProt':98,'helpSwitch':85,'steals':60,'rebounding':96,'athleticism':96},
            "stats": {"pts":22.9,"ast":1.4,"reb":14.1,"stl":1.4,"blk":2.4,"fg_pct":59.3,"tp_pct":0.0,"ft_pct":59.6,"gp":78,"mpg":37.6}
        },
        {
            "id": "yao-07", "name": "姚明 (07)", "position": "C",
            "team": "火箭", "color": "#CE1141", "season": "2006-07",
            "attrs": {'threePT':5,'midRange':82,'rimFin':88,'FT':86,'playmaking':45,'ballHandle':45,'perimD':60,'rimProt':85,'helpSwitch':65,'steals':30,'rebounding':85,'athleticism':55},
            "stats": {"pts":25.0,"ast":2.0,"reb":9.4,"stl":0.4,"blk":2.0,"fg_pct":51.6,"tp_pct":0.0,"ft_pct":86.2,"gp":48,"mpg":33.8}
        },
        {
            "id": "ewing-95", "name": "帕特里克·尤因 (95)", "position": "C",
            "team": "尼克斯", "color": "#F58426", "season": "1994-95",
            "attrs": {'threePT':15,'midRange':82,'rimFin':85,'FT':72,'playmaking':48,'ballHandle':48,'perimD':78,'rimProt':90,'helpSwitch':78,'steals':55,'rebounding':88,'athleticism':72},
            "stats": {"pts":23.9,"ast":2.7,"reb":11.0,"stl":0.9,"blk":2.0,"fg_pct":50.3,"tp_pct":28.6,"ft_pct":75.0,"gp":79,"mpg":37.0}
        },
        # ===== Extra legends =====
        {
            "id": "curry-16", "name": "斯蒂芬·库里 (16)", "position": "PG",
            "team": "勇士", "color": "#FDB927", "season": "2015-16",
            "attrs": {'threePT':99,'midRange':88,'rimFin':72,'FT':94,'playmaking':85,'ballHandle':96,'perimD':65,'rimProt':10,'helpSwitch':55,'steals':82,'rebounding':50,'athleticism':82},
            "stats": {"pts":30.1,"ast":6.7,"reb":5.4,"stl":2.1,"blk":0.2,"fg_pct":50.4,"tp_pct":45.4,"ft_pct":90.8,"gp":79,"mpg":34.2}
        },
        {
            "id": "curry-22", "name": "斯蒂芬·库里 (22)", "position": "PG",
            "team": "勇士", "color": "#FDB927", "season": "2021-22",
            "attrs": {'threePT':94,'midRange':85,'rimFin':65,'FT':92,'playmaking':82,'ballHandle':92,'perimD':62,'rimProt':8,'helpSwitch':52,'steals':72,'rebounding':48,'athleticism':72},
            "stats": {"pts":25.5,"ast":6.3,"reb":5.2,"stl":1.3,"blk":0.4,"fg_pct":43.7,"tp_pct":38.0,"ft_pct":92.3,"gp":64,"mpg":34.5}
        },
        {
            "id": "giannis-21", "name": "字母哥 (21)", "position": "PF",
            "team": "雄鹿", "color": "#00471B", "season": "2020-21",
            "attrs": {'threePT':28,'midRange':50,'rimFin':99,'FT':60,'playmaking':80,'ballHandle':82,'perimD':90,'rimProt':94,'helpSwitch':88,'steals':70,'rebounding':92,'athleticism':99},
            "stats": {"pts":28.1,"ast":5.9,"reb":11.0,"stl":1.2,"blk":1.2,"fg_pct":56.9,"tp_pct":30.3,"ft_pct":68.5,"gp":61,"mpg":33.0}
        },
        {
            "id": "jokic-23", "name": "约基奇 (23)", "position": "C",
            "team": "掘金", "color": "#FEC524", "season": "2022-23",
            "attrs": {'threePT':75,'midRange':94,'rimFin':94,'FT':82,'playmaking':98,'ballHandle':88,'perimD':58,'rimProt':72,'helpSwitch':68,'steals':62,'rebounding':92,'athleticism':65},
            "stats": {"pts":24.5,"ast":9.8,"reb":11.8,"stl":1.3,"blk":0.7,"fg_pct":63.2,"tp_pct":38.3,"ft_pct":82.2,"gp":69,"mpg":33.7}
        },
    ]

    # ── output ──
    out = []
    # Add current players
    for p in sorted(players, key=lambda x: x['pts'], reverse=True):
        out.append({
            'id': p['name'],
            'name': p['name'],
            'position': p['position'],
            'team': p['team'],
            'color': p['color'],
            'attrs': p['attrs'],
            'stats': {
                'pts': p['pts'], 'ast': p['ast'], 'reb': p['reb'],
                'stl': p['stl'], 'blk': p['blk'],
                'fg_pct': p['fg_pct'], 'tp_pct': p['tp_pct'], 'ft_pct': p['ft_pct'],
                'gp': p['gp'], 'mpg': p['mpg'],
            }
        })

    # Append legends (not in the PTS sort — they have their own order)
    out.extend(LEGENDS)

    with open('players.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # ── summary ──
    pos_count = {}
    for p in out:
        pos_count[p['position'] or '?'] = pos_count.get(p['position'] or '?', 0) + 1
    legend_count = len(LEGENDS)
    print(f"\nWrote {len(out)} players → players.json ({len(out) - legend_count} current + {legend_count} legends)")
    print(f"Positions: {pos_count}")
    print("\nTop 15:")
    for p in out[:15]:
        a = p['attrs']
        print(f"  {p['name']:12s} {p['position']:3s} "
              f"3P:{a['threePT']:2d} Mid:{a['midRange']:2d} Rim:{a['rimFin']:2d} FT:{a['FT']:2d} "
              f"A:{a['playmaking']:2d} BH:{a['ballHandle']:2d} Rb:{a['rebounding']:2d} "
              f"PD:{a['perimD']:2d} RP:{a['rimProt']:2d} HS:{a['helpSwitch']:2d} St:{a['steals']:2d} Ath:{a['athleticism']:2d}")

if __name__ == '__main__':
    main()
