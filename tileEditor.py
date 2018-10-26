"""
# Driver Ashley Sands; Navigator: None
"""
# Search '__Add_new__' for places to add new menus, edit windows, buttons & button function
# Todo...

import pygame, sys, library, UI, pathlib, os, image_effects, main, tileGenerator
from pygame.locals import *

class EditorStore:
    # has the editor been initialized
    initialized = False
    # should the image directory be update
    update_image_directory = False
    # the current directory
    current_directory = "./Well Escape tiles"
    # store the tiles path in the current directory
    directory_tiles = []
    # the current menu to display.
    current_menu = None
    current_menu_buttons = None

    # the surface of the tile we are editing
    edit_tile = None
    # selected fx id
    selected_fx_id = -1
    current_fx_options = 0
    # prevents the FX geting applied more than one on a single click
    next_options_pressed = False

    # The amount the tile is zoomed in/out
    tile_zoom = 1
    save_file_name_input = ""


TILE_SIZE = tileGenerator.Tiles.floorImg.get_rect().width
WINDOW_HEIGHT, WINDOW_WIDTH = 750, 1334
WINDOW_MARGIN_X, WINDOW_MARGIN_Y = 50, 50
screen = main.screen
standalone_mode = False

# if screen is set to none initialize py game (standalone mode)
if screen is None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # force to standalone
    standalone_mode = True

# Menus
MENU_START = 0
MENU_SELECT = 1
MENU_EDIT = 2
MENU_SAVE = 3

# FX panels
FX_GRAYSCALE = 0
FX_CHANGECOLOR = 1
FX_POSTER = 2
FX_POSTER_DIST = 3
FX_TINT = 4
FX_BLUR = 5
FX_SETALPHA_DIST = 6


# todo: remove and replace tile_text once cal has push his code.
header_fontface = pygame.font.Font("UI/AMS hand writing.ttf", 55)
sub_header_fontface = pygame.font.Font("UI/AMS hand writing.ttf", 35)
text_fontface = pygame.font.Font("UI/AMS hand writing.ttf", 18)
# headers and sub-headers
header_text_surface = header_fontface.render("Tile Editor", True, library.BLACK)
# The text will get replaced with a text surface containing the text.
sub_headers = {MENU_START: "Main Menu", MENU_SELECT: "Tile Select", MENU_EDIT: "Re-skin tool", MENU_SAVE: "Save To File"}

button = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "Ui/button_000_pressed.png", (360, 75))
button_small = UI.UIButtons("UI/Button_000_hover.png", "UI/Button_000_normal.png", "Ui/button_000_pressed.png", (50, 50))
button_fx = UI.UIButtons(None, None, None, (175, 75))
image_select_button = UI.UIButtons(None, None, None, (750, 113))
button_type = {"default": button, "small": button_small, "fx": button_fx}

# list of tuples (label->str, position->tuple, x_position->int, action->str, button_type -> str)
# tuples with action == run_effect also has effect_ID -> int on the end of the tuple
# tuples with action == tile_select also has directory -> str on the end of the tuple
start_menu_button_data = []
tile_select_menu_button_data = []
edit_tile_button_data = []

# theses are muti purpose sliders
sliders = [None, None, None, None]
sliders[0] = UI.UISlider(None, "UI/temp_slider_handle.png", None, "UI/temp_slider.png", (250, 50), 15, (950, 150))

sliders_r = UI.UISlider(None, "UI/temp_slider_handle.png", None, "UI/temp_slider.png", (250, 50), 15, (950, 150))
sliders_g = UI.UISlider(None, "UI/temp_slider_handle.png", None, "UI/temp_slider.png", (250, 50), 15, (950, 250))
sliders_b = UI.UISlider(None, "UI/temp_slider_handle.png", None, "UI/temp_slider.png", (250, 50), 15, (950, 350))

slider_values = [0]
save_text_input = UI.UIInput((400, 50), 30)


