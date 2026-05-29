"""
Add ~70 All-Star legends (1995-2025) to players.json.
Each entry has estimated 12-axis attrs based on playing style and era.
Stats are approximate career-peak season averages.

Run: python add_allstars.py
"""
import json

ALLSTARS = [
    # ═══════════ 90s-00s PG ═══════════
    {
        "id": "payton-96", "name": "加里·佩顿 (96)", "position": "PG",
        "team": "超音速", "color": "#006633", "season": "1995-96",
        "attrs": {'threePT':65,'midRange':78,'rimFin':70,'FT':75,'playmaking':90,'ballHandle':88,'perimD':98,'rimProt':25,'helpSwitch':92,'steals':95,'rebounding':48,'athleticism':84},
        "stats": {"pts":19.3,"ast":7.5,"reb":4.2,"stl":2.9,"blk":0.2,"fg_pct":48.4,"tp_pct":32.8,"ft_pct":74.8,"gp":81,"mpg":39.0}
    },
    {
        "id": "hardaway-97", "name": "蒂姆·哈达威 (97)", "position": "PG",
        "team": "热火", "color": "#98002E", "season": "1996-97",
        "attrs": {'threePT':78,'midRange':82,'rimFin':65,'FT':82,'playmaking':90,'ballHandle':94,'perimD':78,'rimProt':12,'helpSwitch':68,'steals':78,'rebounding':38,'athleticism':78},
        "stats": {"pts":20.3,"ast":8.6,"reb":3.4,"stl":1.9,"blk":0.1,"fg_pct":41.5,"tp_pct":34.4,"ft_pct":79.9,"gp":81,"mpg":38.7}
    },
    {
        "id": "kj-93", "name": "凯文·约翰逊 (93)", "position": "PG",
        "team": "太阳", "color": "#E56020", "season": "1992-93",
        "attrs": {'threePT':55,'midRange':78,'rimFin':78,'FT':85,'playmaking':88,'ballHandle':90,'perimD':65,'rimProt':15,'helpSwitch':58,'steals':65,'rebounding':35,'athleticism':90},
        "stats": {"pts":18.6,"ast":10.0,"reb":3.2,"stl":2.0,"blk":0.3,"fg_pct":50.3,"tp_pct":21.1,"ft_pct":84.2,"gp":75,"mpg":36.6}
    },
    {
        "id": "parker-08", "name": "托尼·帕克 (08)", "position": "PG",
        "team": "马刺", "color": "#000000", "season": "2007-08",
        "attrs": {'threePT':68,'midRange':86,'rimFin':88,'FT':75,'playmaking':85,'ballHandle':90,'perimD':60,'rimProt':10,'helpSwitch':52,'steals':55,'rebounding':35,'athleticism':88},
        "stats": {"pts":22.0,"ast":6.0,"reb":3.2,"stl":0.8,"blk":0.1,"fg_pct":51.0,"tp_pct":35.0,"ft_pct":74.4,"gp":77,"mpg":33.5}
    },
    {
        "id": "billups-06", "name": "昌西·比卢普斯 (06)", "position": "PG",
        "team": "活塞", "color": "#C8102E", "season": "2005-06",
        "attrs": {'threePT':88,'midRange':82,'rimFin':68,'FT':92,'playmaking':88,'ballHandle':86,'perimD':82,'rimProt':15,'helpSwitch':75,'steals':70,'rebounding':38,'athleticism':68},
        "stats": {"pts":18.5,"ast":8.6,"reb":3.1,"stl":0.9,"blk":0.1,"fg_pct":41.8,"tp_pct":43.3,"ft_pct":89.4,"gp":81,"mpg":36.1}
    },
    {
        "id": "arenas-06", "name": "吉尔伯特·阿里纳斯 (06)", "position": "PG",
        "team": "奇才", "color": "#002B5C", "season": "2005-06",
        "attrs": {'threePT':85,'midRange':82,'rimFin':78,'FT':85,'playmaking':78,'ballHandle':88,'perimD':55,'rimProt':12,'helpSwitch':48,'steals':65,'rebounding':38,'athleticism':82},
        "stats": {"pts":29.3,"ast":6.1,"reb":3.5,"stl":2.0,"blk":0.3,"fg_pct":44.7,"tp_pct":36.9,"ft_pct":82.0,"gp":80,"mpg":42.3}
    },
    {
        "id": "rondo-12", "name": "拉简·朗多 (12)", "position": "PG",
        "team": "凯尔特人", "color": "#007A33", "season": "2011-12",
        "attrs": {'threePT':45,'midRange':65,'rimFin':65,'FT':58,'playmaking':96,'ballHandle':92,'perimD':92,'rimProt':20,'helpSwitch':88,'steals':90,'rebounding':52,'athleticism':82},
        "stats": {"pts":11.9,"ast":11.7,"reb":4.8,"stl":1.8,"blk":0.1,"fg_pct":44.8,"tp_pct":23.8,"ft_pct":59.7,"gp":53,"mpg":36.9}
    },
    {
        "id": "wall-17", "name": "约翰·沃尔 (17)", "position": "PG",
        "team": "奇才", "color": "#002B5C", "season": "2016-17",
        "attrs": {'threePT':62,'midRange':72,'rimFin':78,'FT':78,'playmaking':92,'ballHandle':90,'perimD':78,'rimProt':38,'helpSwitch':72,'steals':75,'rebounding':42,'athleticism':94},
        "stats": {"pts":23.1,"ast":10.7,"reb":4.2,"stl":2.0,"blk":0.6,"fg_pct":45.1,"tp_pct":32.7,"ft_pct":80.1,"gp":78,"mpg":36.4}
    },
    {
        "id": "lowry-18", "name": "凯尔·洛瑞 (18)", "position": "PG",
        "team": "猛龙", "color": "#CE1141", "season": "2017-18",
        "attrs": {'threePT':80,'midRange':72,'rimFin':62,'FT':86,'playmaking':84,'ballHandle':82,'perimD':78,'rimProt':18,'helpSwitch':72,'steals':68,'rebounding':50,'athleticism':70},
        "stats": {"pts":17.3,"ast":6.9,"reb":5.6,"stl":1.1,"blk":0.2,"fg_pct":42.7,"tp_pct":39.9,"ft_pct":85.4,"gp":78,"mpg":32.2}
    },
    {
        "id": "kemba-19", "name": "肯巴·沃克 (19)", "position": "PG",
        "team": "黄蜂", "color": "#1D1160", "season": "2018-19",
        "attrs": {'threePT':78,'midRange':82,'rimFin':68,'FT':85,'playmaking':78,'ballHandle':90,'perimD':55,'rimProt':12,'helpSwitch':48,'steals':62,'rebounding':40,'athleticism':82},
        "stats": {"pts":25.6,"ast":5.9,"reb":4.4,"stl":1.2,"blk":0.4,"fg_pct":43.4,"tp_pct":35.6,"ft_pct":84.4,"gp":82,"mpg":34.9}
    },

    # ═══════════ 90s-00s SG ═══════════
    {
        "id": "miller-95", "name": "雷吉·米勒 (95)", "position": "SG",
        "team": "步行者", "color": "#FDBB30", "season": "1994-95",
        "attrs": {'threePT':95,'midRange':85,'rimFin':62,'FT':92,'playmaking':55,'ballHandle':72,'perimD':70,'rimProt':10,'helpSwitch':58,'steals':65,'rebounding':35,'athleticism':68},
        "stats": {"pts":19.6,"ast":3.0,"reb":2.6,"stl":1.2,"blk":0.2,"fg_pct":46.2,"tp_pct":41.5,"ft_pct":89.7,"gp":81,"mpg":32.9}
    },
    {
        "id": "allen-06", "name": "雷·阿伦 (06)", "position": "SG",
        "team": "超音速", "color": "#006633", "season": "2005-06",
        "attrs": {'threePT':94,'midRange':88,'rimFin':72,'FT':92,'playmaking':62,'ballHandle':80,'perimD':68,'rimProt':12,'helpSwitch':58,'steals':62,'rebounding':42,'athleticism':78},
        "stats": {"pts":25.1,"ast":3.7,"reb":4.3,"stl":1.3,"blk":0.2,"fg_pct":45.4,"tp_pct":41.2,"ft_pct":90.3,"gp":78,"mpg":38.7}
    },
    {
        "id": "carter-01", "name": "文斯·卡特 (01)", "position": "SG",
        "team": "猛龙", "color": "#CE1141", "season": "2000-01",
        "attrs": {'threePT':82,'midRange':80,'rimFin':95,'FT':78,'playmaking':65,'ballHandle':84,'perimD':68,'rimProt':55,'helpSwitch':62,'steals':68,'rebounding':52,'athleticism':96},
        "stats": {"pts":27.6,"ast":3.9,"reb":5.5,"stl":1.5,"blk":1.1,"fg_pct":46.0,"tp_pct":40.8,"ft_pct":76.5,"gp":75,"mpg":39.7}
    },
    {
        "id": "ginobili-08", "name": "马努·吉诺比利 (08)", "position": "SG",
        "team": "马刺", "color": "#000000", "season": "2007-08",
        "attrs": {'threePT':82,'midRange':78,'rimFin':85,'FT':86,'playmaking':78,'ballHandle':90,'perimD':82,'rimProt':28,'helpSwitch':75,'steals':82,'rebounding':45,'athleticism':82},
        "stats": {"pts":19.5,"ast":4.5,"reb":4.8,"stl":1.5,"blk":0.4,"fg_pct":46.0,"tp_pct":40.1,"ft_pct":86.0,"gp":74,"mpg":31.0}
    },
    {
        "id": "richmond-96", "name": "米奇·里奇蒙德 (96)", "position": "SG",
        "team": "国王", "color": "#5A2D81", "season": "1995-96",
        "attrs": {'threePT':82,'midRange':88,'rimFin':75,'FT':88,'playmaking':58,'ballHandle':78,'perimD':72,'rimProt':18,'helpSwitch':62,'steals':68,'rebounding':40,'athleticism':72},
        "stats": {"pts":23.1,"ast":4.1,"reb":4.0,"stl":1.5,"blk":0.3,"fg_pct":46.0,"tp_pct":43.7,"ft_pct":86.6,"gp":81,"mpg":36.4}
    },

    # ═══════════ 00s-10s SF ═══════════
    {
        "id": "hill-97", "name": "格兰特·希尔 (97)", "position": "SF",
        "team": "活塞", "color": "#C8102E", "season": "1996-97",
        "attrs": {'threePT':55,'midRange':78,'rimFin':88,'FT':72,'playmaking':82,'ballHandle':88,'perimD':82,'rimProt':52,'helpSwitch':78,'steals':78,'rebounding':72,'athleticism':92},
        "stats": {"pts":21.4,"ast":7.3,"reb":9.0,"stl":1.8,"blk":0.6,"fg_pct":49.6,"tp_pct":30.3,"ft_pct":71.1,"gp":80,"mpg":39.3}
    },
    {
        "id": "pierce-08", "name": "保罗·皮尔斯 (08)", "position": "SF",
        "team": "凯尔特人", "color": "#007A33", "season": "2007-08",
        "attrs": {'threePT':78,'midRange':88,'rimFin':82,'FT':85,'playmaking':72,'ballHandle':82,'perimD':80,'rimProt':42,'helpSwitch':72,'steals':65,'rebuilding':58,'athleticism':72},
        "stats": {"pts":19.6,"ast":4.5,"reb":5.1,"stl":1.3,"blk":0.4,"fg_pct":46.4,"tp_pct":39.2,"ft_pct":84.3,"gp":80,"mpg":35.9}
    },
    {
        "id": "melo-13", "name": "卡梅隆·安东尼 (13)", "position": "SF",
        "team": "尼克斯", "color": "#F58426", "season": "2012-13",
        "attrs": {'threePT':82,'midRange':92,'rimFin':82,'FT':82,'playmaking':58,'ballHandle':82,'perimD':60,'rimProt':35,'helpSwitch':55,'steals':55,'rebounding':65,'athleticism':78},
        "stats": {"pts":28.7,"ast":2.6,"reb":6.9,"stl":0.8,"blk":0.5,"fg_pct":44.9,"tp_pct":37.9,"ft_pct":83.0,"gp":67,"mpg":37.0}
    },
    {
        "id": "george-19", "name": "保罗·乔治 (19)", "position": "SF",
        "team": "雷霆", "color": "#007AC1", "season": "2018-19",
        "attrs": {'threePT':82,'midRange':82,'rimFin':82,'FT':84,'playmaking':68,'ballHandle':82,'perimD':92,'rimProt':48,'helpSwitch':85,'steals':88,'rebounding':68,'athleticism':88},
        "stats": {"pts":28.0,"ast":4.1,"reb":8.2,"stl":2.2,"blk":0.4,"fg_pct":43.8,"tp_pct":38.6,"ft_pct":83.9,"gp":77,"mpg":36.9}
    },
    {
        "id": "marion-06", "name": "肖恩·马里昂 (06)", "position": "SF",
        "team": "太阳", "color": "#E56020", "season": "2005-06",
        "attrs": {'threePT':62,'midRange':68,'rimFin':82,'FT':78,'playmaking':52,'ballHandle':68,'perimD':88,'rimProt':65,'helpSwitch':85,'steals':85,'rebounding':88,'athleticism':92},
        "stats": {"pts":21.8,"ast":1.8,"reb":11.8,"stl":2.0,"blk":1.7,"fg_pct":52.5,"tp_pct":33.1,"ft_pct":80.9,"gp":81,"mpg":40.3}
    },

    # ═══════════ 90s-10s PF ═══════════
    {
        "id": "kemp-96", "name": "肖恩·坎普 (96)", "position": "PF",
        "team": "超音速", "color": "#006633", "season": "1995-96",
        "attrs": {'threePT':28,'midRange':58,'rimFin':95,'FT':68,'playmaking':45,'ballHandle':60,'perimD':72,'rimProt':78,'helpSwitch':68,'steals':65,'rebounding':90,'athleticism':97},
        "stats": {"pts":19.6,"ast":2.2,"reb":11.4,"stl":1.2,"blk":1.6,"fg_pct":56.1,"tp_pct":41.7,"ft_pct":74.2,"gp":79,"mpg":33.3}
    },
    {
        "id": "webber-01", "name": "克里斯·韦伯 (01)", "position": "PF",
        "team": "国王", "color": "#5A2D81", "season": "2000-01",
        "attrs": {'threePT':55,'midRange':85,'rimFin':88,'FT':68,'playmaking':82,'ballHandle':78,'perimD':78,'rimProt':72,'helpSwitch':78,'steals':70,'rebounding':88,'athleticism':82},
        "stats": {"pts":27.1,"ast":4.2,"reb":11.1,"stl":1.3,"blk":1.7,"fg_pct":48.1,"tp_pct":26.7,"ft_pct":70.3,"gp":70,"mpg":40.5}
    },
    {
        "id": "amare-08", "name": "阿玛雷·斯塔德迈尔 (08)", "position": "PF",
        "team": "太阳", "color": "#E56020", "season": "2007-08",
        "attrs": {'threePT':20,'midRange':75,'rimFin':95,'FT':80,'playmaking':38,'ballHandle':55,'perimD':60,'rimProt':78,'helpSwitch':58,'steals':45,'rebounding':82,'athleticism':94},
        "stats": {"pts":25.2,"ast":1.5,"reb":9.1,"stl":0.8,"blk":2.1,"fg_pct":59.0,"tp_pct":16.1,"ft_pct":80.5,"gp":79,"mpg":33.9}
    },
    {
        "id": "bosh-10", "name": "克里斯·波什 (10)", "position": "PF",
        "team": "猛龙", "color": "#CE1141", "season": "2009-10",
        "attrs": {'threePT':55,'midRange':85,'rimFin':82,'FT':80,'playmaking':48,'ballHandle':62,'perimD':72,'rimProt':65,'helpSwitch':68,'steals':52,'rebounding':85,'athleticism':78},
        "stats": {"pts":24.0,"ast":2.4,"reb":10.8,"stl":0.6,"blk":1.0,"fg_pct":51.8,"tp_pct":36.4,"ft_pct":79.7,"gp":70,"mpg":36.1}
    },
    {
        "id": "love-14", "name": "凯文·乐福 (14)", "position": "PF",
        "team": "森林狼", "color": "#0C2340", "season": "2013-14",
        "attrs": {'threePT':82,'midRange':78,'rimFin':72,'FT':82,'playmaking':58,'ballHandle':58,'perimD':48,'rimProt':38,'helpSwitch':42,'steals':48,'rebounding':94,'athleticism':62},
        "stats": {"pts":26.1,"ast":4.4,"reb":12.5,"stl":0.8,"blk":0.5,"fg_pct":45.7,"tp_pct":37.6,"ft_pct":82.1,"gp":77,"mpg":36.3}
    },
    {
        "id": "griffin-14", "name": "布雷克·格里芬 (14)", "position": "PF",
        "team": "快船", "color": "#C8102E", "season": "2013-14",
        "attrs": {'threePT':42,'midRange':72,'rimFin':96,'FT':68,'playmaking':65,'ballHandle':72,'perimD':62,'rimProt':42,'helpSwitch':55,'steals':62,'rebounding':85,'athleticism':96},
        "stats": {"pts":24.1,"ast":3.9,"reb":9.5,"stl":1.2,"blk":0.6,"fg_pct":52.8,"tp_pct":27.3,"ft_pct":71.5,"gp":80,"mpg":35.8}
    },
    {
        "id": "aldridge-16", "name": "拉马库斯·阿尔德里奇 (16)", "position": "PF",
        "team": "马刺", "color": "#000000", "season": "2015-16",
        "attrs": {'threePT':35,'midRange':94,'rimFin':78,'FT':85,'playmaking':38,'ballHandle':52,'perimD':68,'rimProt':65,'helpSwitch':58,'steals':40,'rebounding':78,'athleticism':62},
        "stats": {"pts":23.5,"ast":1.5,"reb":8.5,"stl":0.5,"blk":1.1,"fg_pct":51.3,"tp_pct":0.0,"ft_pct":82.2,"gp":74,"mpg":30.6}
    },
    {
        "id": "sheed-01", "name": "拉希德·华莱士 (01)", "position": "PF",
        "team": "开拓者", "color": "#E03A3E", "season": "2000-01",
        "attrs": {'threePT':68,'midRange':78,'rimFin':78,'FT':72,'playmaking':48,'ballHandle':58,'perimD':80,'rimProt':75,'helpSwitch':75,'steals':62,'rebounding':75,'athleticism':78},
        "stats": {"pts":19.2,"ast":2.8,"reb":7.8,"stl":1.2,"blk":1.8,"fg_pct":50.1,"tp_pct":35.7,"ft_pct":73.5,"gp":77,"mpg":38.2}
    },

    # ═══════════ 90s-10s C ═══════════
    {
        "id": "mourning-99", "name": "阿朗佐·莫宁 (99)", "position": "C",
        "team": "热火", "color": "#98002E", "season": "1998-99",
        "attrs": {'threePT':10,'midRange':55,'rimFin':88,'FT':68,'playmaking':30,'ballHandle':40,'perimD':78,'rimProt':98,'helpSwitch':82,'steals':45,'rebounding':88,'athleticism':82},
        "stats": {"pts":20.1,"ast":1.6,"reb":11.0,"stl":0.7,"blk":3.9,"fg_pct":51.1,"tp_pct":0.0,"ft_pct":65.2,"gp":46,"mpg":38.1}
    },
    {
        "id": "mutombo-97", "name": "迪肯贝·穆托姆博 (97)", "position": "C",
        "team": "老鹰", "color": "#E03A3E", "season": "1996-97",
        "attrs": {'threePT':5,'midRange':35,'rimFin':72,'FT':62,'playmaking':20,'ballHandle':30,'perimD':72,'rimProt':99,'helpSwitch':82,'steals':35,'rebounding':92,'athleticism':62},
        "stats": {"pts":13.3,"ast":1.4,"reb":11.6,"stl":0.6,"blk":3.3,"fg_pct":52.7,"tp_pct":0.0,"ft_pct":70.5,"gp":80,"mpg":37.2}
    },
    {
        "id": "benwallace-04", "name": "本·华莱士 (04)", "position": "C",
        "team": "活塞", "color": "#C8102E", "season": "2003-04",
        "attrs": {'threePT':5,'midRange':25,'rimFin':58,'FT':35,'playmaking':28,'ballHandle':32,'perimD':94,'rimProt':99,'helpSwitch':96,'steals':78,'rebounding':96,'athleticism':90},
        "stats": {"pts":9.5,"ast":1.7,"reb":12.4,"stl":1.8,"blk":3.0,"fg_pct":42.1,"tp_pct":12.5,"ft_pct":49.0,"gp":81,"mpg":37.7}
    },
    {
        "id": "joneal-05", "name": "杰梅因·奥尼尔 (05)", "position": "C",
        "team": "步行者", "color": "#FDBB30", "season": "2004-05",
        "attrs": {'threePT':10,'midRange':65,'rimFin':82,'FT':72,'playmaking':32,'ballHandle':42,'perimD':72,'rimProt':88,'helpSwitch':75,'steals':42,'rebounding':82,'athleticism':75},
        "stats": {"pts":24.3,"ast":1.9,"reb":8.8,"stl":0.6,"blk":2.0,"fg_pct":45.2,"tp_pct":20.0,"ft_pct":75.4,"gp":44,"mpg":34.8}
    },
    {
        "id": "cousins-16", "name": "德马库斯·考辛斯 (16)", "position": "C",
        "team": "国王", "color": "#5A2D81", "season": "2015-16",
        "attrs": {'threePT':62,'midRange':72,'rimFin':85,'FT':72,'playmaking':55,'ballHandle':62,'perimD':65,'rimProt':72,'helpSwitch':58,'steals':58,'rebuilding':88,'athleticism':68},
        "stats": {"pts":26.9,"ast":3.3,"reb":11.5,"stl":1.6,"blk":1.4,"fg_pct":45.1,"tp_pct":33.3,"ft_pct":71.8,"gp":65,"mpg":34.6}
    },
    {
        "id": "mgasol-15", "name": "马克·加索尔 (15)", "position": "C",
        "team": "灰熊", "color": "#5D76A9", "season": "2014-15",
        "attrs": {'threePT':35,'midRange':78,'rimFin':72,'FT':80,'playmaking':62,'ballHandle':52,'perimD':75,'rimProt':88,'helpSwitch':78,'steals':52,'rebounding':75,'athleticism':48},
        "stats": {"pts":17.4,"ast":3.8,"reb":7.8,"stl":0.9,"blk":1.6,"fg_pct":49.4,"tp_pct":17.6,"ft_pct":79.5,"gp":81,"mpg":33.2}
    },
    {
        "id": "noah-14", "name": "乔金·诺阿 (14)", "position": "C",
        "team": "公牛", "color": "#CE1141", "season": "2013-14",
        "attrs": {'threePT':5,'midRange':45,'rimFin':62,'FT':65,'playmaking':72,'ballHandle':55,'perimD':88,'rimProt':85,'helpSwitch':90,'steals':65,'rebounding':88,'athleticism':72},
        "stats": {"pts":12.6,"ast":5.4,"reb":11.3,"stl":1.2,"blk":1.5,"fg_pct":47.5,"tp_pct":0.0,"ft_pct":73.7,"gp":80,"mpg":35.3}
    },
    {
        "id": "pgasol-09", "name": "保罗·加索尔 (09)", "position": "C",
        "team": "湖人", "color": "#552583", "season": "2008-09",
        "attrs": {'threePT':20,'midRange':82,'rimFin':82,'FT':78,'playmaking':58,'ballHandle':55,'perimD':72,'rimProt':78,'helpSwitch':72,'steals':45,'rebounding':82,'athleticism':65},
        "stats": {"pts":18.9,"ast":3.5,"reb":9.6,"stl":0.6,"blk":1.0,"fg_pct":56.7,"tp_pct":50.0,"ft_pct":78.1,"gp":81,"mpg":37.0}
    },

    # ═══════════ 2010s Stars ═══════════
    {
        "id": "klay-16", "name": "克莱·汤普森 (16)", "position": "SG",
        "team": "勇士", "color": "#FDB927", "season": "2015-16",
        "attrs": {'threePT':95,'midRange':82,'rimFin':68,'FT':88,'playmaking':38,'ballHandle':68,'perimD':88,'rimProt':30,'helpSwitch':75,'steals':55,'rebuilding':38,'athleticism':72},
        "stats": {"pts":22.1,"ast":2.1,"reb":3.8,"stl":0.8,"blk":0.6,"fg_pct":47.0,"tp_pct":42.5,"ft_pct":87.3,"gp":80,"mpg":33.3}
    },
    {
        "id": "derozan-17", "name": "德马尔·德罗赞 (17)", "position": "SG",
        "team": "猛龙", "color": "#CE1141", "season": "2016-17",
        "attrs": {'threePT':45,'midRange':94,'rimFin':82,'FT':85,'playmaking':60,'ballHandle':82,'perimD':58,'rimProt':25,'helpSwitch':48,'steals':55,'rebuilding':48,'athleticism':85},
        "stats": {"pts":27.3,"ast":3.9,"reb":5.2,"stl":1.1,"blk":0.2,"fg_pct":46.7,"tp_pct":26.6,"ft_pct":84.2,"gp":74,"mpg":35.4}
    },
    {
        "id": "dwilliams-10", "name": "德隆·威廉姆斯 (10)", "position": "PG",
        "team": "爵士", "color": "#002B5C", "season": "2009-10",
        "attrs": {'threePT':75,'midRange':82,'rimFin':65,'FT':82,'playmaking':90,'ballHandle':88,'perimD':68,'rimProt':15,'helpSwitch':60,'steals':62,'rebuilding':38,'athleticism':75},
        "stats": {"pts":18.7,"ast":10.5,"reb":4.0,"stl":1.3,"blk":0.2,"fg_pct":46.9,"tp_pct":37.1,"ft_pct":80.1,"gp":76,"mpg":36.9}
    },
    {
        "id": "joejohnson-10", "name": "乔·约翰逊 (10)", "position": "SG",
        "team": "老鹰", "color": "#E03A3E", "season": "2009-10",
        "attrs": {'threePT':78,'midRange':90,'rimFin':68,'FT':82,'playmaking':62,'ballHandle':78,'perimD':58,'rimProt':18,'helpSwitch':48,'steals':52,'rebuilding':42,'athleticism':62},
        "stats": {"pts":21.3,"ast":4.9,"reb":4.6,"stl":1.1,"blk":0.1,"fg_pct":45.8,"tp_pct":36.9,"ft_pct":81.8,"gp":76,"mpg":38.0}
    },
    {
        "id": "brand-06", "name": "埃尔顿·布兰德 (06)", "position": "PF",
        "team": "快船", "color": "#C8102E", "season": "2005-06",
        "attrs": {'threePT':15,'midRange':78,'rimFin':82,'FT':75,'playmaking':42,'ballHandle':48,'perimD':78,'rimProt':88,'helpSwitch':72,'steals':60,'rebuilding':82,'athleticism':75},
        "stats": {"pts":24.7,"ast":2.6,"reb":10.0,"stl":1.0,"blk":2.5,"fg_pct":52.7,"tp_pct":33.3,"ft_pct":77.5,"gp":79,"mpg":39.2}
    },
    {
        "id": "peja-04", "name": "佩贾·斯托贾科维奇 (04)", "position": "SF",
        "team": "国王", "color": "#5A2D81", "season": "2003-04",
        "attrs": {'threePT':96,'midRange':78,'rimFin':62,'FT':94,'playmaking':38,'ballHandle':58,'perimD':52,'rimProt':15,'helpSwitch':42,'steals':52,'rebuilding':52,'athleticism':62},
        "stats": {"pts":24.2,"ast":2.1,"reb":6.3,"stl":1.3,"blk":0.2,"fg_pct":48.0,"tp_pct":43.3,"ft_pct":92.7,"gp":81,"mpg":40.3}
    },
    {
        "id": "roy-09", "name": "布兰登·罗伊 (09)", "position": "SG",
        "team": "开拓者", "color": "#E03A3E", "season": "2008-09",
        "attrs": {'threePT':78,'midRange':90,'rimFin':72,'FT':88,'playmaking':72,'ballHandle':85,'perimD':68,'rimProt':20,'helpSwitch':58,'steals':62,'rebuilding':42,'athleticism':72},
        "stats": {"pts":22.6,"ast":5.1,"reb":4.7,"stl":1.1,"blk":0.3,"fg_pct":48.0,"tp_pct":37.7,"ft_pct":87.7,"gp":78,"mpg":37.2}
    },
    {
        "id": "horford-15", "name": "艾尔·霍福德 (15)", "position": "C",
        "team": "老鹰", "color": "#E03A3E", "season": "2014-15",
        "attrs": {'threePT':55,'midRange':75,'rimFin':72,'FT':75,'playmaking':58,'ballHandle':52,'perimD':75,'rimProt':72,'helpSwitch':75,'steals':52,'rebuilding':72,'athleticism':58},
        "stats": {"pts":15.1,"ast":3.2,"reb":7.2,"stl":0.9,"blk":1.3,"fg_pct":53.8,"tp_pct":30.6,"ft_pct":75.9,"gp":76,"mpg":30.5}
    },
    {
        "id": "millsap-16", "name": "保罗·米尔萨普 (16)", "position": "PF",
        "team": "老鹰", "color": "#E03A3E", "season": "2015-16",
        "attrs": {'threePT':55,'midRange':72,'rimFin':72,'FT':75,'playmaking':55,'ballHandle':58,'perimD':82,'rimProt':72,'helpSwitch':80,'steals':75,'rebuilding':75,'athleticism':68},
        "stats": {"pts":17.0,"ast":3.3,"reb":9.0,"stl":1.8,"blk":1.7,"fg_pct":47.0,"tp_pct":35.6,"ft_pct":75.7,"gp":81,"mpg":32.7}
    },
    {
        "id": "conley-19", "name": "迈克·康利 (19)", "position": "PG",
        "team": "灰熊", "color": "#5D76A9", "season": "2018-19",
        "attrs": {'threePT':78,'midRange':78,'rimFin':55,'FT':85,'playmaking':78,'ballHandle':82,'perimD':80,'rimProt':15,'helpSwitch':72,'steals':65,'rebuilding':35,'athleticism':65},
        "stats": {"pts":21.1,"ast":6.4,"reb":3.4,"stl":1.3,"blk":0.3,"fg_pct":43.8,"tp_pct":36.4,"ft_pct":84.5,"gp":70,"mpg":33.5}
    },
    {
        "id": "deng-13", "name": "洛尔·邓 (13)", "position": "SF",
        "team": "公牛", "color": "#CE1141", "season": "2012-13",
        "attrs": {'threePT':58,'midRange':78,'rimFin':68,'FT':78,'playmaking':48,'ballHandle':62,'perimD':82,'rimProt':38,'helpSwitch':75,'steals':62,'rebuilding':62,'athleticism':72},
        "stats": {"pts":16.5,"ast":3.0,"reb":6.3,"stl":1.1,"blk":0.4,"fg_pct":42.6,"tp_pct":32.2,"ft_pct":81.6,"gp":75,"mpg":38.7}
    },
    {
        "id": "iguodala-12", "name": "安德烈·伊戈达拉 (12)", "position": "SF",
        "team": "76人", "color": "#006BB6", "season": "2011-12",
        "attrs": {'threePT':62,'midRange':65,'rimFin':78,'FT':62,'playmaking':68,'ballHandle':75,'perimD':90,'rimProt':42,'helpSwitch':88,'steals':82,'rebuilding':58,'athleticism':90},
        "stats": {"pts":12.4,"ast":5.5,"reb":6.1,"stl":1.7,"blk":0.5,"fg_pct":45.4,"tp_pct":39.4,"ft_pct":61.7,"gp":62,"mpg":35.6}
    },
    {
        "id": "thomas-17", "name": "以赛亚·托马斯 (17)", "position": "PG",
        "team": "凯尔特人", "color": "#007A33", "season": "2016-17",
        "attrs": {'threePT':82,'midRange':78,'rimFin':72,'FT':92,'playmaking':75,'ballHandle':88,'perimD':35,'rimProt':8,'helpSwitch':30,'steals':48,'rebuilding':28,'athleticism':78},
        "stats": {"pts":28.9,"ast":5.9,"reb":2.7,"stl":0.9,"blk":0.2,"fg_pct":46.3,"tp_pct":37.9,"ft_pct":90.9,"gp":76,"mpg":33.8}
    },
    {
        "id": "oladipo-18", "name": "维克多·奥拉迪波 (18)", "position": "SG",
        "team": "步行者", "color": "#FDBB30", "season": "2017-18",
        "attrs": {'threePT':78,'midRange':75,'rimFin':78,'FT':80,'playmaking':62,'ballHandle':82,'perimD':90,'rimProt':38,'helpSwitch':82,'steals':92,'rebuilding':48,'athleticism':88},
        "stats": {"pts":23.1,"ast":4.3,"reb":5.2,"stl":2.4,"blk":0.8,"fg_pct":47.7,"tp_pct":37.1,"ft_pct":79.9,"gp":75,"mpg":34.0}
    },
    {
        "id": "beal-20", "name": "布拉德利·比尔 (20)", "position": "SG",
        "team": "奇才", "color": "#002B5C", "season": "2019-20",
        "attrs": {'threePT':78,'midRange':85,'rimFin':72,'FT':85,'playmaking':62,'ballHandle':78,'perimD':58,'rimProt':25,'helpSwitch':48,'steals':55,'rebuilding':40,'athleticism':75},
        "stats": {"pts":30.5,"ast":6.1,"reb":4.2,"stl":1.2,"blk":0.4,"fg_pct":45.5,"tp_pct":35.3,"ft_pct":84.2,"gp":57,"mpg":36.0}
    },
    {
        "id": "jrue-19", "name": "朱·霍勒迪 (19)", "position": "PG",
        "team": "鹈鹕", "color": "#0C2340", "season": "2018-19",
        "attrs": {'threePT':65,'midRange':78,'rimFin':72,'FT':78,'playmaking':78,'ballHandle':82,'perimD':90,'rimProt':35,'helpSwitch':85,'steals':82,'rebuilding':48,'athleticism':78},
        "stats": {"pts":21.2,"ast":6.6,"reb":5.0,"stl":1.6,"blk":0.8,"fg_pct":47.2,"tp_pct":32.5,"ft_pct":76.8,"gp":67,"mpg":35.9}
    },
    {
        "id": "middleton-20", "name": "克里斯·米德尔顿 (20)", "position": "SF",
        "team": "雄鹿", "color": "#00471B", "season": "2019-20",
        "attrs": {'threePT':82,'midRange':88,'rimFin':62,'FT':90,'playmaking':58,'ballHandle':72,'perimD':72,'rimProt':15,'helpSwitch':62,'steals':55,'rebuilding':48,'athleticism':62},
        "stats": {"pts":20.9,"ast":4.3,"reb":6.2,"stl":0.9,"blk":0.1,"fg_pct":49.7,"tp_pct":41.5,"ft_pct":91.6,"gp":62,"mpg":29.9}
    },
    {
        "id": "gobert-21", "name": "鲁迪·戈贝尔 (21)", "position": "C",
        "team": "爵士", "color": "#002B5C", "season": "2020-21",
        "attrs": {'threePT':5,'midRange':30,'rimFin':82,'FT':58,'playmaking':20,'ballHandle':28,'perimD':78,'rimProt':99,'helpSwitch':88,'steals':38,'rebuilding':95,'athleticism':78},
        "stats": {"pts":14.3,"ast":1.3,"reb":13.5,"stl":0.6,"blk":2.7,"fg_pct":67.5,"tp_pct":0.0,"ft_pct":62.3,"gp":71,"mpg":30.8}
    },
    {
        "id": "randle-21", "name": "朱利叶斯·兰德尔 (21)", "position": "PF",
        "team": "尼克斯", "color": "#F58426", "season": "2020-21",
        "attrs": {'threePT':72,'midRange':75,'rimFin':78,'FT':80,'playmaking':68,'ballHandle':72,'perimD':62,'rimProt':28,'helpSwitch':52,'steals':52,'rebuilding':78,'athleticism':72},
        "stats": {"pts":24.1,"ast":6.0,"reb":10.2,"stl":0.9,"blk":0.3,"fg_pct":45.6,"tp_pct":41.1,"ft_pct":81.1,"gp":71,"mpg":37.6}
    },
    {
        "id": "sabonis-23", "name": "多曼塔斯·萨博尼斯 (23)", "position": "C",
        "team": "国王", "color": "#5A2D81", "season": "2022-23",
        "attrs": {'threePT':55,'midRange':72,'rimFin':78,'FT':72,'playmaking':82,'ballHandle':65,'perimD':58,'rimProt':42,'helpSwitch':55,'steals':52,'rebuilding':92,'athleticism':58},
        "stats": {"pts":19.1,"ast":7.3,"reb":12.3,"stl":0.8,"blk":0.5,"fg_pct":61.5,"tp_pct":37.3,"ft_pct":74.2,"gp":79,"mpg":34.6}
    },
    {
        "id": "siakam-23", "name": "帕斯卡尔·西亚卡姆 (23)", "position": "PF",
        "team": "猛龙", "color": "#CE1141", "season": "2022-23",
        "attrs": {'threePT':62,'midRange':75,'rimFin':78,'FT':75,'playmaking':62,'ballHandle':72,'perimD':75,'rimProt':42,'helpSwitch':68,'steals':58,'rebuilding':72,'athleticism':78},
        "stats": {"pts":24.2,"ast":5.8,"reb":7.8,"stl":0.9,"blk":0.5,"fg_pct":48.0,"tp_pct":32.4,"ft_pct":77.4,"gp":71,"mpg":37.4}
    },
    {
        "id": "markkanen-23", "name": "劳里·马尔卡宁 (23)", "position": "PF",
        "team": "爵士", "color": "#002B5C", "season": "2022-23",
        "attrs": {'threePT':82,'midRange':72,'rimFin':78,'FT':88,'playmaking':38,'ballHandle':62,'perimD':55,'rimProt':32,'helpSwitch':45,'steals':42,'rebuilding':68,'athleticism':75},
        "stats": {"pts":25.6,"ast":1.9,"reb":8.6,"stl":0.6,"blk":0.6,"fg_pct":49.9,"tp_pct":39.1,"ft_pct":87.5,"gp":66,"mpg":34.4}
    },
    {
        "id": "adebayo-23", "name": "巴姆·阿德巴约 (23)", "position": "C",
        "team": "热火", "color": "#98002E", "season": "2022-23",
        "attrs": {'threePT':15,'midRange':65,'rimFin':78,'FT':78,'playmaking':55,'ballHandle':58,'perimD':88,'rimProt':78,'helpSwitch':88,'steals':65,'rebuilding':82,'athleticism':82},
        "stats": {"pts":20.4,"ast":3.2,"reb":9.2,"stl":1.2,"blk":0.8,"fg_pct":54.0,"tp_pct":0.0,"ft_pct":80.6,"gp":75,"mpg":34.6}
    },
    {
        "id": "lamelo-22", "name": "拉梅洛·鲍尔 (22)", "position": "PG",
        "team": "黄蜂", "color": "#1D1160", "season": "2021-22",
        "attrs": {'threePT':78,'midRange':65,'rimFin':62,'FT':82,'playmaking':85,'ballHandle':90,'perimD':55,'rimProt':22,'helpSwitch':48,'steals':68,'rebuilding':52,'athleticism':72},
        "stats": {"pts":20.1,"ast":7.6,"reb":6.7,"stl":1.6,"blk":0.4,"fg_pct":42.9,"tp_pct":38.9,"ft_pct":87.2,"gp":75,"mpg":32.3}
    },
    {
        "id": "maxey-24", "name": "泰雷斯·马克西 (24)", "position": "SG",
        "team": "76人", "color": "#006BB6", "season": "2023-24",
        "attrs": {'threePT':82,'midRange':78,'rimFin':78,'FT':88,'playmaking':72,'ballHandle':88,'perimD':58,'rimProt':15,'helpSwitch':48,'steals':55,'rebuilding':35,'athleticism':88},
        "stats": {"pts":25.9,"ast":6.2,"reb":3.7,"stl":1.0,"blk":0.5,"fg_pct":45.0,"tp_pct":37.3,"ft_pct":86.8,"gp":70,"mpg":37.5}
    },
    {
        "id": "haliburton-23", "name": "泰雷斯·哈利伯顿 (23)", "position": "PG",
        "team": "步行者", "color": "#FDBB30", "season": "2022-23",
        "attrs": {'threePT':82,'midRange':72,'rimFin':62,'FT':88,'playmaking':94,'ballHandle':90,'perimD':55,'rimProt':18,'helpSwitch':48,'steals':65,'rebuilding':38,'athleticism':68},
        "stats": {"pts":20.7,"ast":10.4,"reb":3.7,"stl":1.6,"blk":0.4,"fg_pct":49.0,"tp_pct":40.0,"ft_pct":87.1,"gp":56,"mpg":33.6}
    },
    {
        "id": "brunson-24", "name": "杰伦·布伦森 (24)", "position": "PG",
        "team": "尼克斯", "color": "#F58426", "season": "2023-24",
        "attrs": {'threePT':78,'midRange':90,'rimFin':72,'FT':85,'playmaking':84,'ballHandle':88,'perimD':52,'rimProt':10,'helpSwitch':42,'steals':55,'rebuilding':35,'athleticism':65},
        "stats": {"pts":28.7,"ast":6.7,"reb":3.6,"stl":0.9,"blk":0.2,"fg_pct":47.9,"tp_pct":40.1,"ft_pct":84.7,"gp":77,"mpg":35.4}
    },
    {
        "id": "edwards-24", "name": "安东尼·爱德华兹 (24)", "position": "SG",
        "team": "森林狼", "color": "#0C2340", "season": "2023-24",
        "attrs": {'threePT':78,'midRange':80,'rimFin':92,'FT':84,'playmaking':68,'ballHandle':85,'perimD':80,'rimProt':38,'helpSwitch':68,'steals':68,'rebuilding':52,'athleticism':96},
        "stats": {"pts":25.9,"ast":5.1,"reb":5.4,"stl":1.3,"blk":0.5,"fg_pct":46.1,"tp_pct":35.7,"ft_pct":83.6,"gp":79,"mpg":35.1}
    },
    {
        "id": "banchero-24", "name": "保罗·班切罗 (24)", "position": "PF",
        "team": "魔术", "color": "#0077C0", "season": "2023-24",
        "attrs": {'threePT':62,'midRange':75,'rimFin':85,'FT':72,'playmaking':68,'ballHandle':78,'perimD':62,'rimProt':42,'helpSwitch':55,'steals':55,'rebuilding':68,'athleticism':82},
        "stats": {"pts":22.6,"ast":5.4,"reb":6.9,"stl":0.9,"blk":0.6,"fg_pct":45.5,"tp_pct":33.9,"ft_pct":72.5,"gp":80,"mpg":35.0}
    },
    {
        "id": "wembanyama-24", "name": "维克托·文班亚马 (24)", "position": "C",
        "team": "马刺", "color": "#000000", "season": "2023-24",
        "attrs": {'threePT':65,'midRange':62,'rimFin':85,'FT':80,'playmaking':55,'ballHandle':65,'perimD':82,'rimProt':98,'helpSwitch':92,'steals':72,'rebuilding':88,'athleticism':92},
        "stats": {"pts":21.4,"ast":3.9,"reb":10.6,"stl":1.2,"blk":3.6,"fg_pct":46.5,"tp_pct":32.5,"ft_pct":79.6,"gp":71,"mpg":29.7}
    },
    {
        "id": "cade-24", "name": "凯德·坎宁安 (24)", "position": "PG",
        "team": "活塞", "color": "#C8102E", "season": "2023-24",
        "attrs": {'threePT':68,'midRange':78,'rimFin':68,'FT':85,'playmaking':82,'ballHandle':82,'perimD':65,'rimProt':35,'helpSwitch':58,'steals':55,'rebuilding':55,'athleticism':72},
        "stats": {"pts":22.7,"ast":7.5,"reb":4.3,"stl":0.9,"blk":0.4,"fg_pct":44.9,"tp_pct":35.5,"ft_pct":86.9,"gp":62,"mpg":33.5}
    },
    {
        "id": "mobley-24", "name": "埃文·莫布利 (24)", "position": "PF",
        "team": "骑士", "color": "#860038", "season": "2023-24",
        "attrs": {'threePT':55,'midRange':65,'rimFin':78,'FT':68,'playmaking':48,'ballHandle':58,'perimD':88,'rimProt':85,'helpSwitch':88,'steals':58,'rebuilding':78,'athleticism':80},
        "stats": {"pts":15.7,"ast":3.2,"reb":9.4,"stl":0.9,"blk":1.4,"fg_pct":58.0,"tp_pct":37.3,"ft_pct":71.9,"gp":50,"mpg":30.6}
    },
    {
        "id": "jjj-23", "name": "小贾伦·杰克逊 (23)", "position": "PF",
        "team": "灰熊", "color": "#5D76A9", "season": "2022-23",
        "attrs": {'threePT':68,'midRange':65,'rimFin':82,'FT':78,'playmaking':28,'ballHandle':48,'perimD':82,'rimProt':95,'helpSwitch':85,'steals':62,'rebuilding':68,'athleticism':82},
        "stats": {"pts":18.6,"ast":1.0,"reb":6.8,"stl":1.0,"blk":3.0,"fg_pct":50.6,"tp_pct":35.5,"ft_pct":78.8,"gp":63,"mpg":28.4}
    },
    {
        "id": "dariusgarland-23", "name": "达里厄斯·加兰 (23)", "position": "PG",
        "team": "骑士", "color": "#860038", "season": "2022-23",
        "attrs": {'threePT':82,'midRange':78,'rimFin':55,'FT':88,'playmaking':85,'ballHandle':88,'perimD':48,'rimProt':8,'helpSwitch':40,'steals':52,'rebuilding':28,'athleticism':68},
        "stats": {"pts":21.6,"ast":7.8,"reb":2.7,"stl":1.2,"blk":0.1,"fg_pct":46.2,"tp_pct":41.0,"ft_pct":86.3,"gp":69,"mpg":35.5}
    },
    {
        "id": "chetholmgren-24", "name": "切特·霍姆格伦 (24)", "position": "C",
        "team": "雷霆", "color": "#007AC1", "season": "2023-24",
        "attrs": {'threePT':72,'midRange':65,'rimFin':78,'FT':80,'playmaking':42,'ballHandle':58,'perimD':78,'rimProt':88,'helpSwitch':80,'steals':48,'rebuilding':75,'athleticism':72},
        "stats": {"pts":16.5,"ast":2.4,"reb":7.9,"stl":0.6,"blk":2.3,"fg_pct":53.0,"tp_pct":37.0,"ft_pct":79.3,"gp":82,"mpg":29.4}
    },
    {
        "id": "shai-23", "name": "谢伊·吉尔杰斯-亚历山大 (23)", "position": "SG",
        "team": "雷霆", "color": "#007AC1", "season": "2022-23",
        "attrs": {'threePT':72,'midRange':90,'rimFin':88,'FT':90,'playmaking':82,'ballHandle':92,'perimD':85,'rimProt':42,'helpSwitch':68,'steals':78,'rebuilding':52,'athleticism':84},
        "stats": {"pts":31.4,"ast":5.5,"reb":4.8,"stl":1.6,"blk":1.0,"fg_pct":51.0,"tp_pct":34.5,"ft_pct":90.5,"gp":68,"mpg":35.5}
    },
    {
        "id": "sengun-24", "name": "阿尔佩伦·申京 (24)", "position": "C",
        "team": "火箭", "color": "#CE1141", "season": "2023-24",
        "attrs": {'threePT':45,'midRange':72,'rimFin':85,'FT':68,'playmaking':72,'ballHandle':65,'perimD':58,'rimProt':58,'helpSwitch':52,'steals':55,'rebuilding':78,'athleticism':55},
        "stats": {"pts":21.1,"ast":5.0,"reb":9.3,"stl":1.2,"blk":0.7,"fg_pct":53.7,"tp_pct":29.7,"ft_pct":69.3,"gp":63,"mpg":32.5}
    },
    {
        "id": "jalenwilliams-24", "name": "杰伦·威廉姆斯 (24)", "position": "SG",
        "team": "雷霆", "color": "#007AC1", "season": "2023-24",
        "attrs": {'threePT':75,'midRange':78,'rimFin':82,'FT':80,'playmaking':62,'ballHandle':78,'perimD':78,'rimProt':38,'helpSwitch':68,'steals':65,'rebuilding':45,'athleticism':82},
        "stats": {"pts":19.1,"ast":4.5,"reb":4.0,"stl":1.1,"blk":0.6,"fg_pct":54.0,"tp_pct":42.7,"ft_pct":81.4,"gp":71,"mpg":31.3}
    },
    {
        "id": "porzingis-23", "name": "克里斯塔普斯·波尔津吉斯 (23)", "position": "C",
        "team": "凯尔特人", "color": "#007A33", "season": "2022-23",
        "attrs": {'threePT':78,'midRange':72,'rimFin':82,'FT':85,'playmaking':38,'ballHandle':52,'perimD':72,'rimProt':82,'helpSwitch':68,'steals':48,'rebuilding':72,'athleticism':62},
        "stats": {"pts":23.2,"ast":2.7,"reb":8.4,"stl":0.9,"blk":1.5,"fg_pct":49.8,"tp_pct":38.5,"ft_pct":85.1,"gp":65,"mpg":32.6}
    },
    {
        "id": "zion-23", "name": "蔡恩·威廉森 (23)", "position": "PF",
        "team": "鹈鹕", "color": "#0C2340", "season": "2022-23",
        "attrs": {'threePT':25,'midRange':55,'rimFin':96,'FT':65,'playmaking':58,'ballHandle':78,'perimD':58,'rimProt':38,'helpSwitch':48,'steals':58,'rebuilding':65,'athleticism':98},
        "stats": {"pts":26.0,"ast":4.6,"reb":7.0,"stl":1.1,"blk":0.6,"fg_pct":60.8,"tp_pct":34.3,"ft_pct":71.4,"gp":29,"mpg":33.0}
    },
    {
        "id": "swipa-23", "name": "达龙·福克斯 (23)", "position": "PG",
        "team": "国王", "color": "#5A2D81", "season": "2022-23",
        "attrs": {'threePT':72,'midRange':82,'rimFin':82,'FT':78,'playmaking':78,'ballHandle':90,'perimD':68,'rimProt':22,'helpSwitch':55,'steals':68,'rebuilding':40,'athleticism':94},
        "stats": {"pts":25.0,"ast":6.1,"reb":4.2,"stl":1.1,"blk":0.3,"fg_pct":51.2,"tp_pct":32.4,"ft_pct":78.0,"gp":73,"mpg":33.4}
    },
    {
        "id": "towns-24", "name": "卡尔-安东尼·唐斯 (24)", "position": "C",
        "team": "森林狼", "color": "#0C2340", "season": "2023-24",
        "attrs": {'threePT':82,'midRange':82,'rimFin':82,'FT':88,'playmaking':58,'ballHandle':62,'perimD':62,'rimProt':65,'helpSwitch':55,'steals':48,'rebuilding':78,'athleticism':68},
        "stats": {"pts":21.8,"ast":3.1,"reb":8.3,"stl":0.7,"blk":0.7,"fg_pct":50.4,"tp_pct":41.6,"ft_pct":87.3,"gp":62,"mpg":32.7}
    },
]


def main():
    with open("players.json", "r", encoding="utf-8") as f:
        players = json.load(f)

    existing_ids = {p["id"] for p in players}
    added = 0
    for a in ALLSTARS:
        if a["id"] not in existing_ids:
            players.append(a)
            added += 1

    # Remove duplicates (keep first occurrence by id)
    seen = set()
    deduped = []
    for p in players:
        if p["id"] not in seen:
            seen.add(p["id"])
            deduped.append(p)

    with open("players.json", "w", encoding="utf-8") as f:
        json.dump(deduped, f, ensure_ascii=False, indent=2)

    print(f"Added {added} new All-Stars.")
    print(f"Total: {len(deduped)} players")
    cur = sum(1 for p in deduped if "season" not in p)
    leg = sum(1 for p in deduped if "season" in p)
    print(f"Current: {cur}, Legends/All-Stars: {leg}")


if __name__ == "__main__":
    main()
