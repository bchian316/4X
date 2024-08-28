#if there's a weird bug, try switching the for loop iterable variable from _ to something else
#maybe that'll help

'''REMINDER:
WHENEVER CALLING unit.display_x or unit.display_y, YOU MUST ADD offset_x or offset_y TO GET THE TRUE BLIT COORDS
display_map_hex takes up a lot of processing power
with it, fps < 10
without is, fps > 30
'''

#THINGS ARE NOT BEING DISPLAYED BECAUSE CODE CANNOT EXIT THE CHOOSE ACTION SEQUENCE METHOD for some reason
#self.movement_range in self.do_action has some really weird values
#eg [-28, -7], [-6, -28]
#too many loops or something, the loop is running too many times and values are too high, there are coordinates that do not exist in self.movement_range
#Answer: i am adding values to self.movement_range while I am using it as an iterable in a for loop, so the list will keep having values added to it, and the for loop will never end
#MUST MAKE A NEW LIST
#ANSWER: when i am creating self.movement_range_placeholder, I copied self.movement_range, but list variables only contain references to lists, so I have to use copy.deepcopy instead to copy the list

#problem: not all tiles can be selected as location - only tiles in the first 2 rows can be selected
#answer: i was using row as the iterable, not row[1] because i was using enumerate

'''
TODO:
- DO THIS FIRST: 
- calibrate damage formula
- make more images for different units
ADVANCED (save for later):
- decide on this: should other players be able to see the production of foreign buildings and the cooldown of foreign cities?
'''
import pygame, sys
pygame.init()
from math import sqrt, degrees, atan
from copy import deepcopy
from random import randint
SCREENLENGTH = 700
SCREENHEIGHT = 700
FPS = 40
num_displays = pygame.display.get_num_displays()

# Choose the display you want to use (change index as needed)
if num_displays == 2:
  display_index = 1  # make the window always appear on my monitor
else:
  display_index = 0
# Get the dimensions of the chosen display
#display_info = pygame.display.Info()
#SCREENLENGTH = display_info.current_w
#SCREENHEIGHT = display_info.current_h

flags = pygame.DOUBLEBUF

# Set the display mode on the chosen display
screen = pygame.display.set_mode((SCREENLENGTH, SCREENHEIGHT), flags=flags, display=display_index)# Game code goes here
player_alpha_shade = 70
transparent_screen = pygame.Surface((SCREENLENGTH, SCREENHEIGHT), pygame.SRCALPHA)
transparent_screen.set_alpha(player_alpha_shade)
#make sure transparent_screen.blit goes below all displays that are drawn on it
# Add game logic and functions
clock = pygame.time.Clock()
pygame.display.set_caption('pingatopia')
mouse_pos = pygame.mouse.get_pos()
mouse_pos = list(mouse_pos)
mouse_clicked = False
mouse_up = True
mouse_down = False
#later, change this to "home" and create a home screen; this is temporary only
status = "home"
#when using pygame.transform for any pygame.Surface object (image), the image will be a little distorted after each transformation, so keep a variable set to the original undistorted image and use that image to transform the actual image so it will only be distorted once after each transformation, rather than all the transformations adding up to decay the image very fast
#only use this procedure for images that undergo pygame.transform.rotate/scale/etc 
#for images that that don't undergo these transformations, use the original image as the image to transform to save code length

#break
print(pygame.font.get_fonts())
#good fonts: harrington, 
def text(size, message, color, textx, texty, alignx = "left", aligny = "top", font = "harrington"):
  myfont = pygame.font.SysFont(font, size)
  text_width, text_height = myfont.size(message)
  text_surface = myfont.render(message, True, color)
  if alignx == "left":
    pass
  elif alignx == "center":
    textx = textx - (text_width/2)
  elif alignx == "right":
    textx = textx - text_width
  if aligny == "top":
    pass
  elif aligny == "center":
    texty = texty - (text_height/2)
  elif aligny == "bottom":
    texty = texty - text_height
  screen.blit(text_surface, (textx, texty))

btn_pressed_this_frame = False
def button(x, y, width, height, radius = 0, stroke = 0, available = True, acolor = (0, 255, 0), ucolor = (145, 145, 145, 145), hcolor = (43, 186, 43)):
  global coins, btn_pressed_this_frame
  #available is a boolean that determines whether the button is available to be pressed or not
  if available:
    if mouse_pos[0] >= x and mouse_pos[0] <= x + width and mouse_pos[1] >= y and mouse_pos[1] <= y + height:
      pygame.draw.rect(screen, hcolor, (x, y, width, height), stroke, radius)
      if mouse_clicked and btn_pressed_this_frame == False:
        btn_pressed_this_frame = True
        return True
    else:
      pygame.draw.rect(screen, acolor, (x, y, width, height), stroke, radius)
  else:
    pygame.draw.rect(screen, ucolor, (x, y, width, height), stroke, radius)
  return False
def rect_collided(x1, y1, length1, height1, x2, y2, length2, height2):
  #1 = object
  #2 = target
  if x1 > x2 - length1 and x1 < x2 + length2 and y1 > y2 - height1 and y1 < y2 + height2:
    return True
  return False
def circle_collided(x1, y1, radius1, x2, y2, radius2):
  distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
  if distance <= radius1 + radius2:
    return True
  return False
def circle_rect_collided(rect_x, rect_y, rect_width, rect_height, circle_x, circle_y, circle_diameter):
    #circle_x and circle_y are the left top anchor of the circle (similar to a rectangle); they are not the coordinates to the circle center
    circle_radius = circle_diameter / 2
    circle_center_x = circle_x + circle_radius
    circle_center_y = circle_y + circle_radius

    if circle_center_x < rect_x:
      closest_x = rect_x
    elif circle_center_x > rect_x + rect_width:
      closest_x = rect_x + rect_width
    else:
      closest_x = circle_center_x
    if circle_center_y < rect_y:
      closest_y = rect_y
    elif circle_center_y > rect_y + rect_height:
      closest_y = rect_y + rect_height
    else:
      closest_y = circle_center_y

    distance_x = circle_center_x - closest_x
    distance_y = circle_center_y - closest_y
    distance = sqrt(distance_x**2 + distance_y**2)

    return distance <= circle_radius
def get_vel(x1, y1, x2, y2, speed):
  distancex = x2 - x1
  distancey = y2 - y1
  distance = sqrt(distancex**2 + distancey**2)
  divisor = distance/speed
  #divisor is how many frames it would take for the bullet to reach its destination
  #speed * divisor = distance (rt = d)
  velx = distancex/divisor
  vely = distancey/divisor
  return velx, vely
def get_angle(x_start, y_start, target_x, target_y):
  #ANGLES ARE COUNTERCLOCKWISE
  #ALWAYS FROM START TO TARGET
  y_distance = abs(y_start - target_y)
  x_distance = abs(x_start - target_x)
  if (x_distance == 0):
    if (target_y > y_start):
      angle = 0
    if (target_y < y_start):
      angle = 180
  elif (y_distance == 0):
    if (target_x > x_start):
      angle = 270
    if (target_x < x_start):
      angle = 90
  else:
    #this part uses the right triangle created by x_distance, y_distance, and the line connect the start and the target (hypotenuse)
    #Lets say the angle from the start to target (the angle we're trying to find) is theta
    #the opposite side of theta will always be the y_distance
    #the adjacent side of theta will always be the x_distance
    #because tangent is opposite/adjacent, tan(theta) = y_distance/x_distance
    #by isolating theta, we can arctangent (tan-1) both sides, which leaves theta = arctangent(y_distance/x_distance)
    #atan returns the angle in radians, so we just convert it into degrees
    angle = degrees(atan(y_distance/x_distance))
    if ((target_x < x_start) and (target_y > y_start)):
      angle = 90 + angle
    elif ((target_x > x_start) and (target_y > y_start)):
      angle = 270 - angle
    elif (target_x < x_start) and (target_y < y_start):
      angle = 90 - angle
    elif (target_x > x_start) and (target_y < y_start):
      angle = 270 + angle
  return angle
def rotate_center(img, og_img, deg, og_deg = 0):
  #this rotates an image around its center counterclockwise (no x and y parameters needed)
  #use og_image as the raw image directly loaded from the file to prevent image distortion and multiple sizing increases (because of the rotation)
  og_width, og_height = og_img.get_size()
  og_center = (og_width/2, og_height/2)
  img = pygame.transform.rotate(og_img, deg-og_deg)
  width, height = img.get_size()
  center = (width/2, height/2)
  offsetx = center[0] - og_center[0]
  offsety = center[1] - og_center[1]
  return img, offsetx, offsety
  #find offset to center to make it equal to og_center
  #subtract offset from regular image coords to make the center constant
def pivot(angle, offset):
  #counterclockwise
  #offset should be a pygame.math.Vector2 class with its arguments as the difference from the pivot point to the center of the image
  #for example, if the pivot point is 25 pixels to the left and 50 pixels below of the center of the image, then the pygame.math.Vector2 should be (25, -50)
  #pivot_point_x + offset_x = image_center_x
  #pivot_point_y + offset_y = image_center_y
  #USE THE ORIGINAL IMAGE FOR THIS NOT THE UPDATE IMAGE THATS BEING DISPLAYED
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
  #the rotation should be counterclockwise, but in reality is clockwise because pygame has an inverted y-axis
    # Add the offset vector to the center/pivot point to shift the rect.
    return rotated_offset # Return the rotated image
    #add rotated_offset to the x and y coordinates when you display the image
'''class Timer:
  def __init__(self, seconds, running = False):
    self.start_time = time()
    self.end_time = time()
    self.time = seconds
    self.running = running
  def update(self):
    if self.running:
      self.end_time = time()
      if self.end_time - self.start_time >= self.time:
        return True
    return False
  def start(self, seconds = None):
    if seconds != None:
      self.time = seconds
    self.running = True
    self.start_time = time()
    self.end_time = time()
  def stop(self):
    self.running = False'''
hex_size = 100
offset_x = 250
offset_y = 100

class Location:
  plains_img = pygame.image.load("terrain/plains.png").convert_alpha()
  forest_img = pygame.image.load("terrain/forest.png").convert_alpha()
  water_img = pygame.image.load("terrain/water.png").convert_alpha()
  ocean_img = pygame.image.load("terrain/ocean.png").convert_alpha()
  mountain_img = pygame.image.load("terrain/mountain.png").convert_alpha()
  def __init__(self, coordx, coordy, terrain, features):
    self.terrain = terrain
    self.find_img()
    self.features = features
    self.coord_x = coordx
    self.coord_y = coordy
    self.display_x = (self.coord_y - 1)*(-hex_size/4)*sqrt(3)
    self.display_y = (self.coord_y - 1)*(hex_size*0.75)
    #for every x:
    self.display_x += (self.coord_x - 1)*(hex_size/2)*sqrt(3)
      #incorporate offsets

  def find_img(self):
    if self.terrain == "plains":
      self.img = Location.plains_img
    elif self.terrain == "forest":
      self.img = Location.forest_img
    elif self.terrain == "mountain":
      self.img = Location.mountain_img
    elif self.terrain == "water":
      self.img = Location.water_img
    elif self.terrain == "ocean":
      self.img = Location.ocean_img
    else:
      #this is a void
      pass

  def display(self, custom = None):
    if custom != None:
      coords = custom
    else:
      coords = (self.display_x + offset_x, self.display_y + offset_y)
    try:
      screen.blit(self.img, coords)
    except:
      pass
    if "crop" in self.features:
      screen.blit(crop_img, coords)
    elif "harvested crop" in self.features:
      screen.blit(harvested_crop_img, coords)
    if "seaweed" in self.features:
      screen.blit(seaweed_img, coords)
    if "village" in self.features:
      screen.blit(village_img, coords)

