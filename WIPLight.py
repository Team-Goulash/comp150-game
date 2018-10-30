import main
import pygame
import sys
import dungeonGenerator


class Variables:
    """

    """

    light = 60 #variable that activates lightning sequence
    currentposx = dungeonGenerator.GameStore.playerX  #dungeonGenerator.GameStore.playerX    #characters position
    currentposy = dungeonGenerator.GameStore.playerY  #dungeonGenerator.GameStore.playerY    #characters position
    ctx = 1                    #x tile that character is on
    cty = 1                     #y tile that character is on
    previoustilex = 0                       #x tile that character was on 1 frame ago
    previoustiley = 0                       #y tile that character was on 1 frame ago
    MAP_WIDTH = dungeonGenerator.GameStore.MAP_WIDTH
    MAP_HEIGHT = dungeonGenerator.GameStore.MAP_HEIGHT
    light_surface = None
    tile_size = dungeonGenerator.TILE_SIZE


"""PUTTING GRID INTO THE GAME"""


def light_map_creation(light_values, light_position):

    for y in range(len(light_values[0])):
        for x in range(len(light_values)):
            # surface, rect(x, y, width, height)
            pygame.draw.polygon(Variables.light_surface, (0, 0, 0, 255 * light_values[x][y]),
                                ((x * Variables.tile_size, y * Variables.tile_size),
                                ((x + 1) * Variables.tile_size, y * Variables.tile_size),
                                ((x + 1) * Variables.tile_size, (y + 1) * Variables.tile_size),
                                ((x + 1) * Variables.tile_size, y * Variables.tile_size))
                                )
            pygame.draw.rect(((x* Variables.tile_size))




def translate_light_map(light_map, range_value):
    light_tiles_map = []
    for yy in range(len(light_map[0])):
        temp_light = []
        for xx in range(len(light_map)):
            xa = -(range_value-1)/2 + xx
            ya = -(range_value-1)/2 + yy
            if xa < 0:
                xa = xa * -1
            if ya < 0:
                ya = ya * -1
            xintens = (-1 * xa + 5) / 10 * Variables.light / 100
            yintens = (-1 * ya + 5) / 10 * Variables.light / 100
            lintens = (xintens + yintens)
            lintens = round(lintens, 2)
            temp_light.append(lintens)

        light_tiles_map.append(temp_light)
    print(light_tiles_map, light_map)
    #light_map_creation(light_tiles_map)


def create_light_map(range_value):
    """

    :param range_value:
    :return:
    """
    temp_storage = []
    for y in range(range_value):
        temp_small_storage = []
        for x in range(range_value):
            temp_small_storage.append(int(-(range_value-1)/2 + x))
        temp_storage.append(temp_small_storage)
    light_map = temp_storage

    print(light_map)
    translate_light_map(light_map, range_value)


def check_light_distance(light_intensity):
    """

    :param light_intensity:
    :return:
    """
    if light_intensity > 66:
        range_value = 9
    elif Variables.light > 33:
        range_value = 7
    else:
        range_value = 5

    light_surface_size = range_value * Variables.tile_size


    Variables.light_surface = pygame.Surface((light_surface_size, light_surface_size), pygame.SRCALPHA)
    create_light_map(range_value)



def apply():
    """

    :return:
    """
    Variables.previoustilex = Variables.ctx
    Variables.previoustiley = Variables.cty
    check_light_distance(Variables.light)


def position_check(current_position, current_tile, previous_tile, length):
    """

    :param current_position:
    :param current_tile:
    :param previous_tile:
    :param length:
    :return:
    """
    for i in range(length):
        r = i * 90
        t = current_position - r
        if t < 0:
            current_tile = i - 1
        if current_tile is not previous_tile:
            return True
        if i == (length - 1):
            return False


def check():
    """

    :return:
    """
    change_in_x = position_check(Variables.currentposx, Variables.ctx,
                                 Variables.previoustilex, Variables.MAP_WIDTH)
    change_in_y = position_check(Variables.currentposy, Variables.cty,
                                 Variables.previoustiley, Variables.MAP_HEIGHT)

    if change_in_x or change_in_y:
        apply()
