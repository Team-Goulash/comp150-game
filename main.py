"""MAIN CODEBASE."""

import pygame
import timeManager
from stateContr import StateController
from player import Player
import sys
import library
import random
import UI
import os
import soundEffects
import shutil
import playerLight
import math
from fuelMeter import *
from pygame.locals import *

import dungeonGenerator as dunGen
import MelodyGenerator as melGen
import colorBlindFilter
import CollisionDetection as colDetect
import aiAnimations

import mainMenu

# initialize pygame
pygame.init()
# Set the window size
WINDOW_HEIGHT = 750
WINDOW_WIDTH = 1334

# create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

import tileEditor as Editor

# set the load bar font here so we know pygame has initialized
library.loading_bar_font_face = pygame.font.Font("UI/AMS hand writing.ttf", 18)
debug_header_font_face = pygame.font.Font("UI/AMS hand writing.ttf", 36)
debug_font_face = pygame.font.Font("UI/AMS hand writing.ttf", 22)

menu = mainMenu.Menu()
menus = None            # this is set just befor main is called at the end of the script

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

aiAnimationPaths = aiAnimations.AiAnimation()

# Game and menu states
game_state = StateController()
menu_state = StateController()
time = timeManager.TimeManager(pygame.time.get_ticks() / 1000.0)
player_object = Player(75, (0.9, 0.9), time)

sound_effects = soundEffects.SoundFX()

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
            elif event.key == K_y:
                sound_effects.apply_echo()
            elif event.key == K_h:
                sound_effects.play_echo_sound()
            elif event.key == K_SPACE:
                library.KEY_PRESSED["space"] = event.type == KEYDOWN

        if event.type == KEYUP:
            if event.key == K_F12:
                library.debug_mode = not library.debug_mode

            if event.key == library.PAUSE and library.MAIN_MENU is False: # Pauses the game
                if game_state.get_state() == "game":
                    game_state.set_state("paused")
                elif game_state.get_state() == "paused":
                    game_state.set_state("game")
                # Todo remove once new ui has been implemented
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
                    dunGen.DungeonGenerator.reset(dunGen.DungeonGenerator, True)

                library.HAD_FIRST_RUN = True

                # Starts a new game
                game_state.set_state("game")
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
                game_state.set_state("editor")
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
                game_state.set_state("game")
            elif option_buttons["options"].is_pressed(pygame.mouse.get_pos(), (460, 288), library.KEY_PRESSED["mouse"])\
                    and library.PAUSE_MENU is True:
                #   Opens the options interface
                library.OPTIONS = True
            elif option_buttons["restart"].is_pressed(pygame.mouse.get_pos(), (460, 388), library.KEY_PRESSED["mouse"])\
                    and library.PAUSE_MENU is True:
                #  Restarts the game
                library.PAUSED = False
                game_state.set_state("game")
                # Todo this needs to just reset the current room insted of makeing a new one.
                dunGen.DungeonGenerator.reset(dunGen.DungeonGenerator, dunGen.DungeonGenerator.current_dungeon == 0, True)
            elif option_buttons["controls"].is_pressed(pygame.mouse.get_pos(), (460, 488), library.KEY_PRESSED["mouse"])\
                    and library.PAUSE_MENU is True:
                # Opens the controls interface
                library.CONTROLS = True
                print("pause controls")
            elif option_buttons["exit"].is_pressed(pygame.mouse.get_pos(), (460, 588), library.KEY_PRESSED["mouse"])\
                    and library.PAUSE_MENU is True:
                # Sends you to the main menu
                print("menu test")
                game_state.set_state("main menu")
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
                dunGen.DungeonGenerator.reset(dunGen.DungeonGenerator, True, True)

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
    level_rect = dunGen.DungeonGenerator.levels[0].get_rect()

    if dunGen.DungeonGenerator.well_room:
        # find a random floor tile and get it's position coordinates
        spawn_x = (math.ceil(len(dunGen.floorTilesX) * 0.5)
                   + random.randint(-2, 2)) * dunGen.TILE_SIZE
        spawn_y = (math.ceil(len(dunGen.floorTilesY) * 0.5)
                   + random.randint(-1, 1)) * dunGen.TILE_SIZE
        dunGen.DungeonGenerator.playerSpawnPoint = [spawn_x, spawn_y]
        dunGen.DungeonGenerator.well_room = False
    else:
        door_pos = dunGen.allTilePositions[dunGen.allTiles.index(2)]
        dunGen.DungeonGenerator.playerSpawnPoint = [door_pos[0], door_pos[1]
                                                    + (dunGen.TILE_SIZE * 0.5)]

    player_object.position[0] = dunGen.DungeonGenerator.playerSpawnPoint[0]
    player_object.position[1] = dunGen.DungeonGenerator.playerSpawnPoint[1]

    # variables for centering the level
    dunGen.DungeonGenerator.x = screen_rect.centerx - level_rect.centerx
    dunGen.DungeonGenerator.y = screen_rect.centery - level_rect.centery

    # variables for offsetting everything
    # so the starting tile is always at the center
    dunGen.DungeonGenerator.offsetX = -level_rect.centerx + \
                                      dunGen.DungeonGenerator.playerSpawnPoint[0]
    dunGen.DungeonGenerator.offsetY = -level_rect.centery + \
                                      dunGen.DungeonGenerator.playerSpawnPoint[1]
    library.RESET = False

