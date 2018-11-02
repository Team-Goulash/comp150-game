"""MAIN CODEBASE."""
import pygame
import sys
import library
import random
import UI
import os
import shutil
import playerLight
import math
from fuelMeter import *
from pygame.locals import *
from animator import Animator

import dungeonGenerator as dunGen
import colorBlindFilter
import CollisionDetection as colDetect
import aiAnimations

# initialize pygame
pygame.init()
# Set the window size
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1334

# create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

import tileEditor as Editor
# UI Buttons
main_menu_buttons = {"new game": None, "continue": None, "options": None,
                     "controls": None, "quit game": None, "back": None}

# UI Buttons
game_over_buttons = {"restart": None, "exit to menu": None, "quit game": None}
game_over_buttons["restart"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                             (460, 110))
game_over_buttons["exit to menu"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                             (460, 110))
game_over_buttons["quit game"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                             (460, 110))
main_menu_buttons = {"new game": None, "tile editor": None, "continue": None, "options": None, "controls": None, "quit game": None, "back": None}
main_menu_buttons["new game"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                             (460, 75))
main_menu_buttons["tile editor"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                             (460, 75))
main_menu_buttons["continue"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                             (460, 75))
main_menu_buttons["options"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                            (460, 75))
main_menu_buttons["controls"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                             (460, 75))
main_menu_buttons["quit game"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                              (460, 75))
main_menu_buttons["back"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                      (160, 110))
option_buttons = {"resume": None, "options": None, "controls": None, "exit": None, "back": None, "restart": None}
option_buttons["resume"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                        (460, 85))
option_buttons["options"] = UI.UIButtons("UI/Button_000_hover.png",
                                         "UI/Button_000_normal.png",
                                         "UI/button_000_pressed.png",
                                         (460, 85))
option_buttons["controls"] = UI.UIButtons("UI/Button_000_hover.png",
                                          "UI/Button_000_normal.png",
                                          "UI/button_000_pressed.png",
                                          (460, 85))
option_buttons["exit"] = UI.UIButtons("UI/Button_000_hover.png",
                                      "UI/Button_000_normal.png",
                                      "UI/button_000_pressed.png",
                                      (460, 85))
option_buttons["back"] = UI.UIButtons("UI/Button_000_hover.png",
                                      "UI/Button_000_normal.png",
                                      "UI/button_000_pressed.png",
                                      (160, 110))
option_buttons["restart"] = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "UI/button_000_pressed.png",
                                         (460, 85))
# set the window caption
pygame.display.set_caption("Well Escape")

# set the FPS
FPS = 60
# initialize the FPS clock
fps_clock = pygame.time.Clock()

fuel_meter = Torch()

# text size
title_text = pygame.font.Font("UI/AMS hand writing.ttf", 115)
button_text = pygame.font.Font("UI/AMS hand writing.ttf", 55)
button_text_60 = pygame.font.Font("UI/AMS hand writing.ttf", 60)


# set player animations
player_animation = ["", "", "", ""]
# Todo turn magic numbers in animations into constants
# set left animation
player_animation[library.LEFT] = Animator("Characters/"
                                          "girl_sideLeft_spriteSheet.png",
                                          library.scaleNum, 3, 7, 0.75)
# set right animation
player_animation[library.RIGHT] = Animator("Characters/"
                                           "girl_sideRight_spriteSheet.png",
                                           library.scaleNum, 3, 7, 0.75)
# set forwards animation
player_animation[library.FORWARDS] = Animator("Characters/"
                                              "girl_back_spriteSheet.png",
                                              library.scaleNum, 3, 7, 0.75)
# set backwards animation
player_animation[library.BACKWARDS] = Animator("Characters/"
                                               "girl_front_spriteSheet.png",
                                               library.scaleNum, 3, 7, 0.75)

# set player idle animations
player_idle_animation = ["", "", "", ""]
# set left idle animation
player_idle_animation[library.LEFT] = Animator("Characters/girl_sideLeftIdle"
                                               "_spriteSheet.png",
                                               library.scaleNum, 3, 7, 1.5)
