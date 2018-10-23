# Driver Ashley Sands; Navigator: None
import pygame, math, library


def gray_scale_image(pixel_color, color_weight=(1, 1, 1)):
    """
    grey scales an image
    :param pixel_color:     color of pixel
    :param color_weight:    color channel weights
    :return:                gray scale image
    """
    # apply the weights the color
    weighted_color = multiply_color(pixel_color, color_weight)
    # get the average
    color_average = (weighted_color[0] + weighted_color[1] + weighted_color[2]) // 3
    # clamp the color to 255
    if color_average > 255:
        color_average = 255

    return color_average, color_average, color_average


def distance(color_base, color_comparitor):
    """
    it does ent matter what way base and comparitor are
    :param color_base:          Color to remove
    :param color_comparitor:    Color to test
    :return:                    difference
    """
    red = (color_base[0] - color_comparitor[0]) ** 2
    green = (color_base[1] - color_comparitor[1]) ** 2
    blue = (color_base[2] - color_comparitor[2]) ** 2

    return math.sqrt(red + green + blue)


def close_enough(pixle_color, color_comparitor, tolerance):
    """

    :param pixle_color:         color
    :param color_comparitor:    color to test agants
    :param tolerance:           tolerance 0 - 1
    :return:                    turn if close enough
    """
    if distance(pixle_color, color_comparitor) < (tolerance*450):
        return True
    else:
        return False


def change_color(color_base, color_comparitor, tolerance, replace_color):
    if close_enough(color_base, color_comparitor, tolerance):
        return replace_color[2], replace_color[1], replace_color[0]
    else:
        return color_base[2], color_base[1], color_base[0]


def multiply_color(pixel_color, color_weights):
    """
    Multiply the color chanel by color weight
    :param pixel_color:     (r, g, b) color
    :param color_weights:   weights tuple (r, g, b)
    :return:                weighted color
    """
    # make shore that pixel color is list so we can edit it
    pixel_color = list(pixel_color)
    for c in range(3):
        pixel_color[c] *= color_weights[c]
    return tuple(pixel_color)


def clamp255_color(pixel_color):
    """clamps color chanel to 255"""
    # make shore that pixel color is list so we can edit it
    pixel_color = list(pixel_color)
    for c in range(3):
        if pixel_color[c] > 255:
            pixel_color[c] = 255
    return tuple(pixel_color)


def clamp0_color(pixel_color):
    """clamps color chanel to 0"""
    # make shore that pixel color is list so we can edit it
    pixel_color = list(pixel_color)
    for c in range(3):
        if pixel_color[c] < 0:
            pixel_color[c] = 0
    return tuple(pixel_color)


def run_effect(effect_name, image_to_update, effect_inputs=None, loading_function=None):
    """
    Runs a single effect
    :param effect_name:         name of effect to run
    :param image_to_update:     image to be updated
    :param effect_inputs:       inputs for applied fx. See effect function for inputs. (must be tuple and in order)
    :param loading_function:    loading function, surface and rect position. tuple(function, surface, rect).
    if none then not displayed
    :return:                    None
    """

    # get the pixel array for the image we want to update
    pixel_array = pygame.PixelArray(image_to_update)

    # start an update pixel count for loading bar
    updated_pixel_count = 0
    # get the total amount of pixels for loading bar
    total_pixels = len(pixel_array) * len(pixel_array[0])

    # loop x and y pixels
    for x in range(0, len(pixel_array)):
        for y in range(0, len(pixel_array[x])):
            # get the color at the current pixel
            pixel_color = image_to_update.get_at((x, y))

            # find effect to run
            if effect_name == "greyscale":
                pixel_color = gray_scale_image(pixel_color)
            elif effect_name == "change_color":
                pixel_color = change_color(pixel_color, library.BLUE, 0.5, library.RED)
            else:
                # print message in console if fx is not found
                print("[image_effects.run_effect]Error: effect not found ", effect_name)

            # update the current pixel
            pixel_array[x, y] = pixel_color
            # count the update
            updated_pixel_count += 1

        # if there is a loading function display it
        if loading_function is not None:
            loading_function[0](loading_function[1], loading_function[2], (updated_pixel_count/total_pixels))
    # remove the pixel_array so we can display the image
    del pixel_array

