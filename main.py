# DON'T FORGET TO COMMENT YOUR CODE PLEASE!!!
import pygame, sys, library, random, UI
from pygame.locals import *
from random import choices

# initialize py game
pygame.init()
# Set the window size
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1334

# create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
main_menu_buttons = {"new game": None, "continue": None, "options": None, "controls": None, "quit game": None, "back": None}
main_menu_buttons["new game"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "Ui/button_000_pressed.png",
                                             (460, 75))
main_menu_buttons["continue"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "Ui/button_000_pressed.png",
                                             (460, 75))
main_menu_buttons["options"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "Ui/button_000_pressed.png",
                                            (460, 75))
main_menu_buttons["controls"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "Ui/button_000_pressed.png",
                                             (460, 75))
main_menu_buttons["quit game"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "Ui/button_000_pressed.png",
                                              (460, 75))
main_menu_buttons["back"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                      (160, 110))
option_buttons = {"resume": None, "options": None, "controls": None, "exit": None, "back": None}
option_buttons["resume"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                        (460, 110))
option_buttons["options"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                         (460, 110))
option_buttons["controls"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                          (460, 110))
option_buttons["exit"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                      (460, 110))
option_buttons["back"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                      (160, 110))

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
            if event.key == K_r:
                start()  # resets the level
            elif event.key == library.PAUSE:
                library.PAUSED = not library.PAUSED
                library.CONTROLS = False
                library.OPTIONS = False
        elif event.type == MOUSEBUTTONDOWN:                     # has a mouse button just been pressed?
            library.KEY_PRESSED["mouse"] = True
            print("This is mouse down")
        elif event.type == MOUSEBUTTONUP:                       # has a mouse button just been released?
            if main_menu_buttons["new game"].is_pressed(pygame.mouse.get_pos(), (460, 188),
                                                        library.KEY_PRESSED["mouse"]):
                library.HAS_STARTED = True
            elif main_menu_buttons["continue"].is_pressed(pygame.mouse.get_pos(), (460, 288),
                                                          library.KEY_PRESSED["mouse"]):
                library.HAS_STARTED = True
            elif main_menu_buttons["options"].is_pressed(pygame.mouse.get_pos(), (460, 388),
                                                         library.KEY_PRESSED["mouse"]):
                library.SETTINGS = True
            elif main_menu_buttons["controls"].is_pressed(pygame.mouse.get_pos(), (460, 488),
                                                          library.KEY_PRESSED["mouse"]):
                library.MAIN_MENU_CONTROLS = True
            elif main_menu_buttons["quit game"].is_pressed(pygame.mouse.get_pos(), (460, 588),
                                                           library.KEY_PRESSED["mouse"]):
                exit_game()
            elif library.SETTINGS is True and main_menu_buttons["back"].is_pressed(pygame.mouse.get_pos(), (51, 613),
                                                                                   library.KEY_PRESSED["mouse"]):
                library.SETTINGS = False
            elif library.MAIN_MENU_CONTROLS is True and main_menu_buttons["back"].is_pressed(pygame.mouse.get_pos(), (51, 613),
                                                                                   library.KEY_PRESSED["mouse"]):
                library.MAIN_MENU_CONTROLS = False
            if option_buttons["resume"].is_pressed(pygame.mouse.get_pos(), (460, 188), library.KEY_PRESSED["mouse"]):
                library.PAUSED = False
            elif option_buttons["options"].is_pressed(pygame.mouse.get_pos(), (460, 338), library.KEY_PRESSED["mouse"]):
                library.OPTIONS = True
            elif option_buttons["controls"].is_pressed(pygame.mouse.get_pos(), (460, 488), library.KEY_PRESSED["mouse"]):
                library.CONTROLS = True
            elif option_buttons["exit"].is_pressed(pygame.mouse.get_pos(), (460, 638), library.KEY_PRESSED["mouse"]):
                main_menu()
                library.HAS_STARTED = False
            elif library.CONTROLS is True and option_buttons["back"].is_pressed(pygame.mouse.get_pos(), (51, 613),
                                                                                library.KEY_PRESSED["mouse"]):
                library.CONTROLS = False
            elif library.OPTIONS is True and option_buttons["back"].is_pressed(pygame.mouse.get_pos(), (51, 613),
                                                                               library.KEY_PRESSED["mouse"]):
                library.OPTIONS = False
            library.KEY_PRESSED["mouse"] = False
            print("This is mouse up", pygame.mouse.get_pos())


def text_objects(text, font):
    text_surface = font.render(text, True, library.BLACK)
    return text_surface, text_surface.get_rect()