# set right idle animation
player_idle_animation[library.RIGHT] = Animator("Characters/girl_sideRightIdle"
                                                "_spriteSheet.png",
                                                library.scaleNum, 3, 7, 1.5)
# set forwards idle animation
player_idle_animation[library.FORWARDS] = Animator("Characters/girl_backIdle"
                                                   "_spriteSheet.png",
                                                   library.scaleNum, 3, 7, 1.5)
# set backwards idle animation
player_idle_animation[library.BACKWARDS] = Animator("Characters/girl_frontIdle"
                                                    "_spriteSheet.png",
                                                    library.scaleNum,
                                                    3, 7, 1.5)

ghost_animations = Animator("Well Escape Tiles/ghostTiles/ghost_0_face_3.png",
                            library.scaleNum, 3, 7, 1.5)  # list()

aiAnimationPaths = aiAnimations.AiAnimation()

if not os.path.exists("Well Escape tiles/varieties"):
    os.makedirs("Well Escape tiles/varieties")
else:
    shutil.rmtree("Well Escape tiles/varieties")
    os.makedirs("Well Escape tiles/varieties")


def event_inputs():
    """Get the inputs and set the key presses."""
    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            exit_game()
        # change the key pressed state
        elif event.type == KEYDOWN or event.type == KEYUP:

            # set left key pressed (A)
            if event.key == library.MOVE["left"]:
                library.KEY_PRESSED["left"] = event.type == KEYDOWN

                # set right key pressed (D)
            elif event.key == library.MOVE["right"]:
                library.KEY_PRESSED["right"] = event.type == KEYDOWN

                # set forwards key pressed (W)
            elif event.key == library.MOVE["forwards"]:
                library.KEY_PRESSED["forwards"] = event.type == KEYDOWN

                # set backwards key pressed (S)
            elif event.key == library.MOVE["backwards"]:
                library.KEY_PRESSED["backwards"] = event.type == KEYDOWN

            elif event.key == K_p:
                colorBlindFilter.color_blind_filter()
                colorBlindFilter.loop_image()
                print("taking color blind screenshot")
            elif event.key == K_SPACE:
                library.KEY_PRESSED["space"] = event.type == KEYDOWN

        if event.type == KEYUP:
            if event.key == library.PAUSE and library.MAIN_MENU is False: # Pauses the game
                library.PAUSED = not library.PAUSED
                library.CONTROLS = False
                library.OPTIONS = False

        # has a mouse button just been pressed?
        elif event.type == MOUSEBUTTONDOWN:
            library.KEY_PRESSED["mouse"] = True

        elif event.type == MOUSEBUTTONUP:                       # has a mouse button just been released?
            if main_menu_buttons["new game"].is_pressed(pygame.mouse.get_pos(), (460, 168),
                                                        library.KEY_PRESSED["mouse"]) and library.MAIN_MENU is True:
                if library.HAD_FIRST_RUN:
                    dunGen.reset(True)

                library.HAD_FIRST_RUN = True

                # Starts a new game
                library.HAS_STARTED = True
                library.MAIN_MENU = False
                library.PAUSED = False
            elif main_menu_buttons["continue"].is_pressed(pygame.mouse.get_pos(), (460, 268),
                                                          library.KEY_PRESSED["mouse"]) and library.MAIN_MENU is True:
                #   just starts a new game for now will be changed to a load game function
                library.HAS_STARTED = True
                library.MAIN_MENU = False
            elif main_menu_buttons["options"].is_pressed(pygame.mouse.get_pos(), (460, 368),
                                                         library.KEY_PRESSED["mouse"]) and library.MAIN_MENU is True:
                #   Opens up settings from the main menu
                library.SETTINGS = True
            elif main_menu_buttons["controls"].is_pressed(pygame.mouse.get_pos(), (460, 468),
                                                          library.KEY_PRESSED["mouse"]) and library.MAIN_MENU is True:
                # Opens up controls from the main menu
                library.MAIN_MENU_CONTROLS = True
            elif main_menu_buttons["quit game"].is_pressed(pygame.mouse.get_pos(), (460, 668),
                                                           library.KEY_PRESSED["mouse"]) and library.MAIN_MENU is True:
                # Quits the game
                exit_game()
            elif main_menu_buttons["tile editor"].is_pressed(pygame.mouse.get_pos(), (460, 568),
                                                           library.KEY_PRESSED["mouse"]) and library.MAIN_MENU is True:
                # Opens tile editor
                library.EDITOR = True
            elif library.SETTINGS is True and main_menu_buttons["back"].is_pressed(pygame.mouse.get_pos(), (51, 613),
                                                                                   library.KEY_PRESSED["mouse"]):
                # Checks to see if you're in settings before going back to the main menu
                library.SETTINGS = False

            elif library.MAIN_MENU_CONTROLS is True and \
                    main_menu_buttons["back"].\
                    is_pressed(pygame.mouse.get_pos(),
                               (51, 613), library.KEY_PRESSED["mouse"]):
                # Checks to see if you're in controls
                # before going back to the main menu
                library.MAIN_MENU_CONTROLS = False
            if option_buttons["resume"].is_pressed(pygame.mouse.get_pos(), (460, 188), library.KEY_PRESSED["mouse"])\
                    and library.PAUSE_MENU is True:
                #   Resumes the game
                library.PAUSED = False
            elif option_buttons["options"].is_pressed(pygame.mouse.get_pos(), (460, 288), library.KEY_PRESSED["mouse"])\
                    and library.PAUSE_MENU is True:
                #   Opens the options interface
                library.OPTIONS = True
            elif option_buttons["restart"].is_pressed(pygame.mouse.get_pos(), (460, 388), library.KEY_PRESSED["mouse"])\
                    and library.PAUSE_MENU is True:
                #  Restarts the game
                library.PAUSED = False
                # Todo this needs to just reset the current room insted of makeing a new one.
                dunGen.reset(dunGen.GameStore.current_dungeon == 0, True)
            elif option_buttons["controls"].is_pressed(pygame.mouse.get_pos(), (460, 488), library.KEY_PRESSED["mouse"])\
                    and library.PAUSE_MENU is True:
                # Opens the controls interface
                library.CONTROLS = True
                print("pause controls")
            elif option_buttons["exit"].is_pressed(pygame.mouse.get_pos(), (460, 588), library.KEY_PRESSED["mouse"])\
                    and library.PAUSE_MENU is True:
                # Sends you to the main menu
                print("menu test")
                main_menu()
                library.HAS_STARTED = False

            elif library.CONTROLS is True and option_buttons["back"].\
                    is_pressed(pygame.mouse.get_pos(), (51, 613),
                               library.KEY_PRESSED["mouse"]):
                #   A check to make sure you're in controls when clicking back
                library.CONTROLS = False
            elif library.OPTIONS is True and option_buttons["back"].\
                    is_pressed(pygame.mouse.get_pos(), (51, 613),
                               library.KEY_PRESSED["mouse"]):
                #  this is a check to see if you're in options
                #  when clicking back
                library.OPTIONS = False

            if game_over_buttons["restart"].is_pressed(pygame.mouse.get_pos(), (460, 168), library.KEY_PRESSED["mouse"]
                                                         and library.GAME_OVER is True):
                library.GAME_OVER = False
                library.RESET = True
                dunGen.reset(True)

            elif game_over_buttons["exit to menu"].is_pressed(pygame.mouse.get_pos(), (460, 318),
                                                            library.KEY_PRESSED["mouse"] and library.GAME_OVER is True):
                main_menu()
                library.GAME_OVER = False
                library.HAS_STARTED = False
            elif game_over_buttons["quit game"].is_pressed(pygame.mouse.get_pos(), (460, 468),
                                                           library.KEY_PRESSED["mouse"] and library.GAME_OVER is True):
                exit_game()

            library.KEY_PRESSED["mouse"] = False


