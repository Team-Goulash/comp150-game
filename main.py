# DON'T FORGET TO COMMENT YOUR CODE PLEASE!!!
import pygame, sys, random
from pygame.locals import *
# Set the window size
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1334

# set the FPS
FPS = 60;
# initialize the FPS clock
fps_clock = pygame.time.Clock()

# set Colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set materials
CONCRETE = 0
GRASS = 1
WATER = 2
SNOW = 3

# set colors to materials
colours = {
    CONCRETE: GREY,
    GRASS: GREEN,
    WATER: BLUE,
    SNOW: WHITE
}

# Tile Size
TILE_SIZE = 40
MAP_WIDTH = (WINDOW_WIDTH // TILE_SIZE) + 1           # // To round to int and add 1 to tile size so there is no border
MAP_HEIGHT = (WINDOW_HEIGHT // TILE_SIZE) + 1

# tilemap = []          # [] = List.
i = 0                   # ???


def gen_rand_map_tiles():
    # use ''' ''' to add a description to your functions
    '''
    Generates the randome map tiles
    :return: tile type ID [x][y]
    '''
    tiles = []                  # [] = list
    for y in range(MAP_HEIGHT):
        tile = []
        for x in range(MAP_WIDTH):
            item = random.randint(0, 3)
            tile.append(item)
        tiles.append(tile)
    return tiles


def main():
    # initialize py game
    pygame.init()
    # set the window size
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # set the window caption
    pygame.display.set_caption("Well Escape")

    # stores the tile map
    tile_map = gen_rand_map_tiles()

    # draw the tiles to screen
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            pygame.draw.rect(screen, colours[tile_map[row][column]],
                             (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # main game loop
    while True:
        # inputs
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # wait for the frame to end
        fps_clock.tick(FPS)
        # update the display.
        pygame.display.flip()


if __name__ == "__main__":
    main()
