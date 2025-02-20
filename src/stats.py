from constants import *
#unit stats
#var = ("name", health, regen, attack, defense, range, movement, cost (wood, metal, food, water), timer, sequences, abilities)
man = {"name": "Man", "health": 8, "regen": 3, "attack": 7, "defense": 2, "range": 1, "movement": 2, "cost": {"wood": 0, "metal": 0, "food": 0, "water": 0}, "time": 10, "sequences": (("move", "attack"), ("heal",)), "abilities": ()}
#man can move 1 or attack
swordsman = {"name": "Swordsman", "health": 12, "regen": 4, "attack": 9, "defense": 3, "range": 1, "movement": 2, "cost": {"wood": 0, "metal": 5, "food": 0, "water": 0}, "time": 15, "sequences": (('move', 'attack'), ('heal',)), "abilities": ()}
spearman = {"name": "Spearman", "health": 10, "regen": 3, "attack": 8, "defense": 2, "range": 1, "movement": 2, "cost": {"wood": 6, "metal": 6, "food": 0, "water": 0}, "time": 12, "sequences": (('move', 'attack', 'attack'), ('heal',)), "abilities": ()}
axeman = {"name": "Axeman", "health": 12, "regen": 4, "attack": 25, "defense": 3, "range": 1, "movement": 1, "cost": {"wood": 2, "metal": 9, "food": 1, "water": 3}, "time": 13, "sequences": (('move',), ('attack',), ('heal',)), "abilities": ()}
shieldman = {"name": "Shieldman", "health": 15, "regen": 5, "attack": 6, "defense": 4, "range": 1, "movement": 1, "cost": {"wood": 3, "metal": 10, "food": 1, "water": 2}, "time": 10, "sequences": (('move',), ('attack',)), "abilities": ()}
archer = {"name": "Archer", "health": 8, "regen": 4, "attack": 7, "defense": 1, "range": 2, "movement": 2, "cost": {"wood": 3, "metal": 0, "food": 0, "water": 0}, "time": 14, "sequences": (('attack', 'move'), ('move', 'heal')), "abilities": ()}
crossbowman = {"name": "Crossbowman", "health": 5, "regen": 2, "attack": 15, "defense": 1, "range": 3, "movement": 2, "cost": {"wood": 10, "metal": 5, "food": 3, "water": 2}, "time": 17, "sequences": (('move', 'attack'), ('attack', 'move'), ('heal',)), "abilities": ()}
field_medic = {"name": "Field Medic", "health": 10, "regen": 10, "attack": 0, "defense": 2, "range": 1, "movement": 1, "cost": {"wood": 3, "metal": 1, "food": 2, "water": 3}, "time": 8, "sequences": (('move', 'heal other'), ('move', 'heal')), "abilities": ()}
rider = {"name": "Rider", "health": 9, "regen": 5, "attack": 7, "defense": 2, "range": 1, "movement": 3, "cost": {"wood": 0, "metal": 0, "food": 3, "water": 0}, "time": 12, "sequences": (('move', 'attack'), ('move', 'heal')), "abilities": ()}
knight = {"name": "Knight", "health": 13, "regen": 6, "attack": 7, "defense": 1, "range": 1, "movement": 3, "cost": {"wood": 2, "metal": 4, "food": 6, "water": 3}, "time": 18, "sequences": (('move', 'attack'), ('attack', 'move'), ('heal',)), "abilities": ()}
elephant = {"name": "Elephant", "health": 16, "regen": 6, "attack": 15, "defense": 2, "range": 1, "movement": 3, "cost": {"wood": 5, "metal": 3, "food": 10, "water": 7}, "time": 30, "sequences": (('move', 'attack', 'heal'),), "abilities": ()}

#building stats
#var = ("name", list, cost, production, production speed, possible terrain, abilities, upgrade into)
lumber_hut = {"name": "Lumber Hut", "cost": {"wood": 5, "metal": 3, "food": 3, "water": 3}, "production": {"wood": 3, "metal": 0, "food": 0, "water": 0}, "production time": 1, "terrain": 'forest', "abilities": (), "upgraded building": None}
foundry = {"name": "Foundry", "cost": {"wood": 4, "metal": 9, "food": 6, "water": 6}, "production": {"wood": 0, "metal": 20, "food": 0, "water": 0}, "production time": 2, "terrain": None, "abilities": (), "upgraded building": None}
mine = {"name": "Mine", "cost": {"wood": 5, "metal": 5, "food": 2, "water": 3}, "production": {"wood": 0, "metal": 5, "food": 0, "water": 0}, "production time": 2, "terrain": 'mountain', "abilities": (), "upgraded building": foundry}
shipyard = {"name": "Shipyard", "cost": {"wood": 4, "metal": 3, "food": 5, "water": 7}, "production": {"wood": 0, "metal": 0, "food": 0, "water": 5}, "production time": 1, "terrain": 'water', "abilities": ('shipbuilding'), "upgraded building": None}
pipelines = {"name": "Pipelines", "cost": {"wood": 3, "metal": 3, "food": 6, "water": 5}, "production": {"wood": 0, "metal": 0, "food": 0, "water": 20}, "production time": 3, "terrain": None, "abilities": (), "upgraded building": None}
aqueduct = {"name": "Aqueduct", "cost": {"wood": 2, "metal": 3, "food": 2, "water": 5}, "production": {"wood": 0, "metal": 0, "food": 0, "water": 5}, "production time": 2, "terrain": 'water', "abilities": (), "upgraded building": pipelines}
plantation = {"name": "Plantation", "cost": {"wood": 8, "metal": 4, "food": 6, "water": 7}, "production": {"wood": 0, "metal": 0, "food": 20, "water": 0}, "production time": 1, "terrain": None, "abilities": (), "upgraded building": None}
farm = {"name": "Farm", "cost": {"wood": 0, "metal": 1, "food": 9, "water": 7}, "production": {"wood": 0, "metal": 0, "food": 10, "water": 0}, "production time": 1, "terrain": 'crop', "abilities": (), "upgraded building": plantation}

