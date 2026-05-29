"""
Build complete current NBA player dataset.
1. Scrapes Hupu for real stats (top 50 per category = ~120 players)
2. For each team, ensures all 5 starters are covered
3. Fills in missing starters with manually estimated stats
4. Merges with existing legends/all-stars
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

# ── Extensive position map ──
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
    '达维昂-米切尔': 'PG', '安德鲁-内姆哈德': 'PG', '泰厄斯-琼斯': 'PG',
    '特雷-曼': 'PG', '科比-西蒙斯': 'PG', '小斯科蒂-皮蓬': 'PG',
    '阿门·汤普森': 'PG', '斯蒂芬·卡斯尔': 'PG', '伊曼纽尔-奎克利': 'PG',
    '戴森-丹尼尔斯': 'PG', '拉塞尔-威斯布鲁克': 'PG',

    # SG
    '谢伊-吉尔杰斯-亚历山大': 'SG', '安东尼-爱德华兹': 'SG',
    '多诺万-米切尔': 'SG', '德文-布克': 'SG', '德斯蒙德-贝恩': 'SG',
    '泰雷斯-马克西': 'SG', '杰伦-威廉姆斯': 'SG', '扎克-拉文': 'SG',
    '泰勒-希罗': 'SG', '奥斯汀-里夫斯': 'SG', '布拉德利-比尔': 'SG',
    '乔丹-普尔': 'SG', 'CJ-麦科勒姆': 'SG', '马利克-蒙克': 'SG',
    '巴迪-希尔德': 'SG', '小加里-特伦特': 'SG', '安芬尼-西蒙斯': 'SG',
    '杰伦-格林': 'SG', '卡姆-托马斯': 'SG', '诺曼-鲍威尔': 'SG',
    '德马尔-德罗赞': 'SG', '克里斯-邓恩': 'SG', '克里斯-默里': 'SG',
    '吕冈茨-多尔特': 'SG', '肯塔维奥斯-波普': 'SG', '亚历克斯-卡鲁索': 'SG',
    '博格丹-博格达诺维奇': 'SG', '克里斯蒂安·布劳恩': 'SG', '凯文-赫尔特': 'SG',

    # SF
    '杰森-塔图姆': 'SF', '杰伦-布朗': 'SF', '科怀-伦纳德': 'SF',
    '勒布朗-詹姆斯': 'SF', '吉米-巴特勒': 'SF', '保罗-乔治': 'SF',
    '弗朗茨-瓦格纳': 'SF', '布兰登-英格拉姆': 'SF', '米卡尔-布里奇斯': 'SF',
    'OG-阿奴诺比': 'SF', '德马尔-德罗赞': 'SF', '约什-哈特': 'SF',
    '赫伯特-琼斯': 'SF', '狄龙-布鲁克斯': 'SF', '凯尔-库兹马': 'SF',
    '托拜厄斯-哈里斯': 'SF', '八村垒': 'SF', '杰登-麦克丹尼尔斯': 'SF',
    'RJ-巴雷特': 'SF', '哈里森-巴恩斯': 'SF', '阿夫迪亚-德尼': 'SF',
    '杰伦-约翰逊': 'SF', '迈克尔-波特': 'SF', '凯尔登-约翰逊': 'SF',
    '杰里米-索汉': 'SF', '基冈-默里': 'SF', '杰伦-威尔逊': 'SF',
    '本尼迪克特-马瑟林': 'SF', '比拉尔-库利巴利': 'SF', '戴森-丹尼尔斯': 'SF',
    '特雷-墨菲': 'SF', '尼基尔-亚历山大-沃克': 'SF',

    # PF
    '扬尼斯-阿德托昆博': 'PF', '凯文-杜兰特': 'PF', '杰森-塔特姆': 'PF',
    '帕斯卡尔-西亚卡姆': 'PF', '保罗-班切罗': 'PF', '埃文-莫布利': 'PF',
    '小贾伦-杰克逊': 'PF', '朱利叶斯-兰德尔': 'PF', '劳里-马尔卡宁': 'PF',
    '蔡恩-威廉森': 'PF', '切特-霍姆格伦': 'PF', '德雷蒙德-格林': 'PF',
    '阿隆-戈登': 'PF', '杰拉米-格兰特': 'PF', '约翰-科林斯': 'PF',
    '小贾巴里-史密斯': 'PF', '基根-默里': 'PF', 'PJ-华盛顿': 'PF',
    '奥比-托平': 'PF', '迈尔斯-布里奇斯': 'PF', '杰伦-约翰逊': 'PF',
    '德尼-阿夫迪亚': 'PF', '纳兹-里德': 'PF', 'GG-杰克逊': 'PF',
    '马塔斯·布泽利斯': 'PF', '乔纳森-库明加': 'PF', '泰勒-史密斯': 'PF',
    '桑蒂-阿尔达马': 'PF', '布兰登-克拉克': 'PF', '特雷-莱尔斯': 'PF',
    '多里安-芬尼-史密斯': 'PF', '博比-波蒂斯': 'PF', '凯尔-安德森': 'PF',

    # C
    '尼古拉-约基奇': 'C', '乔尔-恩比德': 'C', '安东尼-戴维斯': 'C',
    '巴姆-阿德巴约': 'C', '鲁迪-戈贝尔': 'C', '卡尔-安东尼-唐斯': 'C',
    '维克托-文班亚马': 'C', '多曼塔斯-萨博尼斯': 'C', '伊维察-祖巴茨': 'C',
    '布鲁克-洛佩斯': 'C', '迈尔斯-特纳': 'C', '贾勒特-阿伦': 'C',
    '尼古拉-武切维奇': 'C', '克林特-卡佩拉': 'C', '约纳斯-瓦兰丘纳斯': 'C',
    '艾尔佩伦-申京': 'C', '优素福-努尔基奇': 'C', '雅各布-珀尔特尔': 'C',
    '德安德烈-艾顿': 'C', '史蒂文-亚当斯': 'C', '纳兹-里德': 'C',
    '丹尼尔-加福德': 'C', '沃克-凯斯勒': 'C', '以赛亚-哈尔滕施泰因': 'C',
    '阿尔佩伦-申京': 'C', '杰伦-杜伦': 'C', '马克-威廉姆斯': 'C',
    '瓦西里耶-米西奇': 'C', '德雷克-莱夫利': 'C', '凯肖恩-乔治': 'C',
    '多诺万-克林根': 'C', '扎克-伊迪': 'C', '亚历山大-萨尔': 'C',
}


def match_position(name):
    if name in POSITIONS:
        return POSITIONS[name]
    alt = name.replace('·', '-')
    if alt in POSITIONS:
        return POSITIONS[alt]
    return ''


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  WARN: {url} -> {e}")
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


# ── additional starters not on Hupu leaderboards ──
# (Players who start but don't appear in top 50 of any stat category)
# Minimal entries: name, position, team, estimated stats
EXTRA_STARTERS = [
    # ATL
    {"id": "戴森-丹尼尔斯-ATL", "name": "戴森·丹尼尔斯", "position": "SG", "team": "老鹰", "stats": {"pts": 14.8, "ast": 4.2, "reb": 5.8, "stl": 3.0, "blk": 0.7, "fg_pct": 47.2, "tp_pct": 34.8, "ft_pct": 65.0, "gp": 72, "mpg": 34.2}},
    {"id": "扎卡里-里萨谢", "name": "扎卡里·里萨谢", "position": "SF", "team": "老鹰", "stats": {"pts": 12.1, "ast": 1.5, "reb": 3.8, "stl": 0.8, "blk": 0.5, "fg_pct": 44.2, "tp_pct": 36.5, "ft_pct": 73.0, "gp": 70, "mpg": 26.8}},
    {"id": "奥涅卡-奥孔古", "name": "奥涅卡·奥孔古", "position": "C", "team": "老鹰", "stats": {"pts": 12.5, "ast": 2.0, "reb": 9.5, "stl": 0.7, "blk": 1.3, "fg_pct": 62.5, "tp_pct": 28.0, "ft_pct": 75.0, "gp": 68, "mpg": 28.5}},
    # BKN
    {"id": "卡梅隆-托马斯-BKN", "name": "卡梅隆·托马斯", "position": "SG", "team": "篮网", "stats": {"pts": 22.0, "ast": 3.5, "reb": 3.8, "stl": 0.8, "blk": 0.3, "fg_pct": 43.8, "tp_pct": 35.2, "ft_pct": 85.5, "gp": 55, "mpg": 32.5}},
    {"id": "诺阿-克劳尼", "name": "诺阿·克劳尼", "position": "PF", "team": "篮网", "stats": {"pts": 10.8, "ast": 1.8, "reb": 6.5, "stl": 0.7, "blk": 1.0, "fg_pct": 46.5, "tp_pct": 35.8, "ft_pct": 72.0, "gp": 68, "mpg": 27.8}},
    {"id": "尼古拉斯-克拉克斯顿", "name": "尼古拉斯·克拉克斯顿", "position": "C", "team": "篮网", "stats": {"pts": 11.2, "ast": 2.2, "reb": 9.2, "stl": 0.8, "blk": 2.1, "fg_pct": 63.0, "tp_pct": 0.0, "ft_pct": 55.0, "gp": 65, "mpg": 29.5}},
    # CHA
    {"id": "瓦西里耶-米西奇-CHA", "name": "瓦西里耶·米西奇", "position": "PG", "team": "黄蜂", "stats": {"pts": 10.2, "ast": 5.8, "reb": 2.8, "stl": 0.8, "blk": 0.1, "fg_pct": 42.5, "tp_pct": 35.5, "ft_pct": 82.0, "gp": 58, "mpg": 24.8}},
    {"id": "布兰登-米勒", "name": "布兰登·米勒", "position": "SG", "team": "黄蜂", "stats": {"pts": 19.8, "ast": 3.5, "reb": 4.8, "stl": 1.0, "blk": 0.6, "fg_pct": 43.5, "tp_pct": 36.2, "ft_pct": 82.5, "gp": 65, "mpg": 33.2}},
    {"id": "约什-格林-CHA", "name": "约什·格林", "position": "SF", "team": "黄蜂", "stats": {"pts": 9.5, "ast": 2.2, "reb": 4.2, "stl": 0.9, "blk": 0.3, "fg_pct": 44.8, "tp_pct": 37.8, "ft_pct": 72.0, "gp": 70, "mpg": 27.5}},
    {"id": "格兰特-威廉姆斯-CHA", "name": "格兰特·威廉姆斯", "position": "PF", "team": "黄蜂", "stats": {"pts": 9.8, "ast": 2.5, "reb": 5.2, "stl": 0.7, "blk": 0.5, "fg_pct": 44.5, "tp_pct": 37.0, "ft_pct": 78.0, "gp": 55, "mpg": 28.0}},
    # CHI
    {"id": "约什-吉迪-CHI", "name": "约什·吉迪", "position": "PG", "team": "公牛", "stats": {"pts": 13.8, "ast": 6.8, "reb": 7.5, "stl": 1.2, "blk": 0.6, "fg_pct": 46.2, "tp_pct": 37.5, "ft_pct": 78.0, "gp": 68, "mpg": 30.8}},
    {"id": "阿约-多森姆", "name": "阿约·多森姆", "position": "SG", "team": "公牛", "stats": {"pts": 13.2, "ast": 4.8, "reb": 3.5, "stl": 1.0, "blk": 0.4, "fg_pct": 49.5, "tp_pct": 38.5, "ft_pct": 80.0, "gp": 72, "mpg": 32.5}},
    {"id": "帕特里克-威廉姆斯-CHI", "name": "帕特里克·威廉姆斯", "position": "PF", "team": "公牛", "stats": {"pts": 10.5, "ast": 1.8, "reb": 4.8, "stl": 1.0, "blk": 0.8, "fg_pct": 45.8, "tp_pct": 38.0, "ft_pct": 78.5, "gp": 60, "mpg": 28.5}},
    # CLE
    {"id": "达里厄斯-加兰-CLE", "name": "达里厄斯·加兰", "position": "PG", "team": "骑士", "stats": {"pts": 21.5, "ast": 7.5, "reb": 3.2, "stl": 1.3, "blk": 0.2, "fg_pct": 47.8, "tp_pct": 40.5, "ft_pct": 87.0, "gp": 72, "mpg": 33.8}},
    {"id": "贾勒特-阿伦-CLE", "name": "贾勒特·阿伦", "position": "C", "team": "骑士", "stats": {"pts": 15.2, "ast": 2.5, "reb": 10.8, "stl": 0.9, "blk": 1.5, "fg_pct": 67.5, "tp_pct": 0.0, "ft_pct": 73.0, "gp": 75, "mpg": 31.5}},
    {"id": "迪恩-韦德", "name": "迪恩·韦德", "position": "SF", "team": "骑士", "stats": {"pts": 6.5, "ast": 1.0, "reb": 4.5, "stl": 0.8, "blk": 0.5, "fg_pct": 43.0, "tp_pct": 39.2, "ft_pct": 72.0, "gp": 58, "mpg": 22.5}},
    # DAL
    {"id": "克莱-汤普森-DAL", "name": "克莱·汤普森", "position": "SG", "team": "独行侠", "stats": {"pts": 15.8, "ast": 2.2, "reb": 3.8, "stl": 0.8, "blk": 0.4, "fg_pct": 43.2, "tp_pct": 39.5, "ft_pct": 90.5, "gp": 68, "mpg": 28.5}},
    {"id": "PJ-华盛顿-DAL", "name": "PJ·华盛顿", "position": "PF", "team": "独行侠", "stats": {"pts": 13.8, "ast": 2.2, "reb": 7.2, "stl": 1.2, "blk": 1.0, "fg_pct": 44.8, "tp_pct": 36.5, "ft_pct": 72.0, "gp": 65, "mpg": 31.5}},
    {"id": "德雷克-莱夫利-DAL", "name": "德雷克·莱夫利", "position": "C", "team": "独行侠", "stats": {"pts": 9.8, "ast": 2.2, "reb": 8.5, "stl": 0.7, "blk": 1.5, "fg_pct": 68.5, "tp_pct": 0.0, "ft_pct": 58.0, "gp": 62, "mpg": 25.8}},
    # DEN
    {"id": "克里斯蒂安-布劳恩-DEN", "name": "克里斯蒂安·布劳恩", "position": "SG", "team": "掘金", "stats": {"pts": 16.2, "ast": 2.5, "reb": 5.5, "stl": 1.3, "blk": 0.6, "fg_pct": 56.5, "tp_pct": 38.5, "ft_pct": 78.0, "gp": 78, "mpg": 33.8}},
    {"id": "阿隆-戈登-DEN", "name": "阿隆·戈登", "position": "PF", "team": "掘金", "stats": {"pts": 13.2, "ast": 3.2, "reb": 6.2, "stl": 0.7, "blk": 0.5, "fg_pct": 52.5, "tp_pct": 30.5, "ft_pct": 65.0, "gp": 58, "mpg": 28.5}},
    # DET
    {"id": "贾登-艾维", "name": "贾登·艾维", "position": "SG", "team": "活塞", "stats": {"pts": 18.2, "ast": 4.5, "reb": 4.2, "stl": 1.0, "blk": 0.4, "fg_pct": 43.8, "tp_pct": 35.5, "ft_pct": 76.0, "gp": 68, "mpg": 31.5}},
    {"id": "奥萨尔-汤普森", "name": "奥萨尔·汤普森", "position": "SF", "team": "活塞", "stats": {"pts": 10.2, "ast": 2.8, "reb": 6.8, "stl": 1.8, "blk": 0.9, "fg_pct": 51.5, "tp_pct": 22.0, "ft_pct": 62.0, "gp": 62, "mpg": 28.5}},
    {"id": "托拜厄斯-哈里斯-DET", "name": "托拜厄斯·哈里斯", "position": "PF", "team": "活塞", "stats": {"pts": 12.8, "ast": 2.5, "reb": 5.8, "stl": 0.9, "blk": 0.5, "fg_pct": 47.2, "tp_pct": 35.8, "ft_pct": 85.0, "gp": 72, "mpg": 30.5}},
    {"id": "杰伦-杜伦-DET", "name": "杰伦·杜伦", "position": "C", "team": "活塞", "stats": {"pts": 12.8, "ast": 2.5, "reb": 11.2, "stl": 0.7, "blk": 1.2, "fg_pct": 65.5, "tp_pct": 0.0, "ft_pct": 68.0, "gp": 68, "mpg": 28.8}},
    # GSW
    {"id": "巴迪-希尔德-GSW", "name": "巴迪·希尔德", "position": "SG", "team": "勇士", "stats": {"pts": 12.5, "ast": 2.0, "reb": 3.5, "stl": 0.8, "blk": 0.3, "fg_pct": 42.8, "tp_pct": 38.5, "ft_pct": 85.0, "gp": 78, "mpg": 24.8}},
    {"id": "乔纳森-库明加-GSW", "name": "乔纳森·库明加", "position": "PF", "team": "勇士", "stats": {"pts": 17.5, "ast": 2.5, "reb": 5.8, "stl": 0.9, "blk": 0.6, "fg_pct": 48.5, "tp_pct": 33.5, "ft_pct": 72.0, "gp": 65, "mpg": 28.5}},
    {"id": "昆滕-波斯特", "name": "昆滕·波斯特", "position": "C", "team": "勇士", "stats": {"pts": 8.5, "ast": 1.5, "reb": 5.5, "stl": 0.5, "blk": 0.7, "fg_pct": 48.5, "tp_pct": 38.0, "ft_pct": 72.0, "gp": 45, "mpg": 20.5}},
    # HOU
    {"id": "阿门-汤普森-HOU", "name": "阿门·汤普森", "position": "SG", "team": "火箭", "stats": {"pts": 14.8, "ast": 4.5, "reb": 7.5, "stl": 1.6, "blk": 1.0, "fg_pct": 54.5, "tp_pct": 28.0, "ft_pct": 68.0, "gp": 75, "mpg": 30.5}},
    {"id": "狄龙-布鲁克斯-HOU", "name": "狄龙·布鲁克斯", "position": "SF", "team": "火箭", "stats": {"pts": 14.2, "ast": 1.8, "reb": 3.8, "stl": 0.9, "blk": 0.3, "fg_pct": 43.5, "tp_pct": 38.8, "ft_pct": 82.0, "gp": 72, "mpg": 31.5}},
    {"id": "小贾巴里-史密斯-HOU", "name": "小贾巴里·史密斯", "position": "PF", "team": "火箭", "stats": {"pts": 12.5, "ast": 1.8, "reb": 7.8, "stl": 0.7, "blk": 1.0, "fg_pct": 44.8, "tp_pct": 36.5, "ft_pct": 80.0, "gp": 70, "mpg": 30.5}},
    # IND
    {"id": "安德鲁-内姆哈德-IND", "name": "安德鲁·内姆哈德", "position": "PG", "team": "步行者", "stats": {"pts": 12.5, "ast": 5.5, "reb": 3.5, "stl": 1.2, "blk": 0.2, "fg_pct": 47.5, "tp_pct": 37.5, "ft_pct": 80.0, "gp": 62, "mpg": 29.5}},
    {"id": "阿伦-内史密斯", "name": "阿伦·内史密斯", "position": "SF", "team": "步行者", "stats": {"pts": 11.2, "ast": 1.8, "reb": 4.2, "stl": 0.8, "blk": 0.5, "fg_pct": 48.5, "tp_pct": 42.5, "ft_pct": 80.0, "gp": 55, "mpg": 27.5}},
    {"id": "迈尔斯-特纳-IND", "name": "迈尔斯·特纳", "position": "C", "team": "步行者", "stats": {"pts": 17.2, "ast": 1.5, "reb": 7.5, "stl": 0.7, "blk": 2.2, "fg_pct": 48.5, "tp_pct": 36.5, "ft_pct": 78.0, "gp": 72, "mpg": 29.5}},
    # LAC
    {"id": "詹姆斯-哈登-LAC", "name": "詹姆斯·哈登", "position": "PG", "team": "快船", "stats": {"pts": 17.5, "ast": 8.8, "reb": 5.2, "stl": 1.3, "blk": 0.6, "fg_pct": 41.5, "tp_pct": 36.5, "ft_pct": 87.0, "gp": 72, "mpg": 34.5}},
    {"id": "诺曼-鲍威尔-LAC", "name": "诺曼·鲍威尔", "position": "SG", "team": "快船", "stats": {"pts": 20.8, "ast": 2.0, "reb": 3.5, "stl": 1.1, "blk": 0.3, "fg_pct": 48.8, "tp_pct": 42.5, "ft_pct": 83.0, "gp": 62, "mpg": 32.8}},
    {"id": "克里斯-邓恩-LAC", "name": "克里斯·邓恩", "position": "SF", "team": "快船", "stats": {"pts": 6.8, "ast": 3.5, "reb": 3.8, "stl": 1.8, "blk": 0.4, "fg_pct": 45.5, "tp_pct": 34.0, "ft_pct": 68.0, "gp": 68, "mpg": 24.5}},
    # LAL
    {"id": "八村垒-LAL", "name": "八村垒", "position": "SF", "team": "湖人", "stats": {"pts": 13.2, "ast": 1.5, "reb": 5.2, "stl": 0.8, "blk": 0.5, "fg_pct": 52.5, "tp_pct": 41.5, "ft_pct": 75.0, "gp": 65, "mpg": 31.5}},
    {"id": "多里安-芬尼-史密斯-LAL", "name": "多里安·芬尼-史密斯", "position": "PF", "team": "湖人", "stats": {"pts": 8.8, "ast": 1.5, "reb": 4.5, "stl": 0.9, "blk": 0.5, "fg_pct": 44.5, "tp_pct": 38.5, "ft_pct": 72.0, "gp": 65, "mpg": 28.5}},
    {"id": "贾克森-海斯", "name": "贾克森·海斯", "position": "C", "team": "湖人", "stats": {"pts": 7.2, "ast": 1.2, "reb": 5.5, "stl": 0.6, "blk": 1.0, "fg_pct": 68.5, "tp_pct": 0.0, "ft_pct": 68.0, "gp": 55, "mpg": 22.5}},
    # MEM
    {"id": "斯科蒂-皮蓬-MEM", "name": "小斯科蒂·皮蓬", "position": "PG", "team": "灰熊", "stats": {"pts": 11.8, "ast": 5.2, "reb": 3.8, "stl": 1.5, "blk": 0.3, "fg_pct": 46.5, "tp_pct": 36.5, "ft_pct": 75.0, "gp": 72, "mpg": 26.5}},
    {"id": "卢克-肯纳德", "name": "卢克·肯纳德", "position": "SG", "team": "灰熊", "stats": {"pts": 10.5, "ast": 3.5, "reb": 3.2, "stl": 0.6, "blk": 0.1, "fg_pct": 46.8, "tp_pct": 44.5, "ft_pct": 88.0, "gp": 62, "mpg": 23.8}},
    {"id": "桑蒂-阿尔达马-MEM", "name": "桑蒂·阿尔达马", "position": "PF", "team": "灰熊", "stats": {"pts": 14.2, "ast": 2.5, "reb": 7.2, "stl": 0.8, "blk": 0.7, "fg_pct": 48.5, "tp_pct": 36.5, "ft_pct": 72.0, "gp": 68, "mpg": 27.5}},
    # MIA
    {"id": "特里-罗齐尔-MIA", "name": "特里·罗齐尔", "position": "PG", "team": "热火", "stats": {"pts": 14.5, "ast": 4.8, "reb": 4.2, "stl": 0.8, "blk": 0.3, "fg_pct": 42.5, "tp_pct": 34.5, "ft_pct": 85.0, "gp": 62, "mpg": 30.5}},
    {"id": "凯莱布-马丁", "name": "凯莱布·马丁", "position": "SF", "team": "热火", "stats": {"pts": 10.2, "ast": 2.0, "reb": 4.8, "stl": 0.9, "blk": 0.4, "fg_pct": 45.5, "tp_pct": 36.5, "ft_pct": 76.0, "gp": 60, "mpg": 27.8}},
    {"id": "凯尔-韦尔", "name": "凯尔·韦尔", "position": "C", "team": "热火", "stats": {"pts": 8.8, "ast": 1.0, "reb": 7.2, "stl": 0.6, "blk": 1.3, "fg_pct": 56.5, "tp_pct": 28.0, "ft_pct": 68.0, "gp": 55, "mpg": 22.5}},
    # MIL
    {"id": "达米安-利拉德-MIL", "name": "达米安·利拉德", "position": "PG", "team": "雄鹿", "stats": {"pts": 24.5, "ast": 7.2, "reb": 4.5, "stl": 1.1, "blk": 0.2, "fg_pct": 44.5, "tp_pct": 37.5, "ft_pct": 92.0, "gp": 62, "mpg": 35.2}},
    {"id": "小加里-特伦特-MIL", "name": "小加里·特伦特", "position": "SG", "team": "雄鹿", "stats": {"pts": 11.2, "ast": 1.5, "reb": 2.5, "stl": 1.0, "blk": 0.2, "fg_pct": 43.5, "tp_pct": 38.5, "ft_pct": 85.0, "gp": 72, "mpg": 25.8}},
    {"id": "博比-波蒂斯-MIL", "name": "博比·波蒂斯", "position": "C", "team": "雄鹿", "stats": {"pts": 13.5, "ast": 2.0, "reb": 8.5, "stl": 0.8, "blk": 0.6, "fg_pct": 49.5, "tp_pct": 38.5, "ft_pct": 78.0, "gp": 72, "mpg": 25.8}},
    # MIN
    {"id": "杰登-麦克丹尼尔斯-MIN", "name": "杰登·麦克丹尼尔斯", "position": "SF", "team": "森林狼", "stats": {"pts": 11.5, "ast": 1.8, "reb": 5.8, "stl": 1.2, "blk": 0.9, "fg_pct": 48.5, "tp_pct": 35.5, "ft_pct": 75.0, "gp": 75, "mpg": 30.8}},
    {"id": "迈克-康利-MIN", "name": "迈克·康利", "position": "PG", "team": "森林狼", "stats": {"pts": 9.5, "ast": 5.5, "reb": 2.8, "stl": 1.2, "blk": 0.2, "fg_pct": 42.5, "tp_pct": 40.5, "ft_pct": 88.0, "gp": 65, "mpg": 26.5}},
    {"id": "唐特-迪温琴佐-MIN", "name": "唐特·迪温琴佐", "position": "SG", "team": "森林狼", "stats": {"pts": 12.5, "ast": 3.5, "reb": 3.8, "stl": 1.3, "blk": 0.3, "fg_pct": 43.5, "tp_pct": 39.5, "ft_pct": 78.0, "gp": 72, "mpg": 27.5}},
    # NOP
    {"id": "特雷-墨菲-NOP", "name": "特雷·墨菲", "position": "SG", "team": "鹈鹕", "stats": {"pts": 22.5, "ast": 3.2, "reb": 5.5, "stl": 1.1, "blk": 0.7, "fg_pct": 46.5, "tp_pct": 38.5, "ft_pct": 86.0, "gp": 58, "mpg": 34.5}},
    {"id": "布鲁斯-布朗-NOP", "name": "布鲁斯·布朗", "position": "SF", "team": "鹈鹕", "stats": {"pts": 10.5, "ast": 2.8, "reb": 4.5, "stl": 0.9, "blk": 0.4, "fg_pct": 46.5, "tp_pct": 34.5, "ft_pct": 75.0, "gp": 62, "mpg": 27.5}},
    {"id": "优素福-努尔基奇-NOP", "name": "优素福·努尔基奇", "position": "C", "team": "鹈鹕", "stats": {"pts": 9.2, "ast": 2.5, "reb": 9.5, "stl": 0.8, "blk": 1.0, "fg_pct": 50.5, "tp_pct": 25.0, "ft_pct": 68.0, "gp": 58, "mpg": 25.5}},
    # NYK
    {"id": "OG-阿奴诺比-NYK", "name": "OG·阿奴诺比", "position": "SF", "team": "尼克斯", "stats": {"pts": 17.5, "ast": 2.2, "reb": 5.5, "stl": 1.5, "blk": 0.8, "fg_pct": 48.5, "tp_pct": 38.5, "ft_pct": 78.0, "gp": 68, "mpg": 35.5}},
    {"id": "约什-哈特-NYK", "name": "约什·哈特", "position": "PF", "team": "尼克斯", "stats": {"pts": 12.8, "ast": 5.5, "reb": 8.8, "stl": 1.3, "blk": 0.4, "fg_pct": 50.5, "tp_pct": 34.5, "ft_pct": 75.0, "gp": 75, "mpg": 36.5}},
    {"id": "米切尔-罗宾逊-NYK", "name": "米切尔·罗宾逊", "position": "C", "team": "尼克斯", "stats": {"pts": 6.5, "ast": 0.8, "reb": 9.5, "stl": 0.9, "blk": 1.8, "fg_pct": 62.5, "tp_pct": 0.0, "ft_pct": 48.0, "gp": 42, "mpg": 24.5}},
    # OKC
    {"id": "杰伦-威廉姆斯-OKC", "name": "杰伦·威廉姆斯", "position": "SF", "team": "雷霆", "stats": {"pts": 21.5, "ast": 5.5, "reb": 5.8, "stl": 1.7, "blk": 0.8, "fg_pct": 50.5, "tp_pct": 38.5, "ft_pct": 80.0, "gp": 72, "mpg": 33.5}},
    {"id": "吕冈茨-多尔特-OKC", "name": "吕冈茨·多尔特", "position": "SG", "team": "雷霆", "stats": {"pts": 11.2, "ast": 1.8, "reb": 4.2, "stl": 1.0, "blk": 0.6, "fg_pct": 44.5, "tp_pct": 39.5, "ft_pct": 78.0, "gp": 72, "mpg": 28.5}},
    {"id": "亚历克斯-卡鲁索-OKC", "name": "亚历克斯·卡鲁索", "position": "PG", "team": "雷霆", "stats": {"pts": 7.5, "ast": 3.5, "reb": 3.2, "stl": 1.8, "blk": 0.6, "fg_pct": 44.5, "tp_pct": 38.5, "ft_pct": 75.0, "gp": 58, "mpg": 22.5}},
    # ORL
    {"id": "科尔-安东尼-ORL", "name": "科尔·安东尼", "position": "PG", "team": "魔术", "stats": {"pts": 11.5, "ast": 4.5, "reb": 3.8, "stl": 0.8, "blk": 0.3, "fg_pct": 43.5, "tp_pct": 35.5, "ft_pct": 82.0, "gp": 72, "mpg": 24.5}},
    {"id": "肯塔维奥斯-波普-ORL", "name": "肯塔维奥斯·波普", "position": "SG", "team": "魔术", "stats": {"pts": 9.5, "ast": 1.8, "reb": 2.5, "stl": 1.2, "blk": 0.3, "fg_pct": 43.5, "tp_pct": 38.5, "ft_pct": 86.0, "gp": 72, "mpg": 28.5}},
    {"id": "温德尔-卡特-ORL", "name": "温德尔·卡特", "position": "C", "team": "魔术", "stats": {"pts": 10.5, "ast": 2.2, "reb": 8.2, "stl": 0.7, "blk": 0.6, "fg_pct": 50.5, "tp_pct": 32.5, "ft_pct": 72.0, "gp": 58, "mpg": 26.5}},
    # PHI
    {"id": "贾里德-麦凯恩", "name": "贾里德·麦凯恩", "position": "PG", "team": "76人", "stats": {"pts": 15.5, "ast": 3.5, "reb": 3.2, "stl": 0.8, "blk": 0.1, "fg_pct": 44.5, "tp_pct": 38.5, "ft_pct": 83.0, "gp": 42, "mpg": 28.5}},
    {"id": "凯利-乌布雷-PHI", "name": "凯利·乌布雷", "position": "SF", "team": "76人", "stats": {"pts": 14.5, "ast": 1.8, "reb": 5.8, "stl": 1.3, "blk": 0.6, "fg_pct": 45.5, "tp_pct": 33.5, "ft_pct": 75.0, "gp": 68, "mpg": 31.5}},
    {"id": "盖尔雄-亚布塞莱", "name": "盖尔雄·亚布塞莱", "position": "PF", "team": "76人", "stats": {"pts": 9.5, "ast": 1.8, "reb": 5.5, "stl": 0.7, "blk": 0.4, "fg_pct": 50.5, "tp_pct": 38.5, "ft_pct": 72.0, "gp": 65, "mpg": 22.5}},
    {"id": "德安德烈-乔丹-PHI", "name": "德安德烈·乔丹", "position": "C", "team": "76人", "stats": {"pts": 3.5, "ast": 0.8, "reb": 5.5, "stl": 0.3, "blk": 0.6, "fg_pct": 62.5, "tp_pct": 0.0, "ft_pct": 48.0, "gp": 48, "mpg": 14.5}},
    # PHX
    {"id": "泰厄斯-琼斯-PHX", "name": "泰厄斯·琼斯", "position": "PG", "team": "太阳", "stats": {"pts": 11.5, "ast": 7.2, "reb": 2.8, "stl": 1.1, "blk": 0.2, "fg_pct": 47.5, "tp_pct": 42.5, "ft_pct": 85.0, "gp": 75, "mpg": 30.5}},
    {"id": "罗伊斯-奥尼尔-PHX", "name": "罗伊斯·奥尼尔", "position": "SF", "team": "太阳", "stats": {"pts": 8.5, "ast": 2.5, "reb": 5.5, "stl": 0.9, "blk": 0.6, "fg_pct": 43.5, "tp_pct": 38.5, "ft_pct": 72.0, "gp": 72, "mpg": 26.5}},
    {"id": "尼克-理查兹-PHX", "name": "尼克·理查兹", "position": "C", "team": "太阳", "stats": {"pts": 9.5, "ast": 1.0, "reb": 8.5, "stl": 0.4, "blk": 1.2, "fg_pct": 63.5, "tp_pct": 0.0, "ft_pct": 72.0, "gp": 62, "mpg": 24.5}},
    # POR
    {"id": "斯库特-亨德森-POR", "name": "斯库特·亨德森", "position": "PG", "team": "开拓者", "stats": {"pts": 14.5, "ast": 6.5, "reb": 3.5, "stl": 1.2, "blk": 0.3, "fg_pct": 42.5, "tp_pct": 34.5, "ft_pct": 80.0, "gp": 68, "mpg": 28.5}},
    {"id": "谢登-夏普", "name": "谢登·夏普", "position": "SG", "team": "开拓者", "stats": {"pts": 18.5, "ast": 2.8, "reb": 5.2, "stl": 0.9, "blk": 0.4, "fg_pct": 45.5, "tp_pct": 34.5, "ft_pct": 80.0, "gp": 65, "mpg": 32.5}},
    {"id": "德尼-阿夫迪亚-POR", "name": "德尼·阿夫迪亚", "position": "SF", "team": "开拓者", "stats": {"pts": 16.5, "ast": 3.8, "reb": 7.2, "stl": 1.1, "blk": 0.5, "fg_pct": 48.5, "tp_pct": 36.5, "ft_pct": 76.0, "gp": 72, "mpg": 30.5}},
    {"id": "多诺万-克林根-POR", "name": "多诺万·克林根", "position": "C", "team": "开拓者", "stats": {"pts": 6.5, "ast": 1.0, "reb": 7.5, "stl": 0.5, "blk": 1.8, "fg_pct": 54.5, "tp_pct": 28.0, "ft_pct": 58.0, "gp": 58, "mpg": 20.5}},
    # SAC
    {"id": "基冈-默里-SAC", "name": "基冈·默里", "position": "SF", "team": "国王", "stats": {"pts": 14.5, "ast": 1.8, "reb": 6.5, "stl": 1.0, "blk": 0.8, "fg_pct": 45.5, "tp_pct": 36.5, "ft_pct": 80.0, "gp": 72, "mpg": 33.5}},
    {"id": "特雷-莱尔斯-SAC", "name": "特雷·莱尔斯", "position": "PF", "team": "国王", "stats": {"pts": 7.8, "ast": 1.5, "reb": 5.2, "stl": 0.4, "blk": 0.4, "fg_pct": 44.5, "tp_pct": 37.5, "ft_pct": 72.0, "gp": 65, "mpg": 20.5}},
    {"id": "约纳斯-瓦兰丘纳斯-SAC", "name": "约纳斯·瓦兰丘纳斯", "position": "C", "team": "国王", "stats": {"pts": 9.5, "ast": 2.2, "reb": 8.8, "stl": 0.5, "blk": 0.7, "fg_pct": 54.5, "tp_pct": 28.0, "ft_pct": 78.0, "gp": 72, "mpg": 22.5}},
    # SAS
    {"id": "达龙-福克斯-SAS", "name": "达龙·福克斯", "position": "PG", "team": "马刺", "stats": {"pts": 23.5, "ast": 6.5, "reb": 4.5, "stl": 1.5, "blk": 0.4, "fg_pct": 46.5, "tp_pct": 34.5, "ft_pct": 78.0, "gp": 68, "mpg": 35.5}},
    {"id": "德文-瓦塞尔", "name": "德文·瓦塞尔", "position": "SG", "team": "马刺", "stats": {"pts": 18.5, "ast": 3.5, "reb": 4.2, "stl": 1.2, "blk": 0.4, "fg_pct": 45.5, "tp_pct": 37.5, "ft_pct": 80.0, "gp": 62, "mpg": 32.5}},
    {"id": "凯尔登-约翰逊-SAS", "name": "凯尔登·约翰逊", "position": "SF", "team": "马刺", "stats": {"pts": 12.5, "ast": 2.0, "reb": 5.5, "stl": 0.7, "blk": 0.3, "fg_pct": 46.5, "tp_pct": 34.5, "ft_pct": 76.0, "gp": 72, "mpg": 26.5}},
    {"id": "杰里米-索汉-SAS", "name": "杰里米·索汉", "position": "PF", "team": "马刺", "stats": {"pts": 11.5, "ast": 2.8, "reb": 6.5, "stl": 0.9, "blk": 0.5, "fg_pct": 46.5, "tp_pct": 32.5, "ft_pct": 72.0, "gp": 58, "mpg": 28.5}},
    # TOR
    {"id": "伊曼纽尔-奎克利-TOR", "name": "伊曼纽尔·奎克利", "position": "PG", "team": "猛龙", "stats": {"pts": 17.5, "ast": 6.2, "reb": 4.2, "stl": 0.9, "blk": 0.2, "fg_pct": 43.5, "tp_pct": 38.5, "ft_pct": 85.0, "gp": 48, "mpg": 32.5}},
    {"id": "雅各布-珀尔特尔-TOR", "name": "雅各布·珀尔特尔", "position": "C", "team": "猛龙", "stats": {"pts": 14.5, "ast": 2.8, "reb": 10.2, "stl": 0.8, "blk": 1.5, "fg_pct": 62.5, "tp_pct": 0.0, "ft_pct": 58.0, "gp": 62, "mpg": 28.5}},
    {"id": "奥柴-阿巴吉", "name": "奥柴·阿巴吉", "position": "SF", "team": "猛龙", "stats": {"pts": 10.5, "ast": 1.8, "reb": 4.2, "stl": 0.9, "blk": 0.5, "fg_pct": 46.5, "tp_pct": 38.5, "ft_pct": 75.0, "gp": 68, "mpg": 27.5}},
    {"id": "乔纳森-莫格博", "name": "乔纳森·莫格博", "position": "PF", "team": "猛龙", "stats": {"pts": 8.5, "ast": 1.5, "reb": 5.8, "stl": 0.8, "blk": 0.5, "fg_pct": 47.5, "tp_pct": 34.5, "ft_pct": 68.0, "gp": 58, "mpg": 22.5}},
    # UTA
    {"id": "科比-乔治-UTA", "name": "科比·乔治", "position": "PG", "team": "爵士", "stats": {"pts": 15.5, "ast": 5.5, "reb": 3.8, "stl": 0.8, "blk": 0.2, "fg_pct": 40.5, "tp_pct": 34.5, "ft_pct": 80.0, "gp": 68, "mpg": 31.5}},
    {"id": "科林-塞克斯顿-UTA", "name": "科林·塞克斯顿", "position": "SG", "team": "爵士", "stats": {"pts": 17.5, "ast": 4.5, "reb": 2.8, "stl": 0.8, "blk": 0.2, "fg_pct": 47.5, "tp_pct": 38.5, "ft_pct": 85.0, "gp": 72, "mpg": 29.5}},
    {"id": "约翰-科林斯-UTA", "name": "约翰·科林斯", "position": "PF", "team": "爵士", "stats": {"pts": 18.5, "ast": 2.5, "reb": 9.2, "stl": 0.8, "blk": 1.0, "fg_pct": 54.5, "tp_pct": 38.5, "ft_pct": 78.0, "gp": 68, "mpg": 31.5}},
    # WAS
    {"id": "马尔科姆-布罗格登-WAS", "name": "马尔科姆·布罗格登", "position": "PG", "team": "奇才", "stats": {"pts": 14.5, "ast": 5.2, "reb": 4.2, "stl": 0.8, "blk": 0.3, "fg_pct": 45.5, "tp_pct": 39.5, "ft_pct": 86.0, "gp": 48, "mpg": 28.5}},
    {"id": "凯肖恩-乔治-WAS", "name": "凯肖恩·乔治", "position": "SF", "team": "奇才", "stats": {"pts": 9.5, "ast": 2.2, "reb": 4.5, "stl": 0.9, "blk": 0.6, "fg_pct": 42.5, "tp_pct": 34.5, "ft_pct": 72.0, "gp": 68, "mpg": 27.5}},
    {"id": "亚历山大-萨尔-WAS", "name": "亚历山大·萨尔", "position": "C", "team": "奇才", "stats": {"pts": 13.5, "ast": 2.5, "reb": 7.8, "stl": 0.7, "blk": 1.8, "fg_pct": 44.5, "tp_pct": 32.5, "ft_pct": 68.0, "gp": 68, "mpg": 28.5}},
    {"id": "布兰丁-波杰姆斯基-WAS", "name": "布兰丁·波杰姆斯基", "position": "SG", "team": "奇才", "stats": {"pts": 10.5, "ast": 4.2, "reb": 5.5, "stl": 1.0, "blk": 0.3, "fg_pct": 44.5, "tp_pct": 35.5, "ft_pct": 72.0, "gp": 58, "mpg": 27.5}},
    # Additional key players for teams with thin coverage
    {"id": "以赛亚-哈尔滕施泰因-OKC", "name": "以赛亚·哈尔滕施泰因", "position": "C", "team": "雷霆", "stats": {"pts": 13.5, "ast": 4.5, "reb": 11.5, "stl": 1.0, "blk": 1.2, "fg_pct": 58.5, "tp_pct": 0.0, "ft_pct": 68.0, "gp": 58, "mpg": 30.5}},
    {"id": "丹尼尔-加福德-DAL", "name": "丹尼尔·加福德", "position": "C", "team": "独行侠", "stats": {"pts": 12.5, "ast": 1.5, "reb": 7.5, "stl": 0.6, "blk": 2.0, "fg_pct": 72.5, "tp_pct": 0.0, "ft_pct": 68.0, "gp": 68, "mpg": 24.5}},
    {"id": "沃克-凯斯勒-UTA", "name": "沃克·凯斯勒", "position": "C", "team": "爵士", "stats": {"pts": 10.5, "ast": 1.5, "reb": 11.5, "stl": 0.5, "blk": 2.8, "fg_pct": 68.5, "tp_pct": 0.0, "ft_pct": 55.0, "gp": 65, "mpg": 29.5}},
    {"id": "马克-威廉姆斯-CHA", "name": "马克·威廉姆斯", "position": "C", "team": "黄蜂", "stats": {"pts": 14.5, "ast": 2.0, "reb": 10.5, "stl": 0.7, "blk": 1.5, "fg_pct": 62.5, "tp_pct": 0.0, "ft_pct": 72.0, "gp": 42, "mpg": 27.5}},
    {"id": "杰拉米-格兰特-POR", "name": "杰拉米·格兰特", "position": "PF", "team": "开拓者", "stats": {"pts": 15.5, "ast": 2.5, "reb": 4.5, "stl": 0.8, "blk": 0.8, "fg_pct": 44.5, "tp_pct": 38.5, "ft_pct": 82.0, "gp": 55, "mpg": 32.5}},
    {"id": "安芬尼-西蒙斯-POR", "name": "安芬尼·西蒙斯", "position": "PG", "team": "开拓者", "stats": {"pts": 20.5, "ast": 5.2, "reb": 3.5, "stl": 0.8, "blk": 0.2, "fg_pct": 43.5, "tp_pct": 37.5, "ft_pct": 88.0, "gp": 65, "mpg": 33.5}},
    {"id": "马利克-蒙克-SAC", "name": "马利克·蒙克", "position": "SG", "team": "国王", "stats": {"pts": 18.5, "ast": 6.2, "reb": 3.8, "stl": 0.9, "blk": 0.5, "fg_pct": 44.5, "tp_pct": 36.5, "ft_pct": 82.0, "gp": 72, "mpg": 29.5}},
    {"id": "纳兹-里德-MIN", "name": "纳兹·里德", "position": "C", "team": "森林狼", "stats": {"pts": 14.5, "ast": 2.0, "reb": 6.5, "stl": 0.8, "blk": 1.0, "fg_pct": 50.5, "tp_pct": 40.5, "ft_pct": 75.0, "gp": 75, "mpg": 27.5}},
    {"id": "科比-怀特-CHI", "name": "科比·怀特", "position": "PG", "team": "公牛", "stats": {"pts": 19.5, "ast": 5.5, "reb": 4.2, "stl": 1.0, "blk": 0.3, "fg_pct": 44.5, "tp_pct": 37.5, "ft_pct": 84.0, "gp": 72, "mpg": 34.5}},
    {"id": "克里斯-保罗-SAS", "name": "克里斯·保罗", "position": "PG", "team": "马刺", "stats": {"pts": 9.5, "ast": 7.5, "reb": 3.8, "stl": 1.2, "blk": 0.2, "fg_pct": 45.5, "tp_pct": 38.5, "ft_pct": 88.0, "gp": 68, "mpg": 27.5}},
    {"id": "布鲁克-洛佩斯-MIL", "name": "布鲁克·洛佩斯", "position": "C", "team": "雄鹿", "stats": {"pts": 13.5, "ast": 1.8, "reb": 5.8, "stl": 0.7, "blk": 2.2, "fg_pct": 48.5, "tp_pct": 36.5, "ft_pct": 82.0, "gp": 75, "mpg": 28.5}},
]

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


def main():
    # ── 1. Scrape Hupu ──
    print("Scraping Hupu NBA stats...")
    cat_data = {}
    for cat in CATEGORIES:
        url = f"{BASE}/{cat}"
        print(f"  {cat} ...", end=" ", flush=True)
        rows = parse_table(fetch(url))
        cat_data[cat] = {r['球员']: r for r in rows}
        print(f"{len(rows)} players")
        time.sleep(0.5)

    # ── 2. Build current players from Hupu data ──
    all_names = set()
    for cat in CATEGORIES:
        all_names.update(cat_data[cat].keys())

    # Collect all players that appear in pts (scoring) category
    players = []
    for name in all_names:
        if name not in cat_data['pts']:
            continue
        cat_count = sum(1 for cat in CATEGORIES if name in cat_data[cat])

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

        # Team from pts page
        p['team'] = cat_data['pts'][name].get('球队', '')

        players.append(p)

    print(f"\nHupu current players: {len(players)}")

    # ── 3. Calculate percentiles ──
    def pctile(values, v):
        if not values or max(values) == min(values):
            return 50
        rank = sum(1 for x in values if x <= v)
        return round((rank / len(values)) * 99)

    all_pts = [p['pts'] for p in players]
    all_tpp = [p['tp_pct'] for p in players]
    all_ftp = [p['ft_pct'] for p in players]
    all_ast = [p['ast'] for p in players]
    all_reb = [p['reb'] for p in players]
    all_stl = [p['stl'] for p in players]
    all_blk = [p['blk'] for p in players]
    all_tov = [p['tov'] for p in players]
    all_fga = [p.get('fga', 0) for p in players]
    all_fgm = [p.get('fgm', 0) for p in players]

    # ── 4. Known star overrides ──
    overrides = {
        '斯蒂芬-库里': {'threePT': 99, 'midRange': 90, 'rimFin': 60, 'FT': 95, 'playmaking': 92, 'ballHandle': 97, 'perimD': 60, 'rimProt': 10, 'helpSwitch': 55, 'steals': 70, 'rebounding': 45, 'athleticism': 75},
        '尼古拉-约基奇': {'threePT': 78, 'midRange': 95, 'rimFin': 95, 'FT': 85, 'playmaking': 99, 'ballHandle': 90, 'perimD': 60, 'rimProt': 78, 'helpSwitch': 72, 'steals': 65, 'rebounding': 95, 'athleticism': 68},
        '扬尼斯-阿德托昆博': {'threePT': 30, 'midRange': 55, 'rimFin': 99, 'FT': 50, 'playmaking': 82, 'ballHandle': 84, 'perimD': 88, 'rimProt': 95, 'helpSwitch': 85, 'steals': 72, 'rebounding': 90, 'athleticism': 99},
        '卢卡-东契奇': {'threePT': 82, 'midRange': 88, 'rimFin': 85, 'FT': 78, 'playmaking': 95, 'ballHandle': 94, 'perimD': 68, 'rimProt': 40, 'helpSwitch': 60, 'steals': 70, 'rebounding': 72, 'athleticism': 72},
        '凯文-杜兰特': {'threePT': 90, 'midRange': 97, 'rimFin': 85, 'FT': 88, 'playmaking': 82, 'ballHandle': 86, 'perimD': 80, 'rimProt': 82, 'helpSwitch': 78, 'steals': 68, 'rebounding': 72, 'athleticism': 78},
        '杰森-塔图姆': {'threePT': 85, 'midRange': 84, 'rimFin': 82, 'FT': 82, 'playmaking': 78, 'ballHandle': 84, 'perimD': 86, 'rimProt': 78, 'helpSwitch': 80, 'steals': 72, 'rebounding': 76, 'athleticism': 88},
        '谢伊-吉尔杰斯-亚历山大': {'threePT': 78, 'midRange': 92, 'rimFin': 88, 'FT': 90, 'playmaking': 86, 'ballHandle': 92, 'perimD': 88, 'rimProt': 55, 'helpSwitch': 72, 'steals': 85, 'rebounding': 60, 'athleticism': 86},
        '安东尼-爱德华兹': {'threePT': 88, 'midRange': 80, 'rimFin': 90, 'FT': 82, 'playmaking': 72, 'ballHandle': 84, 'perimD': 82, 'rimProt': 55, 'helpSwitch': 68, 'steals': 72, 'rebounding': 65, 'athleticism': 96},
        '科怀-伦纳德': {'threePT': 84, 'midRange': 94, 'rimFin': 82, 'FT': 88, 'playmaking': 70, 'ballHandle': 82, 'perimD': 94, 'rimProt': 68, 'helpSwitch': 80, 'steals': 88, 'rebounding': 68, 'athleticism': 82},
        '维克托-文班亚马': {'threePT': 72, 'midRange': 65, 'rimFin': 88, 'FT': 80, 'playmaking': 60, 'ballHandle': 68, 'perimD': 78, 'rimProt': 98, 'helpSwitch': 90, 'steals': 70, 'rebounding': 90, 'athleticism': 95},
        '乔尔-恩比德': {'threePT': 74, 'midRange': 88, 'rimFin': 92, 'FT': 88, 'playmaking': 72, 'ballHandle': 68, 'perimD': 84, 'rimProt': 94, 'helpSwitch': 76, 'steals': 65, 'rebounding': 85, 'athleticism': 78},
        '勒布朗-詹姆斯': {'threePT': 78, 'midRange': 82, 'rimFin': 94, 'FT': 72, 'playmaking': 94, 'ballHandle': 88, 'perimD': 78, 'rimProt': 72, 'helpSwitch': 82, 'steals': 68, 'rebounding': 78, 'athleticism': 85},
        '贾-莫兰特': {'threePT': 68, 'midRange': 72, 'rimFin': 92, 'FT': 78, 'playmaking': 88, 'ballHandle': 92, 'perimD': 60, 'rimProt': 25, 'helpSwitch': 50, 'steals': 65, 'rebounding': 48, 'athleticism': 96},
        '多诺万-米切尔': {'threePT': 84, 'midRange': 82, 'rimFin': 78, 'FT': 86, 'playmaking': 76, 'ballHandle': 86, 'perimD': 78, 'rimProt': 35, 'helpSwitch': 60, 'steals': 75, 'rebounding': 50, 'athleticism': 90},
        '泰雷斯-马克西': {'threePT': 82, 'midRange': 75, 'rimFin': 72, 'FT': 88, 'playmaking': 70, 'ballHandle': 84, 'perimD': 60, 'rimProt': 20, 'helpSwitch': 48, 'steals': 65, 'rebounding': 40, 'athleticism': 88},
        '凯德-坎宁安': {'threePT': 74, 'midRange': 78, 'rimFin': 72, 'FT': 85, 'playmaking': 82, 'ballHandle': 80, 'perimD': 68, 'rimProt': 45, 'helpSwitch': 62, 'steals': 65, 'rebounding': 65, 'athleticism': 74},
        '保罗-班切罗': {'threePT': 65, 'midRange': 78, 'rimFin': 84, 'FT': 72, 'playmaking': 72, 'ballHandle': 76, 'perimD': 65, 'rimProt': 58, 'helpSwitch': 60, 'steals': 58, 'rebounding': 72, 'athleticism': 84},
        '帕斯卡尔-西亚卡姆': {'threePT': 68, 'midRange': 80, 'rimFin': 82, 'FT': 76, 'playmaking': 68, 'ballHandle': 72, 'perimD': 74, 'rimProt': 60, 'helpSwitch': 68, 'steals': 62, 'rebounding': 72, 'athleticism': 80},
        '杰伦-布朗': {'threePT': 72, 'midRange': 78, 'rimFin': 85, 'FT': 75, 'playmaking': 62, 'ballHandle': 78, 'perimD': 80, 'rimProt': 45, 'helpSwitch': 65, 'steals': 70, 'rebounding': 60, 'athleticism': 92},
    }

    def match_override(name):
        if name in overrides:
            return overrides[name]
        alt = name.replace('·', '-')
        if alt in overrides:
            return overrides[alt]
        return None

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
            'ballHandle': pctile(all_tov, -p['tov']),
            'rebounding': pctile(all_reb, p['reb']),
            'athleticism': 50,
        }
        p['data'] = d
        p['scout'] = dict(d)

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

        ov = match_override(p['name'])
        if ov:
            p['attrs'] = ov
            for axis, val in ov.items():
                p['scout'][axis] = val

        # Fix broken ballHandle
        if p['attrs']['ballHandle'] < 10:
            p['attrs']['ballHandle'] = 50

        # Auto-detect position for unmapped players
        if not p['position']:
            if p['blk'] >= 1.5:
                p['position'] = 'C'
            elif p['ast'] >= 5:
                p['position'] = 'PG' if p['reb'] < 7 else 'SF'
            elif p['reb'] >= 10:
                p['position'] = 'PF'
            else:
                p['position'] = 'SF'

        p['color'] = TEAM_COLORS.get(p['team'], '#3b82f6')

    # ── 5. Add extra starters (not on Hupu leaderboards) ──
    hupu_names = {p['name'] for p in players}

    for es in EXTRA_STARTERS:
        if es['name'] not in hupu_names:
            s = es['stats']
            # Calculate percentile-based attrs for extra starters
            d = {
                'threePT':    pctile(all_tpp, s['tp_pct']),
                'midRange':   pctile(all_fgm, s['fg_pct'] * 8 * s['mpg'] / 36 * 0.45),
                'rimFin':     int(pctile(all_fga, s['pts'] * 0.35) * 0.5 + pctile(all_ftp, s['ft_pct']) * 0.5),
                'FT':         pctile(all_ftp, s['ft_pct']),
                'perimD':     int(pctile(all_stl, s['stl']) * 0.5 + 25),
                'rimProt':    pctile(all_blk, s['blk']),
                'helpSwitch': int((pctile(all_stl, s['stl']) + pctile(all_blk, s['blk'])) / 2),
                'steals':     pctile(all_stl, s['stl']),
                'playmaking': pctile(all_ast, s['ast']),
                'ballHandle': 50,
                'rebounding': pctile(all_reb, s['reb']),
                'athleticism': 50,
            }
            # Apply weighted blend
            w = {
                'threePT': 0.75, 'midRange': 0.4, 'rimFin': 0.4, 'FT': 0.75,
                'perimD': 0.35, 'rimProt': 0.4, 'helpSwitch': 0.25, 'steals': 0.5,
                'playmaking': 0.65, 'ballHandle': 0.4, 'rebounding': 0.55, 'athleticism': 0.15,
            }
            attrs = {}
            for axis in d:
                wd = w.get(axis, 0.5)
                score = round(wd * d[axis] + (1 - wd) * d[axis])
                attrs[axis] = max(1, min(99, score))

            players.append({
                'name': es['name'],
                'position': es['position'],
                'team': es['team'],
                'color': TEAM_COLORS.get(es['team'], '#3b82f6'),
                'pts': s['pts'], 'ast': s['ast'], 'reb': s['reb'],
                'stl': s['stl'], 'blk': s['blk'],
                'fg_pct': s['fg_pct'], 'tp_pct': s['tp_pct'], 'ft_pct': s['ft_pct'],
                'gp': s['gp'], 'mpg': s['mpg'],
                'attrs': attrs,
            })

    print(f"After adding extra starters: {len(players)} current players")

    # ── 6. Load existing legends and merge ──
    with open("players.json", "r", encoding="utf-8") as f:
        existing = json.load(f)

    # Keep legends/all-stars (players with 'season' field or non-current IDs)
    legends = [p for p in existing if p.get('season')]
    print(f"Existing legends/all-stars: {len(legends)}")

    # Build output: current players + legends
    current_names = {p['name'] for p in players}

    out = []
    for p in sorted(players, key=lambda x: x.get('pts', 0), reverse=True):
        out.append({
            'id': p['name'],
            'name': p['name'],
            'position': p['position'],
            'team': p.get('team', ''),
            'color': p.get('color', '#3b82f6'),
            'attrs': p['attrs'],
            'stats': {
                'pts': round(p['pts'], 1), 'ast': round(p['ast'], 1), 'reb': round(p['reb'], 1),
                'stl': round(p['stl'], 2), 'blk': round(p['blk'], 2),
                'fg_pct': round(p['fg_pct'], 1), 'tp_pct': round(p['tp_pct'], 1), 'ft_pct': round(p['ft_pct'], 1),
                'gp': p['gp'], 'mpg': round(p['mpg'], 1),
            }
        })

    # Add legends (skip duplicates by name)
    for l in legends:
        if l['name'] not in current_names:
            out.append(l)

    with open('players.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    # ── Summary ──
    current_count = sum(1 for p in out if not p.get('season'))
    legend_count = sum(1 for p in out if p.get('season'))
    pos_counts = {}
    team_counts = {}
    for p in out:
        pos_counts[p['position'] or '?'] = pos_counts.get(p['position'] or '?', 0) + 1
        if p.get('team'):
            team_counts[p['team']] = team_counts.get(p['team'], 0) + 1

    print(f"\nDone! {len(out)} total ({current_count} current + {legend_count} legends)")
    print(f"Positions: {pos_counts}")
    print(f"Teams represented: {len(team_counts)}")
    for team, count in sorted(team_counts.items(), key=lambda x: -x[1]):
        print(f"  {team}: {count}")


if __name__ == '__main__':
    main()
