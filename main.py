# DON'T FORGET TO COMMENT YOUR CODE PLEASE!!!
import pygame, sys, library, random
from pygame.locals import *
from random import choices
# import the Animator class
from animator import Animator

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

# set player animations
player_animation = ["", "", "", ""]
# set left animation
player_animation[library.LEFT] = Animator("Characters/girl_sideLeft_spriteSheet.png", library.scaleNum, 3, 7, 0.75)
# set right animation
player_animation[library.RIGHT] = Animator("Characters/girl_sideRight_spriteSheet.png", library.scaleNum, 3, 7, 0.75)
# set forwards animation
player_animation[library.FORWARDS] = Animator("Characters/girl_back_spriteSheet.png", library.scaleNum, 3, 7, 0.75)
# set backwards animation
player_animation[library.BACKWARDS] = Animator("Characters/girl_front_spriteSheet.png", library.scaleNum, 3, 7, 0.75)

# set player idle animations
player_idle_animation = ["", "", "", ""]
# set left idle animation
player_idle_animation[library.LEFT] = Animator("Characters/girl_sideLeftIdle_spriteSheet.png",
                                               library.scaleNum, 3, 7, 1.5)
# set right idle animation
player_idle_animation[library.RIGHT] = Animator("Characters/girl_sideRightIdle_spriteSheet.png",
                                                library.scaleNum, 3, 7, 1.5)
# set forwards idle animation
player_idle_animation[library.FORWARDS] = Animator("Characters/girl_backIdle_spriteSheet.png",
                                                   library.scaleNum, 3, 7, 1.5)
# set backwards idle animation
player_idle_animation[library.BACKWARDS] = Animator("Characters/girl_frontIdle_spriteSheet.png",
                                                    library.scaleNum, 3, 7, 1.5)


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


def change_direction(last_dir, current_dir):
    """
    Reset the players animator if the direction changes
    :param last_dir:        players direction from last frame
    :param current_dir:     players direction this frame
    :return:                current direction
    """
    if last_dir != current_dir:
        player_animation[last_dir].reset()
    return current_dir


def animation_direction(last_direction):
    """
    Gets the next animation direction.
    this prevents it from resetting if two keys are pressed at the same time!
    :return: (Direction, idle)
    """
    # find if any keys are pressed and set it to idle
    idle = not library.KEY_PRESSED["left"] and not library.KEY_PRESSED["right"] \
        and not library.KEY_PRESSED["forwards"] and not library.KEY_PRESSED["backwards"]

    # if theres no keys pressed return early as theres nothing to test
    if idle:
        return (last_direction, idle)

    # set direction to last direction encase there is opposite keys being pressed
    direction = last_direction

    # set to idle if both left and right keys are pressed
    if library.KEY_PRESSED["left"] and library.KEY_PRESSED["right"]:
        idle = True
    elif library.KEY_PRESSED["left"]:       # set left direction
        direction = library.LEFT
    elif library.KEY_PRESSED["right"]:      # set right direction
        direction = library.RIGHT

    # do forwards and backwards in separate if as the animation trumps left and right
    # set to idle if both forwards and backwards keys are pressed
    if library.KEY_PRESSED["forwards"] and library.KEY_PRESSED["backwards"]:
        # set to idle if neither left or right is pressed
        idle = not library.KEY_PRESSED["left"] and not library.KEY_PRESSED["right"]
    elif library.KEY_PRESSED["forwards"]:
        direction = library.FORWARDS        # set forwards direction
        idle = False
    elif library.KEY_PRESSED["backwards"]:
        direction = library.BACKWARDS       # set backwards direction
        idle = False

    return (direction, idle)


def main():

    start()
    ticks_since_last_frame = 0

    # players current direction
    current_direction = library.BACKWARDS

    # main game loop
    while True:
        t = pygame.time.get_ticks()
        # amount of time that passed since the last frame in seconds
        delta_time = (t - ticks_since_last_frame) / 1000.0
        # Get inputs
        event_inputs()

        # set the players animation direction and idle for the animation
        next_animation_direction, player_idle = animation_direction(current_direction)
        # set the current direction
        current_direction = change_direction(current_direction, next_animation_direction)

        # multiply the movement by delta_time to ensure constant speed no matter the FPS
        movement_speed = 75 * delta_time

        # Key press actions
        if library.KEY_PRESSED["left"]:
            # left key action
            GameStore.playerX -= movement_speed
            GameStore.x += movement_speed
            # set the current direction
            # current_direction = change_direction(current_direction, library.LEFT)
            # player_idle = False

        if library.KEY_PRESSED["right"]:
            # right key action
            GameStore.playerX += movement_speed
            GameStore.x -= movement_speed
            # set the current direction
            # current_direction = change_direction(current_direction, library.RIGHT)
            # player_idle = False

        if library.KEY_PRESSED["forwards"]:
            # forwards key action
            GameStore.playerY -= movement_speed
            GameStore.y += movement_speed
            # set the current direction
            # current_direction = change_direction(current_direction, library.FORWARDS)
            # player_idle = False

        if library.KEY_PRESSED["backwards"]:
            # backwards key action
            GameStore.playerY += movement_speed
            GameStore.y -= movement_speed
            # set the current direction
            # current_direction = change_direction(current_direction, library.BACKWARDS)
            # player_idle = False



        # switch between active and idle
        if not player_idle:
            player = player_animation[current_direction]
        else:
            player = player_idle_animation[current_direction]

        # update the avatars animation time
        player.update_time(delta_time)

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
        screen.blit(pygame.transform.scale(player.get_current_sprite(),
                    (int(library.scaleNum * 0.9), int(library.scaleNum * 0.9))),
                    (GameStore.x + GameStore.playerX - GameStore.offsetX,
                     GameStore.y + GameStore.playerY - GameStore.offsetY))

        # update the display.
        pygame.display.flip()
        ticks_since_last_frame = t


if __name__ == "__main__":
    main()
