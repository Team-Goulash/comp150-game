# DON'T FORGET TO COMMENT YOUR CODE PLEASE!!!
import pygame, sys, library, random, os, shutil
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
TILE_SIZE = library.Tiles.floorImg.get_rect().width

# [] = list
tiles = []
tileTypes = []
tileMats = []
floorTiles = []
wallTiles = []
doorTiles = []

tile_class = library.Tiles()
materials = tile_class.tileTypes

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

if not os.path.exists("Well Escape tiles/varieties"):
    os.makedirs("Well Escape tiles/varieties")
else:
    shutil.rmtree("Well Escape tiles/varieties")
    os.makedirs("Well Escape tiles/varieties")


class GameStore:
    playerX = 0
    playerY = 0
    offsetX = 0
    offsetY = 0
    x = 0
    y = 0
    playerSpawnPoint = []
    mud_variations = 15
    moss_variations = 15
    pixel_map = pygame.Surface
    MAP_WIDTH = 0
    MAP_HEIGHT = 0
    top_col = False
    bottom_col = False
    left_col = False
    right_col = False
    start_x = 0
    start_y = 0
    levelCount = 5
    levels = []
    starting_point_x = []
    starting_point_y = []


for num in range(GameStore.levelCount):
    GameStore.levels.append(pygame.Surface)
    GameStore.starting_point_x.append(0)
    GameStore.starting_point_y.append(0)


def gen_rand_map_tiles(instance):
    # use """ """ to add a description to your functions
    """
    Generates the random map tiles with different probabilities
    :return: tile type ID [x][y]
    """

    # choose a random pixel map and generate a surface for the tiles
    if instance == 0:
        GameStore.pixel_map = tile_class.get_dungeon_room(True)
    else:
        GameStore.pixel_map = tile_class.get_dungeon_room(False)
    GameStore.MAP_WIDTH = GameStore.pixel_map.get_width()
    GameStore.MAP_HEIGHT = GameStore.pixel_map.get_height()

    # reset all lists
    tiles.clear()
    tileTypes.clear()
    tileMats.clear()

    # set variables for random material variation
    material_types = [0, 1, 2]
    material_weights = [0.9, 0.6, 0.3]

    # choose random types of the floor and wall images
    floor = random.randrange(len(tile_class.tileTypes[0]))
    wall = random.randrange(len(tile_class.tileTypes[1]))

    '''
    Scroll through each pixel in a map and assign according tiles depending on the pixel brightness.
    
    Assign a randomly chosen material type value to each tile.
    '''
    for y in range(GameStore.MAP_HEIGHT):
        tile_row = []
        type_row = []
        mat_row = []
        for x in range(GameStore.MAP_WIDTH):
            pixel = GameStore.pixel_map.get_at((x, y))
            pixel_tone = (pixel.r + pixel.g + pixel.b) / 3      # pixel brightness
            if pixel_tone == 255:
                tile = 0
                t_type = floor
            elif pixel_tone == 0:
                tile = 1
                t_type = wall
            elif pixel_tone < 150:
                if instance == 0:
                    tile = 2
                    t_type = 0
                else:
                    tile = 0
                    t_type = floor
            else:
                if instance == len(GameStore.levels) - 1:
                    tile = 2
                    t_type = 1
                else:
                    tile = 0
                    t_type = floor
                GameStore.start_x = x
                GameStore.start_y = y
            tile_row.append(tile)                    # horizontal row of tiles
            type_row.append(t_type)                    # horizontal row of tile types

            material = choices(material_types, material_weights)[0]                  # single material
            mat_row.append(material)                 # horizontal row of materials

        tiles.append(tile_row)               # vertical column of horizontal tile rows
        tileTypes.append(type_row)           # vertical column of horizontal type rows
        tileMats.append(mat_row)             # vertical column of horizontal material rows
    return tiles


def initialize_level(surface_id):
    """Draws the tiles with according images on a blank surface"""
    # generate the map
    gen_rand_map_tiles(surface_id)
    GameStore.levels[surface_id] = pygame.Surface((GameStore.MAP_WIDTH * TILE_SIZE, GameStore.MAP_HEIGHT * TILE_SIZE))
    # generate material variations
    while GameStore.mud_variations > 0:
        for i in range(len(tile_class.tileTypes[1])):
            tile_class.generate_material(1, i, 1, GameStore.mud_variations)
        GameStore.mud_variations -= 1
    while GameStore.moss_variations > 0:
        for i in range(len(tile_class.tileTypes[1])):
            tile_class.generate_material(1, i, 2, GameStore.moss_variations)
        GameStore.moss_variations -= 1
    # draw the tiles to the level surface
    for column in range(GameStore.MAP_HEIGHT):
        for row in range(GameStore.MAP_WIDTH):
            x_pos = row * TILE_SIZE
            y_pos = column * TILE_SIZE
            if tiles[column][row] == 0:
                if surface_id == 0:
                    floorTiles.append([x_pos + GameStore.starting_point_x[surface_id], y_pos +
                                       GameStore.starting_point_y[surface_id]])
                material = tile_class.assign_material(tiles[column][row], tileTypes[column][row], tileMats[column][row])
            elif tiles[column][row] == 1:
                wallTiles.append([x_pos + GameStore.starting_point_x[surface_id], y_pos +
                                  GameStore.starting_point_y[surface_id]])
                material = tile_class.assign_material(tiles[column][row], tileTypes[column][row], tileMats[column][row])
            elif tiles[column][row] == 2:
                doorTiles.append([x_pos + GameStore.starting_point_x[surface_id], y_pos +
                                  GameStore.starting_point_y[surface_id]])
                material = tile_class.assign_material(tiles[column][row], tileTypes[column][row], tileMats[column][row])

            """
            files = [f for f in os.listdir("Well Escape tiles/varieties")
                     if os.path.isfile(os.path.join("Well Escape tiles/varieties", f))]
            variety_amount = len(files)
            """

            GameStore.levels[surface_id].blit(material, (x_pos, y_pos, TILE_SIZE, TILE_SIZE))


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
    shutil.rmtree("Well Escape tiles/varieties")
    pygame.quit()
    sys.exit()