#lets make the map a constant size (4 side length: hexagon) = 37 tiles
#lets make 9 diagonal columns because there are 2x-1 columns when x is side length
#the map will be the constant variable that revolves around all the players
#it will show the terrain of every tile in the game
#MAP = [4 items, 5 items, 6, 7, 6, 5, 4] because there is a side length of 4
TERRAIN = [["plains", "plains", "mountain", "plains", "forest", "", "", "", ""], 
       ["mountain", "plains", "plains", "plains", "forest", "forest", "", "", ""], 
       ["plains", "plains", "mountain", "plains", "plains", "mountain", "forest", "", ""], 
       ["plains", "plains", "plains", "plains", "mountain", "forest", "forest", "forest", ""], 
       ["mountain", "mountain", "mountain", "mountain", "plains", "forest", "mountain", "mountain", "forest"], 
       ["", "plains", "mountain", "plains", "plains", "plains", "forest", "forest", "forest"],
       ["", "", "plains", "plains", "plains", "mountain", "forest", "forest", "forest"],
       ["", "", "", "water", "water", "water", "water", "water", "water"], 
       ["", "", "", "", "ocean", "ocean", "ocean", "ocean", "ocean"]]
#this is the side length of the map
map_length = len(TERRAIN)-1
#useless for now
crop = [[5, 1], [5, 2], [6, 2], [3, 3]]
harvested_crop = []
seaweed = [[6, 7], [7, 7], [8, 7], [6, 8], [7, 8]]
villages = [[0, 2], [1, 0], [2, 4], [5, 1], [5, 7], [6, 6], [3, 7]]
MAP = []
#configure map
for row in enumerate(TERRAIN):
  coordy = row[0]
  MAP.append([])
  for tile in enumerate(row[1]):
    coordx = tile[0]
    features = []
    if [coordx, coordy] in crop:
      features.append("crop")
    if [coordx, coordy] in harvested_crop:
      features.append("harvested crop")
    if [coordx, coordy] in seaweed:
      features.append("seaweed")
    if [coordx, coordy] in villages:
      features.append("village")
    MAP[coordy].append(Location(coordx, coordy, tile[1], features))
#important variables for selection and stuff
selected_object = None
selected_collision_range = 75
#this is the circle diameter for checking if the player clicked on something
#to make stat display easier
selected_object_display = (0, 50)
text_display_size = 20
player_action_x = 250
player_action_y = SCREENHEIGHT - 100
player_action_size = 75
#when options are listed, start at this x value
option_x = 425
selection_frame = pygame.image.load("selection frame.png").convert_alpha()
production_frame = pygame.image.load("production frame.png").convert_alpha()
#reset selected_unit after player turn is done to prevent other players from controlling a unit that's not theirs
#terrain images
#selected images
unit_select_img = pygame.image.load("selection/owns select.png").convert_alpha()
building_select_img = pygame.transform.scale(unit_select_img, (75, 75)).convert_alpha()
location_select_img = pygame.image.load("selection/owns location.png").convert_alpha()
unit_location_img = pygame.image.load("selection/owns unit location.png").convert_alpha()
foreign_unit_select_img = pygame.image.load("selection/foreign select.png").convert_alpha()
foreign_building_select_img = pygame.transform.scale(foreign_unit_select_img, (75, 75)).convert_alpha()
location_img = pygame.image.load("selection/foreign location.png").convert_alpha()

#player_action icons
chop_img = pygame.image.load("player actions/chop.png").convert_alpha()
cultivate_img = pygame.image.load("player actions/cultivate.png").convert_alpha()
harvest_img = pygame.image.load("player actions/harvest.png").convert_alpha()
grow_img = pygame.image.load("player actions/grow.png").convert_alpha()
#icon imgs for unit stats
#defense_img = pygame.image.load("defense.png").convert_alpha()

#map features (food, seaweed, etc)
crop_img = pygame.image.load("terrain/crop.png").convert_alpha()
harvested_crop_img = pygame.image.load("terrain/harvested crop.png").convert_alpha()
seaweed_img = pygame.image.load("terrain/seaweed.png").convert_alpha()
village_img = pygame.image.load("terrain/village.png").convert_alpha()
def display_map_hex(map):
  #use offsets to move the entire map around
  for row in map:
    for tile in row:
      #coord_x and coord_y are the coordinates of the tile in the map, not the screen blit coords
      #the map is a list of lists, so the first list is the first row, the second list is the second row
      #the first item in the list is the first tile, the second item is the second tile, etc.
      #display_x and display_y will be the screen blit coords of the tile
      tile.display()
      
#displays the map in hexagonal form
#MAP[0][0] would be plains
#MAP[0][1] wouild be forest
#MAP[0][2] would be desert
#MAP[0][3] would be plains
#MAP[1][0] would be ocean
#make a list for buildings you can build on the map

def return_Adjacent_hex(x, y):
  #returns a list of all the adjacent hexes based on one hex
  #the items returned are x and y coords to be used on the map
  adjacent_hexes = []
  adjacent_hexes.append([x-1, y-1])
  adjacent_hexes.append([x, y-1])
  adjacent_hexes.append([x-1, y])
  adjacent_hexes.append([x+1, y])
  adjacent_hexes.append([x, y+1])
  adjacent_hexes.append([x+1, y+1])
  return adjacent_hexes
  #adjacent_hexes has the coordinates of all the adjacent hexes, not their terrain stuff
  #u can call the terrain manually


def shadeTile(coord_x, coord_y, color):
  #coord_x and coord_y are coordinates, not display coordinates
  global hex_size, offset_x, offset_y
  center_x = (coord_y - 1)*(-hex_size/4)*sqrt(3)
  center_y = (coord_y - 1)*(hex_size*0.75)
  center_x += (coord_x - 1)*(hex_size/2)*sqrt(3)
  #allocate for image size (off of hex_side)
  center_x += ((hex_size/2)*sqrt(3))/2
  center_y += hex_size/2
  #add offsets
  center_x += offset_x
  center_y += offset_y
  #(display_x, display_y) will be the center of the corresponding hex
  #points go clockwise from the top-left vertex
  point1 = (center_x - hex_size*sqrt(3)/4, center_y - hex_size/4)
  point2 = (center_x, center_y - hex_size/2)
  point3 = (center_x + hex_size*sqrt(3)/4, center_y - hex_size/4)
  point4 = (center_x + hex_size*sqrt(3)/4, center_y + hex_size/4)
  point5 = (center_x, center_y + hex_size/2)
  point6 = (center_x - hex_size*sqrt(3)/4, center_y + hex_size/4)
  pygame.draw.polygon(transparent_screen, color, [point1, point2, point3, point4, point5, point6])


def display_units(units, offset_x, offset_y, p_number, p_color, availability_marker_size = 10):
  global current_player
  #p_number is the player number
  #this displays a list of specific units (a unit type)
  #units would be a list containing a specific unit type
  for a_unit in units:
    shadeTile(a_unit.coord_x, a_unit.coord_y, p_color)
    screen.blit(a_unit.image, (a_unit.display_x + offset_x, a_unit.display_y + offset_y))
    #this will display a text version of the unit health: text(25, str(a_unit.health) + "/" + str(a_unit.max_health), (255, 0, 0), a_unit.display_x + unit_size + offset_x, a_unit.display_y + offset_y)
    #health bar:
    pygame.draw.rect(screen, (255, 0, 0), (a_unit.display_x + offset_x, a_unit.display_y + offset_y - 12.5, Unit.unit_size, 10))
    pygame.draw.rect(screen, (0, 255, 0), (a_unit.display_x + offset_x, a_unit.display_y + offset_y - 12.5, Unit.unit_size*(a_unit.health/a_unit.max_health), 10))
    text(15, str(a_unit.health) + "/" + str(a_unit.max_health), (0, 0, 0), a_unit.display_x + offset_x + Unit.unit_size/2, a_unit.display_y + offset_y - 7.5, alignx = "center", aligny = "center")
    text(25, str(p_number + 1), (255, 255, 255), a_unit.display_x + offset_x + Unit.unit_size/2, a_unit.display_y + offset_y + Unit.unit_size/2, alignx = "center", aligny = "center")
    if p_number == current_player:
      pygame.draw.circle(screen, (255, 0, 0), (a_unit.display_x + offset_x, a_unit.display_y + offset_y), availability_marker_size)
      if not a_unit.turn_done:
        pygame.draw.circle(screen, (0, 255, 0), (a_unit.display_x + offset_x, a_unit.display_y + offset_y), availability_marker_size)
    else:
      pygame.draw.circle(screen, (125, 125, 125), (a_unit.display_x + offset_x, a_unit.display_y + offset_y), availability_marker_size)
    text(30, str(p_number + 1), (0, 0, 0), a_unit.display_x + offset_x, a_unit.display_y + offset_y, alignx = "center", aligny = "center")
def unit_reset(unit):
  unit.action = None
  unit.action_index = 0
  unit.action_sequence = []
  unit.action_range = [[unit.coord_x, unit.coord_y]]

def calculate_damage(attacker, defender):
  attack_damage = (attacker.health/attacker.max_health)*attacker.attack
  defend_damage = (defender.health/defender.max_health)*defender.defense
  #3 will affect the general damage of all attacks
  #attack_damage *= 3
  #no damage scaler
  damage = attack_damage/defend_damage
  if damage < 0:
    damage = 0
  return round(damage)

def calculate_heal(healer, target):
  #DO THIS LATER
  pass

class Player:
  #contains all the players
  player_list = []
  chop_cost = 5
  cultivate_cost = 10
  grow_cost = 15
  def __init__(self, player_number):
    #player number determines the order the players play in starting from 0 not 1
    self.player_number = player_number
    self.color = (randint(0, 255), randint(0, 255), randint(0, 255))
    self.money = 5
    self.metal = 1
    self.wood = 1
    self.food = 1
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
    self.available_units = []
    self.available_naval_units = []
    #available terrain the player's units can be on
    self.available_terrain = ["plains", "forest"]
  def update(self, player_num):
    global selected_object, selected_object
    #this is the update function for the player
    #kill buildings with bad guys on them
    deletion_counter = 0
    while deletion_counter < len(self.buildings):
      #building_type will be a list of a specific building type
      if return_occupied(self.buildings[deletion_counter].coord_x, self.buildings[deletion_counter].coord_y, object = "unit") and not return_occupied(self.buildings[deletion_counter].coord_x, self.buildings[deletion_counter].coord_y, object = "unit") in self.units:
        #if there is dude on buildings AND u don't own him
        #remove the building
        print("building dead")
        if selected_object == self.buildings[deletion_counter]:
          selected_object = None
        self.buildings.pop(deletion_counter)
        continue
      deletion_counter += 1
    #delete dead units
    deletion_counter = 0
    while deletion_counter < len(self.units):
      if self.units[deletion_counter].health <= 0:
        #if unit has 0 or less health
        print("unit dead")
        if selected_object == self.units[deletion_counter]:
          selected_object = None
        self.units.pop(deletion_counter)
        continue
      deletion_counter += 1
    deletion_counter = 0
    for unit in self.units:
      if return_occupied(unit.coord_x, unit.coord_y, object = "city"):
        #if there is a unit on the city
        if not player_num == return_occupied(unit.coord_x, unit.coord_y, object = "city").player_number:
          #if unit's player doesn't own the city
          stolen_city = return_occupied(unit.coord_x, unit.coord_y, object = "city")
          #stolen_city is the city that the unit is on, will be a object of City
          Player.player_list[stolen_city.player_number].cities.remove(stolen_city)
          #remove city from previous player's list
          stolen_city.player_number = player_num
          Player.player_list[player_num].cities.append(stolen_city)
          #add city to player's list
      elif [unit.coord_x, unit.coord_y] in villages:
        #if unit is on a village
        Player.player_list[player_num].cities.append(City(unit.coord_x, unit.coord_y, player_num))
        MAP[unit.coord_y][unit.coord_x].features.remove("village")
        print("village converted")
    #display stuff here
    #display buildings
    display_buildings(self.buildings, offset_x, offset_y, player_num, self.color)
    #display cities
    display_cities(self.cities, offset_x, offset_y, player_num, self.color)
    #display units
    for unit in self.units:
      unit.action_range = [[unit.coord_x, unit.coord_y]]
    display_units(self.units, offset_x, offset_y, player_num, self.color)
    #update everything:
    #add the money per turn, resources per turn
  def owns_unit(self, unit):
    for _unit in self.units:
        if unit == _unit:
          return True
  def owns_building(self, building):
    for _building in self.buildings:
      if building == _building:
        return True
  def owns_city(self, city):
    for _city in self.cities:
      if city == _city:
        return True
  def owns_tech(self, tech_name):
    #tech_name should be a string, the name of the tech
    for _tech in self.techs:
      if _tech.name == tech_name:
        return True
  def player_action(self, action, cost = 0):
    if action == "chop":
      #get wood by cutting down forest into plains
      #location must be at forest tile
      self.wood += 5
      selected_object.terrain = "plains"
    elif action == "cultivate":
      self.food += 3
      selected_object.features.remove("crop")
      selected_object.features.append("harvested crop")
    elif action == "harvest":
      self.money += 10
      selected_object.features.remove("seaweed")
    elif action == "grow":
      #grow forest from plains
      selected_object.terrain = "forest"
    self.money -= cost
  def turn_update_before(self):
    #this takes place at the beginning of turn, where buildings and cities produce resources
    global current_player, selected_object
    #reset crop resource
    for row in MAP:
      for tile in row:
        if "harvested crop" in tile.features:
          tile.features.remove("harvested crop")
          tile.features.append("crop")
    for building in self.buildings:
      building.produce()
    for city in self.cities:
      city.produce()
      if return_occupied(city.coord_x, city.coord_y, "unit") == False:
        #cities cannot cooldown if there's a person on it
        city.spawn_timer -= City.spawn_cooldown*city.max_spawn_timer
        if city.spawn_timer < 0:
          city.spawn_timer = 0
    
    #reset variables so u can't control dudes that belong to other players
    selected_object = None
    #move on to next player
  def turn_update_after(self):
    #this takes place after turn, where units gain energy
    for unit in self.units:
      unit.turn_done = False
      unit_reset(unit)
    #change player_count to alter the number of players