def initialize():
    """
    initialize the Editor.
    This should only be run once
    :return: None
    """
    # set current menu to start
    EditorStore.current_menu = MENU_START
    # set font surfaces
    sub_headers[MENU_START] = sub_header_fontface.render(sub_headers[MENU_START], True, library.BLACK)
    sub_headers[MENU_SELECT] = sub_header_fontface.render(sub_headers[MENU_SELECT], True, library.BLACK)
    sub_headers[MENU_EDIT] = sub_header_fontface.render(sub_headers[MENU_EDIT], True, library.BLACK)
    sub_headers[MENU_SAVE] = sub_header_fontface.render(sub_headers[MENU_SAVE], True, library.BLACK)

    # Set basic select tile button
    # Todo: turn into function
    # normal button
    image_select_button.button_normal = pygame.Surface((750, 113))
    image_select_button.button_normal.fill(library.BLACK)
    pygame.draw.rect(image_select_button.button_normal, library.WHITE, (113, 10, 625, 93))
    # hover button
    image_select_button.button_hover = pygame.Surface((750, 113))
    image_select_button.button_hover.fill(library.DARK_GREY)
    pygame.draw.rect(image_select_button.button_hover, library.WHITE, (113, 10, 625, 93))
    # pressed button
    image_select_button.button_pressed = pygame.Surface((750, 113))
    image_select_button.button_pressed.fill(library.LIGHT_GREY)
    pygame.draw.rect(image_select_button.button_pressed, library.WHITE, (113, 10, 625, 93))

    # add start menu button data
    start_menu_button_data.append(("Select Floor Tile", (60, 180), 90, "tile_select", "default", "./Well Escape tiles/FloorTiles"))
    start_menu_button_data.append(("Select Wall Tile", (60, 280), 90, "tile_select", "default", "./Well Escape tiles/WallTiles"))
    start_menu_button_data.append(("Select Player Tile", (60, 380), 90, "tile_select", "default", "./Characters"))
    start_menu_button_data.append(("Select ghost Tile", (60, 480), 90, "tile_select", "default", "./Well Escape tiles/ghostTiles"))
    start_menu_button_data.append(("Return To Menu", (60, 580), 70, "return", "default"))
    # add tile select menu button data
    tile_select_menu_button_data.append(("Return To Menu", (60, 580), 70, "return", "default"))
    # add edit tile button data
    edit_tile_button_data.append(("-", (390, 75), 20, "-_zoom", "small"))
    edit_tile_button_data.append(("+", (575, 75), 20, "+_zoom", "small"))
    # edit tile fx buttons
    edit_tile_button_data.append(("Apply Grey Scale...", (60, 180), 5, "run_effect", "fx", FX_GRAYSCALE))
    edit_tile_button_data.append(("Change Color...", (60, 280), 5, "run_effect", "fx", FX_CHANGECOLOR))
    edit_tile_button_data.append(("Posterization...", (60, 380), 5, "run_effect", "fx", FX_POSTER))
    edit_tile_button_data.append(("Posterization By Distance Tolerance...", (60, 480), 5, "run_effect", "fx", FX_POSTER_DIST))
    edit_tile_button_data.append(("Tint...", (250, 180), 5, "run_effect", "fx", FX_TINT))
    edit_tile_button_data.append(("Blur...", (250, 280), 5, "run_effect", "fx", FX_BLUR))
    edit_tile_button_data.append(("Set Alpha by Color Tolerance...", (250, 380), 5, "run_effect", "fx", FX_SETALPHA_DIST))
    edit_tile_button_data.append(("Some name", (250, 480), 5, "run_effect", "fx", -1))
    # edit tile save button
    edit_tile_button_data.append(("Save Image", (900, 600), 70, "save", "default"))
    # edit tile back button
    edit_tile_button_data.append(("Return To Menu", (60, 580), 70, "return", "default"))

    # set the current button set to start menu
    EditorStore.current_menu_buttons = start_menu_button_data