def game_over():

    controls_text = pygame.font.Font("UI/AMS hand writing.ttf", 175)
    screen.fill(library.WHITE)
    # title
    text_surf, text_rect = library.text_objects("Game Over", controls_text)
    text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 8))
    # Restart Game button
    restart_surf, restart_rect = library.text_objects("Restart", button_text_60)
    restart_rect.center = (690, 220)
    # Exit to menu Button
    menu_surf, menu_rect = library.text_objects("Exit to Menu", button_text_60)
    menu_rect.center = (690, 370)
    # Quit button
    quit_surf, quit_rect = library.text_objects("Quit Game", button_text_60)
    quit_rect.center = (690, 520)
    # blits the buttons
    screen.blit(text_surf, text_rect)
    # button positioning
    screen.blit(game_over_buttons["restart"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                          (460, 168)), (460, 168))
    screen.blit(game_over_buttons["exit to menu"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                          (460, 318)), (460, 318))
    screen.blit(game_over_buttons["quit game"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                         (460, 468)), (460, 468))
    # blits
    screen.blit(restart_surf, restart_rect)
    screen.blit(menu_surf, menu_rect)
    screen.blit(quit_surf, quit_rect)


def main_menu():
    if library.MAIN_MENU_CONTROLS is True: # if the controls are true it'll display the controls from the main menu
        library.MAIN_MENU = False
        controls = pygame.transform.scale(pygame.image.load("UI/Controls.png"), (800, 600))
        screen.fill(library.WHITE)
        text_surf, text_rect = library.text_objects("Controls", title_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 8))
        back_surf, back_rect = library.text_objects("Back", button_text_60)
        back_rect.center = (134, 664)

        screen.blit(main_menu_buttons["back"].
                    draw_button(pygame.mouse.get_pos(),
                                library.KEY_PRESSED["mouse"],
                                (60, 640)), (51, 613))

        screen.blit(text_surf, text_rect)
        screen.blit(back_surf, back_rect)
        screen.blit(controls, (250, 130))
        pygame.display.flip()
    elif library.SETTINGS is True: # if the settings are true it'll display the settings interface from the main menu
        library.MAIN_MENU = False


        screen.fill(library.WHITE)
        text_surf, text_rect = library.text_objects("Settings", title_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 7))
        back_surf, back_rect = library.text_objects("Back", button_text_60)
        back_rect.center = (134, 664)

        screen.blit(main_menu_buttons["back"].
                    draw_button(pygame.mouse.get_pos(),
                                library.KEY_PRESSED["mouse"],
                                (60, 640)), (51, 613))

        screen.blit(text_surf, text_rect)
        screen.blit(back_surf, back_rect)

    # if neither are true it'll display the main menu
    else:
        library.MAIN_MENU = True
        controls_text = pygame.font.Font("UI/AMS hand writing.ttf", 175)
        screen.fill(library.WHITE)

        # title
        text_surf, text_rect = library.text_objects("Well Escape", controls_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 8))

        # New Game button
        new_game_surf, new_game_rect = library.text_objects("New Game", button_text_60)
        new_game_rect.center = (690, 204)

        # Load Game Button
        continue_game_surf, continue_game_rect = library.text_objects("Load Game", button_text_60)
        continue_game_rect.center = (690, 306)

        # Settings button
        options_surf, options_rect = library.text_objects("Settings", button_text_60)
        options_rect.center = (690, 403)

        # Controls button
        controls_surf, controls_rect = library.text_objects("Controls", button_text_60)
        controls_rect.center = (690, 504)

        # Quit Game button
        quit_surf, quit_rect = library.text_objects("Quit Game", button_text_60)
        quit_rect.center = (690, 704)
        # Tile Editor button
        tile_editor_surf, tile_editor_rect = library.text_objects("Tile Editor", button_text_60)
        tile_editor_rect.center = (690, 604)

        # blits the buttons
        screen.blit(text_surf, text_rect)

        # button positioning
        # blits
        screen.blit(main_menu_buttons["new game"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 168)), (460, 168))
        screen.blit(main_menu_buttons["continue"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 268)), (460, 268))
        screen.blit(main_menu_buttons["options"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 368)), (460, 368))
        screen.blit(main_menu_buttons["controls"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 468)), (460, 468))
        screen.blit(main_menu_buttons["quit game"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                              (460, 668)), (460, 668))
        screen.blit(main_menu_buttons["tile editor"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                               (460, 568)), (460, 568))

        screen.blit(new_game_surf, new_game_rect)
        screen.blit(tile_editor_surf, tile_editor_rect)
        screen.blit(continue_game_surf, continue_game_rect)
        screen.blit(options_surf, options_rect)
        screen.blit(controls_surf, controls_rect)
        screen.blit(quit_surf, quit_rect)