#player_count is the number of players
player_count = 2
for _ in range(player_count):
  Player.player_list.append(Player(_ - 1))
#starts at 0, so the first player is player 0
current_player = 0
#Player.player_list[current_player] -> this is a Player class object
#taking that.units is taking that player's units list

Player.player_list[0].color = (0, 255, 255)
Player.player_list[1].color = (255, 0, 0)
#unit stats
#var = ["name", attack, defense, health, regen, range, movement, cost (materials to make him) [money, wood, metal, food], timer, sequences, abilities]
man = ["Man", 6, 2, 8, 3, 1, 2, [5, 1, 1, 1], 5, [["move", "attack"], ["heal"]], []]
#man can move 1 or attack
swordsman = ["Swordsman", 9, 3, 12, 4, 1, 2, [10, 2, 5, 2], 5, [["move", "attack"], ["heal"]], []]
spearman = ["Spearman", 8, 2, 10, 3, 2, 2, [5, 5, 3, 2], 5, [["move", "attack", "attack"], ["heal"]], []]
axeman = ["Axeman", 20, 3, 12, 4, 1, 1, [5, 2, 5, 1], 5, [["move"], ["attack"], ["heal"]], []]
shieldman = ["Shieldman", 6, 4, 15, 5, 1, 1, [5, 0, 10, 0], 5, [["move"], ["attack"], ["heal"]], []]
#scout = ["Scout", Player.player_list[current_player].scouts, 3, 1, 5, 3, 1, 3, [3, 1, 0, 0], 3, [["move", "attack", "move"]], []]
#scout can move 3, attack 3, and move 3
#catapult = ["Catapult", Player.player_list[current_player].units, 5, 0, 10, 3, 3, 1, [3, 3, 0, 0], 8, [["move"], ["attack"]], []]
#catapult can move 1 or attack 1
archer = ["Archer", 7, 1, 8, 4, 2, 2, [5, 3, 0, 0], 7, [["attack", "move"], ["move", "heal"]], []]
crossbowman = ["Crossbowman", 15, 1, 5, 2, 3, 2, [25, 10, 5, 3], 7, [["move", "attack"], ["attack", "move"], ["heal"]], []]
rider = ["Rider", 7, 2, 9, 5, 1, 3, [10, 0, 0, 3], 6, [["move", "attack"], ["move", "heal"]], []]
ship = ["Ship", 10, 3, 10, 3, 1, 2, [15, 5, 0, 0], 0, [["move", "attack"], ["move", "heal", "move"]], ["float"]]
steeler = ["Steeler", 15, 4, 30, 8, 1, 2, [20, 0, 3, 0], 0, [["move", "attack", "move"], ["heal"]], ["float"]]

#building stats
#var = ["name", list, cost, production, production speed, possible terrain, abilities, upgrade into]
lumber_hut = ["Lumber Hut", [10, 2, 0, 0], [3, 0, 0], 1, ["forest"], [], None]
foundry = ["Foundry", [20, 0, 5, 0], [0, 20, 0], 2, None, [], None]
#foundry is upgradable, so there's no terrain restrictions: u just build it on top of a mine
mine = ["Mine", [20, 0, 2, 0], [0, 5, 0], 2, ["mountain"], [], foundry]
shipyard = ["Shipyard", [25, 3, 0, 0], [0, 0, 0], 1, ["water"], ["shipbuilding"], None]
port = ["Port", [30, 3, 3, 3], [20, 20, 20], 3, [], ["shipbuilding"], None]
market = ["Market", [20, 1, 1, 1], [3, 3, 3], 2, ["market"], [], port]
plantation = ["Plantation", [30, 5, 0, 0], [0, 0, 20], 1, None, ["cultivate"], None]
farm = ["Farm", [15, 0, 0, 3], [0, 0, 10], 1, ["plains", "forest", "mountain", "water"], ["cultivate"], plantation]

#make it so all players can make units
for _ in Player.player_list:
  _.available_units.append(man)
  _.available_naval_units.append(ship)

'''Player.player_list[0].available_actions.append("chop")
Player.player_list[0].available_actions.append("cultivate")
Player.player_list[0].available_actions.append("harvest")
Player.player_list[0].available_actions.append("grow")'''


#def return_hex_details(x, y)

class Unit:
  #unit constructor
  health_stat_img = pygame.image.load("stats/health.png").convert_alpha()
  attack_stat_img = pygame.image.load("stats/attack.png").convert_alpha()
  defense_stat_img = pygame.image.load("stats/defense.png").convert_alpha()
  range_stat_img = pygame.image.load("stats/range.png").convert_alpha()
  movement_stat_img = pygame.image.load("stats/movement.png").convert_alpha()
  unit_size = 50
  man_img = pygame.image.load("unit/man.png").convert_alpha()
  rider_img = pygame.image.load("unit/rider.png").convert_alpha()
  swordsman_img = pygame.image.load("unit/swordsman.png").convert_alpha()
  spearman_img = pygame.image.load("unit/spearman.png").convert_alpha()
  axeman_img = pygame.image.load("unit/axeman.png").convert_alpha()
  shieldman_img = pygame.image.load("unit/shieldman.png").convert_alpha()
  archer_img = pygame.image.load("unit/archer.png").convert_alpha()
  crossbowman_img = pygame.image.load("unit/crossbowman.png").convert_alpha()
  ship_img = pygame.image.load("unit/ship.png").convert_alpha()
  steeler_img = pygame.image.load("unit/steeler.png").convert_alpha()
  unit_max_stack = 3
  img_dict = {"Man":man_img, "Rider":rider_img, "Swordsman":swordsman_img, "Spearman":spearman_img, "Axeman":axeman_img, "Shieldman":shieldman_img, "Archer":archer_img, "Crossbowman":crossbowman_img, "Ship":ship_img, "Steeler":steeler_img}
  def __init__(self, stats, x, y):
    #these are hex positions, not blit coords
    self.coord_x = x
    self.coord_y = y
    #these are blit coords
    self.display_x = (self.coord_y - 1)*(-hex_size/4)*sqrt(3)
    self.display_y = (self.coord_y - 1)*(hex_size*0.75)
    self.display_x += (self.coord_x - 1)*(hex_size/2)*sqrt(3)
    #allocate for image size (off of hex_side)
    self.display_x += ((hex_size/2)*sqrt(3))/2
    self.display_y += hex_size/2
    #allocate for image size (off of own image)
    self.display_x -= Unit.unit_size/2
    self.display_y -= Unit.unit_size/2
    #get stats from list
    self.name = stats[0]
    self.attack = stats[1]
    self.defense = stats[2]
    self.health = stats[3]
    self.max_health = stats[3]
    self.regen_value = stats[4]
    self.range = stats[5]
    self.movement = stats[6]
    self.cost = stats[7]
    #cost is [money, wood, metal, food]
    self.timer = stats[8]
    self.action_sequences = stats[9]
    self.abilities = stats[10]
    self.image = pygame.image.load("unit/"+str(self.name).lower()+".png").convert_alpha()
    #all image names should be unit name + .png eg. man.png
    self.turn_done = False
    self.action_sequence = []
    self.action = None
    self.action_index = 0
    #action_index starts at 0
    self.action_range = [[self.coord_x, self.coord_y]]
    self.action_range_placeholder = deepcopy(self.action_range)
    #moverange is a list of all the adjacent hexes that the unit can be moved to
  def next_action(self):
    global selected_object, selected_object
    try:
      self.action = self.action_sequence[self.action_index + 1]
      self.action_index += 1
      selected_object = self
    except IndexError:
      unit_reset(self)
      self.turn_done = True
      print("turn done")
  def do_action(self, object):
    global btn_pressed_this_frame
    #calculate the ranges in display_hints, and actually do the action here
    global selected_object, selected_object
    if self.action == "move" and object != None:
      #action is a movement order
      #self.action is the number of maximum hexes to move

      if [object.coord_x, object.coord_y] in self.action_range:
        btn_pressed_this_frame = True
        #location is within movement range and is not occupied
        print("successful move")
        self.coord_x = object.coord_x
        self.coord_y = object.coord_y
        #the move is valid, so we move on to the next action
        self.next_action()

    elif self.action == "attack" and object != None and not Player.player_list[current_player].owns_unit(object):
      # if the action is an attack and the targeted unit exists and the targeted unit does not belong to the current player (no friendly fire)
      #action is a attack order
      #self.action is the number of maximum hexes to move
      #self.action_range will only contain the hexes of the available targeted units, unlike during movement, self.action_range will contain all the hexes within the movement range

      if [object.coord_x, object.coord_y] in self.action_range:
        btn_pressed_this_frame = True
        print("successful attack", type(object))
        #the attack is valid, so we move on to the next action
        for animation in range(calculate_damage(self, object)):
          animation_list.append(damageAnimation(object.display_x + Unit.unit_size/2 + offset_x - damageAnimation.img_size/2, object.display_y + Unit.unit_size/2 + offset_y - damageAnimation.img_size/2))
          print("animation created")
        #make the targeted_unit lose health
        object.health -= calculate_damage(self, object)
        self.next_action()
    elif self.action == "heal" and object == self:
      btn_pressed_this_frame = True
      #action is a heal order

      self.health += self.regen_value
      #no going over max health
      if self.health > self.max_health:
        self.health = self.max_health
      print("successful heal")
      self.next_action()


    '''
    run this every time a valid action is executed, so the unit moves on to the next action
        try:
          self.action = self.action_sequence[self.action_index + 1]
        except IndexError:
          unit_reset(self)
          self.turn_done = True
'''

    #reset display coords (just in case)
    #these are blit coords
    self.display_x = (self.coord_y - 1)*(-hex_size/4)*sqrt(3)
    self.display_y = (self.coord_y - 1)*(hex_size*0.75)
    self.display_x += (self.coord_x - 1)*(hex_size/2)*sqrt(3)
    #allocate for image size (off of hex_side)
    self.display_x += ((hex_size/2)*sqrt(3))/2
    self.display_y += hex_size/2
    #allocate for image size (off of own image)
    self.display_x -= Unit.unit_size/2
    self.display_y -= Unit.unit_size/2

    #change this later
    #self.turn_done = True
    #self.action_range = [[self.coord_x, self.coord_y]]

    #move on to next action
  def display_hints(self):
    #display the hints for the unit
    #this also calculates the action ranges for the units, not during do_action
    global selected_object, selected_object
    if self.action == "move":
      #get movement_range
      #self.movement_range_placeholder has 2 uses
      #the first one is to make sure the iterable doesn't keep have items added to it which would make a forever loop
      #the second one is to delete all the duplicates and restricts movement range based on bad guy units, because usint the set method does not work since this is a list of lists, not a list of something else
      #some stuff for the float ability
      #set the available terrain as only water and ocean
      #available terrain has no effect on float units; they have a terrain of ocean and water
      if "float" in self.abilities:
        available_terrain_placeholder = deepcopy(Player.player_list[current_player].available_terrain)
        Player.player_list[current_player].available_terrain = ["water", "ocean"]
      for movement_counter in range(self.movement):
        #this next for loop extends self.movement_range by 1 hex in every direction
        self.action_range_placeholder = deepcopy(self.action_range)

        for movement_tile in self.action_range_placeholder:
          if return_occupied(movement_tile[0], movement_tile[1], object = "unit") == False or Player.player_list[current_player].owns_unit(return_occupied(movement_tile[0], movement_tile[1], object = "unit")):
          #if empty spot or player owns dude that is there
            if movement_tile[0] >= 0 and movement_tile[0] <= map_length and movement_tile[1] >= 0 and movement_tile[1] <= map_length:
              #if inside the map
              if MAP[movement_tile[1]][movement_tile[0]].terrain in Player.player_list[current_player].available_terrain:
                #in good terrain?
                self.action_range.extend(return_Adjacent_hex(movement_tile[0], movement_tile[1]))
                #now we have all the hexes we can move to minus the ones blocked by enemy units or bad terrain
      #remove duplicates from list
      self.action_range_placeholder = deepcopy(self.action_range)
      self.action_range.clear()
      for movement_tile in self.action_range_placeholder:
        if movement_tile not in self.action_range and return_occupied(movement_tile[0], movement_tile[1], object = "unit") == False:
          #remove duplicates and places occupied by other ppl
          if movement_tile[0] >= 0 and movement_tile[0] <= map_length and movement_tile[1] >= 0 and movement_tile[1] <= map_length:
            #if inside the map
            if MAP[movement_tile[1]][movement_tile[0]].terrain in Player.player_list[current_player].available_terrain:
              #remove places that are bad terrain
              self.action_range.append(movement_tile)
      if "float" in self.abilities:
        #reset terrain for float units
        Player.player_list[current_player].available_terrain = deepcopy(available_terrain_placeholder)
      #display hints to show the possible move locations
    elif self.action == "attack":
      for attack_counter in range(self.range):
        self.action_range_placeholder = deepcopy(self.action_range)

        for movement_tile in self.action_range_placeholder:
          self.action_range.extend(return_Adjacent_hex(movement_tile[0], movement_tile[1]))
      self.action_range_placeholder = deepcopy(self.action_range)
      self.action_range.clear()
      for movement_tile in self.action_range_placeholder:
        if movement_tile not in self.action_range:
          if return_occupied(movement_tile[0], movement_tile[1], object = "unit") and not Player.player_list[current_player].owns_unit(return_occupied(movement_tile[0], movement_tile[1], object = "unit")):
            self.action_range.append(movement_tile)
      #display hints to show the possible attack locations
    elif self.action == "heal":
      self.action_range = [[self.coord_x, self.coord_y]]
    for hint in self.action_range:
      hint_x = (hint[1] - 1)*(-hex_size/4)*sqrt(3)
      hint_y = (hint[1] - 1)*(hex_size*0.75)
      #for every x:
      hint_x += (hint[0] - 1)*(hex_size/2)*sqrt(3)
      #allocate for image size (off of hex_side)
      hint_x += ((hex_size/2)*sqrt(3))/2
      hint_y += hex_size/2
      pygame.draw.circle(screen, (255, 255, 0), (hint_x + offset_x, hint_y + offset_y), 10)

  def display_stats(self, x, y, text_display_size = 20):
    #x and y should be unit display coords
    #name shown above the unit
    text(text_display_size, str(self.name), (0, 0, 0), x + Unit.unit_size/2, y - 25, alignx = "center")
    #health and regen value shown underneath the unit
    screen.blit(Unit.health_stat_img, (x - 25, y + Unit.unit_size))
    text(text_display_size, str(self.health) + "/" + str(self.max_health) + " (+" + str(self.regen_value) + ")", (255, 0, 140), x, y + Unit.unit_size)
    #attack and defense shown left of the unit
    screen.blit(Unit.attack_stat_img, (x - 25, y))
    text(text_display_size, str(self.attack), (0, 0, 0), x - 25, y, alignx = "right")
    screen.blit(Unit.defense_stat_img, (x - 25, y + 25))
    text(text_display_size, str(self.defense), (0, 0, 0), x - 25, y + 25, alignx = "right")
    #range and movement shown right of the unit
    screen.blit(Unit.range_stat_img, (x + 50, y))
    text(text_display_size, str(self.range), (0, 0, 0), x + 75, y)
    screen.blit(Unit.movement_stat_img, (x + 50, y + 25))
    text(text_display_size, str(self.movement), (0, 0, 0), x + 75, y + 25)
      