def get_files_in_directory(directory, file_type):
    """
    gets a list of files in a directory. does not include sub folders
    also un-sets EditorStore.update_image_directory
    :param directory:         the directory to search.
    :param file_type:   the extension so search for
    :return:            list of files in directory
    """
    file_list = []
    files = pathlib.Path(directory)
    for f in files.iterdir():

        if f.is_file() and os.path.splitext(f)[1] == file_type:
            file_list.append(str(f.absolute()))

    EditorStore.update_image_directory = False

    return file_list


def display_select_tile():
    """updates the images form directory and call the button display"""
    if EditorStore.update_image_directory:
        EditorStore.directory_tiles = get_files_in_directory(EditorStore.current_directory, ".png")

    # Todo move this into the if, when the optimize is done in display_select_tile_button
    display_select_tile_button()


def display_select_tile_button():
    """Draws the buttons to screen and selects the tile for edit if pressed"""
    # todo: optimize this so the buttons are called from the main button function so they dont get draw every frame

    # loop each image that can be edited
    for i in range(len(EditorStore.directory_tiles)):
        # Add File name text
        temp_surface = label_button(image_select_button.draw_button(pygame.mouse.get_pos(),
                                                                    library.KEY_PRESSED["mouse"],
                                                                    (450, 100 + (125 * i))),
                                    "File Name: Todo...", text_fontface, 117, 15)
        # Add path text
        temp_surface = label_button(temp_surface, EditorStore.directory_tiles[i], text_fontface, 117, 35)
        # display the image on the button
        temp_surface.blit(resize_preview_image(pygame.image.load(EditorStore.directory_tiles[i])), (10, 10))

        screen_position = (450, 100 + (125 * i))
        # display the button
        screen.blit(temp_surface, screen_position)

        # select the tile to be edited if has been pressed.
        if image_select_button.is_pressed(pygame.mouse.get_pos(), screen_position , library.KEY_PRESSED["mouse"]):
            select_tile(i)


def select_tile(image_path_id):

    EditorStore.edit_tile = pygame.image.load(EditorStore.directory_tiles[image_path_id])
    button_action("edit_tile")


def display_tile_editor():

    # get the tile size and work out the new size when zoomed
    zoomed_size_x, zoomed_size_y = EditorStore.edit_tile.get_size()
    zoomed_size_x = int(zoomed_size_x * EditorStore.tile_zoom)
    zoomed_size_y = int(zoomed_size_y * EditorStore.tile_zoom)
    # center the X axis
    x_center = ((WINDOW_WIDTH-100) // 2) - (zoomed_size_x // 2)
    y_center = ((WINDOW_HEIGHT-300) // 2) - (zoomed_size_y // 2)

    # display the zoom text at top of screen
    zoom_text = text_fontface.render("Zoom: "+str(EditorStore.tile_zoom*100)+"%", True, library.BLACK)

    # display text input
    save_text_input.draw_text_input(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (450, 615),
                                    EditorStore.save_file_name_input, screen)

    screen.blit(zoom_text, (450, 75))
    # display the image being edited
    screen.blit(pygame.transform.scale(EditorStore.edit_tile, (zoomed_size_x, zoomed_size_y)),
                (100+x_center, 200+y_center))

    display_fx_panel(EditorStore.selected_fx_id)


def display_fx_panel(panel_id):
    """
    Displays the FX pannel for the selected fx
    :param panel_id:    fx id
    :return:            None
    """

    total_options = 1

    if panel_id == FX_GRAYSCALE:
        rgb_sliders("Color Weights")
    if panel_id == FX_BLUR:
        fx_panel_header("Blend Tolerance")
        draw_slider(0, "Amount")

    # add apporate text to the apply button
    button_position = 1025, 500
    if total_options - (EditorStore.current_fx_options + 1) <= 0:
        fx_button = label_button(button_fx.draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                      button_position), "Apply FX", sub_header_fontface, 15, 15)
    else:
        fx_button = label_button(button_fx.draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                       button_position), "Next", sub_header_fontface, 15, 15)

    if panel_id > -1:
        # display the apply button if in a valid panel
        screen.blit(fx_button, button_position)
        if button_fx.is_pressed(pygame.mouse.get_pos(), button_position, library.KEY_PRESSED["mouse"]) and \
                not EditorStore.next_options_pressed:
            # run fx if apply button is pressed and reset the selected FX
            if total_options - (EditorStore.current_fx_options + 1) <= 0:
                run_effect(panel_id)
                EditorStore.selected_fx_id = -1
                EditorStore.current_fx_options = 0

            EditorStore.current_fx_options += 1
            EditorStore.next_options_pressed = True
            print(EditorStore.current_fx_options, total_options, (total_options - (EditorStore.current_fx_options + 1)))
        elif not button_fx.is_pressed(pygame.mouse.get_pos(), button_position, library.KEY_PRESSED["mouse"]) and \
                not library.KEY_PRESSED["mouse"]:
            EditorStore.next_options_pressed = False