def pause_menu():
    """Display the pause menu."""
    # checks if the library.conrols is true
    # before displaying the controls interface
    if library.CONTROLS is True:
        controls = pygame.transform.scale(
            pygame.image.load("UI/Controls.png"), (800, 600))

        screen.fill(library.WHITE)
        text_surf, text_rect = library.text_objects("Controls", title_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 8))
        back_surf, back_rect = library.text_objects("Back", button_text_60)
        back_rect.center = (134, 664)

        screen.blit(option_buttons["back"].
                    draw_button(pygame.mouse.get_pos(),
                                library.KEY_PRESSED["mouse"],
                                (60, 640)), (51, 613))

        screen.blit(text_surf, text_rect)
        screen.blit(back_surf, back_rect)
        screen.blit(controls, (250, 130))
        pygame.display.flip()

    # this checks if library.options is true
    # before displaying the options interface
    elif library.OPTIONS is True:
        screen.fill(library.WHITE)
        text_surf, text_rect = library.text_objects("Options", title_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 7))
        back_surf, back_rect = library.text_objects("Back", button_text_60)
        back_rect.center = (134, 664)

        screen.blit(option_buttons["back"].
                    draw_button(pygame.mouse.get_pos(),
                                library.KEY_PRESSED["mouse"],
                                (60, 640)), (51, 613))

        screen.blit(text_surf, text_rect)
        screen.blit(back_surf, back_rect)

    else:  # if neither are true it'll display the pause screen
        library.PAUSED = True
        library.PAUSE_MENU = True
        button_text2 = pygame.font.Font("UI/AMS hand writing.ttf", 50)
        screen.fill(library.WHITE)
        # title
        text_surf, text_rect = library.text_objects("Paused", title_text)
        text_rect.center = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 7))
        # Resume button
        screen.blit(option_buttons["resume"].
                    draw_button(pygame.mouse.get_pos(),
                                library.KEY_PRESSED["mouse"],
                                (460, 208)), (460, 188))

        # Options button
        screen.blit(option_buttons["options"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (460, 288)),
                    (460, 288))
        # Restart button
        screen.blit(
            option_buttons["restart"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (460, 388)),
            (460, 388))
        # Controls button
        screen.blit(option_buttons["controls"].
                    draw_button(pygame.mouse.get_pos(),
                                library.KEY_PRESSED["mouse"],
                                (460, 508)), (460, 488))

        # Exit button
        screen.blit(option_buttons["exit"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (460, 588)),
                    (460, 588))
        resume_surf, resume_rect = library.text_objects("Resume", button_text_60)
        resume_rect.center = (690, 228)
        options_surf, options_rect = library.text_objects("Options", button_text_60)
        options_rect.center = (690, 328)
        restart_surf, restart_rect = library.text_objects("Restart", button_text_60)
        restart_rect.center = (690, 428)
        controls_surf, controls_rect = library.text_objects("Controls", button_text_60)
        controls_rect.center = (690, 528)
        quit_surf, quit_rect = library.text_objects("Exit to Main Menu", button_text2)
        quit_rect.center = (690, 628)

        screen.blit(quit_surf, quit_rect)
        screen.blit(controls_surf, controls_rect)
        screen.blit(options_surf, options_rect)
        screen.blit(restart_surf, restart_rect)
        screen.blit(text_surf, text_rect)
        screen.blit(resume_surf, resume_rect)


