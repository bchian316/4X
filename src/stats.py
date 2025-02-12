from constants import *
#unit stats
#var = ["name", health, regen, attack, defense, range, movement, cost [wood, metal, food, water], timer, sequences, abilities]
man = ["Man", 8, 3, 6, 2,  1, 2, [0, 0, 0, 0], 10, [["move", "attack"], ["heal"]], []]
#man can move 1 or attack
swordsman = ["Swordsman", 12, 4, 9, 3, 1, 2, [0, 5, 0, 0], 15, [["move", "attack"], ["heal"]], []]
spearman = ["Spearman", 10, 3, 8, 2, 1, 2, [6, 6, 0, 0], 12, [["move", "attack", "attack"], ["heal"]], []]
axeman = ["Axeman", 12, 4, 25, 3, 1, 1, [2, 9, 1, 3], 13, [["move"], ["attack"], ["heal"]], []]
shieldman = ["Shieldman", 15, 5, 6, 4, 1, 1, [3, 10, 1, 2], 10, [["move"], ["attack"]], []]
#scout = ["Scout", Player.player_list[current_player].scouts, 3, 1, 5, 3, 1, 3, [3, 1, 0, 0], 3, [["move", "attack", "move"]], []]
#scout can move 3, attack 3, and move 3
#catapult = ["Catapult", Player.player_list[current_player].units, 5, 0, 10, 3, 3, 1, [3, 3, 0, 0], 8, [["move"], ["attack"]], []]
#catapult can move 1 or attack 1
archer = ["Archer", 8, 4, 7, 1, 2, 2, [3, 0, 0, 0], 14, [["attack", "move"], ["move", "heal"]], []]
crossbowman = ["Crossbowman", 5, 2, 15, 1, 3, 2, [10, 5, 3, 2], 17, [["move", "attack"], ["attack", "move"], ["heal"]], []]
field_medic = ["Field Medic", 10, 10, 0, 2, 1, 1, [3, 1, 2, 3], 8, [["move", "heal other"], ["move", "heal"]], []]
rider = ["Rider", 9, 5, 7, 2, 1, 3, [0, 0, 3, 0], 12, [["move", "attack"], ["move", "heal"]], []]
knight = ["Knight", 13, 6, 7, 1, 1, 3, [2, 4, 6, 3], 18, [["move", "attack"], ["attack", "move"], ["heal"]], []]
elephant = ["Elephant", 18, 6, 15, 2, 1, 3, [5, 3, 10, 7], 30, [["move", "attack", "heal"]], []]
ship = ["Ship", 10, 3, 1, 1, 0, 0, [0, 0, 0, 3], 0, [["move", "attack"], ["move", "heal", "move"]], ["float"]]
steeler = ["Steeler", 20, 5, 1.5, 1.5, 0, 0, [2, 6, 3, 8], 0, [["move", "attack", "move"], ["heal"]], ["float"]]

#building stats
#var = ["name", list, cost, production, production speed, possible terrain, abilities, upgrade into]
lumber_hut = ["Lumber Hut", [5, 3, 3, 3], [3, 0, 0, 0], 1, ["forest"], [], None]
foundry = ["Foundry", [4, 9, 6, 6], [0, 20, 0, 0], 2, None, [], None]
#foundry is upgradable, so there's no terrain restrictions: u just build it on top of a mine
mine = ["Mine", [5, 5, 2, 3], [0, 5, 0, 0], 2, ["mountain"], [], foundry]
shipyard = ["Shipyard", [4, 3, 5, 7], [0, 0, 0, 5], 1, ["water"], ["shipbuilding"], None]
pipelines = ["Pipelines", [3, 3, 6, 5], [0, 0, 0, 20], 3, [], [], None]
aqueduct = ["Aqueduct", [2, 3, 2, 5], [0, 0, 0, 5], 2, ["water"], [], pipelines]
plantation = ["Plantation", [8, 4, 6, 7], [0, 0, 20, 0], 1, None, [], None]
farm = ["Farm", [0, 1, 9, 7], [0, 0, 10, 0], 1, ["fertile land"], [], plantation]