def save_tile(surface, path, file_name):

    # todo check if file already exist
    if len(file_name) == 0:
        print("Error: Unable to save no file name")
        return
    path = path + "/" + file_name + ".png"
    pygame.image.save(surface, path)
    print("Image save to ", path)


def rgb_sliders(header):

    fx_panel_header(header)
    screen.blit(get_label("Red", text_fontface, (75, 30), library.BLACK, library.WHITE), (950, 125))
    sliders_r.draw_slider(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], screen)  # (950, 150)
    screen.blit(get_label(str(sliders_r.value), text_fontface, (75, 30), library.BLACK, library.WHITE),
                (1200, 160))

    screen.blit(get_label("Green", text_fontface, (75, 30), library.BLACK, library.WHITE), (950, 225))
    sliders_g.draw_slider(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], screen)
    screen.blit(get_label(str(sliders_g.value), text_fontface, (75, 30), library.BLACK, library.WHITE),
                (1200, 260))

    screen.blit(get_label("Blue", text_fontface, (75, 30), library.BLACK, library.WHITE), (950, 325))
    sliders_b.draw_slider(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], screen)
    screen.blit(get_label(str(sliders_b.value), text_fontface, (75, 30), library.BLACK, library.WHITE),
                (1200, 360))


def draw_slider(slider_id, label):

    screen.blit(get_label(label, text_fontface, (100, 30), library.BLACK, library.WHITE), (950, 125))
    sliders[slider_id].draw_slider(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], screen)  # (950, 150)
    screen.blit(get_label(str(sliders[slider_id].value), text_fontface, (75, 30), library.BLACK, library.WHITE),
                (1200, 160))


def fx_panel_header(header):
    screen.blit(get_label(header, sub_header_fontface, (250, 50), library.BLACK, library.WHITE), (950, 55))


def label_button(button_surface, text, fontface, x_position, y_position):
    """Adds labels to buttons"""

    temp_surface = pygame.Surface(button_surface.get_size(), pygame.SRCALPHA)
    temp_surface.blit(button_surface, (0, 0))
    temp_surface.blit(fontface.render(text, True, library.BLACK), (x_position, y_position))
    return temp_surface


def get_label(text, fontface, size, text_color=(0, 0, 0, 255), background_color = (255, 255, 255, 0)):
    """
    creates a text label
    :param text:                Label text
    :param fontface:            Fontface
    :param text_color:          font color (r, g, b, a)
    :param background_color:    background color (r, g, b, a)
    :param size:                label size (x, y)
    :return:                    label surface
    """

    label_surface = pygame.Surface(size, pygame.SRCALPHA)
    label_surface.fill(background_color)
    label_surface.blit(fontface.render(text, True, text_color), (5, 5))

    return label_surface


