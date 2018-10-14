# DON'T FORGET TO COMMENT YOUR CODE PLEASE!!!
import pygame, sys, library, random
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
MAP_WIDTH = 10
MAP_HEIGHT = 5
print(TILE_SIZE * MAP_WIDTH)

level = pygame.Surface((TILE_SIZE * MAP_WIDTH, TILE_SIZE * MAP_HEIGHT))
# [] = array
tiles = []
floorTiles = []
wallTiles = []
doorTiles = []

player = library.playerImg


class GameStore:
    playerX = 0
    playerY = 0
    offsetX = 0
    offsetY = 0
    x = 0
    y = 0
    playerSpawnPoint = []


def gen_rand_map_tiles():
    # use """ """ to add a description to your functions
    """
    Generates the random map tiles with different probabilities
    :return: tile type ID [x][y]
    """
    tiles.clear()
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
    # generate the map
    gen_rand_map_tiles()
    # draw the tiles to the level surface
    for row in range(MAP_HEIGHT):
        for column in range(MAP_WIDTH):
            level.blit(library.materials[tiles[row][column]],
                       (column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

            if tiles[row][column] == 0:
                floorTiles.append([column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE])
            elif tiles[row][column] == 1:
                wallTiles.append([column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE])
            elif tiles[row][column] == 2:
                doorTiles.append([column * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE])


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
                start()     # resets the level
        elif event.type == MOUSEBUTTONDOWN:                     # has a mouse button just been pressed?
            pass      # replace pass with mouse button up action/function.
        elif event.type == MOUSEBUTTONUP:                       # has a mouse button just been released?
            pass      # replace pass with pause action/function.


def exit_game():
    """Exits the game to desktop"""
    pygame.quit()
    sys.exit()


# creates a new level and positions everything accordingly in that level
def start():
    # create the level
    initialize_level()

    # create movement variables

    screen_rect = screen.get_rect()
    level_rect = level.get_rect()

    # find a random floor tile and get it's position coordinates
    GameStore.playerSpawnPoint = floorTiles[random.randint(0, len(floorTiles))]
    GameStore.playerX = GameStore.playerSpawnPoint[0]
    GameStore.playerY = GameStore.playerSpawnPoint[1]

    # variables for centering the level
    GameStore.x = screen_rect.centerx - level_rect.centerx
    GameStore.y = screen_rect.centery - level_rect.centery

    # variables for offsetting everything so the starting tile is always at the center
    GameStore.offsetX = -level_rect.centerx + Rect(GameStore.playerSpawnPoint).centerx
    GameStore.offsetY = -level_rect.centery + Rect(GameStore.playerSpawnPoint).centery


def main():
    start()
    ticks_since_last_frame = 0
    # main game loop
    while True:
        t = pygame.time.get_ticks()
        # amount of time that passed since the last frame in seconds
        delta_time = (t - ticks_since_last_frame) / 1000.0
        # Get inputs
        event_inputs()

        # multiply the movement by delta_time to ensure constant speed no matter the FPS
        movement_speed = 75 * delta_time

        # Key press actions
        if library.KEY_PRESSED["forwards"]:
            # forwards key action
            GameStore.playerY -= movement_speed
            GameStore.y += movement_speed

        if library.KEY_PRESSED["backwards"]:
            # backwards key action
            GameStore.playerY += movement_speed
            GameStore.y -= movement_speed

        if library.KEY_PRESSED["left"]:
            # left key action
            GameStore.playerX -= movement_speed
            GameStore.x += movement_speed

        if library.KEY_PRESSED["right"]:
            # right key action
            GameStore.playerX += movement_speed
            GameStore.x -= movement_speed

        # wait for the frame to end
        fps_clock.tick(FPS)
        # fill the background
        screen.fill(library.BLACK)
        # render the level on screen
        screen.blit(level, (GameStore.x - GameStore.offsetX, GameStore.y - GameStore.offsetY))
        # draw starting point rect (testing)
        pygame.draw.rect(screen, library.BLUE,
                         [GameStore.x + GameStore.playerSpawnPoint[0] - GameStore.offsetX,
                          GameStore.y + GameStore.playerSpawnPoint[1] - GameStore.offsetY,
                          GameStore.playerSpawnPoint[2],
                          GameStore.playerSpawnPoint[3]])
        # draw the player
        screen.blit(player, (GameStore.x + GameStore.playerX - GameStore.offsetX,
                             GameStore.y + GameStore.playerY - GameStore.offsetY))
        # update the display.
        pygame.display.flip()
        ticks_since_last_frame = t


if __name__ == "__main__":
    main()