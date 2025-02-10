import dynamics
from constants import *
class Tech:
  tech_size = 100
  def __init__(self, stats: List[Any], player_number: int):
    #stats = [name, cost, x, y, preceding_tech, unit, building, player_action, terrain]
    #x and y are where they should be displayed
    self.name = stats[0]
    self.cost = stats[1]
    #cost is only a number because it is only money
    self.display_coords = stats[2]
    self.preceding_tech = stats[3]
    #preceding tech should be the entire tech, not the class object, which would be a list of stats
    #preceding_tech[0] would be the name; use this in owns_tech
    self.unit = stats[4]
    self.building = stats[5]
    self.upgraded_building = stats[6]
    self.player_action = stats[7]
    self.terrain = stats[8]
    self.img = stats[9]
    dynamics.player_list[player_number].techs.append(self.name)
    if self.unit != None:
      if "float" in self.unit[9]:
        dynamics.player_list[player_number].available_naval_units.append(self.unit)
      else:
        dynamics.player_list[player_number].available_units.append(self.unit)
    if self.building != None:
      dynamics.player_list[player_number].available_buildings.append(self.building)
    if self.upgraded_building != None:
      dynamics.player_list[player_number].available_upgraded_buildings.append(self.upgraded_building)
    if self.player_action != None:
      dynamics.player_list[player_number].available_actions.append(self.player_action)
    if self.terrain != None:
      dynamics.player_list[player_number].available_terrain.append(self.terrain)