"""
Comprehensive headshot fetcher - maps ALL Chinese player names to NBA IDs.
"""
import json
import time
from nba_api.stats.static import players as nba_players

HEADSHOT = "https://cdn.nba.com/headshots/nba/latest/260x190/{pid}.png"

# Comprehensive Chinese name → English mapping
CN_TO_EN = {
    # Stars (dash format)
    "卢卡-东契奇": "Luka Doncic",
    "谢伊-吉尔杰斯-亚历山大": "Shai Gilgeous-Alexander",
    "安东尼-爱德华兹": "Anthony Edwards",
    "杰伦-布朗": "Jaylen Brown",
    "泰雷斯-马克西": "Tyrese Maxey",
    "多诺万-米切尔": "Donovan Mitchell",
    "科怀-伦纳德": "Kawhi Leonard",
    "尼古拉-约基奇": "Nikola Jokic",
    "德文-布克": "Devin Booker",
    "杰伦-布伦森": "Jalen Brunson",
    "凯文-杜兰特": "Kevin Durant",
    "贾马尔-默里": "Jamal Murray",
    "帕斯卡尔-西亚卡姆": "Pascal Siakam",
    "凯德-坎宁安": "Cade Cunningham",
    "保罗-班切罗": "Paolo Banchero",
    "布兰登-英格拉姆": "Brandon Ingram",
    "朱利叶斯-兰德尔": "Julius Randle",
    "蔡恩-威廉森": "Zion Williamson",
    "勒布朗-詹姆斯": "LeBron James",
    "德斯蒙德-贝恩": "Desmond Bane",
    "巴姆-阿德巴约": "Bam Adebayo",
    "卡尔-安东尼-唐斯": "Karl-Anthony Towns",
    "拉梅洛-鲍尔": "LaMelo Ball",
    "德马尔-德罗赞": "DeMar DeRozan",
    "埃文-莫布利": "Evan Mobley",
    "萨迪克-贝": "Saddiq Bey",
    "达龙-福克斯": "De'Aaron Fox",

    # Stars (middle dot format)
    "达米安·利拉德": "Damian Lillard",
    "达龙·福克斯": "De'Aaron Fox",
    "特雷·墨菲": "Trey Murphy",
    "卡梅隆·托马斯": "Cam Thomas",
    "诺曼·鲍威尔": "Norman Powell",
    "杰伦·威廉姆斯": "Jalen Williams",
    "达里厄斯·加兰": "Darius Garland",
    "安芬尼·西蒙斯": "Anfernee Simons",
    "布兰登·米勒": "Brandon Miller",
    "科比·怀特": "Coby White",
    "谢登·夏普": "Shaedon Sharpe",
    "德文·瓦塞尔": "Devin Vassell",
    "约翰·科林斯": "John Collins",
    "马利克·蒙克": "Malik Monk",
    "贾登·艾维": "Jaden Ivey",
    "乔纳森·库明加": "Jonathan Kuminga",
    "詹姆斯·哈登": "James Harden",
    "OG·阿奴诺比": "OG Anunoby",
    "伊曼纽尔·奎克利": "Immanuel Quickley",
    "科林·塞克斯顿": "Collin Sexton",
    "迈尔斯·特纳": "Myles Turner",
    "德尼·阿夫迪亚": "Deni Avdija",
    "克里斯蒂安·布劳恩": "Christian Braun",
    "克莱·汤普森": "Klay Thompson",
    "贾里德·麦凯恩": "Jared McCain",
    "科比·乔治": "Keyonte George",
    "杰拉米·格兰特": "Jerami Grant",
    "贾勒特·阿伦": "Jarrett Allen",
    "戴森·丹尼尔斯": "Dyson Daniels",
    "特里·罗齐尔": "Terry Rozier",
    "凯利·乌布雷": "Kelly Oubre Jr.",
    "斯库特·亨德森": "Scoot Henderson",
    "基冈·默里": "Keegan Murray",
    "雅各布·珀尔特尔": "Jakob Poeltl",
    "马尔科姆·布罗格登": "Malcolm Brogdon",
    "马克·威廉姆斯": "Mark Williams",
    "纳兹·里德": "Naz Reid",
    "狄龙·布鲁克斯": "Dillon Brooks",
    "桑蒂·阿尔达马": "Santi Aldama",
    "约什·吉迪": "Josh Giddey",
    "PJ·华盛顿": "PJ Washington",
    "博比·波蒂斯": "Bobby Portis",
    "亚历山大·萨尔": "Alex Sarr",
    "以赛亚·哈尔滕施泰因": "Isaiah Hartenstein",
    "布鲁克·洛佩斯": "Brook Lopez",
    "阿约·多森姆": "Ayo Dosunmu",
    "阿隆·戈登": "Aaron Gordon",
    "八村垒": "Rui Hachimura",
    "托拜厄斯·哈里斯": "Tobias Harris",
    "杰伦·杜伦": "Jalen Duren",
    "约什·哈特": "Josh Hart",
    "奥涅卡·奥孔古": "Onyeka Okongwu",
    "巴迪·希尔德": "Buddy Hield",
    "小贾巴里·史密斯": "Jabari Smith Jr.",
    "安德鲁·内姆哈德": "Andrew Nembhard",
    "唐特·迪温琴佐": "Donte DiVincenzo",
    "凯尔登·约翰逊": "Keldon Johnson",
    "丹尼尔·加福德": "Daniel Gafford",
    "扎卡里·里萨谢": "Zaccharie Risacher",
    "小斯科蒂·皮蓬": "Scotty Pippen Jr.",
    "杰登·麦克丹尼尔斯": "Jaden McDaniels",
    "科尔·安东尼": "Cole Anthony",
    "泰厄斯·琼斯": "Tyus Jones",
    "杰里米·索汉": "Jeremy Sochan",
    "尼古拉斯·克拉克斯顿": "Nicolas Claxton",
    "阿伦·内史密斯": "Aaron Nesmith",
    "小加里·特伦特": "Gary Trent Jr.",
    "吕冈茨·多尔特": "Luguentz Dort",
    "诺阿·克劳尼": "Noah Clowney",
    "帕特里克·威廉姆斯": "Patrick Williams",
    "卢克·肯纳德": "Luke Kennard",
    "布鲁斯·布朗": "Bruce Brown",
    "温德尔·卡特": "Wendell Carter Jr.",
    "奥柴·阿巴吉": "Ochai Agbaji",
    "布兰丁·波杰姆斯基": "Brandin Podziemski",
    "沃克·凯斯勒": "Walker Kessler",
    "瓦西里耶·米西奇": "Vasilije Micic",
    "奥萨尔·汤普森": "Ausar Thompson",
    "凯莱布·马丁": "Caleb Martin",
    "格兰特·威廉姆斯": "Grant Williams",
    "德雷克·莱夫利": "Dereck Lively II",
    "约什·格林": "Josh Green",
    "迈克·康利": "Mike Conley",
    "肯塔维奥斯·波普": "Kentavious Caldwell-Pope",
    "盖尔雄·亚布塞莱": "Guerschon Yabusele",
    "尼克·理查兹": "Nick Richards",
    "约纳斯·瓦兰丘纳斯": "Jonas Valanciunas",
    "凯肖恩·乔治": "Kyshawn George",
    "克里斯·保罗": "Chris Paul",
    "优素福·努尔基奇": "Jusuf Nurkic",
    "多里安·芬尼-史密斯": "Dorian Finney-Smith",
    "凯尔·韦尔": "Kel'el Ware",
    "昆滕·波斯特": "Quinten Post",
    "罗伊斯·奥尼尔": "Royce O'Neale",
    "乔纳森·莫格博": "Jonathan Mogbo",
    "特雷·莱尔斯": "Trey Lyles",
    "亚历克斯·卡鲁索": "Alex Caruso",
    "贾克森·海斯": "Jaxson Hayes",
    "克里斯·邓恩": "Kris Dunn",
    "迪恩·韦德": "Dean Wade",
    "米切尔·罗宾逊": "Mitchell Robinson",
    "多诺万·克林根": "Donovan Clingan",
    "德安德烈·乔丹": "DeAndre Jordan",
    "康-克尼普尔": "Kon Knueppel",
     "诺曼-鲍威尔": "Norman Powell",
     "卡梅隆-托马斯": "Cameron Thomas",

    # Dash format duplicates
    "詹姆斯-哈登": "James Harden",
    "德斯蒙德-贝恩": "Desmond Bane",
    "德马尔-德罗赞": "DeMar DeRozan",
    "特雷-墨菲": "Trey Murphy",
    "安芬尼-西蒙斯": "Anfernee Simons",
    "以赛亚-哈尔滕施泰因": "Isaiah Hartenstein",
    "纳兹-里德": "Naz Reid",
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
    "阿门-汤普森": "Amen Thompson",
    "斯蒂芬-卡斯尔": "Stephon Castle",
    "德里克-怀特": "Derrick White",
    "伊曼纽尔-奎克利": "Immanuel Quickley",
    "马塔斯-布泽利斯": "Matas Buzelis",
    "VJ-埃奇库姆": "VJ Edgecombe",
    "狄龙-布鲁克斯": "Dillon Brooks",
    "阿隆-戈登": "Aaron Gordon",
    "约翰-科林斯": "John Collins",
    "迈尔斯-布里奇斯": "Miles Bridges",
    "杰伦-约翰逊": "Jalen Johnson",
    "尼基尔-亚历山大-沃克": "Nickeil Alexander-Walker",
    "佩顿-普里查德": "Payton Pritchard",
    "莱恩-罗林斯": "Ryan Rollins",
    "库珀-弗拉格": "Cooper Flagg",
    "贾勒特-阿伦": "Jarrett Allen",
    "谢登-夏普": "Shaedon Sharpe",
    "杰拉米-格兰特": "Jerami Grant",
    "朱利叶斯-兰德尔": "Julius Randle",
}


def search(english):
    try:
        results = nba_players.find_players_by_full_name(english)
        if results:
            return results[0]['id']
    except:
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

        name = p["name"]
        english = CN_TO_EN.get(name)

        if not english:
            failed.append(f"NO-MAP: {name}")
            continue

        pid = search(english)
        if pid:
            p["image"] = HEADSHOT.format(pid=pid)
            updated += 1
            print(f"  OK: {english} -> {pid}")
        else:
            failed.append(f"API-MISS: {name} -> {english}")

        time.sleep(0.06)

    with open("players.json", "w", encoding="utf-8") as f:
        json.dump(player_list, f, ensure_ascii=False, indent=2)

    total = len(player_list)
    with_img = sum(1 for p in player_list if p.get("image"))
    print(f"\n{updated} updated, {len(failed)} misses")
    print(f"{with_img}/{total} have images ({round(with_img/total*100)}%)")
    if failed:
        for f in failed[:20]:
            print(f"  {f}")


if __name__ == "__main__":
    main()
