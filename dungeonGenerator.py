import pygame, sys, library, random, UI, os, shutil
import tileGenerator

from pygame.locals import *
from random import choices

tile_class = tileGenerator.Tiles()

tiles = []
tileTypes = []
tileMats = []
floorTiles = []
wallTiles = []
doorTiles = []

TILE_SIZE = tile_class.floorImg.get_rect().width
materials = tile_class.tileTypes


class GameStore:
    playerX = 0
    playerY = 0
    offsetX = 0
    offsetY = 0
    x = 0
    y = 0
    playerSpawnPoint = []
    mud_variations = 15
    moss_variations = 15
    pixel_map = pygame.Surface
    MAP_WIDTH = 10
    MAP_HEIGHT = 10
    top_col = False
    bottom_col = False
    left_col = False
    right_col = False
    start_x = 0
    start_y = 0
    levelCount = 5
    levels = []
    starting_point_x = []
    starting_point_y = []

    # Todo remove temp animation variable
    temp_lerp_timer = 0
    temp_rev_lerp = False


for num in range(GameStore.levelCount):
    GameStore.levels.append(pygame.Surface)
    GameStore.starting_point_x.append(0)
    GameStore.starting_point_y.append(0)


def gen_rand_map_tiles(instance):
    # use """ """ to add a description to your functions
    """
    Generates the random map tiles with different probabilities
    :return: tile type ID [x][y]
    """

    # choose a random pixel map and generate a surface for the tiles
    if instance == 0:
        GameStore.pixel_map = tile_class.get_dungeon_room(True)
    else:
        GameStore.pixel_map = tile_class.get_dungeon_room(False)
    GameStore.MAP_WIDTH = GameStore.pixel_map.get_width()
    GameStore.MAP_HEIGHT = GameStore.pixel_map.get_height()

    # reset all lists
    tiles.clear()
    tileTypes.clear()
    tileMats.clear()

    # set variables for random material variation
    material_types = [0, 1, 2]
    material_weights = [0.9, 0.6, 0.3]

    # choose random types of the floor and wall images
    floor = random.randrange(len(tile_class.tileTypes[0]))
    wall = random.randrange(len(tile_class.tileTypes[1]))

    '''
    Scroll through each pixel in a map and assign according tiles depending on the pixel brightness.

    Assign a randomly chosen material type value to each tile.
    '''
    for y in range(GameStore.MAP_HEIGHT):
        tile_row = []
        type_row = []
        mat_row = []
        for x in range(GameStore.MAP_WIDTH):
            pixel = GameStore.pixel_map.get_at((x, y))
            pixel_tone = (pixel.r + pixel.g + pixel.b) / 3  # pixel brightness
            if pixel_tone == 255:
                tile = 0
                t_type = floor
            elif pixel_tone == 0:
                tile = 1
                t_type = wall
            elif pixel_tone < 150:
                if instance == 0:
                    tile = 2
                    t_type = 0
                else:
                    tile = 0
                    t_type = floor
            else:
                if instance == len(GameStore.levels) - 1:
                    tile = 2
                    t_type = 1
                else:
                    tile = 0
                    t_type = floor
                GameStore.start_x = x
                GameStore.start_y = y
            tile_row.append(tile)  # horizontal row of tiles
            type_row.append(t_type)  # horizontal row of tile types

            material = choices(material_types, material_weights)[0]  # single material
            mat_row.append(material)  # horizontal row of materials

        tiles.append(tile_row)  # vertical column of horizontal tile rows
        tileTypes.append(type_row)  # vertical column of horizontal type rows
        tileMats.append(mat_row)  # vertical column of horizontal material rows
    return tiles


def get_position_with_offset(x_pos, y_pos):
    """gets the objects position with the map offset included"""
    x_pos = GameStore.x + x_pos - GameStore.offsetX
    y_pos = GameStore.y + y_pos - GameStore.offsetY

    return x_pos, y_pos


def get_positon_by_tile_coordinates(x_cord, y_cord):

    x_pos, y_pos = get_position_with_offset(TILE_SIZE * x_cord, TILE_SIZE * y_cord)

    return x_pos, y_pos

def get_coordiantes_from_position(x_position, y_position):
    """
    Driver: ashley
    :param x_position:      x position to get coords for
    :param y_position:      y position to get coords for
    :return:                (X coords, Y Coords)
    """

    x_coords = x_position / TILE_SIZE + 0.5
    y_coords = y_position / TILE_SIZE + 0.85

    return int(x_coords), int(y_coords)


def initialize_level(surface_id):
    """Draws the tiles with according images on a blank surface"""
    # generate the map
    gen_rand_map_tiles(surface_id)
    GameStore.levels[surface_id] = pygame.Surface((GameStore.MAP_WIDTH * TILE_SIZE, GameStore.MAP_HEIGHT * TILE_SIZE))
    # generate material variations
    while GameStore.mud_variations > 0:
        for i in range(len(tile_class.tileTypes[1])):
            tile_class.generate_material(1, i, 1, GameStore.mud_variations)
        GameStore.mud_variations -= 1
    while GameStore.moss_variations > 0:
        for i in range(len(tile_class.tileTypes[1])):
            tile_class.generate_material(1, i, 2, GameStore.moss_variations)
        GameStore.moss_variations -= 1
    # draw the tiles to the level surface
    for column in range(GameStore.MAP_HEIGHT):
        for row in range(GameStore.MAP_WIDTH):
            x_pos = row * TILE_SIZE
            y_pos = column * TILE_SIZE
            if tiles[column][row] == 0:
                if surface_id == 0:
                    floorTiles.append([x_pos + GameStore.starting_point_x[surface_id], y_pos +
                                       GameStore.starting_point_y[surface_id]])
                material = tile_class.assign_material(tiles[column][row], tileTypes[column][row], tileMats[column][row])
            elif tiles[column][row] == 1:
                wallTiles.append([x_pos + GameStore.starting_point_x[surface_id], y_pos +
                                  GameStore.starting_point_y[surface_id]])
                material = tile_class.assign_material(tiles[column][row], tileTypes[column][row], tileMats[column][row])
            elif tiles[column][row] == 2:
                doorTiles.append([x_pos + GameStore.starting_point_x[surface_id], y_pos +
                                  GameStore.starting_point_y[surface_id]])
                material = tile_class.assign_material(tiles[column][row], tileTypes[column][row], tileMats[column][row])

            """
            files = [f for f in os.listdir("Well Escape tiles/varieties")
                     if os.path.isfile(os.path.join("Well Escape tiles/varieties", f))]
            variety_amount = len(files)
            """

            GameStore.levels[surface_id].blit(material, (x_pos, y_pos, TILE_SIZE, TILE_SIZE))


