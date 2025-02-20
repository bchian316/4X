import dynamics
from entity import *
from map import *
from animations import resourceAnimation
class Building(Entity):
  #building constructor
  #buildings can only be built where a unit of the same player is
  #buildings are destroyed when other player units move on top of it
  building_size = 75
  cooldown_stat_img = pygame.image.load("../stats/cooldown.png").convert_alpha()
  lumber_hut_img = pygame.image.load("../building/lumber hut.png").convert_alpha()
  mine_img = pygame.image.load("../building/mine.png").convert_alpha()
  shipyard_img = pygame.image.load("../building/shipyard.png").convert_alpha()
  farm_img = pygame.image.load("../building/farm.png").convert_alpha()
  plantation_img = pygame.image.load("../building/plantation.png").convert_alpha()
  foundry_img = pygame.image.load("../building/foundry.png").convert_alpha()
  aqueduct_img = pygame.image.load("../building/aqueduct.png").convert_alpha()
  pipelines_img = pygame.image.load("../building/pipelines.png").convert_alpha()
  img_dict = {"Lumber Hut":lumber_hut_img, "Mine":mine_img, "Shipyard":shipyard_img, "Farm":farm_img, "Plantation":plantation_img, "Foundry":foundry_img, "Aqueduct":aqueduct_img, "Pipelines":pipelines_img}
  def __init__(self, location: Location, stats: Dict, coords: Tuple[int, int], player_number: int):
    self.name = stats["name"]
    super().__init__(player_number, coords, pygame.image.load("../building/"+str(self.name).lower()+".png").convert_alpha())
    #get stats from list
    self.cost = stats["cost"]
    #cost is [wood, metal, food, water]
    self.production = stats["production"]
    self.production_time = stats["production time"]
    self.production_timer = 0
    #production is [wood, metal, food, water]
    #production_time is how many turns it takes for the materials to be produced
    #add them to player resources when end_turn button is clicked
    self.terrain = stats["terrain"]
    #this is a list of the terrain types that the building can be built on
    self.abilities = stats["abilities"]
    #upgrade should be a list of the building stats
    self.upgraded_building = stats["upgraded building"]
    location.building = self
  def produce(self) -> None:
    #this is where the building produces resources
    #run this in the end_turn button clicked
    self.production_timer += 1
    if self.production_timer == self.production_time:
      self.production_timer = 0
      for resource in self.production.keys():
        for animation in range(self.production[resource]):
          dynamics.animation_list.append(resourceAnimation(resource, resourceAnimation.resourceAnimationCoords(self.coords), 25))
  def display_stats(self, x: int, y: int, text_display_size: int = 20) -> None:
    #change these to imgs later
    screen.blit(self.image, (x, y))
    text(text_display_size, str(self.name), (0, 0, 0), x + 37.5, y - 15, alignx = "center")
    screen.blit(production_frame, (x + 85, y - 33))
    text(text_display_size, "Produce ", (0, 0, 0), x + 135, y - 25, alignx = "center")
    display_resources(self.production, x + 125, y)
    screen.blit(Building.cooldown_stat_img, (x - 12.5, y + 75))
    text(text_display_size, str(self.production_timer + 1) + "/" + str(self.production_time) + " turns", (255, 0, 0), x + 12.5, y + 75)
    if self.production_timer + 1 == self.production_time:
      text(text_display_size, str(self.production_timer + 1) + "/" + str(self.production_time) + " turns", (0, 184, 0), x + 12.5, y + 75)
  def upgrade(self, location: Location) -> None:
    #buildings can only be upgraded into one building
    dynamics.player_list[self.player_number].buildings.append(Building(location, self.upgraded_building, self.coords, self.player_number))
    dynamics.selected_object = dynamics.player_list[self.player_number].buildings[-1]
    dynamics.player_list[self.player_number].buildings.remove(self)
  def draw(self, color):
    Map.shadeTile(self.coords, color)
    screen.blit(self.image, (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y))
    pygame.draw.rect(screen, (122, 122, 122), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y + Building.building_size*0.85, Building.building_size, 10))
    pygame.draw.rect(screen, (255, 0, 255), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y + Building.building_size*0.85, Building.building_size*((self.production_timer + 1)/self.production_time), 10))
    #the +1 is for UI ease
    if self.production_timer + 1 == self.production_time:
        pygame.draw.rect(screen, (0, 255, 0), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y + Building.building_size*0.85, Building.building_size, 10))
    for level_counter in range(self.production_time + 1):
        pygame.draw.line(screen, (0, 0, 0), (self.display_coords[0] + dynamics.offset_x + level_counter*(Building.building_size/self.production_time), self.display_coords[1] + dynamics.offset_y + Building.building_size*0.85), (self.display_coords[0] + dynamics.offset_x + level_counter*(Building.building_size/self.production_time), self.display_coords[1] + dynamics.offset_y + Building.building_size*0.85 + 10), 2)
    text(25, str(self.player_number + 1), (255, 255, 255), self.display_coords[0] + dynamics.offset_x + Building.building_size/2, self.display_coords[1] + dynamics.offset_y + Building.building_size/2, alignx = "center", aligny = "center")
  def getConquered(self, player_num: int):
    dynamics.player_list[self.player_number].cities.remove(self)
    self.player_number = player_num
    dynamics.player_list[self.player_number].cities.append(self)