def main_menu():
    if library.MAIN_MENU_CONTROLS is True:
        controls_text = pygame.font.Font("UI/AMS hand writing.ttf", 115)
        button_text = pygame.font.Font("UI/AMS hand writing.ttf", 55)
        controls = pygame.transform.scale(pygame.image.load("UI/Controls.png"), (800, 600))
        screen.fill(library.WHITE)
        text_surf, text_rect = text_objects("Controls", controls_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 8))
        back_surf, back_rect = text_objects("Back", button_text)
        back_rect.center = (134, 664)
        screen.blit(main_menu_buttons["back"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (60, 640)),
                    (51, 613))
        screen.blit(text_surf, text_rect)
        screen.blit(back_surf, back_rect)
        screen.blit(controls, (250, 130))
        pygame.display.flip()
    elif library.SETTINGS is True:
        options_text = pygame.font.Font("UI/AMS hand writing.ttf", 115)
        button_text = pygame.font.Font("UI/AMS hand writing.ttf", 55)
        screen.fill(library.WHITE)
        text_surf, text_rect = text_objects("Settings", options_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 7))
        back_surf, back_rect = text_objects("Back", button_text)
        back_rect.center = (134, 664)
        screen.blit(main_menu_buttons["back"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (60, 640)),
                    (51, 613))
        screen.blit(text_surf, text_rect)
        screen.blit(back_surf, back_rect)
    else:
        controls_text = pygame.font.Font("UI/AMS hand writing.ttf", 175)
        button_text = pygame.font.Font("UI/AMS hand writing.ttf", 60)
        screen.fill(library.WHITE)
        text_surf, text_rect = text_objects("Well Escape", controls_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 8))
        new_game_surf, new_game_rect = text_objects("New Game", button_text)
        new_game_rect.center = (690, 224)
        continue_game_surf, continue_game_rect = text_objects("Load Game", button_text)
        continue_game_rect.center = (690, 326)
        options_surf, options_rect = text_objects("Settings", button_text)
        options_rect.center = (690, 423)
        controls_surf, controls_rect = text_objects("Controls", button_text)
        controls_rect.center = (690, 524)
        quit_surf, quit_rect = text_objects("Quit Game", button_text)
        quit_rect.center = (690, 624)
        screen.blit(text_surf, text_rect)
        screen.blit(main_menu_buttons["new game"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 208)), (460, 188))
        screen.blit(main_menu_buttons["continue"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 308)), (460, 288))
        screen.blit(main_menu_buttons["options"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 408)), (460, 388))
        screen.blit(main_menu_buttons["controls"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 508)), (460, 488))
        screen.blit(main_menu_buttons["quit game"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 608)), (460, 588))
        screen.blit(new_game_surf, new_game_rect)
        screen.blit(continue_game_surf, continue_game_rect)
        screen.blit(options_surf, options_rect)
        screen.blit(controls_surf, controls_rect)
        screen.blit(quit_surf, quit_rect)


def pause_menu():
    if library.CONTROLS is True:
        controls_text = pygame.font.Font("UI/AMS hand writing.ttf", 115)
        button_text = pygame.font.Font("UI/AMS hand writing.ttf", 55)
        controls = pygame.transform.scale(pygame.image.load("UI/Controls.png"), (800,600))
        screen.fill(library.WHITE)
        text_surf, text_rect = text_objects("Controls", controls_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 8))
        back_surf, back_rect = text_objects("Back", button_text)
        back_rect.center = (134, 664)
        screen.blit(option_buttons["back"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (60, 640)),
                    (51, 613))
        screen.blit(text_surf, text_rect)
        screen.blit(back_surf, back_rect)
        screen.blit(controls, (250, 130))
        pygame.display.flip()
    elif library.OPTIONS is True:
        options_text = pygame.font.Font("UI/AMS hand writing.ttf", 115)
        button_text = pygame.font.Font("UI/AMS hand writing.ttf", 55)
        screen.fill(library.WHITE)
        text_surf, text_rect = text_objects("Options", options_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 7))
        back_surf, back_rect = text_objects("Back", button_text)
        back_rect.center = (134, 664)
        screen.blit(option_buttons["back"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (60, 640)),
                    (51, 613))
        screen.blit(text_surf, text_rect)
        screen.blit(back_surf, back_rect)

    else:
        pause_text = pygame.font.Font("UI/AMS hand writing.ttf", 115)
        button_text = pygame.font.Font("UI/AMS hand writing.ttf", 60)
        button_text2 = pygame.font.Font("UI/AMS hand writing.ttf", 50)
        screen.fill(library.WHITE)
        text_surf, text_rect = text_objects("Paused", pause_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 7))
        screen.blit(option_buttons["resume"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (460, 208)),
                    (460, 188))
        screen.blit(option_buttons["options"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (460, 358)),
                    (460, 338))
        screen.blit(option_buttons["controls"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (460, 508)),
                    (460, 488))
        screen.blit(option_buttons["exit"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (460, 658)),
                    (460, 638))
        resume_surf, resume_rect = text_objects("Resume", button_text)
        resume_rect.center = (690, 238)
        options_surf, options_rect = text_objects("Options", button_text)
        options_rect.center = (690, 388)
        controls_surf, controls_rect = text_objects("Controls", button_text)
        controls_rect.center = (690, 538)
        quit_surf, quit_rect = text_objects("Exit to Main Menu", button_text2)
        quit_rect.center = (690, 688)
        screen.blit(quit_surf, quit_rect)
        screen.blit(controls_surf, controls_rect)
        screen.blit(options_surf, options_rect)
        screen.blit(text_surf, text_rect)
        screen.blit(resume_surf, resume_rect)


def pausing_game():
    for event in pygame.event.get():
        if paused is False:
            if event.type == library.PAUSE:
                paused = not paused
                pause_menu()

        if paused:
            pause_menu()
            continue


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
    level_init = False
    start()
    ticks_since_last_frame = 0
    # main game loop
    while True:
        t = pygame.time.get_ticks()
        # amount of time that passed since the last frame in seconds
        delta_time = (t - ticks_since_last_frame) / 1000.0
        # Get inputs
        event_inputs()
        display_pause_menu = False

        # multiply the movement by delta_time to ensure constant speed no matter the FPS
        movement_speed = 75 * delta_time
        if not library.PAUSED:
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
        else:
            display_pause_menu = True

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

        if not library.HAS_STARTED:
            main_menu()
        elif display_pause_menu is True:
            pause_menu()

        # update the display.
        pygame.display.flip()
        ticks_since_last_frame = t



if __name__ == "__main__":
    main()