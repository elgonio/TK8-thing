stage_dict = {
     100: 'Arena',
     101: 'Arena Underground',
     200: 'Urban Square',
     201: 'Urban Square Evening',
     300: 'Yakushima',
     400: 'Coliseum of Fate',
     500: 'Rebel Hangar',
     700: 'Fallen Destiny',
     900: 'Descent into Subconscious',
    1000: 'Sanctum',
    1100: 'Into the Stratosphere',
    1200: 'Ortiz Farm',
    1300: 'Celebration On The Seine',
    1400: 'Secluded Training Ground',
    1500: 'Elegant Palace',
    1600: 'Midnight Siege',
}

char_dict = {
	0:  'Paul',
	1:  'Law',
	2:  'King',
	3:  'Yoshimitsu',
	4:  'Hwoarang',
	5:  'Xiaoyu',
	6:  'Jin',
	7:  'Bryan',
	8:  'Kazuya',
	9:  'Steve',
	10: 'Jack-8',
	11: 'Asuka',
	12: 'Devil Jin',
	13: 'Feng',
	14: 'Lili',
	15: 'Dragunov',
	16: 'Leo',
	17: 'Lars',
	18: 'Alisa',
	19: 'Claudio',
	20: 'Shaheen',
	21: 'Nina',
	22: 'Lee',
	23: 'Kuma',
	24: 'Panda',
	28: 'Zafina',
	29: 'Leroy',
	32: 'Jun',
	33: 'Reina',
	34: 'Azucena',
	35: 'Victor',
	36: 'Raven',
    38: 'Eddy',
    39: 'Lidia',
    40: 'Heihachi',
}

battle_type_dict = {
    1: 'quick match',
    2: 'ranked match',
    3: 'group match',
    4: 'player match'
}

# There are only 3 unique platforms
# 3 is clearly pc
# 8 and 9 are console
# 8 is probably PS since it vastly outnumbers 9 approx 37 : 6
# 9 is probably Xbox
platform_dict = {
    3: 'pc',
    8: 'console/PS?', # PS?
    9: 'console/XBOX?', # Xbox?
}

region_dict = {
    0: 'Asia',
    1: 'Middle East',
    2: 'Oceania',
    3: 'America',
    4: 'Europe',
}

# TODO: double check this
area_dict = {
    0: 'Asia',
    1: 'Middle East',
    2: 'Oceania',
    3: 'America',
    4: 'Europe',
    5: 'africa',
}

dan_names_dict = {
    0: "Beginner",
    1: "1st Dan",
    2: "2nd Dan",
    3: "Fighter",
    4: "Strategist",
    5: "Combatant",
    6: "Brawler",
    7: "Ranger",
    8: "Cavalry",
    9: "Warrior",
    10: "Assailant",
    11: "Dominator",
    12: "Vanquisher",
    13: "Destroyer",
    14: "Eliminator",
    15: "Garyu",
    16: "Shinryu",
    17: "Tenryu",
    18: "Mighty Ruler",
    19: "Flame Ruler",
    20: "Battle Ruler",
    21: "Fujin",
    22: "Raijin",
    23: "Kishin",
    24: "Bushin",
    25: "Tekken King",
    26: "Tekken Emperor",
    27: "Tekken God",
    28: "Tekken God Supreme",
    # God of destruction is officially dan 100 but in the data it is 29
    29: "God of Destruction",
    100: "God of Destruction"
}
