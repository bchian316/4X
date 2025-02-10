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
  fertile_land_img = pygame.image.load("../terrain/fertile land.png").convert_alpha()
  img_dict = {"plains":plains_img, "forest":forest_img, "water":water_img, "ocean":ocean_img, "mountain":mountain_img, "dense forest":dense_forest_img}
  crop_img = pygame.image.load("../terrain/crop.png").convert_alpha()
  harvested_crop_img = pygame.image.load("../terrain/harvested crop.png").convert_alpha()
  mineral_img = pygame.image.load("../terrain/mineral.png").convert_alpha()
  ore_img = pygame.image.load("../terrain/ore.png").convert_alpha()
  village_img = pygame.image.load("../terrain/village.png").convert_alpha()
  deposit_x = 15
  deposit_y = 15
  def __init__(self, coords: Tuple[int, int], terrain: str, features: List[str], deposit: Tuple[int, int, int, int]):
    self.terrain = terrain
    if self.terrain: #if terrain is not a void
      self.image = Location.img_dict[self.terrain]
    self.features = features
    self.coords = coords
    self.display_coords = coordConvert(self.coords, returnCenter = False)
    self.deposit = deposit

  def display(self) -> None:
    
    coords = (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y)
    
    try:
      screen.blit(self.image, coords)
    except:
      pass
    if "crop" in self.features:
      screen.blit(Location.crop_img, coords)
    elif "harvested crop" in self.features:
      screen.blit(Location.harvested_crop_img, coords)
    if "mineral" in self.features:
      screen.blit(Location.mineral_img, coords)
    if "ore" in self.features:
      screen.blit(Location.ore_img, coords)
    for resource_type in enumerate(self.deposit):
      #resource_type[0] is the x coord, resource is the y coord
      for resource in range(resource_type[1]):
        if resource_type[0] == 0:
          screen.blit(wood_resource_img, (coords[0] + resource_type[0]*Location.deposit_x + 15, coords[1] + ((hex_size/2)*sqrt(3))/2 + resource*Location.deposit_y - resource_type[1]*Location.deposit_y/2))
        elif resource_type[0] == 1:
          screen.blit(metal_resource_img, (coords[0] + resource_type[0]*Location.deposit_x + 15, coords[1] + ((hex_size/2)*sqrt(3))/2 + resource*Location.deposit_y - resource_type[1]*Location.deposit_y/2))
        elif resource_type[0] == 2:
          screen.blit(food_resource_img, (coords[0] + resource_type[0]*Location.deposit_x + 15, coords[1] + ((hex_size/2)*sqrt(3))/2 + resource*Location.deposit_y - resource_type[1]*Location.deposit_y/2))
        elif resource_type[0] == 3:
          screen.blit(water_resource_img, (coords[0] + resource_type[0]*Location.deposit_x + 15, coords[1] + ((hex_size/2)*sqrt(3))/2 + resource*Location.deposit_y - resource_type[1]*Location.deposit_y/2))
  def display_stats(self, x, y):
    #do some text for features and name of terrain and stuff
    screen.blit(self.image, (x, y))
    text(20, self.terrain.capitalize(), (0, 0, 0), x + 44, y - 25, alignx="center")
  def give_deposit(self):
    if self.deposit != (0, 0, 0, 0):
      animation_coords = coordConvert(self.coords, returnCenter=True)
      for _ in range(self.deposit[0]):
        dynamics.animation_list.append(resourceAnimation("wood", resourceAnimation.resourceAnimationCoords(self.coords), (SCREENLENGTH - 12.5, 87.5), 25))
      for _ in range(self.deposit[1]):
        dynamics.animation_list.append(resourceAnimation("metal", resourceAnimation.resourceAnimationCoords(self.coords), (SCREENLENGTH - 12.5, 112.5), 25))
      for _ in range(self.deposit[2]):
        dynamics.animation_list.append(resourceAnimation("food", resourceAnimation.resourceAnimationCoords(self.coords), (SCREENLENGTH - 12.5, 137.5), 25))
      for _ in range(self.deposit[3]):
        dynamics.animation_list.append(resourceAnimation("water", resourceAnimation.resourceAnimationCoords(self.coords), (SCREENLENGTH - 12.5, 162.5), 25))
      
      self.deposit = (0, 0, 0, 0)
  def display_map_hex(map: List[List['Location']]) -> None:
    #use offsets to move the entire map around
    for row in map:
      for tile in row:
        #coords[0] and coords[1] are the coordinates of the tile in the map, not the screen blit coords
        #the map is a list of lists, so the first list is the first row, the second list is the second row
        #the first item in the list is the first tile, the second item is the second tile, etc.
        #display_coords[0] and display_coords[1] will be the screen blit coords of the tile
        tile.display()

  def return_Adjacent_hex(coords: Tuple[int, int]) -> List[Tuple[int, int]]:
    #returns a list of all the adjacent hexes based on one hex
    #the items returned are x and y coords to be used on the map
    return [(coords[0]-1, coords[1]-1), (coords[0], coords[1]-1), (coords[0]-1, coords[1]), (coords[0]+1, coords[1]), (coords[0], coords[1]+1), (coords[0]+1, coords[1]+1)]
    #adjacent_hexes has the coordinates of all the adjacent hexes, not their terrain stuff
    #u can call the terrain manually

  def shadeTile(coords: Tuple[int, int], color: Tuple[int, int, int]) -> None:
    #coords[0] and coords[1] are coordinates, not display coordinates
    center_x = (coords[1] - 1)*(-hex_size/4)*sqrt(3)
    center_y = (coords[1] - 1)*(hex_size*0.75)
    center_x += (coords[0] - 1)*(hex_size/2)*sqrt(3)
    #allocate for image size (off of hex_side)
    center_x += ((hex_size/2)*sqrt(3))/2
    center_y += hex_size/2
    #add offsets
    center_x += dynamics.offset_x
    center_y += dynamics.offset_y
    #(display_coords[0], display_coords[1]) will be the center of the corresponding hex
    #points go clockwise from the top-left vertex
    point1 = (center_x - hex_size*sqrt(3)/4, center_y - hex_size/4)
    point2 = (center_x, center_y - hex_size/2)
    point3 = (center_x + hex_size*sqrt(3)/4, center_y - hex_size/4)
    point4 = (center_x + hex_size*sqrt(3)/4, center_y + hex_size/4)
    point5 = (center_x, center_y + hex_size/2)
    point6 = (center_x - hex_size*sqrt(3)/4, center_y + hex_size/4)
    pygame.draw.polygon(transparent_screen, color, [point1, point2, point3, point4, point5, point6])
  def configure_map() -> None:
    #set or reset map (just in case we need to reset entire map for some reason)
    MAP.clear()
    for row in enumerate(TERRAIN):
      coordy = row[0]
      MAP.append([])
      for tile in enumerate(row[1]):
        coordx = tile[0]
        features = []
        if (coordx, coordy) in CROP:
          features.append("crop")
        if (coordx, coordy) in HARVESTED_CROP:
          features.append("harvested crop")
        if (coordx, coordy) in MINERAL:
          features.append("mineral")
        if (coordx, coordy) in ORE:
          features.append("ore")
        if randint(1, 10) == 1 and tile[1] != "":
          deposit = (randint(0, 5), randint(0, 5), randint(0, 5), randint(0, 5))
        else:
          deposit = (0, 0, 0, 0)
        MAP[coordy].append(Location((coordx, coordy), tile[1], features, deposit))
  def in_map(tile: Tuple[int, int]) -> bool:
    if tile[0] >= 0 and tile[0] <= MAP_LENGTH and tile[1] >= 0 and tile[1] <= MAP_LENGTH and dynamics.MAP[tile[1]][tile[0]].terrain != "":
      return True
    return False
  def in_terrain(tile: Tuple[int, int], available: List[str]) -> bool:
    if MAP[tile[1]][tile[0]].terrain in available:
      return True
    return False