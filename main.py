import pygame, sys, random
from pygame.locals import *

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CONCRETE = 0
GRASS = 1
WATER = 2
SNOW = 3

colours = {
    CONCRETE: GREY,
    GRASS: GREEN,
    WATER: BLUE,
    SNOW: WHITE
}

TILESIZE = 10
MAPWIDTH = 50
MAPHEIGHT = 50

tilemap = list()
i = 0

for x in range(MAPHEIGHT):
    tile = list()
    for i in range(MAPWIDTH):
        item = random.randint(0, 3)
        tile.append(item)
    tilemap.append(tile)
print(tilemap)



pygame.init()

screen = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
pygame.display.set_caption("Well Escape")

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            pygame.draw.rect(screen, colours[tilemap[row][column]], (column * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE))

    pygame.display.flip()