import dynamics
from entity import *
from map import *
from animations import resourceAnimation
class City(Entity):
  #building constructor
  #buildings can only be built where a unit of the same player is
  #buildings are destroyed when other player units move on top of it
  city_size = 75
  max_level = 5
  cooldown_img = pygame.image.load("../stats/timer.png").convert_alpha()
  upgrade_img = pygame.image.load("../city/upgrade.png").convert_alpha()
  def __init__(self, location: Location, coords: Tuple[int, int], player_number: int, level: int = 1):
    self.level = level
    super().__init__(player_number, coords, pygame.image.load("../city/"+str(self.level)+".png").convert_alpha())
    self.income = self.level * 5
    self.cost = {"wood": self.level**2, "metal": self.level**2, "food": self.level**2, "water": self.level**2}
    #prevent unit spamming
    self.spawn_timer = 0
    self.max_spawn_timer = self.level * 10
    location.city = self
  def produce(self) -> None:
    #this is where the city produces money
    #run this in the end_turn button clicked
    #add for loop for animation
    for _ in range(self.income):
      dynamics.animation_list.append(resourceAnimation("money", resourceAnimation.resourceAnimationCoords(self.coords), 25))
  def upgrade(self) -> None:
    self.level += 1
    self.income = self.level * 5
    dynamics.player_list[self.player_number].deduct_costs(self.cost)
    self.cost = {"wood": self.level**2, "metal": self.level**2, "food": self.level**2, "water": self.level**2}
    self.max_spawn_timer = self.level * 10
    self.image = pygame.image.load("../city/"+str(self.level)+".png").convert_alpha()
  def display_stats(self, x: int, y: int, text_display_size: int = 20) -> None:
    screen.blit(self.image, (x, y))
    if self.level > 0:
      text(text_display_size, "Level " + str(self.level), (0, 0, 0), x + 75, y - 12.5, alignx= "center")
      screen.blit(money_resource_img, (x + 75, y + 7.5))
      text(20, str(self.income), money_color, x + 112.5, y + 15)
      screen.blit(City.cooldown_img, (x + 75, y + 37.5))
      text(text_display_size, str(self.spawn_timer) + "/" + str(self.max_spawn_timer), (0, 255, 0), x + 112.5, y + 42.5)
      if self.spawn_timer >= self.max_spawn_timer:
        #spawn timer is full and can't make any more units (draw on top of green letters)
        text(text_display_size, str(self.spawn_timer) + "/" + str(self.max_spawn_timer), (255, 0, 0), x + 112.5, y + 42.5)
    else:
      text(30, "Village", (0, 0, 0), x, y, alignx= "center")
  def draw(self, color = None):
    if color != None:
      #city is owned (not a village)
      Map.shadeTile(self.coords, color)
      pygame.draw.rect(screen, (0, 255, 0), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y + City.city_size*0.85, City.city_size, 10))
      pygame.draw.rect(screen, (0, 0, 255), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y + City.city_size*0.85, City.city_size*(self.spawn_timer/self.max_spawn_timer), 10))
      if self.spawn_timer >= self.max_spawn_timer:
          pygame.draw.rect(screen, (255, 0, 0), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y + City.city_size*0.85, City.city_size*(self.spawn_timer/self.max_spawn_timer), 10))
      for level_counter in range(self.level + 1):
          pygame.draw.line(screen, (0, 0, 0), (self.display_coords[0] + dynamics.offset_x + level_counter*(City.city_size/self.level), self.display_coords[1] + dynamics.offset_y + City.city_size*0.85), (self.display_coords[0] + dynamics.offset_x + level_counter*(City.city_size/self.level), self.display_coords[1] + dynamics.offset_y + City.city_size*0.85 + 10), 2)
    screen.blit(self.image, (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y))
  def getConquered(self, player_num: int):
    print("got to getconquered")
    dynamics.player_list[player_num].cities.append(self) #add to player who conquered it
    if self.player_number != -1:#city was previously owned by someone
      print("city converting")
      dynamics.player_list[self.player_number].cities.remove(self)
      print("city converted")
    else:#upgrade village into city
      dynamics.villages.remove(self)
      self.upgrade()
    self.player_number = player_num
    