def draw_menu_buttons():
    """Draws buttons for the current menu"""
    # loop button for the current menu
    for bt in list(button_type):
        for b in EditorStore.current_menu_buttons:
            # skip if this is not the correct button time
            if bt != b[4]:
                continue
            # draw buttons
            screen.blit(
                label_button(button_type[bt].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], b[1]),
                             b[0], get_button_type_fontface(bt), b[2], 15), b[1])


def get_button_type_fontface(button_type):
    """
    get the fontface for a button type.
    :param button_type:     type of button
    :return:                fontface for button type
    """

    if button_type == "fx":
        return text_fontface
    else:
        return sub_header_fontface


def button_pressed():
    """Finds if any button are pressed in the current menu"""
    # tile select buttons are in display_select_tile_button()

    # loop events to look for mouse up on button 1
    for event in pygame.event.get():
        # event: exit game! (via window X or alt-F4)
        if event.type == QUIT:
            quit()
        elif event.type == KEYUP:
            EditorStore.save_file_name_input = text_input(event, EditorStore.save_file_name_input, save_text_input)
            print(EditorStore.save_file_name_input)
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            library.KEY_PRESSED["mouse"] = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            # loop buttons to find if any are pressed
            for bt in list(button_type):
                for b in EditorStore.current_menu_buttons:
                    # skip if this is not the correct button time
                    if bt != b[4]:
                        continue
                    if button_type[bt].is_pressed(pygame.mouse.get_pos(), b[1], library.KEY_PRESSED["mouse"]):
                        # run the button action
                        button_action(b[3], b)

            # un-set the mouse press
            library.KEY_PRESSED["mouse"] = False


def button_action(action_type, button_data=None):
    """Runs the pressed buttons action"""

    if action_type == "return":
        # return to main menu if we are on the editor start menu else return to start menu
        if EditorStore.current_menu == MENU_START:
            # just quit if in standalone mode
            if standalone_mode:
                quit()
            # un-set the editor
            library.EDITOR = False
            # Set buttons back to start menu so if we return to editor its good to go.
            EditorStore.current_menu_buttons = start_menu_button_data
        elif EditorStore.current_menu == MENU_EDIT:
            # when going back to the select image menu force the button direction to the current direction
            button_data = list(button_data)
            if len(button_data) < 6:
                button_data.append(EditorStore.current_directory)
            else:
                button_data[5] = EditorStore.current_directory
            # set to update the file list
            EditorStore.update_image_directory = True
            button_action("tile_select", button_data)
        else:
            set_menu(MENU_START, start_menu_button_data)
    elif action_type == "tile_select":
        # set tile select menu + buttons
        set_menu(MENU_SELECT, tile_select_menu_button_data)
        # Set floor tile diectory
        print(button_data[5])
        set_directory(button_data[5])
    elif action_type == "edit_tile":
        # set edit tile menu + buttons
        set_menu(MENU_EDIT, edit_tile_button_data)
    elif action_type == "+_zoom":
        if EditorStore.tile_zoom < 5:
            EditorStore.tile_zoom += 0.25
    elif action_type == "-_zoom":
        if EditorStore.tile_zoom > 0.5:
            EditorStore.tile_zoom -= 0.25
    elif action_type == "run_effect":
        EditorStore.selected_fx_id = button_data[5]
    elif action_type == "save":
        save_tile(EditorStore.edit_tile, EditorStore.current_directory, EditorStore.save_file_name_input)
        EditorStore.save_file_name_input = ""
    else:
        print("Error button action", action_type, "not found")


def set_menu(menu_id, buttons=None):
    """
    Sets the current menu
    :param menu_id:     menu id to set to
    :param buttons:     the menus buttons (if none button remain the same)
    :return:            None
    """

    EditorStore.current_menu = menu_id
    if buttons is not None:
        EditorStore.current_menu_buttons = buttons


