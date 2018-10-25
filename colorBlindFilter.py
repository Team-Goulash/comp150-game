import pygame
import main


class CBFilter_Store:
    surface = None


def initialization():
    CBFilter_Store.surface = pygame.Surface((main.WINDOW_WIDTH, main.WINDOW_HEIGHT))


def color_blind_filter():
    CBFilter_Store.surface.blit(main.screen, (0, 0))
    save(".", "ColorBlind", CBFilter_Store.surface)


def save(path, file_name, surf):
    pygame.image.save(surf, path + "/" + file_name + ".png")
    print("saving image")