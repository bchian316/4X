# if there's a weird bug, try switching the for loop iterable variable from _ to something else
#maybe that'll help
#if action_sequence is [], turn_done is false
'''REMINDER:
WHENEVER THE PLAYER DOES SOMETHING THAT CAN CHANGE A UNIT's ACTION RANGE, MAKE SURE YOU RESET THE UNIT
SO THE PLAYER HAS TO RECLICK ON THE SAME UNIT
- THEREFORE, YOU RESET THE ACTION_RANGE SO THE UNIT CAN GET THE UPDATED ACTION_RANGE INSTEAD OF THE
ACTION_RANGE STAYING THE SAME
WHENEVER CALLING unit.display_coords, YOU MUST ADD dynamics.offset_x or dynamics.offset_y TO GET THE TRUE BLIT COORDS
display_map_hex takes up a lot of processing power
with it, fps < 10
without is, fps > 30
'''


'''
TODO:
- DO THIS FIRST: 
- calibrate damage formula
- make more images for different units
ADVANCED (save for later):
- decide on this: should other players be able to see the production of foreign buildings and the cooldown of foreign cities?
'''
import dynamics
from functions import *
from stats import all_techs
from tech import Tech
from animations import Animation
from location import Location
from map import Map
from player import Player
from unit import Unit
from building import Building
from city import City

#when using pygame.transform for any pygame.Surface object (image), the image will be a little distorted after each transformation, so keep a variable set to the original undistorted image and use that image to transform the actual image so it will only be distorted once after each transformation, rather than all the transformations adding up to decay the image very fast
#only use this procedure for images that undergo pygame.transform.rotate/scale/etc 
#for images that that don't undergo these transformations, use the original image as the image to transform to save code length

#break
print(pygame.font.get_fonts())
#good fonts: harrington, 

MAP = Map()
MAP.configure_map()

def receive_input(class_object: type) -> Any:
  #run through all objects that can be clicked on based on given type
  #can only receive input if user hasn't clicked on anything yet (dynamics.btn_pressed_this_frame == False)
  if dynamics.mouse_clicked and dynamics.btn_pressed_this_frame == False:
    if class_object == Unit:
      for player in dynamics.player_list:
        for unit in player.units:
          if circle_collided(dynamics.mouse_pos[0], dynamics.mouse_pos[1], 1, unit.display_coords[0] + Unit.unit_size/2 + dynamics.offset_x, unit.display_coords[1] + Unit.unit_size/2 + dynamics.offset_y, selected_collision_range/2):
            dynamics.btn_pressed_this_frame = True
            return unit
    elif class_object == Building:
      for player in dynamics.player_list:
        for building in player.buildings:
          if circle_collided(dynamics.mouse_pos[0], dynamics.mouse_pos[1], 1, building.display_coords[0] + Building.building_size/2 + dynamics.offset_x, building.display_coords[1] + Building.building_size/2 + dynamics.offset_y, selected_collision_range/2):
            dynamics.btn_pressed_this_frame = True
            return building
    elif class_object == City:
      for player in dynamics.player_list:
        for city in player.cities:
          if circle_collided(dynamics.mouse_pos[0], dynamics.mouse_pos[1], 1, city.display_coords[0] + City.city_size/2 + dynamics.offset_x, city.display_coords[1] + City.city_size/2 + dynamics.offset_y, selected_collision_range/2):
            dynamics.btn_pressed_this_frame = True
            return city
    elif class_object == Location:
      for row in MAP.map:
        for tile in row:
          if circle_collided(dynamics.mouse_pos[0], dynamics.mouse_pos[1], 1, tile.display_coords[0] + dynamics.offset_x + hex_size*sqrt(3)/4, tile.display_coords[1] + dynamics.offset_y + hex_size/2, selected_collision_range/2):
            if MAP.in_map(tile.coords):
              dynamics.btn_pressed_this_frame = True
              return tile
  return None
