# DON'T FORGET TO COMMENT YOUR CODE PLEASE!!!
import pygame, sys, library
from pygame.locals import *
from random import choices

# initialize py game
pygame.init()
# Set the window size
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1334
# create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# set the window caption
pygame.display.set_caption("Well Escape")

# set the FPS
FPS = 60
# initialize the FPS clock
fps_clock = pygame.time.Clock()

# Tile Size
TILE_SIZE = library.floorImg.get_rect().width
MAP_WIDTH = 250
MAP_HEIGHT = 150
print(TILE_SIZE * MAP_WIDTH)

level = pygame.Surface((TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT))


def gen_rand_map_tiles():
    # use """ """ to add a description to your functions
    """
    Generates the random map tiles with different probabilities
    :return: tile type ID [x][y]
    """

    tiles = []                  # [] = array
    population = [0, 1, 2]
    weights = [0.75, 0.3, 0.075]
    for y in range(MAP_HEIGHT):
        tile = []
        for x in range(MAP_WIDTH):
            item = choices(population, weights)[0]
            tile.append(item)
        tiles.append(tile)
    return tiles


def initialize_level():
    """Draws the tiles with according images on a blank surface"""
    # stores the tile map
    tile_map = gen_rand_map_tiles()

    # draw the tiles to the level surface
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            level.blit(library.materials[tile_map[row][column]],
                       (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))


def event_inputs():
    """Gets the inputs and sets the key presses."""
    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            exit_game()
        # change the key pressed state
        elif event.type == KEYDOWN or event.type == KEYUP:
            if event.key == library.MOVE["left"]:                # set left key pressed (A)
                library.KEY_PRESSED["left"] = event.type == KEYDOWN
            elif event.key == library.MOVE["right"]:             # set right key pressed (D)
                library.KEY_PRESSED["right"] = event.type == KEYDOWN
            elif event.key == library.MOVE["forwards"]:          # set forwards key pressed (W)
                library.KEY_PRESSED["forwards"] = event.type == KEYDOWN
            elif event.key == library.MOVE["backwards"]:         # set backwards key pressed (S)
                library.KEY_PRESSED["backwards"] = event.type == KEYDOWN

        if event.type == KEYUP:
            if event.key == library.PAUSE:                     # get paused key down.
                initialize_level()  # generate a new level in-game(testing)

        elif event.type == MOUSEBUTTONDOWN:                     # has a mouse button just been pressed?
            pass      # replace pass with mouse button up action/function.
        elif event.type == MOUSEBUTTONUP:                       # has a mouse button just been released?
            pass      # replace pass with pause action/function.


def exit_game():
    """Exits the game to desktop"""
    pygame.quit()
    sys.exit()


def main():
    # create the level
    initialize_level()
    # create movement variables
    ticks_since_last_frame = 0
    x = 0
    y = 0
    # main game loop
    while True:
        t = pygame.time.get_ticks()
        # amount of time that passed since the last frame in seconds
        delta_time = (t - ticks_since_last_frame) / 1000.0
        # Get inputs
        event_inputs()

        # multiply the movement by delta_time to ensure constant speed no matter the FPS
        movement_speed = 500 * delta_time

        # Key press actions
        if library.KEY_PRESSED["forwards"]:
            # forwards key action
            y += movement_speed

        if library.KEY_PRESSED["backwards"]:
            # backwards key action
            y -= movement_speed

        if library.KEY_PRESSED["left"]:
            # left key action
            x += movement_speed

        if library.KEY_PRESSED["right"]:
            # right key action
            x -= movement_speed

        # wait for the frame to end
        fps_clock.tick(FPS)
        # fill the background
        screen.fill(library.BLACK)
        # render the level on screen
        screen.blit(level, (x, y))
        # update the display.
        pygame.display.flip()
        ticks_since_last_frame = t


if __name__ == "__main__":
    main()
