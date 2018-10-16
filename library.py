import pygame
from pygame.locals import *

# assign variables or names to used keys
PAUSE = K_ESCAPE
MOVE = {"left": K_a, "right": K_d, "forwards": K_w, "backwards": K_s}

# boolean values for key pressed states
KEY_PRESSED = {"left": False, "right": False, "forwards": False, "backwards": False, "mouse": False}

# set Colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set images
scaleNum = 90
buttonSize = (600, 100)

doorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/DoorTile.png"), (scaleNum, scaleNum))
floorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/FloorTile.png"), (scaleNum, scaleNum))
wallImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/WallTile.png"), (scaleNum, scaleNum))
#   UI Buttons
buttonOneHover = pygame.transform.scale(pygame.image.load("UI/Button_000_hover.png"), buttonSize)
buttonTwoHover = pygame.transform.scale(pygame.image.load("UI/Button_001_hover.png"), buttonSize)
buttonOneClick = pygame.transform.scale(pygame.image.load("UI/Button_000_pressed.png"), buttonSize)
buttonTwoClick = pygame.transform.scale(pygame.image.load("UI/Button_001_pressed.png"), buttonSize)
buttonOne = pygame.transform.scale(pygame.image.load("UI/Button_000_normal.png"), buttonSize)
buttonTwo = pygame.transform.scale(pygame.image.load("UI/Button_001_normal.png"), buttonSize)

playerImg = pygame.transform.scale(pygame.image.load("Characters/Player.png"),
                                   (int(scaleNum * 0.75), int(scaleNum * 0.75)))

# set materials
FLOOR = 0
WALL = 1
DOOR = 2

# set colors to materials
materials = {FLOOR: floorImg, WALL: wallImg, DOOR: doorImg}