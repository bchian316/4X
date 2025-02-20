import dynamics
from functions import *
from animations import resourceAnimation
class Location:
  plains_img = pygame.image.load("../terrain/plains.png").convert_alpha()
  forest_img = pygame.image.load("../terrain/forest.png").convert_alpha()
  water_img = pygame.image.load("../terrain/water.png").convert_alpha()
  ocean_img = pygame.image.load("../terrain/ocean.png").convert_alpha()
  mountain_img = pygame.image.load("../terrain/mountain.png").convert_alpha()
  dense_forest_img = pygame.image.load("../terrain/dense forest.png").convert_alpha()
  crop_img = pygame.image.load("../terrain/crop.png").convert_alpha()
  img_dict = {"plains":plains_img, "forest":forest_img, "water":water_img, "ocean":ocean_img, "mountain":mountain_img, "dense forest":dense_forest_img, "crop":crop_img}
  mineral_img = pygame.image.load("../terrain/mineral.png").convert_alpha()
  ore_img = pygame.image.load("../terrain/ore.png").convert_alpha()
  deposit_x = 15
  deposit_y = 15
  max_deposits = 5 #max deposits cant exceed this
  deposit_coords = ((30, 40), (10, 25), (60, 40), (25, 15), (40, 60))
  def __init__(self, coords: Tuple[int, int], terrain: str, features: List[str]):
    self.terrain = terrain
    if self.terrain: #if terrain is not a void
      self.image = Location.img_dict[self.terrain]
    self.features = features
    self.coords = coords
    self.display_coords = coordConvert(self.coords, returnCenter = False)
    self.player_acted_on = False
    #these are references to entities that are located on the unit
    self.unit = None
    self.building = None
    self.city = None
    self.deposit = {"wood": 0, "metal": 0, "food": 0, "water": 0}
    if self.terrain == "crop":
      self.deposit["food"] = randint(2, 4)
    elif self.terrain == "forest":
      self.deposit["wood"] = randint(1, 3)
    elif self.terrain == "dense forest":
      self.deposit["wood"] = randint(2, 4)
    elif self.terrain == "mountain":
      self.deposit["metal"] = randint(3, 5)
    elif self.terrain == "water":
      self.deposit["water"] = randint(1, 3)
    elif self.terrain == "ocean":
      self.deposit["water"] = randint(3, 5)

  def display(self) -> None:
    
    coords = (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y)
    
    try:
      screen.blit(self.image, coords)
    except:
      pass
    if "mineral" in self.features:
      screen.blit(Location.mineral_img, coords)
    if "ore" in self.features:
      screen.blit(Location.ore_img, coords)
    if self.deposit != None:
      for resource in self.deposit.keys():
        #resource_type[0] is the x coord, resource is the y coord
        for resource_num in range(self.deposit[resource]):
          screen.blit(resource_imgs[resource], (coords[0] + Location.deposit_coords[resource_num][0], coords[1] + Location.deposit_coords[resource_num][1]))
  def display_stats(self, x, y):
    #do some text for features and name of terrain and stuff
    screen.blit(self.image, (x, y))
    text(20, self.terrain.capitalize(), (0, 0, 0), x + 44, y - 25, alignx="center")
  def give_deposit(self):
    if self.deposit != None:
      for resource in self.deposit.keys():
        for animation in range(self.deposit[resource]):
          dynamics.animation_list.append(resourceAnimation(resource, resourceAnimation.resourceAnimationCoords(self.coords), 25))
      self.deposit = None