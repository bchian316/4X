#only functions can import this, not anything else
import pygame, sys
pygame.init()
from math import sqrt
from copy import deepcopy
from random import randint
from typing import *
SCREENLENGTH = 1000
SCREENHEIGHT = 700
FPS = 40
hex_size = 100
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
shade_width = 10 #for shadeTile method
transparent_screen = pygame.Surface((SCREENLENGTH, SCREENHEIGHT), pygame.SRCALPHA)
transparent_screen.set_alpha(player_alpha_shade)
#make sure transparent_screen.blit goes below all displays that are drawn on it
# Add game logic and functions
clock = pygame.time.Clock()
pygame.display.set_caption('Project #1')
#../resource colors
money_color = (229, 184, 11)
wood_color = (124, 71, 0)
metal_color = (185, 185, 185)
food_color = (66, 25, 33)
water_color = (0, 157, 255)
money_resource_img = pygame.image.load("../resource/money.png").convert_alpha()
wood_resource_img = pygame.image.load("../resource/wood.png").convert_alpha()
metal_resource_img = pygame.image.load("../resource/metal.png").convert_alpha()
food_resource_img = pygame.image.load("../resource/food.png").convert_alpha()
water_resource_img = pygame.image.load("../resource/water.png").convert_alpha()
resource_colors = {"wood": wood_color, "metal": metal_color, "food": food_color, "water": water_color}
resource_imgs = {"wood": wood_resource_img, "metal": metal_resource_img, "food": food_resource_img, "water": water_resource_img}
#lets make the map a constant size (4 side length: hexagon) = 37 tiles
#lets make 9 diagonal columns because there are 2x-1 columns when x is side length
#the map will be the constant variable that revolves around all the players
#it will show the terrain of every tile in the game
#MAP = [4 items, 5 items, 6, 7, 6, 5, 4] because there is a side length of 4
TERRAIN = (("mountain", "mountain", "mountain", "plains", "water", "water", "ocean", "", "", "", ""), 
       ("mountain", "mountain", "crop", "forest", "crop", "water", "ocean", "ocean", "", "", "", "", ""), 
       ("forest", "mountain", "dense forest", "crop", "water", "ocean", "ocean", "ocean", "water", "", "", "", ""), 
       ("plains", "mountain", "dense forest", "water", "water", "forest", "plains", "mountain", "ocean", "ocean", "", "", ""), 
       ("water", "forest", "plains", "dense forest", "water", "mountain", "plains", "water", "mountain", "forest", "forest", "", ""), 
       ("dense forest", "water", "plains", "mountain", "plains", "plains", "mountain", "water", "plains", "forest", "plains", "plains", ""),
       ("dense forest", "forest", "mountain", "mountain", "mountain", "mountain", "water", "plains", "mountain", "plains", "forest", "plains", "plains"),
       ("", "forest", "mountain", "water", "water", "mountain", "plains", "ocean", "plains", "water", "dense forest", "dense forest", "dense forest"), 
       ("", "", "mountain", "ocean", "mountain", "ocean", "mountain", "forest", "mountain", "mountain", "dense forest", "dense forest", "dense forest"),
       ("", "", "", "mountain", "water", "ocean", "plains", "plains", "water", "plains", "dense forest", "dense forest", "dense forest"), 
       ("", "", "", "", "mountain", "mountain", "mountain", "mountain", "plains", "plains", "dense forest", "dense forest", "plains"),
       ("", "", "", "", "", "mountain", "mountain", "water", "ocean", "plains", "plains", "dense forest", "dense forest"),
       ("", "", "", "", "", "", "ocean", "ocean", "ocean", "ocean", "ocean", "ocean", "ocean"))
#this is the side length of the map
MAP_LENGTH = len(TERRAIN)-1
#useless for now
MINERAL = ((9, 12), (10, 12), (7, 1), (8, 2), (4, 3), (4, 4), (7, 4), (1, 5), (3, 7), (7, 7), (5, 8), (8, 4))
ORE = ((7, 2), (0, 3), (5, 4), (5, 5), (6, 6), (11, 6), (7, 9), (9, 9), (10, 9), (7, 11), (9, 11), (12, 12))
VILLAGES = ((8, 4), (2, 5), (8, 7), (3, 0), (4, 8), (12, 10), (2, 2))

#important variables for formatting and stuff
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
bank_y = 50
selection_frame = pygame.image.load("../frames/selection frame.png").convert_alpha()
production_frame = pygame.image.load("../frames/production frame.png").convert_alpha()

unit_available_button_frame = pygame.image.load("../frames/unit/available.png").convert_alpha()
unit_hover_button_frame = pygame.image.load("../frames/unit/hover.png").convert_alpha()
unit_unavailable_button_frame = pygame.image.load("../frames/unit/unavailable.png").convert_alpha()
unit_button_frames = {"available": unit_available_button_frame, "hover": unit_hover_button_frame, "unavailable": unit_unavailable_button_frame}
building_available_button_frame = pygame.image.load("../frames/building/available.png").convert_alpha()
building_hover_button_frame = pygame.image.load("../frames/building/hover.png").convert_alpha()
building_unavailable_button_frame = pygame.image.load("../frames/building/unavailable.png").convert_alpha()
building_button_frames = {"available": building_available_button_frame, "hover": building_hover_button_frame, "unavailable": building_unavailable_button_frame}
city_available_button_frame = pygame.image.load("../frames/city/available.png").convert_alpha()
city_hover_button_frame = pygame.image.load("../frames/city/hover.png").convert_alpha()
city_unavailable_button_frame = pygame.image.load("../frames/city/unavailable.png").convert_alpha()
city_button_frames = {"available": city_available_button_frame, "hover": city_hover_button_frame, "unavailable": city_unavailable_button_frame}
#selected images
unit_select_img = pygame.image.load("../selection/owns select.png").convert_alpha()
building_select_img = pygame.transform.scale(unit_select_img, (75, 75)).convert_alpha()
location_select_img = pygame.image.load("../selection/owns location.png").convert_alpha()
unit_location_img = pygame.image.load("../selection/owns unit location.png").convert_alpha()
foreign_unit_select_img = pygame.image.load("../selection/foreign select.png").convert_alpha()
foreign_building_select_img = pygame.transform.scale(foreign_unit_select_img, (75, 75)).convert_alpha()
location_img = pygame.image.load("../selection/foreign location.png").convert_alpha()

#map features (food, mineral, etc)



      
#action sequence images
icon_size = 100
move_img = pygame.image.load("../unit actions/move.png").convert_alpha()
attack_img = pygame.image.load("../unit actions/attack.png").convert_alpha()
heal_img = pygame.image.load("../unit actions/heal.png").convert_alpha()
heal_other_img = pygame.image.load("../unit actions/heal other.png").convert_alpha()
small_icon_size = 50
small_move_img = pygame.transform.scale(move_img, (small_icon_size, small_icon_size))
small_attack_img = pygame.transform.scale(attack_img, (small_icon_size, small_icon_size))
small_heal_img = pygame.transform.scale(heal_img, (small_icon_size, small_icon_size))
small_heal_other_img = pygame.transform.scale(heal_other_img, (small_icon_size, small_icon_size))
skip_action_img = pygame.image.load("../unit actions/skip action.png").convert_alpha()