def pausing_game():
    """Pause the game."""
    for event in pygame.event.get():
        if paused is False:
            if event.type == library.PAUSE:
                paused = not paused
                pause_menu()

        if paused:
            pause_menu()
            continue


def exit_game():
    """Exit the game to desktop."""
    shutil.rmtree("Well Escape tiles/varieties")
    pygame.quit()
    sys.exit()


# creates a new level and positions everything accordingly in that level
def start():
    """Initialise the game."""
    # create movement variables
    screen_rect = screen.get_rect()
    level_rect = dunGen.GameStore.levels[0].get_rect()

    if dunGen.GameStore.well_room:
        # find a random floor tile and get it's position coordinates
        spawn_x = (math.ceil(len(dunGen.floorTilesX) * 0.5)
                   + random.randint(-2, 2)) * dunGen.TILE_SIZE
        spawn_y = (math.ceil(len(dunGen.floorTilesY) * 0.5)
                   + random.randint(-1, 1)) * dunGen.TILE_SIZE
        dunGen.GameStore.playerSpawnPoint = [spawn_x, spawn_y]
        dunGen.GameStore.well_room = False
    else:
        door_pos = dunGen.allTilePositions[dunGen.allTiles.index(2)]
        dunGen.GameStore.playerSpawnPoint = [door_pos[0], door_pos[1]
                                             + (dunGen.TILE_SIZE * 0.5)]

    dunGen.GameStore.playerX = dunGen.GameStore.playerSpawnPoint[0]
    dunGen.GameStore.playerY = dunGen.GameStore.playerSpawnPoint[1]

    # variables for centering the level
    dunGen.GameStore.x = screen_rect.centerx - level_rect.centerx
    dunGen.GameStore.y = screen_rect.centery - level_rect.centery

    # variables for offsetting everything
    # so the starting tile is always at the center
    dunGen.GameStore.offsetX = -level_rect.centerx +\
        dunGen.GameStore.playerSpawnPoint[0]
    dunGen.GameStore.offsetY = -level_rect.centery +\
        dunGen.GameStore.playerSpawnPoint[1]
    library.RESET = False


