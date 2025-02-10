from functions import *
#import Entity constructor anytime u are using a child class of Entity
class Entity:
  def __init__(self, player_number: int, coords: Tuple[int, int], img: pygame.Surface):
    #Entities are things owned by players
    self.player_number = player_number
    self.coords = coords
    self.image = img
    self.img_size = self.image.get_height() #we only need one number bc all images are squares
    self.display_coords = coordConvert(self.coords, allocateSize = self.img_size)
  def owned_by_current_player(self) -> bool:
    return dynamics.current_player == self.player_number