#action sequence images
icon_size = 100
move_img = pygame.image.load("unit actions/move.png").convert_alpha()
attack_img = pygame.image.load("unit actions/attack.png").convert_alpha()
heal_img = pygame.image.load("unit actions/heal.png").convert_alpha()
small_icon_size = 50
small_move_img = pygame.transform.scale(move_img, (small_icon_size, small_icon_size))
small_attack_img = pygame.transform.scale(attack_img, (small_icon_size, small_icon_size))
small_heal_img = pygame.transform.scale(heal_img, (small_icon_size, small_icon_size))

skip_action_img = pygame.image.load("unit actions/skip action.png").convert_alpha()

def display_action_sequence(action_sequence, action_index, x, y, mini = False):
  if not mini:
    size = icon_size
    move = move_img
    attack = attack_img
    heal = heal_img
  else:
    size = small_icon_size
    move = small_move_img
    attack = small_attack_img
    heal = small_heal_img
  for action in enumerate(action_sequence):
    if action[0] == action_index:
      #highlight the action icon if this is the current action the unit is taking
      pygame.draw.circle(screen, (255, 0, 255), (action[0]*size + x + size/2, y + size/2), size/2)
    if action[1] == "move":
      screen.blit(move, (action[0]*size + x, y))
    elif action[1] == "attack":
      screen.blit(attack, (action[0]*size + x, y))
    elif action[1] == "heal":
      screen.blit(heal, (action[0]*size + x, y))

'''Player.player_list[0].units.append(Unit(man, 3, 3))
Player.player_list[0].units.append(Unit(man, 4, 4))
Player.player_list[0].units.append(Unit(archer, 3, 5))
Player.player_list[1].units.append(Unit(man, 4, 3))
Player.player_list[1].units.append(Unit(man, 2, 2))
Player.player_list[0].units.append(Unit(ship, 5, 6))
Player.player_list[0].units.append(Unit(steeler, 6, 7))
Player.player_list[0].units.append(Unit(crossbowman, 1, 1))
Player.player_list[0].units.append(Unit(swordsman, 0, 0))'''

def display_buildings(buildings, offset_x, offset_y, p_number, p_color):
  #p_number is the player number
  #this displays a list of specific units (a unit type)
  #units would be a list containing a specific unit type
  for a_building in buildings:
    shadeTile(a_building.coord_x, a_building.coord_y, p_color)
    screen.blit(a_building.image, (a_building.display_x + offset_x, a_building.display_y + offset_y))
    if a_building.production[0] > 0 or a_building.production[1] > 0 or a_building.production[2] > 0:
      pygame.draw.rect(screen, (122, 122, 122), (a_building.display_x + offset_x, a_building.display_y + offset_y + Building.building_size*0.85, Building.building_size, 10))
      pygame.draw.rect(screen, (255, 0, 255), (a_building.display_x + offset_x, a_building.display_y + offset_y + Building.building_size*0.85, Building.building_size*((a_building.production_timer + 1)/a_building.production_time), 10))
      #the +1 is for UI ease
      if a_building.production_timer + 1 == a_building.production_time:
        pygame.draw.rect(screen, (0, 255, 0), (a_building.display_x + offset_x, a_building.display_y + offset_y + Building.building_size*0.85, Building.building_size, 10))
      for level_counter in range(a_building.production_time + 1):
        pygame.draw.line(screen, (0, 0, 0), (a_building.display_x + offset_x + level_counter*(Building.building_size/a_building.production_time), a_building.display_y + offset_y + Building.building_size*0.85), (a_building.display_x + offset_x + level_counter*(Building.building_size/a_building.production_time), a_building.display_y + offset_y + Building.building_size*0.85 + 10), 2)
    text(25, str(p_number + 1), (255, 255, 255), a_building.display_x + offset_x + Building.building_size/2, a_building.display_y + offset_y + Building.building_size/2, alignx = "center", aligny = "center")

class Building:
  #building constructor
  #buildings can only be built where a unit of the same player is
  #buildings are destroyed when other player units move on top of it
  building_size = 75
  cooldown_stat_img = pygame.image.load("stats/cooldown.png").convert_alpha()
  lumber_hut_img = pygame.image.load("building/lumber hut.png").convert_alpha()
  mine_img = pygame.image.load("building/mine.png").convert_alpha()
  shipyard_img = pygame.image.load("building/shipyard.png").convert_alpha()
  farm_img = pygame.image.load("building/farm.png").convert_alpha()
  plantation_img = pygame.image.load("building/plantation.png").convert_alpha()
  foundry_img = pygame.image.load("building/foundry.png").convert_alpha()
  img_dict = {"Lumber Hut":lumber_hut_img, "Mine":mine_img, "Shipyard":shipyard_img, "Farm":farm_img, "Plantation":plantation_img, "Foundry":foundry_img}
  def __init__(self, stats, x, y):
    self.coord_x = x
    self.coord_y = y
    #these are blit coords
    self.display_x = (self.coord_y - 1)*(-hex_size/4)*sqrt(3)
    self.display_y = (self.coord_y - 1)*(hex_size*0.75)
    self.display_x += (self.coord_x - 1)*(hex_size/2)*sqrt(3)
    #allocate for image size (off of hex_side)
    self.display_x += ((hex_size/2)*sqrt(3))/2
    self.display_y += hex_size/2
    #allocate for image size (off of own image)
    self.display_x -= Building.building_size/2
    self.display_y -= Building.building_size/2
    #get stats from list
    self.name = stats[0]
    self.cost = stats[1]
    #cost is [money, wood, metal, food]
    self.production = stats[2]
    self.production_time = stats[3]
    self.production_timer = 0
    #production is [wood, metal, food]
    #production_time is how many turns it takes for the materials to be produced
    #add them to player resources when end_turn button is clicked
    self.terrain = stats[4]
    #this is a list of the terrain types that the building can be built on
    self.abilities = stats[5]
    self.image = pygame.image.load("building/"+str(self.name).lower()+".png").convert_alpha()
    #upgrade should be a list of the building stats
    self.upgraded_building = stats[6]
  def produce(self):
    #this is where the building produces resources
    #run this in the end_turn button clicked
    self.production_timer += 1
    if self.production_timer == self.production_time:
      for _ in range(self.production[0]):
        animation_list.append(resourceAnimation([0, 1, 0, 0], randint(round(self.display_x + offset_x + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_x + offset_x + City.city_size/2 + resourceAnimation.animation_range/2)), randint(round(self.display_y + offset_y + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_y + offset_y + City.city_size/2 + resourceAnimation.animation_range/2)), SCREENLENGTH - 12.5, 87.5, 25, wood_resource_img))
      for _ in range(self.production[1]):
        animation_list.append(resourceAnimation([0, 0, 1, 0], randint(round(self.display_x + offset_x + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_x + offset_x + City.city_size/2 + resourceAnimation.animation_range/2)), randint(round(self.display_y + offset_y + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_y + offset_y + City.city_size/2 + resourceAnimation.animation_range/2)), SCREENLENGTH - 12.5, 122.5, 25, metal_resource_img))
      self.production_timer = 0
      if "cultivate" in self.abilities and [self.coord_x, self.coord_y] in crop:
        for _ in range(self.production[2]):
          animation_list.append(resourceAnimation([0, 0, 0, 1], randint(round(self.display_x + offset_x + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_x + offset_x + City.city_size/2 + resourceAnimation.animation_range/2)), randint(round(self.display_y + offset_y + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_y + offset_y + City.city_size/2 + resourceAnimation.animation_range/2)), SCREENLENGTH - 12.5, 137.5, 25, food_resource_img))
        MAP[self.coord_y][self.coord_x].features.remove("crop")
        MAP[self.coord_y][self.coord_x].features.append("harvested crop")
  def display_stats(self, x, y, text_display_size = 20):
    #change these to imgs later
    text(text_display_size, str(self.name), (0, 0, 0), x + 37.5, y - 15, alignx = "center")
    if self.production[0] > 0 or self.production[1] > 0 or self.production[2] > 0:
      screen.blit(production_frame, (x + 85, y - 33))
      text(text_display_size, "Produce ", (0, 0, 0), x + 135, y - 25, alignx = "center")
      display_resources([0, self.production[0], self.production[1], self.production[2]], x + 125, y)
      screen.blit(Building.cooldown_stat_img, (x - 12.5, y + 75))
      text(text_display_size, str(self.production_timer + 1) + "/" + str(self.production_time) + " turns", (255, 0, 0), x + 12.5, y + 75)
      if self.production_timer + 1 == self.production_time:
        text(text_display_size, str(self.production_timer + 1) + "/" + str(self.production_time) + " turns", (0, 184, 0), x + 12.5, y + 75)
  def upgrade(self):
    global selected_object
    #buildings can only be upgraded into one building
    Player.player_list[current_player].buildings.append(Building(self.upgraded_building, self.coord_x, self.coord_y))
    selected_object = Player.player_list[current_player].buildings[-1]
    Player.player_list[current_player].buildings.remove(self)

