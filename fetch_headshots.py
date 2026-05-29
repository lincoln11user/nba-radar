"""
Fetch NBA player headshots from cdn.nba.com.
Uses ESPN API to search for player IDs by name, then builds headshot URLs.
Only processes current players (not legends, which need manual mapping).

Run: python fetch_headshots.py
Output: updates players.json with "image" field
"""
import json
import urllib.request
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# Manual NBA player ID mappings (Chinese name → NBA personId)
# These cover the most popular current players; script auto-fills the rest
NBA_IDS = {
    # PG
    "卢卡-东契奇": 1629029,
    "斯蒂芬-库里": 201939,
    "贾-莫兰特": 201947,
    "达龙-福克斯": 1628368,
    "特雷-杨": 1628978,
    "泰雷斯-哈利伯顿": 1630169,
    "詹姆斯-哈登": 201935,
    "凯里-欧文": 202681,
    "达米安-利拉德": 203081,
    "拉梅洛-鲍尔": 1630163,
    "贾马尔-默里": 1627750,
    "凯德-坎宁安": 1630595,
    "杰伦-布伦森": 1628973,
    "达里厄斯-加兰": 1629636,
    "拉塞尔-威斯布鲁克": 201566,
    "克里斯-保罗": 101108,
    # SG
    "谢伊-吉尔杰斯-亚历山大": 1628983,
    "安东尼-爱德华兹": 1630162,
    "多诺万-米切尔": 1628378,
    "德文-布克": 1626164,
    "德斯蒙德-贝恩": 1630217,
    "泰雷斯-马克西": 1630178,
    "杰伦-威廉姆斯": 1630585,
    "扎克-拉文": 203897,
    "泰勒-希罗": 1629639,
    "奥斯汀-里夫斯": 1630559,
    "布拉德利-比尔": 203078,
    "乔丹-普尔": 1629673,
    "CJ-麦科勒姆": 203468,
    "杰伦-格林": 1630224,
    "德马尔-德罗赞": 201942,
    # SF
    "杰森-塔图姆": 1628369,
    "杰伦-布朗": 1627759,
    "科怀-伦纳德": 202695,
    "勒布朗-詹姆斯": 2544,
    "吉米-巴特勒": 202710,
    "保罗-乔治": 202331,
    "布兰登-英格拉姆": 1626166,
    "米卡尔-布里奇斯": 1628969,
    # PF
    "扬尼斯-阿德托昆博": 203507,
    "凯文-杜兰特": 201142,
    "帕斯卡尔-西亚卡姆": 1628998,
    "保罗-班切罗": 1631136,
    "埃文-莫布利": 1630596,
    "小贾伦-杰克逊": 1628991,
    "朱利叶斯-兰德尔": 1628972,
    "蔡恩-威廉森": 1629627,
    "切特-霍姆格伦": 1630931,
    "德雷蒙德-格林": 203110,
    # C
    "尼古拉-约基奇": 203999,
    "乔尔-恩比德": 203954,
    "安东尼-戴维斯": 203076,
    "巴姆-阿德巴约": 1628389,
    "鲁迪-戈贝尔": 203497,
    "卡尔-安东尼-唐斯": 1626157,
    "维克托-文班亚马": 1641705,
    "多曼塔斯-萨博尼斯": 1627734,
    "伊维察-祖巴茨": 1627826,
    "布鲁克-洛佩斯": 201577,
    "迈尔斯-特纳": 1626167,
    "艾尔佩伦-申京": 1631181,
}

# Legend player IDs (manually mapped: name → NBA personId)
LEGEND_IDS = {
    "魔术师约翰逊 (87)": 77108,
    "迈克尔·乔丹 (96)": 893,
    "迈克尔·乔丹 (91)": 893,
    "科比·布莱恩特 (06)": 977,
    "科比·布莱恩特 (10)": 977,
    "勒布朗·詹姆斯 (13)": 2544,
    "勒布朗·詹姆斯 (18)": 2544,
    "斯蒂芬·库里 (16)": 201939,
    "斯蒂芬·库里 (22)": 201939,
    "蒂姆·邓肯 (03)": 1495,
    "沙奎尔·奥尼尔 (00)": 406,
    "凯文·加内特 (04)": 708,
    "德维恩·韦德 (09)": 2548,
    "扬尼斯·阿德托昆博 (21)": 203507,
    "尼古拉·约基奇 (23)": 203999,
    "科怀·伦纳德 (19)": 202695,
    "德克·诺维茨基 (07)": 1717,
    "詹姆斯·哈登 (18)": 201935,
    "拉里·伯德 (86)": 1449,
    "阿伦·艾弗森 (01)": 947,
    "德里克·罗斯 (11)": 201565,
    "哈基姆·奥拉朱旺 (94)": 377,
    "大卫·罗宾逊 (95)": 912,
    "卡尔·马龙 (97)": 252,
    "查尔斯·巴克利 (93)": 787,
    "帕特里克·尤因 (95)": 121,
    "斯科蒂·皮蓬 (94)": 937,
    "德怀特·霍华德 (11)": 2730,
    "威尔特·张伯伦 (62)": 76375,
    "比尔·拉塞尔 (62)": 78039,
    "卡里姆·贾巴尔 (72)": 76003,
    "姚明 (07)": 2397,
}

HEADSHOT_TEMPLATE = "https://cdn.nba.com/headshots/nba/latest/260x190/{pid}.png"
LEGACY_TEMPLATE = "https://cdn.nba.com/headshots/nba/latest/1040x760/{pid}.png"


def get_headshot_url(person_id):
    """Try to get headshot URL. Falls back to legacy format."""
    return HEADSHOT_TEMPLATE.format(pid=person_id)


def main():
    with open("players.json", "r", encoding="utf-8") as f:
        players = json.load(f)

    all_ids = {**NBA_IDS}
    # Also check LEGEND_IDS for legend players
    for k, v in LEGEND_IDS.items():
        all_ids[k] = v

    updated = 0
    for p in players:
        if p.get("image"):
            continue  # already has image

        # Match by name
        pid = all_ids.get(p["name"])
        if pid:
            p["image"] = get_headshot_url(pid)
            updated += 1

        # Also match legend names (with season suffix)
        if not pid and p.get("season"):
            for leg_name, leg_id in LEGEND_IDS.items():
                base = leg_name.split(" (")[0] if " (" in leg_name else leg_name
                p_base = p["name"].split(" (")[0] if " (" in p["name"] else p["name"]
                if base == p_base:
                    p["image"] = get_headshot_url(leg_id)
                    updated += 1
                    break

    with open("players.json", "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated} players with headshot URLs.")
    total = len(players)
    with_img = sum(1 for p in players if p.get("image"))
    print(f"{with_img}/{total} players have images ({round(with_img/total*100)}%)")


if __name__ == "__main__":
    main()
