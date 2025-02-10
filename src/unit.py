import dynamics
from entity import *
from location import Location
from animations import damageAnimation
class Unit(Entity):
  #unit constructor
  health_stat_img = pygame.image.load("../stats/health.png").convert_alpha()
  attack_stat_img = pygame.image.load("../stats/attack.png").convert_alpha()
  defense_stat_img = pygame.image.load("../stats/defense.png").convert_alpha()
  range_stat_img = pygame.image.load("../stats/range.png").convert_alpha()
  movement_stat_img = pygame.image.load("../stats/movement.png").convert_alpha()
  unit_size = 50
  man_img = pygame.image.load("../unit/man.png").convert_alpha()
  rider_img = pygame.image.load("../unit/rider.png").convert_alpha()
  knight_img = pygame.image.load("../unit/knight.png").convert_alpha()
  elephant_img = pygame.image.load("../unit/elephant.png").convert_alpha()
  swordsman_img = pygame.image.load("../unit/swordsman.png").convert_alpha()
  spearman_img = pygame.image.load("../unit/spearman.png").convert_alpha()
  axeman_img = pygame.image.load("../unit/axeman.png").convert_alpha()
  shieldman_img = pygame.image.load("../unit/shieldman.png").convert_alpha()
  archer_img = pygame.image.load("../unit/archer.png").convert_alpha()
  crossbowman_img = pygame.image.load("../unit/crossbowman.png").convert_alpha()
  field_medic_img = pygame.image.load("../unit/field medic.png").convert_alpha()
  ship_img = pygame.image.load("../unit/ship.png").convert_alpha()
  steeler_img = pygame.image.load("../unit/steeler.png").convert_alpha()
  unit_max_stack = 3
  img_dict = {"Man":man_img, "Rider":rider_img, "Knight":knight_img, "Elephant":elephant_img, "Swordsman":swordsman_img, "Spearman":spearman_img, "Axeman":axeman_img, "Shieldman":shieldman_img, "Archer":archer_img, "Crossbowman":crossbowman_img, "Field Medic":field_medic_img, "Ship":ship_img, "Steeler":steeler_img}
  def __init__(self, stats: List[Any], coords: Tuple[int, int], player_number, current_health: int = 0):
    self.name = stats[0]
    super().__init__(player_number, coords, pygame.image.load("../unit/"+str(self.name).lower()+".png").convert_alpha())
    #get stats from list
    if current_health != 0:
      self.health = current_health
    else:
      self.health = stats[1]
    self.max_health = stats[1]
    self.regen_value = stats[2]
    self.attack = stats[3]
    self.defense = stats[4]
    self.range = stats[5]
    self.movement = stats[6]
    self.cost = stats[7]
    #cost is [wood, metal, food, water]
    self.timer = stats[8]
    self.action_sequences = stats[9]
    self.abilities = stats[10]
    #all image names should be unit name + .png eg. man.png
    self.turn_done = False
    self.action_sequence = []
    self.action = None
    self.action_index = 0
    #action_index starts at 0
    self.action_range = [self.coords]
    #moverange is a list of all the adjacent hexes that the unit can be moved to
  def unit_reset(self) -> None: #always reset self.action_range to [self.coords]
    self.action = None
    self.action_index = -1
    self.action_sequence = []
    self.action_range = [self.coords]
    self.turn_done = True
  def next_action(self) -> None:
    try:
      self.action_index += 1
      self.action = self.action_sequence[self.action_index] #if there is an error here, jump to the except
      self.calculate_action_range()
    except IndexError:
      self.unit_reset()
  def calculate_damage(self, defender: 'Unit') -> int:
    attack_damage = (self.health/self.max_health)*self.attack
    defend_damage = (defender.health/defender.max_health)*defender.defense
    #3 will affect the general damage of all attacks
    #attack_damage *= 3
    #no damage scaler
    damage = attack_damage/defend_damage
    if damage < 0:
      damage = 0
    return round(damage)
  def do_action(self, object: Any) -> None:
    #calculate the ranges in calculate_action_range, and actually do the action here
    if self.action == "move" and type(object) == Location:
      #action is a movement order
      #self.action is the number of maximum hexes to move

      if object.coords in self.action_range:
        #location is within movement range and is not occupied
        print("successful move")
        self.coords = deepcopy(object.coords)
        self.display_coords = coordConvert(self.coords, allocateSize = self.img_size)
        MAP[self.coords[1]][self.coords[0]].give_deposit()
        if(return_occupied(self.coords, "building")):
          return_occupied(self.coords, "building").getConquered(self.player_number)
        elif(return_occupied(self.coords, "city")):
          return_occupied(self.coords, "city").getConquered(self.player_number)
        #the move is valid, so we move on to the next action
        self.next_action()

    elif self.action == "attack" and type(object) == Unit and not object.owned_by_current_player():
      # if the action is an attack and the targeted unit exists and the targeted unit does not belong to the current player (no friendly fire)
      #action is a attack order
      #self.action is the number of maximum hexes to move
      #self.action_range will only contain the hexes of the available targeted units, unlike during movement, self.action_range will contain all the hexes within the movement range

      if object.coords in self.action_range:
        print("successful attack", type(object))
        #the attack is valid, so we move on to the next action
        for counter in range(self.calculate_damage(object)):
          dynamics.animation_list.append(damageAnimation((object.display_coords[0] + Unit.unit_size/2 + dynamics.offset_x - damageAnimation.img_size/2, object.display_coords[1] + Unit.unit_size/2 + dynamics.offset_y - damageAnimation.img_size/2)))
          print("animation created")
        #make the targeted_unit lose health
        object.health -= self.calculate_damage(object)
        if object.health <= 0:
          dynamics.player_list[object.player_number].units.remove(object) #kill unit
        self.next_action()
    elif self.action == "heal" and object == self:
      #action is a heal order

      self.health += self.regen_value
      #no going over max health
      if self.health > self.max_health:
        self.health = self.max_health
      print("successful heal")
      self.next_action()
    elif self.action == "heal other" and type(object) == Unit and object.owned_by_current_player():
      object.health += object.regen_value
      if object.health > object.max_health:
        object.health = object.max_health
      print("successful heal other")
      self.next_action()

    #move on to next action
  def calculate_action_range(self) -> None:
    #display the hints for the unit
    #this also calculates the action ranges for the units, not during do_action
    self.action_range = [self.coords]
    if self.action == "move":
      #set the available terrain as only water and ocean
      #available terrain has no effect on float units; they have a terrain of ocean and water
      if "float" in self.abilities:
        available_terrain_placeholder = dynamics.player_list[self.player_number].available_terrain
        dynamics.player_list[self.player_number].available_terrain = ["water", "ocean"]
      for counter in range(self.movement):
        #this next for loop extends self.movement_range by 1 hex in every direction
        #movement_tile is already in the range (we dont have to check terrain and map restrictions), extended_tile is not
        for movement_tile in deepcopy(self.action_range): #try to extend each tile
          for extended_tile in Location.return_Adjacent_hex(movement_tile): #extend movement_tile
            if extended_tile not in self.action_range and not return_occupied(extended_tile, object = "unit"):
              #remove duplicates and places occupied by other ppl
              if Location.in_map(extended_tile) and Location.in_terrain(extended_tile, dynamics.player_list[self.player_number].available_terrain):
                self.action_range.append(extended_tile)
      if "float" in self.abilities:
        #reset terrain for float units
        dynamics.player_list[self.player_number].available_terrain = available_terrain_placeholder
        del(available_terrain_placeholder)
      self.action_range.remove(self.coords)
      #display hints to show the possible move locations
    elif self.action == "attack":
      for counter in range(self.range):
        for movement_tile in deepcopy(self.action_range):
          self.action_range.extend(Location.return_Adjacent_hex(movement_tile))
      counter = 0
      while counter < len(self.action_range):
        if not return_occupied(self.action_range[counter], object = "unit") or return_occupied(self.action_range[counter], object = "unit") in dynamics.player_list[self.player_number].units:
          #if there is no dude there or you own the dude
          self.action_range.pop(counter)
          continue
        counter += 1
    elif self.action == "heal":
      pass
    elif self.action == "heal other":
      for counter in range(self.range):
        for movement_tile in (self.action_range):
          self.action_range.extend(Location.return_Adjacent_hex(movement_tile))
      counter = 0
      while counter < len(self.action_range):
        if not return_occupied(self.action_range[counter], object = "unit") or return_occupied(self.action_range[counter], object = "unit") not in dynamics.player_list[self.player_number].units:
          #if there is no dude there or you DON'T own the dude
          self.action_range.pop(counter)
          continue
        counter += 1

  def display_stats(self, x: int, y: int, text_display_size: int = 20) -> None:
    #x and y should be unit display coords
    screen.blit(self.image, (x + 37.5, y + 12.5))
    #name shown above the unit
    text(text_display_size, str(self.name), (0, 0, 0), x + 62.5, y, alignx = "center", aligny = "center")
    #health and regen value shown underneath the unit
    screen.blit(Unit.health_stat_img, (x + 12.5, y + 62.5))
    text(text_display_size, str(self.health) + "/" + str(self.max_health) + " (+" + str(self.regen_value) + ")", (255, 0, 140), x + 37.5, y + 62.5)
    #attack and defense shown left of the unit
    screen.blit(Unit.attack_stat_img, (x + 12.5, y + 12.5))
    text(text_display_size, str(self.attack), (0, 0, 0), x, y + 25, alignx = "center", aligny = "center")
    screen.blit(Unit.defense_stat_img, (x + 12.5, y + 37.5))
    text(text_display_size, str(self.defense), (0, 0, 0), x, y + 50, alignx = "center", aligny = "center")
    #range and movement shown right of the unit
    screen.blit(Unit.range_stat_img, (x + 87.5, y + 12.5))
    text(text_display_size, str(self.range), (0, 0, 0), x + 125, y + 25, alignx = "center", aligny = "center")
    screen.blit(Unit.movement_stat_img, (x + 87.5, y + 37.5))
    text(text_display_size, str(self.movement), (0, 0, 0), x + 125, y + 50, alignx = "center", aligny = "center")
  def draw(self, color, availability_marker_size):
    Location.shadeTile(self.coords, color)
    screen.blit(self.image, (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y))
    #this will display a text version of the unit health: text(25, str(self.health) + "/" + str(self.max_health), (255, 0, 0), self.display_coords[0] + unit_size + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y)
    #health bar:
    pygame.draw.rect(screen, (255, 0, 0), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y - 12.5, Unit.unit_size, 10))
    pygame.draw.rect(screen, (0, 255, 0), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y - 12.5, Unit.unit_size*(self.health/self.max_health), 10))
    text(15, str(self.health) + "/" + str(self.max_health), (0, 0, 0), self.display_coords[0] + dynamics.offset_x + Unit.unit_size/2, self.display_coords[1] + dynamics.offset_y - 7.5, alignx = "center", aligny = "center")
    #text(25, str(self.player_number + 1), (255, 255, 255), self.display_coords[0] + dynamics.offset_x + Unit.unit_size/2, self.display_coords[1] + dynamics.offset_y + Unit.unit_size/2, alignx = "center", aligny = "center")
    if self.player_number == dynamics.current_player:
        pygame.draw.circle(screen, (255, 0, 0), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y), availability_marker_size)
    if not self.turn_done:
        pygame.draw.circle(screen, (0, 255, 0), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y), availability_marker_size)
    else:
        pygame.draw.circle(screen, (125, 125, 125), (self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y), availability_marker_size)
    text(30, str(self.player_number + 1), (0, 0, 0), self.display_coords[0] + dynamics.offset_x, self.display_coords[1] + dynamics.offset_y, alignx = "center", aligny = "center")