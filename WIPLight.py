"""Creates blocky shadow """
import pygame
import dungeonGenerator


class Variables:
    light = 100
    previous_tile_x = 0
    previous_tile_y = 0
    light_surface = None
    tile_size = dungeonGenerator.TILE_SIZE


def light_map_creation(light_values):
    for y in range(len(light_values[0])):
        for x in range(len(light_values)):
            pygame.draw.rect(Variables.light_surface,
                             (0, 0, 0, 255 * (1-light_values[x][y])),
                             (x * Variables.tile_size,
                              y * Variables.tile_size,
                              Variables.tile_size,
                              Variables.tile_size
                              )
                             )


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
            x_intensity = (-1 * xa + 3) / 6
            y_intensity = (-1 * ya + 3) / 6
            if x_intensity < 0:
                x_intensity = 0
            if y_intensity < 0:
                y_intensity = 0
            total_intensity = (x_intensity + y_intensity)
            total_intensity = round(total_intensity, 2)
            temp_light.append(total_intensity)

        light_tiles_map.append(temp_light)
    print(light_tiles_map)
    light_map_creation(light_tiles_map)


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


# def position_check(current_position, current_tile, previous_tile, length):
def position_check():
    """

    :return: true if the tile has changed
    """

    current_tile_x, current_tile_y = dungeonGenerator.get_coordiantes_from_position(dungeonGenerator.GameStore.playerX,
                                                                                    dungeonGenerator.GameStore.playerY)

    if current_tile_x != Variables.previous_tile_x or current_tile_y != Variables.previous_tile_y:
        Variables.previous_tile_x = current_tile_x
        Variables.previous_tile_y = current_tile_y
        return True

    return False


def check():
    """

    :return:
    """
    if position_check():
        check_light_distance(Variables.light)


def draw_light(surface):

    current_tile_x, current_tile_y = dungeonGenerator.get_coordiantes_from_position(dungeonGenerator.GameStore.playerX,
                                                                                    dungeonGenerator.GameStore.playerY)
    current_tile_x -= 3
    current_tile_y -= 3
    pos_x, pos_y = dungeonGenerator.get_positon_by_tile_coordinates(current_tile_x, current_tile_y)
    surface.blit(Variables.light_surface, (pos_x, pos_y))
