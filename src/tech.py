import dynamics
from constants import *
class Tech:
  tech_size = 100
  def __init__(self, stats: List[Any], player_number: int):
    #stats = [name, cost, x, y, preceding_tech, unit, building, player_action, terrain]
    #x and y are where they should be displayed
    self.name = stats["name"]
    self.cost = stats["cost"]
    #cost is only a number because it is only money
    self.display_coords = stats["coords"]
    self.preceding_tech = stats["preceding tech"]
    #preceding tech should be the entire tech, not the class object, which would be a list of stats
    #preceding_tech[0] would be the name; use this in owns_tech
    self.type = stats["type"]
    self.new = stats["new"]
    self.img = stats["img"]
    dynamics.player_list[player_number].techs.append(self)
    if self.type == "unit":
      dynamics.player_list[player_number].available_units.append(self.new)
    elif self.type == "building":
      dynamics.player_list[player_number].available_buildings.append(self.new)
    if self.type == "upgraded building":
      dynamics.player_list[player_number].available_upgraded_buildings.append(self.new)
    if self.type == "player action":
      dynamics.player_list[player_number].available_actions.append(self.new)
    if self.type == "terrain":
      dynamics.player_list[player_number].available_terrain.append(self.new)