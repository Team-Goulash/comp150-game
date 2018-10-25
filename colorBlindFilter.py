import pygame
import main


class CBFilterStore:
    surface = None


cb_settings = [(0, 0, 0), (0, 1, 1), (100, 89, 255), (100, 89, 255)]

def loop_cb_filters():
    for f in cb_settings:
        pull_image(cb_settings)

def weight_color(color, weights):

    color = list(color)
    color[0] *= weights[0]
    color[1] *= weights[1]
    color[2] *= weights[2]

    return color

def greyscale_pixel(pixel_color):
    red = pixel_color[0]
    green = pixel_color[1]
    blue = pixel_color[2]

    greyscale = (red + green + blue) // 3

    return greyscale, greyscale, greyscale


def pull_image(cb_filter):
    image = pygame.image.load("ColorBlind.png")
    pixel_array = pygame.PixelArray(image)
    for x in range(0, len(pixel_array)):
        for y in range(0, len(pixel_array[x])):
            new_pixel_color = greyscale_pixel(image.get((x, y)))
            # todo make tone function with a better name
            new_pixel_color = (new_pixel_color, cb_filter)
            image.set_at((x, y), new_pixel_color)

    del pixel_array


def grey_scale_screen_shot():
        pull_image()
        grey_scale = (pull_image().red + pull_image().green + pull_image().blue) // 3
        pull_image().pixel_array[pull_image().x, pull_image().y] = grey_scale, grey_scale, grey_scale

        del pull_image().pixel_array
        pygame.image.save(pull_image().image, "./Screenshots/grey_scale.png")


def initialization():
    CBFilterStore.surface = pygame.Surface((main.WINDOW_WIDTH, main.WINDOW_HEIGHT))


def color_blind_filter():
    CBFilterStore.surface.blit(main.screen, (0, 0))
    save(".", "ColorBlind", CBFilterStore.surface)


def save(path, file_name, surf):
    pygame.image.save(surf, path + "/" + file_name + ".png")
    print("saving image")