def run_effect(effect_id):
    """Calls the effect in image_effects"""

    effect_inputs = None

    if effect_id == FX_GRAYSCALE:
        effect_inputs = (sliders_r.value, sliders_g.value, sliders_b.value)
        effect_id = "greyscale"
    elif effect_id == "change_color":
        pass
    elif effect_id == "poster":
        pass
    elif effect_id == "poster_dist":
        pass
    elif effect_id == "tint":
        pass
    elif effect_id == FX_BLUR:
        effect_inputs = sliders[0].value
        effect_id = "blur"
    elif effect_id == "set_alpha_dist":
        pass
    else:
        # display error message if effect is not found
        print("[tileEditor.run_effect] Error: effect not found ", effect_id)

    image_effects.run_effect(effect_id, EditorStore.edit_tile, effect_inputs, (loading_bar, screen,
                                                                               (0, 0, WINDOW_WIDTH, 50)))


def resize_preview_image(preview_image):
    """
    get the size of an image when srunk to TILE_SIZE, keeping the aspect ratio
    :param image_size:  image size (width, height)
    :return:            new image size
    """
    image_size = preview_image.get_size()
    multiplier = 1
    if image_size[0] >= image_size[1]:
        multiplier = TILE_SIZE / image_size[0]
    else:
        multiplier = TILE_SIZE / image_size[1]

    return pygame.transform.scale(preview_image, (int(image_size[0] * multiplier), int(image_size[1] * multiplier)))


def loading_bar(surface, rect, percent):
    """
    Displays a loading bar on surface and updates display
    :param surface: surface to display loading bar on
    :param rect:    the position and size of the loading bar (x, y, width, height)
    :param percent: the loading percentage
    :return:        None
    """
    text_surface = text_fontface.render("Loading", True, library.BLACK)  # str(precent * 100) + "%", True, BLACK)
    pygame.draw.rect(surface, library.GREY, rect)
    pygame.draw.rect(surface, library.WHITE, (rect[0] + 5, rect[1] + 5, (rect[2] - 10) * percent, rect[3] - 8))
    surface.blit(text_surface, (50, 10))
    pygame.display.flip()


def set_directory(directory):
    EditorStore.current_directory = directory
    EditorStore.update_image_directory = True


def text_input(event, current_text, ui_text_input):

    if not ui_text_input.has_focus(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"], (50, 100)):
        return current_text

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    if event.key == K_BACKSPACE:
        new_str = ""
        for s in range(0, len(current_text)-1):
            new_str += current_text[s]
        return new_str
    elif event.key == K_SPACE:
        return current_text + " "

    if event.key >= 48 < 48 + len(numbers):
        for n in range(len(numbers)):
            if event.key == 48 + n:
                return current_text + numbers[n]

    if event.key >= 97 < 97 + len(letters):
        for l in range(len(letters)):
            if event.key == 97 + l:
                return current_text + letters[l]

    return current_text


def display():
    """ Main Editor Loop
    Driver: Ashley Sands, Navigator: N/A
    """

    # initialize the editor
    if not EditorStore.initialized:
        initialize()
        # prevent from initializing again
        EditorStore.initialized = True

    screen.fill(library.BLACK)
    pygame.draw.rect(screen, library.LIGHT_GREY,
                     [WINDOW_MARGIN_X, WINDOW_MARGIN_Y,
                      WINDOW_WIDTH - (WINDOW_MARGIN_X * 2),
                      WINDOW_HEIGHT - (WINDOW_MARGIN_Y * 2)])

    pygame.draw.rect(screen, library.WHITE, [90, 65, 285, 100])
    screen.blit(header_text_surface, (100, 75))
    screen.blit(sub_headers[EditorStore.current_menu], (130, 120))

    if EditorStore.current_menu == MENU_SELECT:
        display_select_tile()
    elif EditorStore.current_menu == MENU_EDIT:
        display_tile_editor()

    draw_menu_buttons()
    button_pressed()

    pygame.display.flip()


def standalone():
    """Runs the editor as a standalone"""
    while True:
        display()


def quit():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    standalone()
