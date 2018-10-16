import pygame
from pygame.locals import *

# assign variables or names to used keys
PAUSE = K_ESCAPE
MOVE = {"left": K_a, "right": K_d, "forwards": K_w, "backwards": K_s}

# directions
LEFT = 0
RIGHT = 1
FORWARDS = 2
BACKWARDS = 3

# boolean values for key pressed states
KEY_PRESSED = {"left": False, "right": False, "forwards": False, "backwards": False}

# set Colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

scaleNum = 90

playerImg = pygame.transform.scale(pygame.image.load("Characters/Player.png"),
                                   (int(scaleNum * 0.75), int(scaleNum * 0.75)))


class Tiles:
    # set images

    doorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/DoorTile.png"), (scaleNum, scaleNum))
    floorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/FloorTile.png"), (scaleNum, scaleNum))
    wallImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/WallTile.png"), (scaleNum, scaleNum))

    # set materials
    FLOOR = 0
    WALL = 1
    DOOR = 2

    # set colors to materials
    tileTypes = {FLOOR: floorImg, WALL: wallImg, DOOR: doorImg}

    def generate_material(self, base_image, mat_type):
        """
        :arg mat_type:      specifies the type of material the function will generate
        :arg base_image:    input image the function will modify
        :return: Tile texture with randomly generated features
        """
        texture = base_image

        pygame.image.save(texture, "Well Escape tiles/randomGen.png")
        return texture