selection_order = [Unit, Building, City, Location, type(None)]
def alternate_selection(object) -> Any:
  #this alternates the parameter object
  for object_type in selection_order[selection_order.index(type(object))+1:]:#check the after types
    if object_type == Unit:
      if MAP.return_tile(object.coords).unit:
        return MAP.return_tile(object.coords).unit
    elif object_type == Building:
      if MAP.return_tile(object.coords).building:
        return MAP.return_tile(object.coords).building
    elif object_type == City:
      if MAP.return_tile(object.coords).city:
        return MAP.return_tile(object.coords).city
    elif object_type == Location:
      return MAP.return_tile(object.coords)
    elif object_type == None:
      return None


def upgrade_to_naval(old_unit: Unit, new_unit: Unit) -> Unit:
  #old and new unit should be unit objects
  #health and regen rates don't change
  new_unit.attack = round(new_unit.attack * old_unit.attack)
  new_unit.defense = round(new_unit.defense * old_unit.defense)
  new_unit.movement += old_unit.movement
  new_unit.range += old_unit.range
  return new_unit


#change player_count to alter the number of players
#player_count is the number of players
player_count = 2
for _ in range(player_count):
  dynamics.player_list.append(Player(_))
current_player = dynamics.player_list[dynamics.current_player]
#starts at 0, so the first player is player 0
#taking that.units is taking that player's units list

dynamics.player_list[0].color = (0, 255, 255)
dynamics.player_list[1].color = (255, 0, 0)

#add starting cities
dynamics.player_list[0].cities.append(City(MAP.return_tile((4, 1)), (4, 1), 0))
dynamics.player_list[1].cities.append(City(MAP.return_tile((9, 10)), (9, 10), 1))
for v in VILLAGES:
  dynamics.villages.append(City(MAP.return_tile(v), v, -1, 0))

#delete later
from stats import man
dynamics.player_list[0].units.append(Unit(MAP.return_tile((11, 11)), man, (11, 11), 0))