# creates a new level and positions everything accordingly in that level
def start():
    # reset all lists
    floorTiles.clear()
    wallTiles.clear()
    doorTiles.clear()
    # generate the dungeon
    for i in range(len(GameStore.levels)):
        if i > 0:
            # set the starting point for the next room
            GameStore.starting_point_x[i] = GameStore.starting_point_x[i-1] + GameStore.start_x * TILE_SIZE - TILE_SIZE
            GameStore.starting_point_y[i] = GameStore.starting_point_y[i-1] + GameStore.start_y * TILE_SIZE
        # create the room
        initialize_level(i)
    # create movement variables
    screen_rect = screen.get_rect()
    level_rect = GameStore.levels[0].get_rect()

    # find a random floor tile and get it's position coordinates
    GameStore.playerSpawnPoint = floorTiles[random.randint(0, len(floorTiles)-1)]
    GameStore.playerX = GameStore.playerSpawnPoint[0]
    GameStore.playerY = GameStore.playerSpawnPoint[1]

    # variables for centering the level
    GameStore.x = screen_rect.centerx - level_rect.centerx
    GameStore.y = screen_rect.centery - level_rect.centery

    # variables for offsetting everything so the starting tile is always at the center
    GameStore.offsetX = -level_rect.centerx + GameStore.playerSpawnPoint[0]
    GameStore.offsetY = -level_rect.centery + GameStore.playerSpawnPoint[1]


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

    # if there's no keys pressed return early as there's nothing to test
    if idle:
        return last_direction, idle

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

    return direction, idle


def detect_collision(player_pos_x, player_pos_y):

    # create and draw the player col
    player_col = Rect(player_pos_x + 14, player_pos_y + (TILE_SIZE * 0.6), TILE_SIZE * 0.6, TILE_SIZE * 0.3)
    pygame.draw.rect(screen, Color("white"), player_col, 2)

    # create and draw tile cols
    for tile in range(len(wallTiles)):
        x = GameStore.x + wallTiles[tile][0] - GameStore.offsetX
        y = GameStore.y + wallTiles[tile][1] - GameStore.offsetY
        tile_col = Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, Color("white"), tile_col, 2)

    return GameStore.top_col, GameStore.bottom_col, GameStore.left_col, GameStore.right_col


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
        if library.KEY_PRESSED["left"] and not GameStore.left_col:
            # left key action
            GameStore.playerX -= movement_speed
            GameStore.x += movement_speed
            # set the current direction

        if library.KEY_PRESSED["right"] and not GameStore.right_col:
            # right key action
            GameStore.playerX += movement_speed
            GameStore.x -= movement_speed
            # set the current direction

        if library.KEY_PRESSED["forwards"] and not GameStore.top_col:
            # forwards key action
            GameStore.playerY -= movement_speed
            GameStore.y += movement_speed
            # set the current direction

        if library.KEY_PRESSED["backwards"] and not GameStore.bottom_col:
            # backwards key action
            GameStore.playerY += movement_speed
            GameStore.y -= movement_speed
            # set the current direction

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
        for i in range(len(GameStore.levels) - 1, -1, -1):
            screen.blit(GameStore.levels[i], (GameStore.x + GameStore.starting_point_x[i] - GameStore.offsetX,
                                              GameStore.y + GameStore.starting_point_y[i] - GameStore.offsetY))

        # update player's position
        player_x_pos = GameStore.x + GameStore.playerX - GameStore.offsetX
        player_y_pos = GameStore.y + GameStore.playerY - GameStore.offsetY
        # detect_collision(player_x_pos, player_y_pos)
        # draw the player
        screen.blit(pygame.transform.scale(player.get_current_sprite(),
                    (int(TILE_SIZE * 0.9), int(TILE_SIZE * 0.9))), (player_x_pos, player_y_pos))

        # update the display.
        pygame.display.flip()
        ticks_since_last_frame = t


if __name__ == "__main__":
    main()
