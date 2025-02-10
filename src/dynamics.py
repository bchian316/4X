from constants import *
#global changing variables (always import this for everything)
#always put dynamics.var, not just var
mouse_pos = pygame.mouse.get_pos()
mouse_clicked = False
#later, change this to "home" and create a home screen; this is temporary only
status = "playing"
btn_pressed_this_frame = False
offset_x = 250
offset_y = 0
tech_offset_x = 0
tech_offset_y = 0

player_list = []
current_player = 0

selected_object = None

villages = []

animating = False
animation_list = []