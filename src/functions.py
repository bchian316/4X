from constants import *
import dynamics
def text(size: int, message: str, color: Set[int], textx: int, texty: int, alignx: str = "left", aligny: str = "top", font: str = "harrington") -> None:
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
def rect_collided(x1: int, y1: int, length1: int, height1: int, x2: int, y2: int, length2: int, height2: int) -> bool:
  #1 = object
  #2 = target
  if x1 > x2 - length1 and x1 < x2 + length2 and y1 > y2 - height1 and y1 < y2 + height2:
    return True
  return False
def circle_collided(x1: int, y1: int, radius1: int, x2: int, y2: int, radius2: int) -> bool:
  distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
  if distance <= radius1 + radius2:
    return True
  return False
def get_vel(x1: int, y1: int, x2: int, y2: int, speed: int) -> Tuple[float, float]:
  distancex = x2 - x1
  distancey = y2 - y1
  distance = sqrt(distancex**2 + distancey**2)
  divisor = distance/speed
  #divisor is how many frames it would take for the bullet to reach its destination
  #speed * divisor = distance (rt = d)
  velx = distancex/divisor
  vely = distancey/divisor
  return velx, vely
def display_resources(resources: Dict, x: int, y: int, money = 0, display_all: bool = False, size: int = 20) -> None:
  #x is the line between the images and the numbers
  #resources is [money, wood, metal, food, water]
  display_counter = 0
  cushion = 25
  text_offset_y = 12.5
  if display_all:
    text(size, str(money), money_color, x, y + text_offset_y, alignx = "right", aligny = "center")
    screen.blit(money_resource_img, (x, y))
    display_counter += 1
    for resource in resources.keys():
      text(size, str(resources[resource]), resource_colors[resource], x, y + display_counter * cushion + text_offset_y, alignx = "right", aligny = "center")
      screen.blit(resource_imgs[resource], (x, y + display_counter * cushion))
      display_counter += 1
  else:
    if money > 0:
      text(size, str(money), money_color, x, y + text_offset_y, alignx = "right", aligny = "center")
      screen.blit(money_resource_img, (x, y))
      display_counter += 1
    for resource in resources.keys():
      if resources[resource] <= 0:
        continue
      text(size, str(resources[resource]), resource_colors[resource], x, y + display_counter * cushion + text_offset_y, alignx = "right", aligny = "center")
      screen.blit(resource_imgs[resource], (x, y + display_counter * cushion))
      display_counter += 1 
def coordConvert(coords: Tuple[int, int], allocateSize: Optional[int] = None, returnCenter = True) -> Tuple[float, float]:
  #this function returns display coordinates from game location coordinates
  #you should only allocateSize if returnCenter is true
  display_x = (coords[1] - 1)*(-hex_size/4)*sqrt(3)
  display_y = (coords[1] - 1)*(hex_size*0.75)
  display_x += (coords[0] - 1)*(hex_size/2)*sqrt(3)
  #allocate for image size (off of hex_side)
  if returnCenter:
    #if returnCenter true, we add so the display_x and y are now in the center of hex
    display_x += ((hex_size/2)*sqrt(3))/2
    display_y += hex_size/2
  if allocateSize:
    display_x -= allocateSize/2
    display_y -= allocateSize/2
  return display_x, display_y
def display_action_sequence(action_sequence: Tuple, action_index: int, x: int, y: int, mini: bool = False) -> None:
    if not mini:
      size = icon_size
      move = move_img
      attack = attack_img
      heal = heal_img
      heal_other = heal_other_img
    else:
      size = small_icon_size
      move = small_move_img
      attack = small_attack_img
      heal = small_heal_img
      heal_other = small_heal_other_img
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
      elif action[1] == "heal other":
        screen.blit(heal_other, (action[0]*size + x, y))
def button(x: int, y: int, width: int, height: int, radius: int = 0, stroke: int = 0, available: bool = True, acolor: Set[int] = (0, 255, 0), ucolor: Set[int] = (145, 145, 145, 145), hcolor: Set[int] = (43, 186, 43), frames: Optional[Dict] = None) -> bool:
  #available is a boolean that determines whether the button is available to be pressed or not
  if available:
    if dynamics.mouse_pos[0] >= x and dynamics.mouse_pos[0] <= x + width and dynamics.mouse_pos[1] >= y and dynamics.mouse_pos[1] <= y + height:
      if frames != None:
        screen.blit(frames["hover"], (x, y))
      else:
        pygame.draw.rect(screen, hcolor, (x, y, width, height), stroke, radius)
      if dynamics.mouse_clicked and dynamics.btn_pressed_this_frame == False:
        dynamics.btn_pressed_this_frame = True
        return True
    else:
      if frames != None:
        screen.blit(frames["available"], (x, y))
      else:
        pygame.draw.rect(screen, acolor, (x, y, width, height), stroke, radius)
  else:
    if frames != None:
      screen.blit(frames["unavailable"], (x, y))
    else:
      pygame.draw.rect(screen, ucolor, (x, y, width, height), stroke, radius)
  return False