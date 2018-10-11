import pygame
from pygame.locals import *

# assign variables or names to used keys
PAUSE = K_ESCAPE
MOVE = {"left": K_a, "right": K_d, "forwards": K_w, "backwards": K_s}

# boolean values for key pressed states
KEY_PRESSED = {"left": False, "right": False, "forwards": False, "backwards": False}

# set Colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set images
scaleNum = 75

doorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/DoorTile.png"), (scaleNum, scaleNum))
floorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/FloorTile.png"), (scaleNum, scaleNum))
wallImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/WallTile.png"), (scaleNum, scaleNum))

# set materials
FLOOR = 0
WALL = 1
DOOR = 2

# set colors to materials
materials = {FLOOR: floorImg, WALL: wallImg, DOOR: doorImg}