def change_direction(last_dir, current_dir):
    """
    Reset the players animator if the direction changes.

    :param last_dir:        players direction from last frame
    :param current_dir:     players direction this frame
    :return:                current direction
    """
    if last_dir != current_dir:
        player_animation[last_dir].reset()
    return current_dir


def animation_direction(last_direction):
    """
    Get the next animation direction.

    this prevents it from resetting if two keys are pressed at the same time!
    :return: (Direction, idle)
    """
    # find if any keys are pressed and set it to idle
    idle = not library.KEY_PRESSED["left"] and not \
        library.KEY_PRESSED["right"] and not \
        library.KEY_PRESSED["forwards"] and not \
        library.KEY_PRESSED["backwards"]

    # if there's no keys pressed return early as there's nothing to test
    if idle:
        return last_direction, idle

    # set direction to last direction
    # in case there is opposite keys being pressed
    direction = last_direction

    # set to idle if both left and right keys are pressed
    if library.KEY_PRESSED["left"] and library.KEY_PRESSED["right"]:
        idle = True
    elif library.KEY_PRESSED["left"]:       # set left direction
        direction = library.LEFT
    elif library.KEY_PRESSED["right"]:      # set right direction
        direction = library.RIGHT

    # do forwards and backwards in separate if
    # as the animation trumps left and right
    # set to idle if both forwards and backwards keys are pressed
    if library.KEY_PRESSED["forwards"] and library.KEY_PRESSED["backwards"]:
        # set to idle if neither left or right is pressed
        idle = not library.KEY_PRESSED["left"] and not\
            library.KEY_PRESSED["right"]
    elif library.KEY_PRESSED["forwards"]:
        direction = library.FORWARDS        # set forwards direction
        idle = False
    elif library.KEY_PRESSED["backwards"]:
        direction = library.BACKWARDS       # set backwards direction
        idle = False

    return direction, idle


