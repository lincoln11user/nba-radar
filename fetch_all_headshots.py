"""
Fetch NBA headshot URLs for all players missing images.
Uses nba_api to search for player IDs by English name.
"""
import json
import time
from nba_api.stats.static import players as nba_players

HEADSHOT_TEMPLATE = "https://cdn.nba.com/headshots/nba/latest/260x190/{pid}.png"

# Comprehensive mapping: player.id → English search name
ID_MAP = {
    # Mixed Chinese-English IDs (current players)
    "OG-阿奴诺比": "OG Anunoby",
    "VJ-阿尔瓦拉多": "Jose Alvarado",
    # Actually these might use the Chinese ID format, let's handle separately

    # Legends / historical stars
    "stockton-95": "John Stockton",
    "nash-06": "Steve Nash",
    "cp3-09": "Chris Paul",
    "westbrook-17": "Russell Westbrook",
    "kidd-03": "Jason Kidd",
    "tmac-03": "Tracy McGrady",
    "giannis-21": "Giannis Antetokounmpo",
    "jokic-23": "Nikola Jokic",

    # 90s-00s PG
    "payton-96": "Gary Payton",
    "hardaway-97": "Tim Hardaway",
    "kj-93": "Kevin Johnson",
    "parker-08": "Tony Parker",
    "billups-06": "Chauncey Billups",
    "arenas-06": "Gilbert Arenas",
    "rondo-12": "Rajon Rondo",
    "wall-17": "John Wall",
    "lowry-18": "Kyle Lowry",
    "kemba-19": "Kemba Walker",

    # 90s-00s SG
    "miller-95": "Reggie Miller",
    "allen-06": "Ray Allen",
    "carter-01": "Vince Carter",
    "ginobili-08": "Manu Ginobili",
    "richmond-96": "Mitch Richmond",

    # SF
    "hill-97": "Grant Hill",
    "pierce-08": "Paul Pierce",
    "melo-13": "Carmelo Anthony",
    "george-19": "Paul George",
    "marion-06": "Shawn Marion",

    # PF
    "kemp-96": "Shawn Kemp",
    "webber-01": "Chris Webber",
    "amare-08": "Amar'e Stoudemire",
    "bosh-10": "Chris Bosh",
    "love-14": "Kevin Love",
    "griffin-14": "Blake Griffin",
    "aldridge-16": "LaMarcus Aldridge",
    "sheed-01": "Rasheed Wallace",

    # C
    "mourning-99": "Alonzo Mourning",
    "mutombo-97": "Dikembe Mutombo",
    "benwallace-04": "Ben Wallace",
    "joneal-05": "Jermaine O'Neal",
    "cousins-16": "DeMarcus Cousins",
    "mgasol-15": "Marc Gasol",
    "noah-14": "Joakim Noah",
    "pgasol-09": "Pau Gasol",

    # 2010s All-Stars
    "klay-16": "Klay Thompson",
    "derozan-17": "DeMar DeRozan",
    "dwilliams-10": "Deron Williams",
    "joejohnson-10": "Joe Johnson",
    "brand-06": "Elton Brand",
    "peja-04": "Peja Stojakovic",
    "roy-09": "Brandon Roy",
    "horford-15": "Al Horford",
    "millsap-16": "Paul Millsap",
    "conley-19": "Mike Conley",
    "deng-13": "Luol Deng",
    "iguodala-12": "Andre Iguodala",
    "thomas-17": "Isaiah Thomas",
    "oladipo-18": "Victor Oladipo",
    "beal-20": "Bradley Beal",
    "jrue-19": "Jrue Holiday",
    "middleton-20": "Khris Middleton",
    "gobert-21": "Rudy Gobert",
    "randle-21": "Julius Randle",

    # 2020s All-Stars
    "sabonis-23": "Domantas Sabonis",
    "siakam-23": "Pascal Siakam",
    "markkanen-23": "Lauri Markkanen",
    "adebayo-23": "Bam Adebayo",
    "lamelo-22": "LaMelo Ball",
    "maxey-24": "Tyrese Maxey",
    "haliburton-23": "Tyrese Haliburton",
    "brunson-24": "Jalen Brunson",
    "edwards-24": "Anthony Edwards",
    "banchero-24": "Paolo Banchero",
    "wembanyama-24": "Victor Wembanyama",
    "cade-24": "Cade Cunningham",
    "mobley-24": "Evan Mobley",
    "jjj-23": "Jaren Jackson Jr.",
    "dariusgarland-23": "Darius Garland",
    "chetholmgren-24": "Chet Holmgren",
    "shai-23": "Shai Gilgeous-Alexander",
    "sengun-24": "Alperen Sengun",
    "jalenwilliams-24": "Jalen Williams",
    "porzingis-23": "Kristaps Porzingis",
    "zion-23": "Zion Williamson",
    "swipa-23": "De'Aaron Fox",
    "towns-24": "Karl-Anthony Towns",
}