#UI functions
def ui_controls():
    screen.blit(pygame.transform.scale(pygame.image.load("UI/Controls.png"), (800, 600)), (200, 200))

def set_game_states(state):

    state.add_state("main menu", "main menu")
    state.add_state("loading", "loading")
    state.add_state("game", "game")
    state.add_state("game over", "game over")
    state.add_state("paused", "paused")
    state.add_state("editor", "editor")

    # set the state to the default main menu
    state.set_state("main menu")


def set_menu_states(state):

    state.add_state("main menu", "Main Menu")
    state.add_state("options", "Options")
    state.add_state("Controls", "Controls")

    # set the state to the default main menu
    state.set_state("main menu")


def menu_audio(is_playing, play):

    if play and not is_playing:
        pygame.mixer.music.play(-1)
        return True

    elif not play and is_playing:
        pygame.mixer.music.stop()
        return False

    return is_playing


def draw_dungeon():

    # Todo this can be optimized so it only draws the rooms we can see.
    for i in range(len(dunGen.DungeonGenerator.levels) - 1, -1, -1):
        screen.blit(dunGen.DungeonGenerator.levels[i],
                    (dunGen.DungeonGenerator.x +
                     dunGen.DungeonGenerator.starting_point_x[i] -
                     dunGen.DungeonGenerator.offsetX, dunGen.DungeonGenerator.y +
                     dunGen.DungeonGenerator.starting_point_y[i] -
                     dunGen.DungeonGenerator.offsetY))


