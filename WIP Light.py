import main
import pygame
import sys
import dungeonGenerator


class Variables:
    """

    """
    light = 100                     #variable that activates lightning sequence
    currentposx = 0  #dungeonGenerator.GameStore.playerX    #characters position
    currentposy = 0  #dungeonGenerator.GameStore.playerY    #characters position
    ctx = 1                    #x tile that character is on
    cty = 1                     #y tile that character is on
    previoustilex = 0                       #x tile that character was on 1 frame ago
    previoustiley = 0                       #y tile that character was on 1 frame ago
    MAP_WIDTH = dungeonGenerator.GameStore.MAP_WIDTH
    MAP_HEIGHT = dungeonGenerator.GameStore.MAP_HEIGHT
    tiles = []


"""PUTTING GRID ITO THE GAME"""


def translate_light_map(light_map):
    temp_tiles = []
    for yy in range(len(light_map[0])):
        temp_light = []
        for xx in range(len(light_map)):
            xa = -4 + xx
            ya = -4 + yy
            if xa < 0:
                xa = xa * -1
            if ya < 0:
                ya = ya * -1
            xintens = (-1 * xa + 5) / 10
            yintens = (-1 * ya + 5) / 10
            lintens = (xintens + yintens)
            lintens = round(lintens*10)/10
            temp_light.append(lintens)

        temp_tiles.append(temp_light)
    Variables.tiles = temp_tiles
    print(Variables.tiles)


def create_light_map(range_value):
    """

    :param range_value:
    :return:
    """
    temp_storage = []
    for y in range(range_value):
        temp_small_storage = []
        for x in range(range_value):
            temp_small_storage.append(-round(range_value/2) + x)
        temp_storage.append(temp_small_storage)
    light_map = temp_storage
    translate_light_map(light_map)


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


check()