'''Player.player_list[0].available_upgraded_buildings.append(plantation)
Player.player_list[0].buildings.append(Building(shipyard, 4, 5))
Player.player_list[0].buildings.append(Building(mine, 2, 1))'''

def display_cities(cities, offset_x, offset_y, p_number, p_color):
  for a_city in cities:
    shadeTile(a_city.coord_x, a_city.coord_y, p_color)
    screen.blit(a_city.image, (a_city.display_x + offset_x, a_city.display_y + offset_y))
    pygame.draw.rect(screen, (0, 255, 0), (a_city.display_x + offset_x, a_city.display_y + offset_y + City.city_size*0.85, City.city_size, 10))
    pygame.draw.rect(screen, (0, 0, 255), (a_city.display_x + offset_x, a_city.display_y + offset_y + City.city_size*0.85, City.city_size*(a_city.spawn_timer/a_city.max_spawn_timer), 10))
    if a_city.spawn_timer >= a_city.max_spawn_timer:
      pygame.draw.rect(screen, (255, 0, 0), (a_city.display_x + offset_x, a_city.display_y + offset_y + City.city_size*0.85, City.city_size*(a_city.spawn_timer/a_city.max_spawn_timer), 10))
    for level_counter in range(a_city.level + 1):
      pygame.draw.line(screen, (0, 0, 0), (a_city.display_x + offset_x + level_counter*(City.city_size/a_city.level), a_city.display_y + offset_y + City.city_size*0.85), (a_city.display_x + offset_x + level_counter*(City.city_size/a_city.level), a_city.display_y + offset_y + City.city_size*0.85 + 10), 2)
    text(25, str(p_number + 1), (255, 255, 255), a_city.display_x + offset_x + City.city_size/2, a_city.display_y + offset_y + City.city_size/2, alignx = "center", aligny = "center")

class City:
  #building constructor
  #buildings can only be built where a unit of the same player is
  #buildings are destroyed when other player units move on top of it
  city_size = 75
  max_level = 5
  #this means reduce the cooldown timer by 25% every end_turn
  spawn_cooldown = 0.25
  cooldown_img = pygame.image.load("stats/timer.png").convert_alpha()
  upgrade_img = pygame.image.load("city/upgrade.png")
  def __init__(self, x, y, player_number = None, level = 1):
    self.coord_x = x
    self.coord_y = y
    #these are blit coords
    self.display_x = (self.coord_y - 1)*(-hex_size/4)*sqrt(3)
    self.display_y = (self.coord_y - 1)*(hex_size*0.75)
    self.display_x += (self.coord_x - 1)*(hex_size/2)*sqrt(3)
    #allocate for image size (off of hex_side)
    self.display_x += ((hex_size/2)*sqrt(3))/2
    self.display_y += hex_size/2
    #allocate for image size (off of own image)
    self.display_x -= City.city_size/2
    self.display_y -= City.city_size/2
    self.player_number = player_number
    self.level = level
    self.image = pygame.image.load("city/"+str(self.level)+".png").convert_alpha()
    self.income = [self.level * 5, self.level, self.level, self.level]
    self.cost = [self.level**2 * 5, self.level**2, self.level**2, self.level**2]
    #prevent unit spamming
    self.spawn_timer = 0
    self.max_spawn_timer = self.level * 10
  def produce(self):
    #this is where the city produces money
    #run this in the end_turn button clicked
    #add for loop for animation
    for _ in range(self.income[0]):
      animation_list.append(resourceAnimation([1, 0, 0, 0], randint(round(self.display_x + offset_x + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_x + offset_x + City.city_size/2 + resourceAnimation.animation_range/2)), randint(round(self.display_y + offset_y + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_y + offset_y + City.city_size/2 + resourceAnimation.animation_range/2)), SCREENLENGTH - 12.5, 62.5, 25, money_resource_img))
    #Player.player_list[current_player].money += 
    for _ in range(self.income[1]):
      animation_list.append(resourceAnimation([0, 1, 0, 0], randint(round(self.display_x + offset_x + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_x + offset_x + City.city_size/2 + resourceAnimation.animation_range/2)), randint(round(self.display_y + offset_y + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_y + offset_y + City.city_size/2 + resourceAnimation.animation_range/2)), SCREENLENGTH - 12.5, 87.5, 25, wood_resource_img))
    for _ in range(self.income[2]):
      animation_list.append(resourceAnimation([0, 0, 1, 0], randint(round(self.display_x + offset_x + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_x + offset_x + City.city_size/2 + resourceAnimation.animation_range/2)), randint(round(self.display_y + offset_y + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_y + offset_y + City.city_size/2 + resourceAnimation.animation_range/2)), SCREENLENGTH - 12.5, 112.5, 25, metal_resource_img))
    for _ in range(self.income[3]):
      animation_list.append(resourceAnimation([0, 0, 0, 1], randint(round(self.display_x + offset_x + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_x + offset_x + City.city_size/2 + resourceAnimation.animation_range/2)), randint(round(self.display_y + offset_y + City.city_size/2 - resourceAnimation.animation_range/2), round(self.display_y + offset_y + City.city_size/2 + resourceAnimation.animation_range/2)), SCREENLENGTH - 12.5, 137.5, 25, food_resource_img))
  def upgrade(self):
    self.level += 1
    self.income[0] += 5
    self.income[1] += 1
    self.income[2] += 1
    self.income[3] += 1
    Player.player_list[current_player].money -= self.cost[0]
    Player.player_list[current_player].wood -= self.cost[1]
    Player.player_list[current_player].metal -= self.cost[2]
    Player.player_list[current_player].food -= self.cost[3]
    self.cost = [self.level**2 * 5, self.level**2, self.level**2, self.level**2]
    self.max_spawn_timer += 10
    self.image = pygame.image.load("city/"+str(self.level)+".png").convert_alpha()
  def display_stats(self, x, y, text_display_size = 20):
    text(text_display_size, "Level " + str(self.level), (0, 0, 0), x + 75, y - 12.5, alignx= "center")
    display_resources(self.income, x + 150, y - 25)
    screen.blit(City.cooldown_img, (x + 75, y + 37.5))
    text(text_display_size, str(self.spawn_timer) + "/" + str(self.max_spawn_timer), (0, 255, 0), x + 100, y + 37.5)
    if self.spawn_timer >= self.max_spawn_timer:
      text(text_display_size, str(self.spawn_timer) + "/" + str(self.max_spawn_timer), (255, 0, 0), x + 100, y + 37.5)
    

Player.player_list[0].cities.append(City(2, 1, player_number = 0))
Player.player_list[1].cities.append(City(4, 6, player_number = 1))

def return_occupied(x, y, object):
  #this returns the occupants of a hex
  #x and y are the coords of the hex
  #these are hex positions, not blit coords
  for player in Player.player_list:
    if object == "unit":
      for an_object in player.units:
        if an_object.coord_x == x and an_object.coord_y == y:
          return an_object
    elif object == "building":
      for an_object in player.buildings:
        if an_object.coord_x == x and an_object.coord_y == y:
          return an_object
    elif object == "city":
      for a_city in player.cities:
        if a_city.coord_x == x and a_city.coord_y == y:
          return a_city
  return False

#resource colors
money_color = (229, 184, 11)
wood_color = (124, 71, 0)
metal_color = (185, 185, 185)
food_color = (66, 25, 33)
money_resource_img = pygame.image.load("resource/money.png").convert_alpha()
wood_resource_img = pygame.image.load("resource/wood.png").convert_alpha()
metal_resource_img = pygame.image.load("resource/metal.png").convert_alpha()
food_resource_img = pygame.image.load("resource/food.png").convert_alpha()

def display_resources(resources, x, y, display_all = False, size = 20):
  #x is the line between the images and the numbers
  #resources is [money, wood, metal, food]
  display_counter = 0
  cushion = 25
  text_offset_y = 12.5
  if display_all:
    text(size, str(resources[0]), money_color, x, y + text_offset_y, alignx = "right", aligny = "center")
    screen.blit(money_resource_img, (x, y))
    display_counter += 1
    text(size, str(resources[1]), wood_color, x, y + display_counter * cushion + text_offset_y, alignx = "right", aligny = "center")
    screen.blit(wood_resource_img, (x, y + display_counter * cushion))
    display_counter += 1
    text(size, str(resources[2]), metal_color, x, y + display_counter * cushion + text_offset_y, alignx = "right", aligny = "center")
    screen.blit(metal_resource_img, (x, y + display_counter * cushion))
    display_counter += 1
    text(size, str(resources[3]), food_color, x, y + display_counter * cushion + text_offset_y, alignx = "right", aligny = "center")
    screen.blit(food_resource_img, (x, y + display_counter * cushion))
  
  else:
    if resources[0] > 0:
      text(size, str(resources[0]), money_color, x, y + text_offset_y, alignx = "right", aligny = "center")
      screen.blit(money_resource_img, (x, y))
      display_counter += 1
    if resources[1] > 0:
      text(size, str(resources[1]), wood_color, x, y + display_counter * cushion + text_offset_y, alignx = "right", aligny = "center")
      screen.blit(wood_resource_img, (x, y + display_counter * cushion))
      display_counter += 1
    if resources[2] > 0:
      text(size, str(resources[2]), metal_color, x, y + display_counter * cushion + text_offset_y, alignx = "right", aligny = "center")
      screen.blit(metal_resource_img, (x, y + display_counter * cushion))
      display_counter += 1
    if resources[3] > 0:
      text(size, str(resources[3]), food_color, x, y + display_counter * cushion + text_offset_y, alignx = "right", aligny = "center")
      screen.blit(food_resource_img, (x, y + display_counter * cushion))
  

class Tech:
  tech_size = 100
  def __init__(self, stats):
    #stats = [name, cost, x, y, preceding_tech, unit, building, player_action, terrain]
    #x and y are where they should be displayed
    self.name = stats[0]
    self.cost = stats[1]
    #cost is only a number because it is only money
    self.display_x = stats[2]
    self.display_y = stats[3]
    self.preceding_tech = stats[4]
    #preceding tech should be the entire tech, not the class object, which would be a list of stats
    #preceding_tech[0] would be the name; use this in owns_tech
    self.unit = stats[5]
    self.building = stats[6]
    self.upgraded_building = stats[7]
    self.player_action = stats[8]
    self.terrain = stats[9]
    self.img = stats[10]
    if self.unit != None:
      if "float" in self.unit[10]:
        Player.player_list[current_player].available_naval_units.append(self.unit)
      else:
        Player.player_list[current_player].available_units.append(self.unit)
    if self.building != None:
      Player.player_list[current_player].available_buildings.append(self.building)
    if self.upgraded_building != None:
      Player.player_list[current_player].available_upgraded_buildings.append(self.upgraded_building)
    if self.player_action != None:
      Player.player_list[current_player].available_actions.append(self.player_action)
    if self.terrain != None:
      Player.player_list[current_player].available_terrain.append(self.terrain)

