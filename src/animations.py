import dynamics
from functions import *

class Animation:
  def __init__(self, start: Tuple[int, int], img: pygame.Surface, img_size: int):
    self.start = start
    self.img = img
    self.img_size = img_size
  def update(self) -> None:
    self.start = (self.start[0] + self.velx, self.start[1] + self.vely)
    try:
      self.distance_traveled += sqrt(self.velx**2 + self.vely**2)
    except:
      pass
    #the blit coords will be where the img center is
    screen.blit(self.img, (self.start[0] - self.img_size/2, self.start[1] - self.img_size/2))
  def destroyAnimation(current_player) -> None:
    deletion_counter = 0
    while deletion_counter < len(dynamics.animation_list):
      #building_type will be a list of a specific building type
      sprite = dynamics.animation_list[deletion_counter]
      if isinstance(sprite, resourceAnimation):
        if rect_collided(sprite.start[0], sprite.start[1], sprite.img_size, sprite.img_size, sprite.target[0], sprite.target[1], sprite.targetsize, sprite.targetsize):
          if(sprite.value == "money"):
            dynamics.player_list[current_player].money += 1
          else:
            dynamics.player_list[current_player].resources[sprite.value] += 1
          dynamics.animation_list.pop(deletion_counter)
          continue
      elif isinstance(sprite, damageAnimation):
        if sprite.distance_traveled >= damageAnimation.max_distance:
          dynamics.animation_list.pop(deletion_counter)
          continue
      deletion_counter += 1
class resourceAnimation(Animation):
  speed_offset = 20 #how many frames it takes for the animation to reach it's destination
  #therefore, the lower the number, the faster the object, and vice versa
  animation_range = 80
  img_size = 25
  img_dict = {"money":money_resource_img, "wood":wood_resource_img, "metal":metal_resource_img, "food":food_resource_img, "water":water_resource_img}
  def __init__(self, value: str, start: Tuple[int, int], target: Tuple[int, int], targetsize: int):
    #value should be a list containing the resource of the thing
    self.value = value
    self.img = resourceAnimation.img_dict[self.value]
    super().__init__(start, self.img, resourceAnimation.img_size)
    self.target = target
    self.targetsize = targetsize
    #make velocity inversely proportional to distance, so if the animation starts farther away, it travels faster
    self.velx, self.vely = get_vel(self.start[0], self.start[1], self.target[0], self.target[1], (sqrt((self.start[0]-self.target[0])**2 + (self.start[1]-self.target[1])**2))/resourceAnimation.speed_offset)
  def resourceAnimationCoords(coords: Tuple[int, int], random_range: int = animation_range) -> Tuple[int, int]:
    centers = coordConvert(coords, returnCenter=True)
    return (randint(round(centers[0] + dynamics.offset_x - resourceAnimation.img_size/2 - random_range/2), round(centers[0] + dynamics.offset_x - resourceAnimation.img_size/2 + random_range/2)), randint(round(centers[1] + dynamics.offset_y - resourceAnimation.img_size/2 - random_range/2), round(centers[1] + dynamics.offset_y - resourceAnimation.img_size/2 + random_range/2)))
class damageAnimation(Animation):
  sprite_speed = 6
  max_distance = 100
  img = pygame.image.load("../stats/health.png").convert_alpha()
  img_size = 25
  def __init__(self, start: Tuple[int, int]):
    super().__init__(start, damageAnimation.img, damageAnimation.img_size)
    self.velx, self.vely = pygame.math.Vector2(0, damageAnimation.sprite_speed).rotate(randint(0, 360))
    self.distance_traveled = 0
class attackAnimation(Animation):
  sprite_speed = 10
  size = 50
  def __init__(self, start: Tuple[int, int], img: pygame.Surface, end: Tuple[int, int]):
    super().__init__(start, attackAnimation.size)