def main():
    """Main game loop."""
    dunGen.create_dungeon()
    ticks_since_last_frame = 0

    # players current direction
    current_direction = library.BACKWARDS

    # main game loop
    while True:
        movement_speed = 0

        t = pygame.time.get_ticks()
        # amount of time that passed since the last frame in seconds
        delta_time = (t - ticks_since_last_frame) / 1000.0

        if library.EDITOR:
            Editor.display()
            ticks_since_last_frame = t
            continue

        # Get inputs
        event_inputs()

        display_pause_menu = False

        # set the players animation direction and idle for the animation
        next_animation_direction, player_idle = \
            animation_direction(current_direction)
        # set the current direction
        current_direction = change_direction(current_direction,
                                             next_animation_direction)

        if not library.PAUSED and library.HAS_STARTED:
            # multiply the movement by delta_time to ensure constant speed
            # no matter the FPS
            movement_speed = 75 * delta_time

        # switch between active and idle
        if not player_idle:
            player = player_animation[current_direction]

        # prevent the player from moving if the game has not finished resetting
        if library.RESET or library.PAUSED or library.GAME_OVER or not library.HAS_STARTED:
            movement_speed = 0

        if not library.RESET:
            if not library.PAUSED:
                colDetect.detect_collision()
                # Key press actions
                if library.KEY_PRESSED["forwards"] and \
                        not library.KEY_PRESSED["backwards"]:
                    dunGen.GameStore.bottom_col = False
                    if not dunGen.GameStore.top_col:
                        # move the player and assign prediction values
                        dunGen.GameStore.previousY = dunGen.GameStore.y
                        dunGen.GameStore.playerY -= movement_speed
                        dunGen.GameStore.y += movement_speed

                        dunGen.GameStore.prediction_Y = -10
                        if not library.KEY_PRESSED["right"] and \
                                not library.KEY_PRESSED["left"]:
                            dunGen.GameStore.prediction_X = 0
                            dunGen.GameStore.secondary_prediction_X = 0

                        if not dunGen.GameStore.left_col and \
                                not dunGen.GameStore.right_col:
                            dunGen.GameStore.secondary_prediction_Y = -10
                    else:
                        # block the player movement
                        dunGen.GameStore.prediction_Y = 0
                        if not dunGen.GameStore.previousY == dunGen.GameStore.y:
                            dunGen.GameStore.y -= movement_speed
                            dunGen.GameStore.previousY = dunGen.GameStore.y
                        dunGen.GameStore.playerY = dunGen.GameStore.previousPlayerY

                if library.KEY_PRESSED["backwards"] and \
                        not library.KEY_PRESSED["forwards"]:
                    dunGen.GameStore.top_col = False
                    if not dunGen.GameStore.bottom_col:
                        # move the player and assign prediction values
                        dunGen.GameStore.previousY = dunGen.GameStore.y
                        dunGen.GameStore.playerY += movement_speed
                        dunGen.GameStore.y -= movement_speed

                        dunGen.GameStore.prediction_Y = 10
                        if not library.KEY_PRESSED["right"] and \
                                not library.KEY_PRESSED["left"]:
                            dunGen.GameStore.prediction_X = 0
                            dunGen.GameStore.secondary_prediction_X = 0

                        if not dunGen.GameStore.left_col and \
                                not dunGen.GameStore.right_col:
                            dunGen.GameStore.secondary_prediction_Y = 10
                    else:
                        # block the player movement
                        dunGen.GameStore.prediction_Y = 0
                        if not dunGen.GameStore.previousY == dunGen.GameStore.y:
                            dunGen.GameStore.y += movement_speed
                            dunGen.GameStore.previousY = dunGen.GameStore.y
                        dunGen.GameStore.playerY = dunGen.GameStore.previousPlayerY

                if library.KEY_PRESSED["left"] and \
                        not library.KEY_PRESSED["right"]:
                    dunGen.GameStore.right_col = False
                    if not dunGen.GameStore.left_col:
                        # move the player and assign prediction values
                        dunGen.GameStore.previousX = dunGen.GameStore.x
                        dunGen.GameStore.playerX -= movement_speed
                        dunGen.GameStore.x += movement_speed

                        dunGen.GameStore.prediction_X = -20
                        if not library.KEY_PRESSED["forwards"] and \
                                not library.KEY_PRESSED["backwards"]:
                            dunGen.GameStore.prediction_Y = 0
                            dunGen.GameStore.secondary_prediction_Y = 0

                        if not dunGen.GameStore.bottom_col and \
                                not dunGen.GameStore.top_col:
                            dunGen.GameStore.secondary_prediction_X = -20
                    else:
                        # block the player movement
                        dunGen.GameStore.prediction_X = 0
                        if not dunGen.GameStore.previousX == dunGen.GameStore.x:
                            dunGen.GameStore.x -= movement_speed
                            dunGen.GameStore.previousX = dunGen.GameStore.x
                        dunGen.GameStore.playerX = dunGen.GameStore.previousPlayerX

                if library.KEY_PRESSED["right"] and \
                        not library.KEY_PRESSED["left"]:
                    dunGen.GameStore.left_col = False
                    if not dunGen.GameStore.right_col:
                        # move the player and assign prediction values
                        dunGen.GameStore.previousX = dunGen.GameStore.x
                        dunGen.GameStore.playerX += movement_speed
                        dunGen.GameStore.x -= movement_speed

                        dunGen.GameStore.prediction_X = 15
                        if not library.KEY_PRESSED["forwards"] and \
                                not library.KEY_PRESSED["backwards"]:
                            dunGen.GameStore.prediction_Y = 0
                            dunGen.GameStore.secondary_prediction_Y = 0

                        if not dunGen.GameStore.bottom_col and \
                                not dunGen.GameStore.top_col:
                            dunGen.GameStore.secondary_prediction_X = 15
                    else:
                        # block the player movement
                        dunGen.GameStore.prediction_X = 0
                        if not dunGen.GameStore.previousX == dunGen.GameStore.x:
                            dunGen.GameStore.x += movement_speed
                            dunGen.GameStore.previousX = dunGen.GameStore.x
                        dunGen.GameStore.playerX = dunGen.GameStore.previousPlayerX

                # switch between active and idle
                if not player_idle:
                    player = player_animation[current_direction]
                else:
                    player = player_idle_animation[current_direction]

                # update animation times
                if not library.GAME_OVER and library.HAS_STARTED:
                    player.update_time(delta_time)
                    ghost_animations.update_time(delta_time)
                    fuel_meter.update_fuel_timer(delta_time)
            else:
                display_pause_menu = True


            # Display main menu if the game has not started
            if not library.HAS_STARTED:
                main_menu()
            elif library.GAME_OVER:
                game_over()
            # display the pause menu if the game paused
            elif display_pause_menu is True:
                pause_menu()
            else:
                # fill the background
                screen.fill(library.BLACK)
                # render the level on screen
                for i in range(len(dunGen.GameStore.levels) - 1, -1, -1):
                    screen.blit(dunGen.GameStore.levels[i],
                                (dunGen.GameStore.x +
                                 dunGen.GameStore.starting_point_x[i] -
                                 dunGen.GameStore.offsetX, dunGen.GameStore.y +
                                 dunGen.GameStore.starting_point_y[i] -
                                 dunGen.GameStore.offsetY))

                # update player's position
                player_x_pos, player_y_pos = dunGen.get_position_with_offset(
                    dunGen.GameStore.playerX, dunGen.GameStore.playerY
                )

                dunGen.draw_chest()

                # draw the player
                screen.blit(pygame.transform.scale(player.get_current_sprite(),
                            (int(dunGen.TILE_SIZE * 0.9),
                             int(dunGen.TILE_SIZE * 0.9))),
                            (player_x_pos, player_y_pos))

                aiAnimationPaths.update_animations(delta_time, screen)

                if aiAnimationPaths.ghost_in_position(player_x_pos, player_y_pos, screen):
                    library.GAME_OVER = True

                playerLight.update_light(fuel_meter.get_fuel_percentage())
                playerLight.initialise_lightning(dunGen.TILE_SIZE)
                playerLight.draw_light(screen, dunGen)
                playerLight.overlay(screen)

                fuel_meter.display_fuel_meter(screen, (630, 50))

        if fuel_meter.torch_time == 0:
            library.GAME_OVER = True
        if dunGen.GameStore.reset_fuel:
            fuel_meter.reset_fuel()
            dunGen.GameStore.reset_fuel = False

        # update the display.
        fps_clock.tick(FPS)
        pygame.display.flip()
        ticks_since_last_frame = t


if __name__ == "__main__":
    colorBlindFilter.initialization()
    main()
