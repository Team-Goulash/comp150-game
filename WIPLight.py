"""Creates 'blocky' shadow and puts overlay on screen."""
import pygame


class Variables:
    """Class that stores all variables."""

    light_intensity = 0.5
    light_range = 9
    light_surface = None
    overlay_image = pygame.image.load('./UI/overlay.png')


def overlay(surface):
    """
    Overlay overlay_image on screen.

    :param surface: Surface that image will be blit to.
    :return:        No return.
    """
    surface.blit(Variables.overlay_image, (0, 0))


def draw_light(surface, other_script):
    """
    Function displays light_surface on a surface.

    :param surface:     Surface that lightning will be displayed on.
    :param other_script:Connects this script with other so I can use its
                        functions.
    :return:            No return.
    """
    current_tile_x, current_tile_y = other_script.\
        get_coordiantes_from_position(other_script.GameStore.playerX,
                                      other_script.GameStore.playerY
                                      )
    current_tile_x -= ((Variables.light_range - 1) // 2)
    current_tile_y -= ((Variables.light_range - 1) // 2)

    pos_x, pos_y = other_script.\
        get_positon_by_tile_coordinates(current_tile_x, current_tile_y)

    surface.blit(Variables.light_surface, (pos_x, pos_y))


def light_map_creation(light_tiles_map, tile_size, light_surface, range_value):
    """
    Function draws a shadow squares on a light_surface.

    :param light_tiles_map: Values are used to set light_surface's squares
                            alpha.
    :param tile_size:       Value used to determine position of a shadow
                            square.
    :param light_surface:   Surface that shadow squares are gonna be drew on.
    :param range_value:     Range of a lightning
    :return:                No return.
    """
    for y in range(range_value):
        for x in range(range_value):
            pygame.draw.rect(light_surface,
                             (0, 0, 0, 255 * (1 - light_tiles_map[x][y])),
                             (x * tile_size,
                              y * tile_size,
                              tile_size,
                              tile_size
                              )
                             )


def create_light_map(range_value, tile_size, light_intensity, light_surface):
    """
    Function applies linear function to modify light_map.

    Function changes and replaces light_map values to a number between 0 and 1
    making them appropriate to modify alpha value of shadows in the next
    function.

    :param range_value:     Value is used to calculate new light_map
    :param tile_size:       Variable used in further functions.
    :param light_intensity: Value changes alpha channel of all squares and
                            lowers them depending on its value
    :param light_surface:   Variable used in further functions.
    :return:                No return.
    """
    light_tiles_map = []
    for yy in range(range_value):
        temp_light = []
        for xx in range(range_value):
            xa = -(range_value - 1) / 2 + xx
            ya = -(range_value - 1) / 2 + yy
            if xa < 0:
                xa = xa * -1
            if ya < 0:
                ya = ya * -1
            x_intensity = (-1 * xa + 3) / 6 * light_intensity
            y_intensity = (-1 * ya + 3) / 6 * light_intensity
            if x_intensity < 0:
                x_intensity = 0
            if y_intensity < 0:
                y_intensity = 0

            total_intensity = (x_intensity + y_intensity)
            total_intensity = round(total_intensity, 2)
            temp_light.append(total_intensity)

        light_tiles_map.append(temp_light)
    print(light_tiles_map)
    light_map_creation(light_tiles_map, tile_size, light_surface, range_value)


def initialisation_of_light_surface(range_value, tile_size,
                                    light_intensity):
    """
    Function calculates size of the light_surface.

    :param range_value:     Variable used to calculate size of a light_surface.
    :param tile_size:       Variable used to calculate size of a light_surface.
    :param light_intensity: Variable used in further functions.
    :return:                No return.
    """
    light_surface_size = range_value * tile_size
    light_surface = pygame.Surface((light_surface_size, light_surface_size),
                                   pygame.SRCALPHA
                                   )
    Variables.light_surface = light_surface
    create_light_map(range_value, tile_size, light_intensity, light_surface)


def initialise_lightning(tile_size):
    """
    Function starts lightning generation procedure.

    :param tile_size:   Variable used in further functions.
    :return:            No return.
    """
    initialisation_of_light_surface(Variables.light_range, tile_size,
                                    Variables.light_intensity
                                    )


def update_light(intensity):
    """
    Function synchronises light_intensity value with other script.

    :param intensity:   Value that replaces current light_intensity value.
    :return:            No return
    """
    Variables.light_intensity = intensity