tech_offset_x = 0
tech_offset_y = 0
#tech = ["Tech", price, x, y, preceding_tech, unit, building, upgraded building, player action, terrain, img]
logging_img = pygame.image.load("tech/logging.png").convert_alpha()
logging = ["Logging", 5, 50, 500, None, None, None, None, "chop", None, logging_img]
archery_img = pygame.image.load("tech/archery.png").convert_alpha()
archery = ["Archery", 10, 100, 300, logging, archer, None, None, None, None, archery_img]
engineering_img = pygame.image.load("tech/engineering.png").convert_alpha()
engineering = ["Engineering", 20, 100, 100, archery, crossbowman, None, None, None, None, engineering_img]
forestry_img = pygame.image.load("tech/forestry.png").convert_alpha()
forestry = ["Forestry", 10, 250, 300, logging, None, lumber_hut, None, None, None, forestry_img]
reforestation_img = pygame.image.load("tech/reforestation.png").convert_alpha()
reforestation = ["Reforestation", 20, 250, 100, forestry, None, None, None, "grow", None, reforestation_img]
climbing_img = pygame.image.load("tech/climbing.png").convert_alpha()
climbing = ["Climbing", 5, 350, 500, None, None, None, None, None, "mountain", climbing_img]
smithery_img = pygame.image.load("tech/smithery.png").convert_alpha()
smithery = ["Smithery", 15, 350, 300, climbing, swordsman, None, None, None, None, smithery_img]
sharpening_img = pygame.image.load("tech/sharpening.png").convert_alpha()
sharpening = ["Sharpening", 25, 450, 100, smithery, spearman, None, None, None, None, sharpening_img]
armoring_img = pygame.image.load("tech/armoring.png")
armoring = ["Armoring", 25, 350, 150, smithery, shieldman, None, None, None, None, armoring_img]
mining_img = pygame.image.load("tech/mining.png").convert_alpha()
mining = ["Mining", 10, 475, 300, climbing, None, mine, None, None, None, mining_img]
smelting_img = pygame.image.load("tech/smelting.png").convert_alpha()
smelting = ["Smelting", 25, 550, 100, mining, None, None, foundry, None, None, smelting_img]
swimming_img = pygame.image.load("tech/swimming.png").convert_alpha()
swimming = ["Swimming", 5, 500, 500, None, None, None, None, None, "water", swimming_img]
sailing_img = pygame.image.load("tech/sailing.png").convert_alpha()
sailing = ["Sailing", 10, 600, 300, swimming, None, shipyard, None, None, None, sailing_img]
harvesting_img = pygame.image.load("tech/harvesting.png").convert_alpha()
harvesting = ["Harvesting", 5, 800, 500, None, None, None, None, "cultivate", None, harvesting_img]
agriculture_img = pygame.image.load("tech/agriculture.png").convert_alpha()
agriculture = ["Agriculture", 10, 750, 300, harvesting, None, farm, None, None, None, agriculture_img]
fertilization_img = pygame.image.load("tech/fertilization.png").convert_alpha()
fertilization = ["Fertilization", 25, 775, 100, agriculture, None, None, plantation, None, None, fertilization_img]
riding_img = pygame.image.load("tech/riding.png").convert_alpha()
riding = ["Riding", 12, 850, 300, harvesting, rider, None, None, None, None, riding_img]
all_techs = [logging, archery, engineering, forestry, reforestation, climbing, smithery, sharpening, armoring, mining, smelting, swimming, sailing, harvesting, riding, agriculture, fertilization]

animating = False
animation_list = []
class Animation:
  def __init__(self, x, y, img, img_size):
    self.x = x
    self.y = y
    self.img = img
    self.img_size = img_size
  def update(self):
    self.x += self.velx
    self.y += self.vely
    try:
      self.distance_traveled += sqrt(self.velx**2 + self.vely**2)
    except:
      pass
    #the blit coords will be where the img center is
    screen.blit(self.img, (self.x - self.img_size/2, self.y - self.img_size/2))
class resourceAnimation(Animation):
  sprite_speed = 12
  animation_range = 80
  img_size = 25
  def __init__(self, value, x, y, targetx, targety, targetsize, img):
    super().__init__(x, y, img, resourceAnimation.img_size)
    #value should be a list containing the resource of the thing
    self.value = value
    self.targetx = targetx
    self.targety = targety
    self.targetsize = targetsize
    self.velx, self.vely = get_vel(self.x, self.y, self.targetx, self.targety, resourceAnimation.sprite_speed)
class damageAnimation(Animation):
  sprite_speed = 6
  max_distance = 100
  img = pygame.image.load("stats/health.png").convert_alpha()
  img_size = 25
  def __init__(self, x, y):
    super().__init__(x, y, damageAnimation.img, damageAnimation.img_size)
    self.velx, self.vely = pygame.math.Vector2(0, damageAnimation.sprite_speed).rotate(randint(0, 360))
    self.distance_traveled = 0
class attackAnimation(Animation):
  sprite_speed = 10
  size = 50
  def __init__(self, x, y, img, start, end):
    super().__init__(x, y, attackAnimation.size)
def destroyAnimation():
  deletion_counter = 0
  while deletion_counter < len(animation_list):
    #building_type will be a list of a specific building type
    sprite = animation_list[deletion_counter]
    if isinstance(sprite, resourceAnimation):
      if rect_collided(sprite.x, sprite.y, sprite.img_size, sprite.img_size, sprite.targetx, sprite.targety, sprite.targetsize, sprite.targetsize):
        for _ in enumerate(sprite.value):
          if _[0] == 0:
            Player.player_list[current_player].money += _[1]
          elif _[0] == 1:
            Player.player_list[current_player].wood += _[1]
          elif _[0] == 2:
            Player.player_list[current_player].metal += _[1]
          elif _[0] == 3:
            Player.player_list[current_player].food += _[1]
        animation_list.pop(deletion_counter)
        continue
    elif isinstance(sprite, damageAnimation):
      if sprite.distance_traveled >= damageAnimation.max_distance:
        animation_list.pop(deletion_counter)
        continue
    deletion_counter += 1

recieving_input = False
def receive_input(class_object):
  global mouse_clicked, MAP, map_length, receiving_input, selected_collision_range
  receiving_input = True
  if mouse_clicked and btn_pressed_this_frame == False:
    if class_object == "unit":
      for player in Player.player_list:
          for unit in player.units:
            if circle_collided(mouse_pos[0], mouse_pos[1], 1, unit.display_x + Unit.unit_size/2 + offset_x, unit.display_y + Unit.unit_size/2 + offset_y, selected_collision_range/2):
              return unit
    elif class_object == "building":
      for player in Player.player_list:
          for building in player.buildings:
            if circle_collided(mouse_pos[0], mouse_pos[1], 1, building.display_x + Building.building_size/2 + offset_x, Building.display_y + Building.building_size/2 + offset_y, selected_collision_range/2):
              return building
    elif class_object == "city":
      for player in Player.player_list:
          for city in player.cities:
            if circle_collided(mouse_pos[0], mouse_pos[1], 1, city.display_x + City.city_size/2 + offset_x, City.display_y + City.city_size/2 + offset_y, selected_collision_range/2):
              return city
    elif class_object == "location":
      for row in enumerate(MAP):
        for tile in enumerate(row[1]):
          if circle_collided(mouse_pos[0], mouse_pos[1], 1, tile[1].display_x + offset_x + hex_size*sqrt(3)/4, tile[1].display_y + offset_y + hex_size/2, selected_collision_range/2):
            if tile[0] >= 0 and tile[0] <= map_length and row[0] >= 0 and row[0] <= map_length:
              if tile[1].terrain != "":
                return tile[1]
    receiving_input = False
  return None
selection_order = [Unit, Building, City, Location, None]
selection_counter = 0
def alternate_selection():
  global selected_object, selection_order, btn_pressed_this_frame
  for object_type in selection_order[selection_order.index(type(selected_object))+1:]:
    if object_type == Unit:
      if return_occupied(selected_object.coord_x, selected_object.coord_y, "unit"):
        btn_pressed_this_frame = True
        return return_occupied(selected_object.coord_x, selected_object.coord_y, "unit")
    elif object_type == Building:
      if return_occupied(selected_object.coord_x, selected_object.coord_y, "building"):
        btn_pressed_this_frame = True
        return return_occupied(selected_object.coord_x, selected_object.coord_y, "building")
    elif object_type == City:
      if return_occupied(selected_object.coord_x, selected_object.coord_y, "city"):
        btn_pressed_this_frame = True
        return return_occupied(selected_object.coord_x, selected_object.coord_y, "city")
    elif object_type == Location:
      btn_pressed_this_frame = True
      return MAP[selected_object.coord_y][selected_object.coord_x]
    elif object_type == None:
      btn_pressed_this_frame = True
      return None
  return None

def same_space(location):
  #contrasts a thing with selected_object
  #returns if 2 things are in the same place
  global selected_object
  if selected_object == None:
    return False
  location2 = (selected_object.coord_x, selected_object.coord_y)
  if location == location2:
    return True
  else:
    return False
  