#tech = ["Tech", price, x, y, preceding_tech, unit, building, upgraded building, player action, terrain, img]
logging_img = pygame.image.load("../tech/logging.png").convert_alpha()
logging = ["Logging", 5, (50, 500), None, None, None, None, "chop", None, logging_img]
trekking_img = pygame.image.load("../tech/trekking.png").convert_alpha()
trekking = ["Trekking", 25, (0, 250), logging, None, None, None, None, "dense forest", trekking_img]
archery_img = pygame.image.load("../tech/archery.png").convert_alpha()
archery = ["Archery", 10, (100, 300), logging, archer, None, None, None, None, archery_img]
engineering_img = pygame.image.load("../tech/engineering.png").convert_alpha()
engineering = ["Engineering", 20, (0, 100), archery, crossbowman, None, None, None, None, engineering_img]
forestry_img = pygame.image.load("../tech/forestry.png").convert_alpha()
forestry = ["Forestry", 10, (250, 300), logging, None, lumber_hut, None, None, None, forestry_img]
reforestation_img = pygame.image.load("../tech/reforestation.png").convert_alpha()
reforestation = ["Reforestation", 20, (100, 0), trekking, None, None, None, "grow", None, reforestation_img]
medicine_img = pygame.image.load("../tech/medicine.png").convert_alpha()
medicine = ["Medicine", 20, (150, 100), forestry, field_medic, None, None, None, None, medicine_img]
climbing_img = pygame.image.load("../tech/climbing.png").convert_alpha()
climbing = ["Climbing", 5, (350, 500), None, None, None, None, None, "mountain", climbing_img]
smithery_img = pygame.image.load("../tech/smithery.png").convert_alpha()
smithery = ["Smithery", 15, (350, 300), climbing, swordsman, None, None, None, None, smithery_img]
sharpening_img = pygame.image.load("../tech/sharpening.png").convert_alpha()
sharpening = ["Sharpening", 25, (450, 100), smithery, spearman, None, None, None, None, sharpening_img]
armoring_img = pygame.image.load("../tech/armoring.png")
armoring = ["Armoring", 25, (350, 150), smithery, shieldman, None, None, None, None, armoring_img]
molding_img = pygame.image.load("../tech/molding.png")
molding = ["Molding", 30, (200, 150), smithery, axeman, None, None, None, None, molding_img]
mining_img = pygame.image.load("../tech/mining.png").convert_alpha()
mining = ["Mining", 10, (475, 300), climbing, None, mine, None, None, None, mining_img]
smelting_img = pygame.image.load("../tech/smelting.png").convert_alpha()
smelting = ["Smelting", 25, (550, 50), mining, None, None, foundry, None, None, smelting_img]
extraction_img = pygame.image.load("../tech/extraction.png").convert_alpha()
extraction = ["Extraction", 15, (475, 25), mining, None, None, None, "extract", None, extraction_img]
refinement_img = pygame.image.load("../tech/refinement.png").convert_alpha()
refinement = ["Refinement", 10, (600, 150), extraction, None, None, None, "refine", None, refinement_img]
swimming_img = pygame.image.load("../tech/swimming.png").convert_alpha()
swimming = ["Swimming", 5, (500, 500), None, None, None, None, None, "water", swimming_img]
sailing_img = pygame.image.load("../tech/sailing.png").convert_alpha()
sailing = ["Sailing", 10, (550, 300), swimming, None, shipyard, None, None, None, sailing_img]
architecture_img = pygame.image.load("../tech/architecture.png").convert_alpha()
architecture = ["Architecture", 15, (650, 300), swimming, None, aqueduct, None, None, None, architecture_img]
waterworks_img = pygame.image.load("../tech/waterworks.png").convert_alpha()
waterworks = ["Waterworks", 10, (650, 50), architecture, None, None, pipelines, None, None, waterworks_img]
cultivation_img = pygame.image.load("../tech/cultivation.png").convert_alpha()
cultivation = ["Cultivation", 5, (800, 500), None, None, None, None, "cultivate", None, cultivation_img]
riding_img = pygame.image.load("../tech/riding.png").convert_alpha()
riding = ["Riding", 12, (850, 300), cultivation, rider, None, None, None, None, riding_img]
honor_img = pygame.image.load("../tech/honor.png").convert_alpha()
honor = ["Honor", 12, (950, 100), riding, knight, None, None, None, None, honor_img]
taming_img = pygame.image.load("../tech/taming.png").convert_alpha()
taming = ["Taming", 30, (850, 0), riding, elephant, None, None, None, None, taming_img]
farming_img = pygame.image.load("../tech/farming.png").convert_alpha()
farming = ["Farming", 10, (750, 300), cultivation, None, farm, None, None, None, farming_img]
agriculture_img = pygame.image.load("../tech/agriculture.png").convert_alpha()
agriculture = ["Agriculture", 25, (750, 50), farming, None, None, plantation, None, None, agriculture_img]
fertilization_img = pygame.image.load("../tech/fertilization.png").convert_alpha()
fertilization = ["Fertilization", 20, (825, 150), farming, None, None, None, "fertilize", None, fertilization_img]
overharvesting_img = pygame.image.load("../tech/overharvesting.png").convert_alpha()
overharvesting = ["Overharvesting", 20, (950, 300), cultivation, None, None, None, "reap", None, overharvesting_img]
all_techs = [logging, trekking, archery, engineering, forestry, reforestation, medicine, climbing, smithery, sharpening, armoring, molding, mining, smelting, extraction, swimming, architecture, waterworks, sailing, refinement, cultivation, riding, honor, taming, farming, agriculture, fertilization, overharvesting]