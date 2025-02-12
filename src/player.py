from location import *
from stats import man, ship
class Player:
  #contains all the players
  player_list = []
  chop_cost = 5
  cultivate_cost = 10
  refine_cost = 30
  extract_cost = 5
  grow_cost = 15
  fertilize_cost = 20
  reap_cost = 5
  collect_cost = 10
  cost_dict = {"chop":chop_cost, "cultivate":cultivate_cost, "refine":refine_cost, "extract":extract_cost, "grow":grow_cost, "fertilize":fertilize_cost, "reap":reap_cost, "collect":collect_cost}
  #player_action icons
  chop_img = pygame.image.load("../player actions/chop.png").convert_alpha()
  cultivate_img = pygame.image.load("../player actions/cultivate.png").convert_alpha()
  refine_img = pygame.image.load("../player actions/refine.png").convert_alpha()
  extract_img = pygame.image.load("../player actions/extract.png").convert_alpha()
  grow_img = pygame.image.load("../player actions/grow.png").convert_alpha()
  fertilize_img = pygame.image.load("../player actions/fertilize.png").convert_alpha()
  reap_img = pygame.image.load("../player actions/reap.png").convert_alpha()
  collect_img = pygame.image.load("../player actions/collect.png").convert_alpha()
  img_dict = {"chop":chop_img, "cultivate":cultivate_img, "refine":refine_img, "extract":extract_img, "grow":grow_img, "fertilize":fertilize_img, "reap":reap_img, "collect":collect_img}
  def __init__(self, player_number: int):
    #player number determines the order the players play in starting from 0 not 1
    self.player_number = player_number
    self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
    self.money = 10000 #0
    self.wood = 10000 #0
    self.metal = 10000 #0
    self.food = 10000 #0
    self.water = 10000 #0
    self.units = []
    self.buildings = []
    self.cities = []
    self.techs = []
    #player can only make the available buildings and must unlock new techs to append to this list
    self.available_buildings = []
    self.available_upgraded_buildings = []
    #make more resources later
    self.available_actions = []
    #available player actions
    self.available_units = [man]
    self.available_naval_units = [ship]
    #available terrain the player's units can be on
    self.available_terrain = ["plains", "forest", "fertile land"]
  def display_units(self, availability_marker_size: int = 10) -> None:
    #this displays a list of specific units (a unit type)
    #units would be a list containing a specific unit type
    for unit in self.units:
      unit.draw(self.color, availability_marker_size)
  def display_buildings(self) -> None:
    #this displays a list of specific units (a unit type)
    #units would be a list containing a specific unit type
    for building in self.buildings:
      building.draw(self.color)
  def display_cities(self) -> None:
    for city in self.cities:
      city.draw(self.color)
  def update(self) -> None:
    #this is the update function for the player
    #display stuff here
    #display buildings
    self.display_buildings()
    #display cities
    self.display_cities()
    #display units
    self.display_units()
    #update everything:
    #add the money per turn, resources per turn
  def player_action_eligible(self, action: str, location: Location) -> bool:
    if action == "chop":
      if location.terrain == "forest" or location.terrain == "dense forest":
        return True
    elif action == "cultivate":
      if location.terrain == "fertile land":
        return True
    elif action == "refine":
      if "mineral" in location.features:
        return True
    elif action == "extract":
      if "ore" in location.features:
        return True
    elif action == "grow":
      if location.terrain == "plains" or location.terrain == "forest":
        return True
    elif action == "fertilize":
      if location.terrain == "plains":
        return True
    elif action == "reap":
      if location.terrain == "fertile land":
        return True
    elif action == "collect":
      if location.terrain == "water":
        return True
    return False
  def player_action(self, action: str, location: Location, cost: int = 0) -> None:
    if action == "chop":
      #get wood by cutting down forest into plains
      #location must be at forest tile
      self.wood += 5
      if location.terrain == "forest":
        location.terrain = "plains"
      elif location.terrain == "dense forest":
        location.terrain = "forest"
    elif action == "cultivate":
      self.food += 3
    elif action == "refine":
      self.metal += 20
      location.features.remove("mineral")
    elif action == "extract":
      self.metal += 10
      location.features.remove("ore")
    elif action == "grow":
      #grow forest from plains
      if location.terrain == "plains":
        location.terrain = "forest"
      if location.terrain == "forest":
        location.terrain = "dense forest"
    elif action == "fertilize":
      location.terrain = "fertile land"
    elif action == "reap":
      location.terrain = "plains"
      self.food += 12
    if action == "collect":
      self.water += 5
      location.terrain = "plains"
    location.image = Location.img_dict[location.terrain]
    location.player_acted_on = True
    self.money -= cost
  def turn_update_before(self) -> None:
    #this takes place at the beginning of turn, where buildings and cities produce resources
    #reset crop resource
    for building in self.buildings:
      building.produce()
    for city in self.cities:
      city.produce()
    
    #reset variables so u can't control dudes that belong to other players
    #move on to next player
  def turn_update_after(self) -> None:
    #this takes place after turn, where units gain energy and cities reset exhaustion
    for unit in self.units:
      unit.unit_reset()
      unit.turn_done = False #gain energy
    for city in self.cities:
      city.spawn_timer -= city.max_spawn_timer
      if city.spawn_timer < 0:
        city.spawn_timer = 0
  def deduct_costs(self, amounts: List[int]) -> None:
    #amounts is a list containing [wood, metal, food, water]
    #if deduct is True, subtract the resources, otherwise, add them
    self.wood -= amounts[0]
    self.metal -= amounts[1]
    self.food -= amounts[2]
    self.water -= amounts[3]
  def owns_unit_there(self, location: Location) -> bool:
    if(location.unit != None and location.unit.player_number == self.player_number):
      return True
    return False