while True:
  while status == "home":
    screen.fill((255, 255, 255, 255))
    pressed_keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = list(mouse_pos)
    btn_pressed_this_frame = False
    
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
        mouse_down = True
        if mouse_up == True:
          mouse_clicked = True
          mouse_up = False
      if event.type == pygame.MOUSEBUTTONUP:
        mouse_up = True
        mouse_down = False
    if button(400, 450, 200, 100, 10):
      #Player.player_list[current_player].turn_update()
      #this allows Player1 to get his resources, since you only get resources when the player before you ends turn
      #this makes it equal
      #or we can take this line away because player1 already has advantage of going first, so maybe he shouldn't get resources
      status = "playing"
    if mouse_clicked:
      mouse_clicked = False
    clock.tick(FPS)
    pygame.display.update()

  while status == "playing":
    screen.fill((255, 255, 255))
    transparent_screen.fill((255, 255, 255, 0))
    pressed_keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = list(mouse_pos)
    #remember to reset this variable so buttons and selections aren't activated at the same time
    btn_pressed_this_frame = False
    receiving_input = False
    animating = False
    if animation_list != []:
      animating = True
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_x:
          pygame.quit()
          sys.exit()
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN and not animating:
        mouse_down = True
        if mouse_up == True:
          mouse_clicked = True
          mouse_up = False
      if event.type == pygame.MOUSEBUTTONUP:
        mouse_up = True
        mouse_down = False

    #move the screen around by arrow keys
    if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
      offset_y += 10
    if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
      offset_y -= 10
    if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
      offset_x += 10
    if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
      offset_x -= 10

    display_map_hex(MAP)
    #create a rect area for selected, targeted, and location
    screen.blit(selection_frame, (0, 0))

    #display selected object
    
    text(20, "Selected:", (0, 0, 255), 0, 50)
    #displaying the selected object at the corner of screen depending on what it is
    if selected_object != None:
      if isinstance(selected_object, Unit):
        #display unit stats
        screen.blit(selected_object.image, (50, 100))
        selected_object.display_stats(50, 100)
        if selected_object.turn_done == False:
          display_action_sequence(selected_object.action_sequence, selected_object.action_index, 0, 300)
          
      elif isinstance(selected_object, Building):
        #display building stats
        screen.blit(selected_object.image, (12.5, 87.5))
        selected_object.display_stats(12.5, 87.5)
          #the +1 is for UI ease; the user will see eg 2/2 turns and know that there is a production this turn, not 1/2 turns and 0/2 turns

      elif isinstance(selected_object, City):
        screen.blit(selected_object.image, (0, 87.5))
        selected_object.display_stats(0, 87.5)
    #display selected location on left side of map
      elif isinstance(selected_object, Location):
        selected_object.display(custom = (0, 100))
        screen.blit(location_img, (0, 100))
        if Player.player_list[current_player].owns_unit(return_occupied(selected_object.coord_x, selected_object.coord_y, "unit")):
          screen.blit(unit_location_img, (0, 100))
        elif Player.player_list[current_player].owns_building(return_occupied(selected_object.coord_x, selected_object.coord_y, "building")):
          screen.blit(location_select_img, (0, 100))
        elif Player.player_list[current_player].owns_city(return_occupied(selected_object.coord_x, selected_object.coord_y, "city")):
          screen.blit(location_select_img, (0, 100))
        #capitalize the first letter of the location
        text(20, str(selected_object.terrain)[0].upper() + str(selected_object.terrain)[1:].lower(), (0, 0, 0), 44, 75, alignx = "center")

    if isinstance(selected_object, Unit):
      #if button(50, SCREENHEIGHT - 100, 100, 50, 10, available = selected_object.action != None):
      #if submit button is clicked
      #do unit action
      if selected_object.turn_done == False:
        try:
          if selected_object.action == "move":
            selected_object.do_action(receive_input("location"))
            if list(receive_input("location")) not in selected_object.action_range:
              receiving_input = False
              btn_pressed_this_frame = False
          elif selected_object.action == "attack":
            selected_object.do_action(receive_input("unit"))
            if [receive_input("unit").coord_x, receive_input("unit").coord_y] not in selected_object.action_range:
              #if player owns the targeted object, switch to that object
              receiving_input = False
              btn_pressed_this_frame = False
          elif selected_object.action == "heal":
            selected_object.do_action(receive_input("unit"))
            if [receive_input("unit").coord_x, receive_input("unit").coord_y] not in selected_object.action_range:
              #if player owns the targeted object, switch to that object
              receiving_input = False
              btn_pressed_this_frame = False
        except:
          #player did not give input yet
          pass

    if button(50, 0, 100, 50, 10):
      selected_object = None

    if button(375, 0, 100, 50, 10):
      status = "tech tree"
    text(30, "Tech", (0, 0, 0), 425, 25, alignx = "center", aligny = "center")
    
      #action skip button is clicked
    if isinstance(selected_object, Unit) and selected_object.action_sequence != [] and selected_object.turn_done == False:
      if button(25, 175, 125, 125, 10):
        selected_object.next_action()
      screen.blit(skip_action_img, (50, 212.5))
      text(25, "Skip Action", (0, 0, 0), 87.5, 200, alignx = "center", aligny = "center")

    if button(SCREENLENGTH - 100, SCREENHEIGHT - 125, 100, 100, 10):
      #if end_turn button is clicked
      Player.player_list[current_player].turn_update_after()
      current_player += 1
      if current_player == player_count:
        current_player = 0
      print("turn ended... moving on to player", current_player)
      Player.player_list[current_player].turn_update_before()
    text(25, "End Turn", (0, 0, 0), SCREENLENGTH - 50, SCREENHEIGHT - 75, alignx = "center", aligny = "center")

    #display player_number
    text(25, str("Player " + str(current_player + 1)) + " turn", Player.player_list[current_player].color, SCREENLENGTH, 0, alignx = "right")
    display_resources([Player.player_list[current_player].money, Player.player_list[current_player].wood, Player.player_list[current_player].metal, Player.player_list[current_player].food], SCREENLENGTH - 25, 50, display_all = True, size = 40)

    #these are all the possible things a player can do: choose unit action, upgrade building, build ships, spawn units, upgrade city, do player actions
    #choose unit sequence
    if isinstance(selected_object, Unit) and selected_object in Player.player_list[current_player].units and selected_object.turn_done == False:
      if selected_object.action_sequence == []:
        for choice in enumerate(selected_object.action_sequences):
          if button(0, option_x + choice[0] * 50, len(choice[1]) * small_icon_size, 50, 10):
            selected_object.action_sequence = choice[1]
            selected_object.action = selected_object.action_sequence[0]
            selected_object.action_index = 0
            selected_object.action_range = [[selected_object.coord_x, selected_object.coord_y]]
            print(selected_object.action_sequence)
            break
          display_action_sequence(choice[1], -1, 0, option_x + choice[0] * 50, mini = True)
    elif isinstance(selected_object, Building) and selected_object in Player.player_list[current_player].buildings:
      if Player.player_list[current_player].owns_unit(return_occupied(selected_object.coord_x, selected_object.coord_y, object = "unit")):
        #upgrade a building if there's a dude on it
        if selected_object.upgraded_building in Player.player_list[current_player].available_upgraded_buildings:
          #if there is no upgraded building, it would be: if None in available buildings, so that would be false
          if button(25, 200, Building.building_size*2, Building.building_size*2, 10, available = bool(Player.player_list[current_player].money >= selected_object.upgraded_building[1][0] and Player.player_list[current_player].wood >= selected_object.upgraded_building[1][1] and Player.player_list[current_player].metal >= selected_object.upgraded_building[1][2] and Player.player_list[current_player].food >= selected_object.upgraded_building[1][3])):
            selected_object.upgrade()
            Player.player_list[current_player].money -= selected_object.cost[0]
            Player.player_list[current_player].wood -= selected_object.cost[1]
            Player.player_list[current_player].metal -= selected_object.cost[2]
            Player.player_list[current_player].food -= selected_object.cost[3]
          if selected_object.upgraded_building != None:
            screen.blit(Building.img_dict[selected_object.upgraded_building[0]], (37.5, 262.5))
            text(20, selected_object.upgraded_building[0], (0, 0, 0), 75, 250, alignx = "center", aligny = "center")
            display_resources(selected_object.upgraded_building[1], 150, 237.5)
          text(25, "Upgrade", (0, 0, 0), 100, 225, alignx = "center", aligny = "center")
      #build ships
      if "shipbuilding" in selected_object.abilities:
        if not return_occupied(selected_object.coord_x, selected_object.coord_y, "unit"):
          #make ship if no dude is on it
          for unit_type in enumerate(Player.player_list[current_player].available_naval_units):
            if button((Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2), Unit.unit_size * 2, Unit.unit_size * 2, 10, available = bool(Player.player_list[current_player].money >= unit_type[1][7][0] and Player.player_list[current_player].wood >= unit_type[1][7][1] and Player.player_list[current_player].metal >= unit_type[1][7][2] and Player.player_list[current_player].food >= unit_type[1][7][3])):
              print(unit_type[1][0] + " naval unit is spawned")
              Player.player_list[current_player].money -= unit_type[1][7][0]
              Player.player_list[current_player].wood -= unit_type[1][7][1]
              Player.player_list[current_player].metal -= unit_type[1][7][2]
              Player.player_list[current_player].food -= unit_type[1][7][3]
              Player.player_list[current_player].units.append(Unit(unit_type[1], selected_object.coord_x, selected_object.coord_y))
              unit_reset(Player.player_list[current_player].units[-1])
              Player.player_list[current_player].units[-1].turn_done = True
              print("turn done")
            screen.blit(Unit.img_dict[unit_type[1][0]], (0, option_x + 25 + unit_type[0] * 50))
            text(20, unit_type[1][0], (0, 0, 0), (Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2))
            display_resources(unit_type[1][7], (Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack) + 75, option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2))
    elif isinstance(selected_object, City) and selected_object in Player.player_list[current_player].cities:
      if not return_occupied(selected_object.coord_x, selected_object.coord_y, "unit"):
      #if a city is selected and there's no dude on it to avoid spawning more than 1 dude
        for unit_type in enumerate(Player.player_list[current_player].available_units):
          if selected_object.spawn_timer < selected_object.max_spawn_timer:
            if button((Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2), Unit.unit_size * 2, Unit.unit_size * 2, 10, available = bool(Player.player_list[current_player].money >= unit_type[1][7][0] and Player.player_list[current_player].wood >= unit_type[1][7][1] and Player.player_list[current_player].metal >= unit_type[1][7][2] and Player.player_list[current_player].food >= unit_type[1][7][3])):
              print(unit_type[1][0] + " unit is spawned")
              Player.player_list[current_player].money -= unit_type[1][7][0]
              Player.player_list[current_player].wood -= unit_type[1][7][1]
              Player.player_list[current_player].metal -= unit_type[1][7][2]
              Player.player_list[current_player].food -= unit_type[1][7][3]
              #add spawn_cooldown to city
              selected_object.spawn_timer += unit_type[1][8]
              Player.player_list[current_player].units.append(Unit(unit_type[1], selected_object.coord_x, selected_object.coord_y))
              unit_reset(Player.player_list[current_player].units[-1])
              Player.player_list[current_player].units[-1].turn_done = True
              print("turn done")
          else:
            pygame.draw.rect(screen, (255, 0, 0), ((Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2), Unit.unit_size * 2, Unit.unit_size * 2), width = 0, border_radius = 10)
          screen.blit(Unit.img_dict[unit_type[1][0]], ((Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2) + 25))
          text(20, unit_type[1][0], (0, 0, 0), (Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack), option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2))
          display_resources(unit_type[1][7], (Unit.unit_size*2)*(unit_type[0]//Unit.unit_max_stack) + 75, option_x + (unit_type[0]%Unit.unit_max_stack) * (Unit.unit_size*2))
      #upgrade button
      if selected_object.level < City.max_level:
        if button(25, 200, City.city_size*2, City.city_size*2, 10, available = bool(Player.player_list[current_player].money >= selected_object.cost[0] and Player.player_list[current_player].wood >= selected_object.cost[1] and Player.player_list[current_player].metal >= selected_object.cost[2] and Player.player_list[current_player].food >= selected_object.cost[2])):
          selected_object.upgrade()
        screen.blit(selected_object.image, (37.5, 250))
        screen.blit(City.upgrade_img, (37.5, 250))
        display_resources(selected_object.cost, 150, 237.5)
        text(25, "Upgrade", (0, 0, 0), 100, 225, alignx = "center", aligny = "center")
      else:
        text(25, "Max Level", (0, 0, 0), 75, 175, alignx = "center", aligny = "center")

    #build building buttons
    elif isinstance(selected_object, Location):
      #run through available buildings and player actions
      #selected object is a location
      #building a building
      for a_building_type in enumerate(Player.player_list[current_player].available_buildings):
        #a_building_type is a list containing the stats of a building
        if not bool(return_occupied(selected_object.coord_x, selected_object.coord_y, object = "building")) and Player.player_list[current_player].owns_unit(return_occupied(selected_object.coord_x, selected_object.coord_y, object = "unit")) and selected_object.terrain in a_building_type[1][4] and not bool(return_occupied(selected_object.coord_x, selected_object.coord_y, object = "city")):
          #if there is no other building there and u own a dude that is there and the terrain is in the building's terrain list and there is no city there
          if bool("cultivate" in a_building_type[1][5] and bool("crop" in selected_object.features or "harvested crop" in selected_object.features)) or bool(not "cultivate" in a_building_type[1][5]):
            #if the building is a cultivating building and it is on a crop/harvested crop or the building is not a cultivating building
            if button(SCREENLENGTH - Building.building_size*2, 200 + a_building_type[0] * (Building.building_size*2), Building.building_size*2, Building.building_size*2, 10, stroke = 0, available = bool(Player.player_list[current_player].money >= a_building_type[1][1][0] and Player.player_list[current_player].wood >= a_building_type[1][1][1] and Player.player_list[current_player].metal >= a_building_type[1][1][2] and Player.player_list[current_player].food >= a_building_type[1][1][3])):
              #build building and subtract resources
              print(a_building_type[1][0] + " is built")
              Player.player_list[current_player].money -= a_building_type[1][1][0]
              Player.player_list[current_player].wood -= a_building_type[1][1][1]
              Player.player_list[current_player].metal -= a_building_type[1][1][2]
              Player.player_list[current_player].food -= a_building_type[1][1][3]
              Player.player_list[current_player].buildings.append(Building(a_building_type[1], selected_object.coord_x, selected_object.coord_y))
            #display the building images on the buttons
            screen.blit(Building.img_dict[a_building_type[1][0]], (SCREENLENGTH - Building.building_size*2 + 25, 250 + a_building_type[0] * (Building.building_size*2)))
            text(20, a_building_type[1][0], (0, 0, 0), SCREENLENGTH - 150, 200 + a_building_type[0] * (Building.building_size*2))
            text(20, "Terrain: " + ", ".join(a_building_type[1][4]), (0, 0, 0), SCREENLENGTH - 150, 210 + a_building_type[0] * (Building.building_size*2))
            display_resources(a_building_type[1][1], SCREENLENGTH - 25, 250 + a_building_type[0] * (Building.building_size*2))
          
      for player_action in enumerate(Player.player_list[current_player].available_actions):
        #doing a player action
        if Player.player_list[current_player].owns_unit(return_occupied(selected_object.coord_x, selected_object.coord_y, object = "unit")) and not bool(return_occupied(selected_object.coord_x, selected_object.coord_y, object = "building")) and not bool(return_occupied(selected_object.coord_x, selected_object.coord_y, object = "city")):
          #if you own a dude there and there is no building there (to avoid chopping forest where there is a lumber hut) and there is no city there
          #can't do player action when there's a building there
          #first if statement checks the action, second if statement checks if terrain is compatible, third is the button
          if player_action[1] == "chop":
            if selected_object.terrain == "forest":
              if button(player_action_x + player_action[0] * player_action_size, player_action_y, player_action_size, player_action_size, 20, available = bool(Player.player_list[current_player].money >= Player.chop_cost)):
                Player.player_list[current_player].player_action("chop", Player.chop_cost)
              screen.blit(chop_img, (player_action_x + player_action[0] * player_action_size, player_action_y))
              text(25, "Chop", (0, 0, 0), (player_action_x + player_action_size/2) + (player_action[0] * player_action_size), player_action_y - 10, alignx = "center")
              text(50, str(Player.chop_cost), money_color, (player_action_x + player_action_size/2) + (player_action[0] * player_action_size), player_action_y + 25, alignx = "center")
              #display chop image
          elif player_action[1] == "cultivate":
            if "crop" in selected_object.features:
              if button(player_action_x + player_action[0] * player_action_size, player_action_y, player_action_size, player_action_size, 20, available = bool(Player.player_list[current_player].money >= Player.cultivate_cost)):
                Player.player_list[current_player].player_action("cultivate", Player.cultivate_cost)
              screen.blit(cultivate_img, (player_action_x + player_action[0] * player_action_size, player_action_y))
              text(25, "Cultivate", (0, 0, 0), (player_action_x + player_action_size/2) + (player_action[0] * player_action_size), player_action_y - 10, alignx = "center")
              text(50, str(Player.cultivate_cost), money_color, (player_action_x + player_action_size/2) + (player_action[0] * player_action_size), player_action_y + 25, alignx = "center")
          elif player_action[1] == "harvest":
            if "seaweed" in selected_object.features:
              if button(player_action_x + player_action[0] * player_action_size, player_action_y, player_action_size, player_action_size, 20):
                #seaweed is free (like whaling in polytopia), btn always available
                Player.player_list[current_player].player_action("harvest")
              screen.blit(harvest_img, (player_action_x + player_action[0] * player_action_size, player_action_y))
              text(25, "Harvest", (0, 0, 0), (player_action_x + player_action_size/2) + (player_action[0] * player_action_size), player_action_y - 10, alignx = "center")
          elif player_action[1] == "grow":
            if selected_object.terrain == "plains":
              if button(player_action_x + player_action[0] * player_action_size, player_action_y, player_action_size, player_action_size, 20, available = bool(Player.player_list[current_player].money >= Player.grow_cost)):
                Player.player_list[current_player].player_action("grow", Player.grow_cost)
              screen.blit(grow_img, (player_action_x + player_action[0] * player_action_size, player_action_y))
              text(25, "Grow", (0, 0, 0), (player_action_x + player_action_size/2) + (player_action[0] * player_action_size), player_action_y - 10, alignx = "center")
              text(50, str(Player.grow_cost), money_color, (player_action_x + player_action_size/2) + (player_action[0] * player_action_size), player_action_y + 25, alignx = "center")

    #keep all buttons on top of this line
    if mouse_clicked and receiving_input == False:
      #selecting the selected_object
      #order is unit, building, city, location when selecting same space
      #base this off of selection order
      #this allows eg if selected unit, next is building
      if not btn_pressed_this_frame:
        for player in Player.player_list:
          for unit in player.units:
            if circle_collided(mouse_pos[0], mouse_pos[1], 1, unit.display_x + Unit.unit_size/2 + offset_x, unit.display_y + Unit.unit_size/2 + offset_y, selected_collision_range/2):
              #if player's click did not land on any unit, we move on to building
              if not same_space((unit.coord_x, unit.coord_y)):
                #if the unit is already the selected object, allow other objects in the same place to be selected
                btn_pressed_this_frame = True
                selected_object = unit
              else:
                #selected object is the same unit
                print("same unit")
                selected_object = alternate_selection()
      if not btn_pressed_this_frame:
        for player in Player.player_list:
          for building in player.buildings:
            if circle_collided(mouse_pos[0], mouse_pos[1], 1, building.display_x + Building.building_size/2 + offset_x, building.display_y + Building.building_size/2 + offset_y, selected_collision_range/2):
              if not same_space((building.coord_x, building.coord_y)):
                #allow the player to select something else on the same square if the object is the same building already
                btn_pressed_this_frame = True
                selected_object = building
              else:
                selected_object = alternate_selection()
      if not btn_pressed_this_frame:
        for player in Player.player_list:
          for city in player.cities:
            if circle_collided(mouse_pos[0], mouse_pos[1], 1, city.display_x + City.city_size/2 + offset_x, city.display_y + City.city_size/2 + offset_y, selected_collision_range/2):
              if not same_space((city.coord_x, city.coord_y)):
                btn_pressed_this_frame = True
                selected_object = city
              else:
                selected_object = alternate_selection()
      if not btn_pressed_this_frame:
        #we are selecting location
        for row in enumerate(MAP):
          for tile in enumerate(row[1]):
            if circle_collided(mouse_pos[0], mouse_pos[1], 1, tile[1].display_x + offset_x + hex_size*sqrt(3)/4, tile[1].display_y + offset_y + hex_size/2, selected_collision_range/2):
              if tile[0] >= 0 and tile[0] <= map_length and row[0] >= 0 and row[0] <= map_length:
                if MAP[tile[0]][row[0]] != "":
                  if not same_space((tile[1].coord_x, tile[1].coord_y)):
                    btn_pressed_this_frame = True
                    selected_object = tile[1]
                  else:
                    selected_object = alternate_selection()
    for a_player in enumerate(Player.player_list):
      #this also resets each unit'saction_range, so keep this above the display_hints method
      a_player[1].update(a_player[0])
    #even though all player units are displayed, make it so only the units belonging to current_player are controlled

    if isinstance(selected_object, Unit) and selected_object.turn_done == False and selected_object.action_sequence != []:
      #only display hints if unit has selected a sequence and his turn is not done
      selected_object.display_hints()
    #display selection icons
    if selected_object != None:
      if isinstance(selected_object, Unit):
        screen.blit(unit_select_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
        if not Player.player_list[current_player].owns_unit(selected_object):
          screen.blit(foreign_unit_select_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
      elif isinstance(selected_object, Building):
        screen.blit(building_select_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
        if not Player.player_list[current_player].owns_building(selected_object):
          #if player does not own the building, draw the unowned icon above the regular icon
          screen.blit(foreign_building_select_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
      elif isinstance(selected_object, City):
        screen.blit(building_select_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
        if not Player.player_list[current_player].owns_city(selected_object):
          screen.blit(foreign_building_select_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
      elif isinstance(selected_object, Location):
        screen.blit(location_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
        if Player.player_list[current_player].owns_unit(return_occupied(selected_object.coord_x, selected_object.coord_y, "unit")):
          screen.blit(unit_location_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
        elif Player.player_list[current_player].owns_building(return_occupied(selected_object.coord_x, selected_object.coord_y, "building")):
          screen.blit(location_select_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
        elif Player.player_list[current_player].owns_city(return_occupied(selected_object.coord_x, selected_object.coord_y, "city")):
          screen.blit(location_select_img, (selected_object.display_x + offset_x, selected_object.display_y + offset_y))
    destroyAnimation()
    for animation in animation_list:
      animation.update()
    if mouse_clicked:
      mouse_clicked = False
    clock.tick(FPS)
    text(20, "FPS: " + str(clock.get_fps()), (0, 0, 0), 300, 0, alignx="center")
    screen.blit(transparent_screen, (0, 0))
    pygame.display.update()

  while status == "tech tree":
    screen.fill((255, 255, 255))
    pressed_keys = pygame.key.get_pressed()
    btn_pressed_this_frame = False
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = list(mouse_pos)

    if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
      tech_offset_y += 10
    if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
      tech_offset_y -= 10
    if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
      tech_offset_x += 10
    if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
      tech_offset_x -= 10
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_x:
          pygame.quit()
          sys.exit()
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_down = True
        if mouse_up == True:
          mouse_clicked = True
          mouse_up = False
      if event.type == pygame.MOUSEBUTTONUP:
        mouse_up = True
        mouse_down = False

    if button(0, 0, 50, 50, 10):
      status = "playing"
    
    text(25, str("Player " + str(current_player + 1)) + " turn", (0, 0, 0), SCREENLENGTH, 0, alignx = "right")
    display_resources([Player.player_list[current_player].money, Player.player_list[current_player].wood, Player.player_list[current_player].metal, Player.player_list[current_player].food], SCREENLENGTH - 25, 50, display_all = True)
    
    for a_tech in all_techs:
      #a_tech is a list of the tech stats, not a class object, therefore, a_tech[0] is the name, a_tech[1] is the cost, a_tech[4] is the preceding tech
      if a_tech[4] == None or Player.player_list[current_player].owns_tech(a_tech[4][0]):
        #if there is no tech that precedes a_tech, or if the player owns the preceding tech, tech is available to buy
        if not Player.player_list[current_player].owns_tech(a_tech[0]):
          #if the player does not own the tech
          if button(a_tech[2] + tech_offset_x, a_tech[3] + tech_offset_y, Tech.tech_size, Tech.tech_size, 10, available = Player.player_list[current_player].money >= a_tech[1]):
          #owns_tech will compare names of the tech, archery[4][0] == "Logging"
            Player.player_list[current_player].money -= a_tech[1]
            Player.player_list[current_player].techs.append(Tech(a_tech))
        else:
          #player owns the tech already
          pygame.draw.rect(screen, (0, 255, 255), (a_tech[2] + tech_offset_x, a_tech[3] + tech_offset_y, Tech.tech_size, Tech.tech_size), 0, 10)
      else:
        #display another color
        #player does not own the preceding tech
        #pygame.draw.rect(screen, (255, 0, 0), (a_tech[2] + tech_offset_x, a_tech[3] + tech_offset_y, Tech.tech_size, Tech.tech_size), 0, 10)
        #don't draw any button or rectangle
        pass
      screen.blit(a_tech[10], (a_tech[2] + tech_offset_x, a_tech[3] + tech_offset_y))
      text(30, a_tech[0], (0, 0, 0), a_tech[2] + Tech.tech_size/2 + tech_offset_x, a_tech[3] + Tech.tech_size/2 - 20 + tech_offset_y, alignx = "center", aligny = "center")
      text(50, str(a_tech[1]), money_color, a_tech[2] + Tech.tech_size/2 + tech_offset_x, a_tech[3] + Tech.tech_size/2 + 15 + tech_offset_y, alignx = "center", aligny = "center")
      if a_tech[4] != None:
        pygame.draw.line(screen, (0, 0, 0), (a_tech[2] + Tech.tech_size/2 + tech_offset_x, a_tech[3] + Tech.tech_size + tech_offset_y), (a_tech[4][2] + Tech.tech_size/2 + tech_offset_x, a_tech[4][3] + tech_offset_y), width = 5)
      

    if mouse_clicked:
      mouse_clicked = False
    clock.tick(FPS)
    text(20, "FPS: " + str(clock.get_fps()), (0, 0, 0), 300, 0, alignx="center")
    pygame.display.update()