# Chinese name → English name for current players without images
CN_NAME_MAP = {
    "维克托-文班亚马": "Victor Wembanyama",
    "切特-霍姆格伦": "Chet Holmgren",
    "OG-阿奴诺比": "OG Anunoby",
    "斯科蒂-巴恩斯": "Scottie Barnes",
    "弗朗茨-瓦格纳": "Franz Wagner",
    "杰伦-萨格斯": "Jalen Suggs",
    "科比-怀特": "Coby White",
    "安芬尼-西蒙斯": "Anfernee Simons",
    "德安吉洛-拉塞尔": "D'Angelo Russell",
    "马利克-蒙克": "Malik Monk",
    "VJ-阿尔瓦拉多": "Jose Alvarado",
    "科林-塞克斯顿": "Collin Sexton",
    "纳兹-里德": "Naz Reid",
    "以赛亚-哈尔滕施泰因": "Isaiah Hartenstein",
    "巴迪-希尔德": "Buddy Hield",
    "PJ-华盛顿": "PJ Washington",
    "约什-吉迪": "Josh Giddey",
    "克里斯塔普斯-波尔津吉斯": "Kristaps Porzingis",
    "劳里-马尔卡宁": "Lauri Markkanen",
    "德尼-阿夫迪亚": "Deni Avdija",
    "小迈克尔-波特": "Michael Porter Jr.",
    "杰伦-杜伦": "Jalen Duren",
    "瓦西里耶-米西奇": "Vasilije Micic",
    "比拉尔-库利巴利": "Bilal Coulibaly",
    "布兰丁-波杰姆斯基": "Brandin Podziemski",
    "GG-杰克逊": "GG Jackson",
    "戴森-丹尼尔斯": "Dyson Daniels",
    "小海梅-哈克斯": "Jaime Jaquez Jr.",
    "图马尼-卡马拉": "Toumani Camara",
    # Names from the earlier fetch run that didn't have entries
    "OG-阿奴诺比": "OG Anunoby",
    "VJ-阿尔瓦拉多": "Jose Alvarado",
    # Additional current players missing from build_players.py mappings
    "维克托·文班亚马": "Victor Wembanyama",
    "杰伦-约翰逊": "Jalen Johnson",
    "特雷-墨菲": "Trey Murphy",
    "库珀-弗拉格": "Cooper Flagg",
    "尼基尔-亚历山大-沃克": "Nickeil Alexander-Walker",
    "阿尔佩伦-申京": "Alperen Sengun",
    "阿门·汤普森": "Amen Thompson",
    "莱恩-罗林斯": "Ryan Rollins",
    "迈尔斯-布里奇斯": "Miles Bridges",
    "佩顿-普里查德": "Payton Pritchard",
    "斯蒂芬·卡斯尔": "Stephon Castle",
    "德里克-怀特": "Derrick White",
    "伊曼纽尔-奎克利": "Immanuel Quickley",
    "马塔斯·布泽利斯": "Matas Buzelis",
    "VJ-埃奇库姆": "VJ Edgecombe",
}


def search_id(english_name):
    """Search for NBA player ID."""
    try:
        results = nba_players.find_players_by_full_name(english_name)
        if results:
            return results[0]['id']
    except Exception:
        pass
    # Try last name for players with special characters
    try:
        parts = english_name.split()
        if len(parts) >= 2:
            last = parts[-1].replace("'", "").replace("-", " ").split()[-1]
            results = nba_players.find_players_by_last_name(last)
            if results and len(results) <= 10:
                eng_lower = english_name.lower().replace("'", "").replace("-", " ")
                for r in results:
                    full_lower = r['full_name'].lower().replace("'", "").replace("-", " ")
                    # Check if first name matches
                    first = parts[0].lower().replace("'", "").replace("-", "")
                    if first in full_lower and last.lower() in full_lower:
                        return r['id']
    except Exception:
        pass
    return None


def main():
    with open("players.json", "r", encoding="utf-8") as f:
        player_list = json.load(f)

    updated = 0
    failed = []

    for p in player_list:
        if p.get("image"):
            continue

        pid_key = p.get("id", "")
        name = p.get("name", "")

        # Try both ID and name mappings
        english = ID_MAP.get(pid_key) or CN_NAME_MAP.get(name)

        if not english:
            failed.append(f"NO-MAP: id={pid_key}, name={name}")
            continue

        nba_id = search_id(english)
        if nba_id:
            p["image"] = HEADSHOT_TEMPLATE.format(pid=nba_id)
            updated += 1
            print(f"  OK: {english} -> {nba_id}")
        else:
            failed.append(f"API-MISS: {name} -> \"{english}\" (not found in NBA API)")

        time.sleep(0.05)

    with open("players.json", "w", encoding="utf-8") as f:
        json.dump(player_list, f, ensure_ascii=False, indent=2)

    total = len(player_list)
    with_img = sum(1 for p in player_list if p.get("image"))
    print(f"\nDone. {updated} updated, {len(failed)} misses.")
    print(f"{with_img}/{total} players have images ({round(with_img/total*100)}%)")

    if failed:
        print("\nMisses:")
        for f in failed[:40]:
            print(f"  {f}")


if __name__ == "__main__":
    main()