#tech = ("Tech", price, x, y, preceding_tech, unit, building, upgraded building, player action, terrain, img)
logging = {"name": "Logging", "cost": 5, "coords": (50, 500), "preceding tech": None, "type": "player action", "new": "chop"}
trekking = {"name": "Trekking", "cost": 25, "coords": (0, 250), "preceding tech": logging, "type": "terrain", "new": "dense forest"}
archery = {"name": "Archery", "cost": 10, "coords": (100, 300), "preceding tech": logging, "type": "unit", "new": archer}
engineering = {"name": "Engineering", "cost": 20, "coords": (0, 100), "preceding tech": archery, "type": "unit", "new": crossbowman}
forestry = {"name": "Forestry", "cost": 10, "coords": (250, 300), "preceding tech": logging, "type": "building", "new": lumber_hut}
reforestation = {"name": "Reforestation", "cost": 20, "coords": (100, 0), "preceding tech": trekking, "type": "player action", "new": "grow"}
medicine = {"name": "Medicine", "cost": 20, "coords": (150, 100), "preceding tech": forestry, "type": "unit", "new": field_medic}
climbing = {"name": "Climbing", "cost": 5, "coords": (350, 500), "preceding tech": None, "type": "terrain", "new": "mountain"}
smithery = {"name": "Smithery", "cost": 15, "coords": (350, 300), "preceding tech": climbing, "type": "unit", "new": swordsman}
sharpening = {"name": "Sharpening", "cost": 25, "coords": (450, 100), "preceding tech": smithery, "type": "unit", "new": spearman}
armoring_img = pygame.image.load("../tech/armoring.png")
armoring = {"name": "Armoring", "cost": 25, "coords": (350, 150), "preceding tech": smithery, "type": "unit", "new": shieldman}
molding_img = pygame.image.load("../tech/molding.png")
molding = {"name": "Molding", "cost": 30, "coords": (200, 150), "preceding tech": smithery, "type": "unit", "new": axeman}
mining = {"name": "Mining", "cost": 10, "coords": (475, 300), "preceding tech": climbing, "type": "building", "new": mine}
smelting = {"name": "Smelting", "cost": 25, "coords": (550, 50), "preceding tech": mining, "type": "upgraded building", "new": foundry}
extraction = {"name": "Extraction", "cost": 15, "coords": (475, 25), "preceding tech": mining, "type": "player action", "new": "extract"}
refinement = {"name": "Refinement", "cost": 10, "coords": (600, 150), "preceding tech": extraction, "type": "player action", "new": "refine"}
swimming = {"name": "Swimming", "cost": 5, "coords": (500, 500), "preceding tech": None, "type": "terrain", "new": "water"}
collection = {"name": "Collection", "cost": 10, "coords": (550, 200), "preceding tech": swimming, "type": "player action", "new": "collect"}
architecture = {"name": "Architecture", "cost": 15, "coords": (650, 300), "preceding tech": swimming, "type": "building", "new": aqueduct}
waterworks = {"name": "Waterworks", "cost": 10, "coords": (650, 50), "preceding tech": architecture, "type": "upgraded building", "new": pipelines}
cultivation = {"name": "Cultivation", "cost": 5, "coords": (800, 500), "preceding tech": None, "type": "player action", "new": "cultivate"}
riding = {"name": "Riding", "cost": 12, "coords": (850, 300), "preceding tech": cultivation, "type": "unit", "new": rider}
honor = {"name": "Honor", "cost": 12, "coords": (950, 100), "preceding tech": riding, "type": "unit", "new": knight}
taming = {"name": "Taming", "cost": 30, "coords": (850, 0), "preceding tech": riding, "type": "unit", "new": elephant}
farming = {"name": "Farming", "cost": 10, "coords": (750, 300), "preceding tech": cultivation, "type": "building", "new": farm}
agriculture = {"name": "Agriculture", "cost": 25, "coords": (750, 50), "preceding tech": farming, "type": "upgraded building", "new": plantation}
fertilization = {"name": "Fertilization", "cost": 20, "coords": (825, 150), "preceding tech": farming, "type": "player action", "new": "fertilize"}
overharvesting = {"name": "Overharvesting", "cost": 20, "coords": (950, 300), "preceding tech": cultivation, "type": "player action", "new": "reap"}
all_techs = (logging, trekking, archery, engineering, forestry, reforestation, medicine, climbing, smithery, sharpening, armoring, molding, mining, smelting, extraction, swimming, collection, architecture, waterworks, refinement, cultivation, riding, honor, taming, farming, agriculture, fertilization, overharvesting)
for tech in all_techs:
    tech["img"] = pygame.image.load("../tech/" + tech["name"].lower() + ".png").convert_alpha()