while True:
  while dynamics.status == "home":
    screen.fill((255, 255, 255, 255))
    pressed_keys = pygame.key.get_pressed()
    dynamics.mouse_pos = pygame.mouse.get_pos()
    dynamics.btn_pressed_this_frame = False
    dynamics.mouse_clicked = False
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_x:
          pygame.quit()
          sys.exit()
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        #you can only click if there is no animation
        dynamics.mouse_clicked = True
    if button(400, 450, 200, 100, 10):
      dynamics.status = "playing"
      current_player = dynamics.player_list[dynamics.current_player]
      #current_player.turn_update()
      #this allows Player1 to get his resources, since you only get resources when the player before you ends turn
      #this makes it equal
      #or we can take this line away because player1 already has advantage of going first, so maybe he shouldn't get resources
      
    clock.tick(FPS)
    pygame.display.update()

  while dynamics.status == "playing":
    screen.fill((255, 255, 255))
    transparent_screen.fill((255, 255, 255, 0))
    pressed_keys = pygame.key.get_pressed()
    dynamics.mouse_pos = pygame.mouse.get_pos()
    dynamics.mouse_clicked = False
    #remember to reset this variable so buttons and selections aren't activated at the same time
    dynamics.btn_pressed_this_frame = False
    dynamics.animating = False
    if dynamics.animation_list != []:
      dynamics.animating = True

    #player input
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN and not dynamics.animating:
        dynamics.mouse_clicked = True

    #move the screen around by arrow keys
    if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
      dynamics.offset_y += 10
    if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
      dynamics.offset_y -= 10
    if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
      dynamics.offset_x += 10
    if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
      dynamics.offset_x -= 10

    '''display order:
    map
    cities/buildings
    units
    hints
    selection icons
    frames
    detailed view of selected object
    buttons/options: (units sequences, buildings, buildings upgrades, city upgrades, player actions, etc)'''

    #display map
    MAP.display_map_hex()

    #display all units, buildings, cities of each player
    for a_player in dynamics.player_list:
      a_player.update()
    #even though all player units are displayed, make it so only the units belonging to dynamics.current_player are controlled
    #display all unowned cities
    for village in dynamics.villages:
      village.draw(None)

    
    #display selection icons
    if dynamics.selected_object != None:
      if isinstance(dynamics.selected_object, Unit):
        screen.blit(unit_select_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
        if not dynamics.selected_object.owned_by_current_player():
          screen.blit(foreign_unit_select_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
      elif isinstance(dynamics.selected_object, Building):
        screen.blit(building_select_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
        if not dynamics.selected_object.owned_by_current_player():
          #if player does not own the building, draw the unowned icon above the regular icon
          screen.blit(foreign_building_select_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
      elif isinstance(dynamics.selected_object, City):
        screen.blit(building_select_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
        if not dynamics.selected_object.owned_by_current_player():
          screen.blit(foreign_building_select_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
      elif isinstance(dynamics.selected_object, Location):
        screen.blit(location_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
        if dynamics.selected_object.unit and dynamics.selected_object.unit.owned_by_current_player():
          screen.blit(location_select_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
          if not dynamics.selected_object.player_acted_on:
            screen.blit(unit_location_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
        elif dynamics.selected_object.building and dynamics.selected_object.building.owned_by_current_player():
          screen.blit(location_select_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))
        elif dynamics.selected_object.city and dynamics.selected_object.city.owned_by_current_player():
          screen.blit(location_select_img, (dynamics.selected_object.display_coords[0] + dynamics.offset_x, dynamics.selected_object.display_coords[1] + dynamics.offset_y))

    #create a rect area for selected, targeted, and location
    screen.blit(selection_frame, (0, 0))
    #display selected object
    text(20, "Selected:", (0, 0, 255), 0, 50)
    #displaying the selected object stats at the corner of screen depending on what it is
    if dynamics.selected_object != None:
      dynamics.selected_object.display_stats(12.5, 87.5)

    #butons

    if button(50, 0, 100, 50, 10):
      dynamics.offset_x = 250
      dynamics.offset_y = 0

    if button(375, 0, 100, 50, 10):
      dynamics.status = "tech tree"
    text(30, "Tech", (0, 0, 0), 425, 25, alignx = "center", aligny = "center")
    

    if button(SCREENLENGTH - 100, SCREENHEIGHT - 125, 100, 100, 10):
      #if end_turn button is clicked
      dynamics.selected_object = None
      current_player.turn_update_after()
      dynamics.current_player += 1
      if dynamics.current_player == player_count:
        dynamics.current_player = 0
      current_player = dynamics.player_list[dynamics.current_player]
      print("turn ended... moving on to player", dynamics.current_player)
      current_player.turn_update_before()
      MAP.turn_reset()
    text(25, "End Turn", (0, 0, 0), SCREENLENGTH - 50, SCREENHEIGHT - 75, alignx = "center", aligny = "center")

    #display player_number
    text(25, str("Player " + str(dynamics.current_player + 1)) + " turn", current_player.color, SCREENLENGTH, 0, alignx = "right")
    display_resources([current_player.money, current_player.wood, current_player.metal, current_player.food, current_player.water], SCREENLENGTH - 25, 50, display_all = True, size = 40)

    #can only choose unit sequence or do actions if unit turn is not over
    if isinstance(dynamics.selected_object, Unit) and dynamics.selected_object.owned_by_current_player() and not dynamics.selected_object.turn_done:
      #if u own the selected unit and his turn isn't done
      if dynamics.selected_object.action_sequence == []:
        #if an action sequence is not chosen yet
        for choice in enumerate(dynamics.selected_object.action_sequences):
          if button(0, option_x + choice[0] * 50, len(choice[1]) * small_icon_size, 50, 10):
            dynamics.selected_object.action_sequence = choice[1]
            #dynamics.selected_object.action = dynamics.selected_object.action_sequence[0]
            dynamics.selected_object.action_index = -1
            dynamics.selected_object.action_range = [dynamics.selected_object.coords]
            dynamics.selected_object.next_action(MAP)
            print(dynamics.selected_object.action_sequence)
            break
          display_action_sequence(choice[1], -1, 0, option_x + choice[0] * 50, mini = True)
      if dynamics.selected_object.action != None:
        #if an action is chosen, display hints
        for hint in dynamics.selected_object.action_range:
          hint_x, hint_y = coordConvert(hint)
          pygame.draw.circle(screen, (255, 255, 0), (hint_x + dynamics.offset_x, hint_y + dynamics.offset_y), 10)
        display_action_sequence(dynamics.selected_object.action_sequence, dynamics.selected_object.action_index, 0, 300)
        if dynamics.selected_object.action == "move":
          dynamics.selected_object.do_action(receive_input(Location), MAP)
        elif dynamics.selected_object.action == "attack":
          dynamics.selected_object.do_action(receive_input(Unit), MAP)
        elif dynamics.selected_object.action == "heal":
          dynamics.selected_object.do_action(receive_input(Unit), MAP)
        elif dynamics.selected_object.action == "heal other":
          dynamics.selected_object.do_action(receive_input(Unit), MAP)
        if button(25, 175, 125, 125, 10):
          dynamics.selected_object.next_action(MAP)
        screen.blit(skip_action_img, (50, 212.5))
        text(25, "Skip Action", (0, 0, 0), 87.5, 200, alignx = "center", aligny = "center")
    #unit upgrade building
    elif isinstance(dynamics.selected_object, Building) and dynamics.selected_object.owned_by_current_player():
      if current_player.owns_unit_there(MAP.return_tile(dynamics.selected_object.coords)):
        #upgrade a building if there's a dude on it
        if dynamics.selected_object.upgraded_building in current_player.available_upgraded_buildings:
          #if there is no upgraded building, it would be: if None in available buildings, so that would be false
          if button(25, 200, Building.building_size*2, Building.building_size*2, 10, available = bool(current_player.wood >= dynamics.selected_object.upgraded_building[1][0] and current_player.metal >= dynamics.selected_object.upgraded_building[1][1] and current_player.food >= dynamics.selected_object.upgraded_building[1][2])):
            dynamics.selected_object.upgrade(MAP.return_tile(dynamics.selected_object.coords))
            current_player.deduct_costs(dynamics.selected_object.cost)
          if dynamics.selected_object.upgraded_building != None:
            screen.blit(Building.img_dict[dynamics.selected_object.upgraded_building[0]], (37.5, 262.5))
            text(20, dynamics.selected_object.upgraded_building[0], (0, 0, 0), 75, 250, alignx = "center", aligny = "center")
            display_resources([0] + dynamics.selected_object.upgraded_building[1], 150, 237.5)
          text(25, "Upgrade", (0, 0, 0), 100, 225, alignx = "center", aligny = "center")
      #spawn new unit
    elif isinstance(dynamics.selected_object, City) and dynamics.selected_object.owned_by_current_player():
      if MAP.return_tile(dynamics.selected_object.coords).unit == None:
      #if a city is selected and there's no dude on it to avoid spawning more than 1 dude
        for unit_type in enumerate(current_player.available_units):
          if dynamics.selected_object.spawn_timer < dynamics.selected_object.max_spawn_timer:
            if button((Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2), Unit.unit_size * 2, Unit.unit_size * 2, 10, available = bool(current_player.wood >= unit_type[1][7][0] and current_player.metal >= unit_type[1][7][1] and current_player.food >= unit_type[1][7][2])):
              print(unit_type[1][0] + " unit is spawned")
              current_player.deduct_costs(unit_type[1][7])
              #add spawn_cooldown to city
              dynamics.selected_object.spawn_timer += unit_type[1][8]
              new_unit = Unit(MAP.return_tile(dynamics.selected_object.coords), unit_type[1], dynamics.selected_object.coords, dynamics.current_player)
              current_player.units.append(new_unit)
              new_unit.unit_reset()
              del(new_unit)
          else:
            pygame.draw.rect(screen, (255, 0, 0), ((Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2), Unit.unit_size * 2, Unit.unit_size * 2), width = 0, border_radius = 10)
          screen.blit(Unit.img_dict[unit_type[1][0]], ((Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2) + 25))
          text(20, unit_type[1][0], (0, 0, 0), (Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2))
          display_resources([0] + unit_type[1][7], (Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack) + 75, option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2) + 12.5)
      #upgrade button
      if dynamics.selected_object.level < City.max_level:
        if button(25, 200, City.city_size*2, City.city_size*2, 10, available = bool(current_player.money >= dynamics.selected_object.cost[0] and current_player.wood >= dynamics.selected_object.cost[1] and current_player.metal >= dynamics.selected_object.cost[2] and current_player.food >= dynamics.selected_object.cost[2]), acolor = (224, 224, 34), hcolor = (140, 140, 3)):
          dynamics.selected_object.upgrade()
        screen.blit(dynamics.selected_object.image, (37.5, 250))
        screen.blit(City.upgrade_img, (37.5, 250))
        display_resources([0] + dynamics.selected_object.cost, 150, 250)
        text(25, "Upgrade", (0, 0, 0), 100, 225, alignx = "center", aligny = "center")
      else:
        text(25, "Max Level", (0, 0, 0), 75, 175, alignx = "center", aligny = "center")

    #build building buttons
    elif isinstance(dynamics.selected_object, Location):
      #run through available buildings and player actions
      #selected object is a location
      #build new building
      for building_type in enumerate(current_player.available_buildings):
        #a_building_type is a list containing the stats of a building
        if dynamics.selected_object.building == None and dynamics.selected_object.city == None and current_player.owns_unit_there(dynamics.selected_object) and dynamics.selected_object.terrain in building_type[1][4]:
          #if there is no other building there and u own a dude that is there and the terrain is in the building's terrain list and there is no city there
          if button(SCREENLENGTH - Building.building_size*2, 200 + building_type[0] * (Building.building_size*2), Building.building_size*2, Building.building_size*2, 10, stroke = 0, available = bool(current_player.wood >= building_type[1][1][0] and current_player.metal >= building_type[1][1][1] and current_player.food >= building_type[1][1][2] and current_player.water >= building_type[1][1][3])):
            #build building and subtract resources
            print(building_type[1][0] + " is built")
            current_player.deduct_costs(building_type[1][1])
            new_building = Building(dynamics.selected_object, building_type[1], dynamics.selected_object.coords, dynamics.current_player)
            current_player.buildings.append(new_building)
            del(new_building)
          #display the building images on the buttons
          screen.blit(Building.img_dict[building_type[1][0]], (SCREENLENGTH - Building.building_size*2 + 25, 250 + building_type[0] * (Building.building_size*2)))
          text(20, building_type[1][0], (0, 0, 0), SCREENLENGTH - 150, 200 + building_type[0] * (Building.building_size*2))
          text(20, "Terrain: " + ", ".join(building_type[1][4]), (0, 0, 0), SCREENLENGTH - 150, 210 + building_type[0] * (Building.building_size*2))
          display_resources([0] + building_type[1][1], SCREENLENGTH - 25, 250 + building_type[0] * (Building.building_size*2))

      #do player action    
      for player_action in enumerate(current_player.available_actions):
        #doing a player action
        if not dynamics.selected_object.player_acted_on and current_player.player_action_eligible(player_action[1], dynamics.selected_object) and current_player.owns_unit_there(dynamics.selected_object) and dynamics.selected_object.building == None and dynamics.selected_object.city == None:
          #if you own a dude there and there is no building there (to avoid chopping forest where there is a lumber hut) and there is no city there
          #can't do player action when there's a building there
          if button(player_action_x + player_action[0] * player_action_size, player_action_y, player_action_size, player_action_size, 20, available = bool(current_player.money >= Player.cost_dict[player_action[1]])):
            current_player.player_action(player_action[1], dynamics.selected_object, Player.cost_dict[player_action[1]])
          screen.blit(Player.img_dict[player_action[1]], (player_action_x + player_action[0] * player_action_size, player_action_y))
          text(25, player_action[1].capitalize(), (0, 0, 0), (player_action_x + player_action_size/2) + (player_action[0] * player_action_size), player_action_y - 10, alignx = "center")
          text(50, str(Player.cost_dict[player_action[1]]), money_color, (player_action_x + player_action_size/2) + (player_action[0] * player_action_size), player_action_y + 25, alignx = "center")          
    #keep all buttons on top of this line
    
    #selecting the dynamics.selected_object
    #order is unit, building, city, location when selecting same space
    #base this off of selection order
    #this allows eg if selected unit, next is building
    #if player's click did not land on any unit, we move on to building
    for object_type in selection_order:
      obj = receive_input(object_type)
      if obj == None:
        continue
      if dynamics.selected_object == None or dynamics.selected_object.coords != obj.coords:
        #if there was no past selected or player selected a different space
        dynamics.selected_object = obj
        dynamics.btn_pressed_this_frame = True
        break
      if dynamics.selected_object and dynamics.selected_object.coords == obj.coords:
        #if player selected the same space
        dynamics.selected_object = alternate_selection(dynamics.selected_object)
        dynamics.btn_pressed_this_frame = True
        break
    del(obj)
      
    Animation.destroyAnimation(dynamics.current_player)
    for animation in dynamics.animation_list:
      animation.update()
    clock.tick(FPS)
    screen.blit(transparent_screen, (0, 0))
    pygame.display.update()

  while dynamics.status == "tech tree":
    screen.fill((255, 255, 255))
    pressed_keys = pygame.key.get_pressed()
    dynamics.btn_pressed_this_frame = False
    dynamics.mouse_pos = pygame.mouse.get_pos()
    dynamics.mouse_clicked = False

    if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
      dynamics.tech_offset_y += 10
    if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
      dynamics.tech_offset_y -= 10
    if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
      dynamics.tech_offset_x += 10
    if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
      dynamics.tech_offset_x -= 10
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_x:
          pygame.quit()
          sys.exit()
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        dynamics.mouse_clicked = True

    if button(0, 0, 50, 50, 10):
      dynamics.status = "playing"
      if isinstance(dynamics.selected_object, Unit) and dynamics.selected_object in current_player.units and dynamics.selected_object.action_sequence != []:
        dynamics.selected_object.calculate_action_range(MAP)
    
    text(25, str("Player " + str(dynamics.current_player + 1)) + " turn", current_player.color, SCREENLENGTH, 0, alignx = "right")
    display_resources([current_player.money, current_player.wood, current_player.metal, current_player.food, current_player.food, current_player.water], SCREENLENGTH - 25, 50, display_all = True)
    
    for a_tech in all_techs:
      #a_tech is a list of the tech stats, not a class object, therefore, a_tech[0] is the name, a_tech[1] is the cost, a_tech[4] is the preceding tech
      if a_tech[3] == None or a_tech[3][0] in current_player.techs:
        #if there is no tech that precedes a_tech, or if the player owns the preceding tech, tech is available to buy
        if a_tech[0] not in current_player.techs:
          #if the player does not own the tech
          if button(a_tech[2][0] + dynamics.tech_offset_x, a_tech[2][1] + dynamics.tech_offset_y, Tech.tech_size, Tech.tech_size, 10, available = current_player.money >= a_tech[1]):
          #owns_tech will compare names of the tech, archery[3][0] == "Logging"
            current_player.money -= a_tech[1]
            Tech(a_tech, dynamics.current_player)
            print("tech bought")
        else:
          #player owns the tech already
          pygame.draw.rect(screen, (0, 255, 255), (a_tech[2][0] + dynamics.tech_offset_x, a_tech[2][1] + dynamics.tech_offset_y, Tech.tech_size, Tech.tech_size), 0, 10)
      else:
        #display another color
        #player does not own the preceding tech
        #pygame.draw.rect(screen, (255, 0, 0), (a_tech[2] + dynamics.tech_offset_x, a_tech[3] + dynamics.tech_offset_y, Tech.tech_size, Tech.tech_size), 0, 10)
        #don't draw any button or rectangle
        pass
      screen.blit(a_tech[9], (a_tech[2][0] + dynamics.tech_offset_x, a_tech[2][1] + dynamics.tech_offset_y))
      text(30, a_tech[0], (0, 0, 0), a_tech[2][0] + Tech.tech_size/2 + dynamics.tech_offset_x, a_tech[2][1] + Tech.tech_size/2 - 20 + dynamics.tech_offset_y, alignx = "center", aligny = "center")
      text(50, str(a_tech[1]), money_color, a_tech[2][0] + Tech.tech_size/2 + dynamics.tech_offset_x, a_tech[2][1] + Tech.tech_size/2 + 15 + dynamics.tech_offset_y, alignx = "center", aligny = "center")
      if a_tech[3] != None:
        pygame.draw.line(screen, (0, 0, 0), (a_tech[2][0] + Tech.tech_size/2 + dynamics.tech_offset_x, a_tech[2][1] + Tech.tech_size + dynamics.tech_offset_y), (a_tech[3][2][0] + Tech.tech_size/2 + dynamics.tech_offset_x, a_tech[3][2][1] + dynamics.tech_offset_y), width = 5)
      
    clock.tick(FPS)
    text(20, "FPS: " + str(clock.get_fps()), (0, 0, 0), 300, 0, alignx="center")
    pygame.display.update()