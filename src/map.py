from location import *
class Map:
    def __init__(self):
        self.map = []
    def configure_map(self) -> None:
        #set or reset map (just in case we need to reset entire map for some reason)
        self.map.clear()
        for row in enumerate(TERRAIN):
            coordy = row[0]
            self.map.append([])
            for tile in enumerate(row[1]):
                coordx = tile[0]
                features = []
                if (coordx, coordy) in MINERAL:
                    features.append("mineral")
                if (coordx, coordy) in ORE:
                    features.append("ore")
                if randint(1, 10) == 1 and tile[1] != "":
                    deposit = (randint(0, 5), randint(0, 5), randint(0, 5), randint(0, 5))
                else:
                    deposit = (0, 0, 0, 0)
                self.map[coordy].append(Location((coordx, coordy), tile[1], features, deposit))
    def display_map_hex(self) -> None:
        #use offsets to move the entire map around
        for row in self.map:
            for tile in row:
                #coords[0] and coords[1] are the coordinates of the tile in the map, not the screen blit coords
                #the map is a list of lists, so the first list is the first row, the second list is the second row
                #the first item in the list is the first tile, the second item is the second tile, etc.
                #display_coords[0] and display_coords[1] will be the screen blit coords of the tile
                tile.display()
        
    def return_tile(self, coords: Tuple[int, int]) -> 'Location':
        return self.map[coords[1]][coords[0]]
    def in_map(self, tile: Tuple[int, int]) -> bool:
        if tile[0] >= 0 and tile[0] <= MAP_LENGTH and tile[1] >= 0 and tile[1] <= MAP_LENGTH and self.return_tile(tile).terrain != "":
            return True
        return False
    def in_terrain(self, tile: Tuple[int, int], available: List[str]) -> bool:
        if self.return_tile(tile).terrain in available:
            return True
        return False
    def turn_reset(self) -> None:
        for row in self.map:
            for tile in row:
                tile.player_acted_on = False

    def return_Adjacent_hex(self, coords: Tuple[int, int]) -> List[Tuple[int, int]]:
        #returns a list of all the adjacent hexes based on one hex
        #the items returned are x and y coords to be used on the map
        available = []
        for tile in [(coords[0]-1, coords[1]-1), (coords[0], coords[1]-1), (coords[0]-1, coords[1]), (coords[0]+1, coords[1]), (coords[0], coords[1]+1), (coords[0]+1, coords[1]+1)]:
            if self.in_map(tile):
                available.append(tile)
        return available
        #omit the tiles that aren't in the map
        #adjacent_hexes has the coordinates of all the adjacent hexes, not their terrain stuff
        #u can call the terrain manually

    def shadeTile(coords: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        #coords[0] and coords[1] are coordinates, not display coordinates
        center_x = (coords[1] - 1)*(-hex_size/4)*sqrt(3)
        center_y = (coords[1] - 1)*(hex_size*0.75)
        center_x += (coords[0] - 1)*(hex_size/2)*sqrt(3)
        #allocate for image size (off of hex_side)
        center_x += ((hex_size/2)*sqrt(3))/2
        center_y += hex_size/2
        #add offsets
        center_x += dynamics.offset_x
        center_y += dynamics.offset_y
        #(display_coords[0], display_coords[1]) will be the center of the corresponding hex
        #points go clockwise from the top-left vertex
        point1 = (center_x - hex_size*sqrt(3)/4, center_y - hex_size/4)
        point2 = (center_x, center_y - hex_size/2)
        point3 = (center_x + hex_size*sqrt(3)/4, center_y - hex_size/4)
        point4 = (center_x + hex_size*sqrt(3)/4, center_y + hex_size/4)
        point5 = (center_x, center_y + hex_size/2)
        point6 = (center_x - hex_size*sqrt(3)/4, center_y + hex_size/4)
        pygame.draw.polygon(transparent_screen, color, [point1, point2, point3, point4, point5, point6])