def main():
    """Main game loop."""
    player_object.get_world_position_funct = dunGen.DungeonGenerator.get_position_with_offset
    dunGen.DungeonGenerator.create_dungeon(dunGen.DungeonGenerator)

    # players current direction
    current_direction = library.BACKWARDS

    # setup the states for both game and menus
    set_game_states(game_state)
    set_menu_states(menu_state)

    dunGen.DungeonGenerator.player = player_object

    melGen.MusicGenerator.generate_track(melGen.MusicGenerator)
    pygame.mixer.music.load(str(melGen.MusicGenerator.filename
                                + str(melGen.MusicGenerator.current_track)
                                + melGen.MusicGenerator.filetype))

    menu_audio_is_playing = False

    # main game loop
    while True:

        time.update_time(pygame.time.get_ticks()/1000.0)

        # amount of time that passed since the last frame in seconds
        delta_time = time.delta_time
        movement_speed = 75 * delta_time

        # Get inputs
        event_inputs()

        # fill the background
        screen.fill(library.BLACK)

        # NEW MAIN CODE
        if game_state.get_state() == "loading": # treat this as RESET.

            menu_audio_is_playing = menu_audio(menu_audio_is_playing, True)
        elif game_state.get_state() == "game":

            sound_effects.play_footprint()

            # Dungeon
            colDetect.CollisionDetector.detect_collision(colDetect.CollisionDetector)

            dunGen.DungeonGenerator. update_dungeon(dunGen.DungeonGenerator, "forwards", "backwards", movement_speed, -10, "right", "left")
            dunGen.DungeonGenerator. update_dungeon(dunGen.DungeonGenerator, "backwards", "forwards", -movement_speed, 10, "right", "left")
            dunGen.DungeonGenerator. update_dungeon(dunGen.DungeonGenerator, "left", "right", movement_speed, -20, "forwards", "backwards")
            dunGen.DungeonGenerator. update_dungeon(dunGen.DungeonGenerator, "right", "left", -movement_speed, 15, "forwards", "backwards")

            draw_dungeon()
            dunGen.DungeonGenerator.draw_chest(dunGen.DungeonGenerator)

            # Ghost Animation
            aiAnimationPaths.update_animations(delta_time, screen)

            # Player
            player_object.block_move_direction(dunGen.DungeonGenerator.top_col, dunGen.DungeonGenerator.right_col, dunGen.DungeonGenerator.bottom_col, dunGen.DungeonGenerator.left_col)
            player_object.update(library.KEY_PRESSED)
            player_object.draw(dunGen.TILE_SIZE, screen)

            player_x_pos, player_y_pos = dunGen.DungeonGenerator.\
                get_position_with_offset(player_object.position[0],
                                         player_object.position[1])

            if not library.debug_mode and aiAnimationPaths.ghost_in_position(player_x_pos, player_y_pos, screen):
                game_state.set_state("game over")

            # Light
            playerLight.update_light(fuel_meter.get_fuel_percentage())
            playerLight.initialise_lightning(dunGen.TILE_SIZE)
            playerLight.draw_light(screen, dunGen)
            playerLight.overlay(screen)

            # Fuel Meta (UI)
            if not library.debug_mode:
                fuel_meter.update_fuel_timer(delta_time)

            fuel_meter.display_fuel_meter(screen, (630, 50))

            if fuel_meter.torch_time == 0:
                game_state.set_state("game over")

            if dunGen.DungeonGenerator.reset_fuel:
                fuel_meter.reset_fuel()
                dunGen.DungeonGenerator.reset_fuel = False
            elif dunGen.DungeonGenerator.add_fuel:
                fuel_meter.add_fuel()
                dunGen.DungeonGenerator.add_fuel = False

            menu_audio_is_playing = menu_audio(menu_audio_is_playing, False)

        elif game_state.get_state() == "game over":
            # todo. nuffing is working on the game over screen!!
            game_over()

            menu_audio_is_playing = menu_audio(menu_audio_is_playing, True)
        elif game_state.get_state() == "main menu":
            # New ui code!
            menus.draw_buttons(screen, pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"])
            menus.is_button_pressed(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"])

            menu_audio_is_playing = menu_audio(menu_audio_is_playing, True)
            if menu_state.get_state() == "Controls":
                ui_controls()
        elif game_state.get_state() == "paused":
            menu_audio_is_playing = menu_audio(menu_audio_is_playing, True)
            pause_menu()
        elif game_state.get_state() == "editor":
            Editor.display()

        if library.debug_mode:
            # display some stats to screen
            debug_header_surface = debug_header_font_face.render("DEBUG MODE", True, library.WHITE)
            debug_room_count_surface = debug_font_face.render("Level Room count: "+ str(dunGen.DungeonGenerator.levelCount), True, library.WHITE)

            for room in range(len(dunGen.DungeonGenerator.starting_point_x)):
                room_numb = room + 1
                room_numb_surface = debug_font_face.render(str(room_numb), True, library.WHITE)
                display_position = dunGen.DungeonGenerator.get_position_with_offset(dunGen.DungeonGenerator.starting_point_x[room] + (dunGen.TILE_SIZE // 2), dunGen.DungeonGenerator.starting_point_y[room]+ (dunGen.TILE_SIZE // 2))
                screen.blit(room_numb_surface, display_position)

            screen.blit(debug_header_surface, (0, 0))
            screen.blit(debug_room_count_surface, (0, 33))

        # update the display.
        fps_clock.tick(FPS)
        pygame.display.flip()


if __name__ == "__main__":

    # set games state in the tile editor so we can return.
    Editor.EditorStore.game_state = game_state

    # set shared functions with the menu system
    menu.set_functions_by_name("exit", exit_game)
    menu.set_functions_by_name("menu_state", menu_state)
    menu.set_functions_by_name("game state", game_state)

    menus = menu.initialize_menu()
    colorBlindFilter.initialization()

    main()
