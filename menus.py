import UI, pygame

class UiMenu:

    active = False
    current_menu = None
    # Todo add default fontfaces
    header_fontface = pygame.font.SysFont("", 100)
    button_fontface = pygame.font.SysFont("", 50)
    menus = {}
    buttons = {}

    def set_font_face(self, header_fontface, button_fontface):
        """ set the fontface, inputs are ignored if None """

        if header_fontface is not None:
            self.header_fontface = header_fontface

        if button_fontface is not None:
            self.button_fontface = button_fontface

    def add_button_type(self, type_name,  normal, hover, pressed, size):
        """Add a new button type.

        :param type_name:       the button type/group name
        :param normal:          src to normal button image  (can be none)
        :param hover:           src to hover button image   (can be none)
        :param pressed:         src to pressed button image (can be none)
        :param size:            button size (width, height)
        :return:                None
        """
        self.buttons[type_name] = UI.UIButtons(hover, normal, pressed, size)

    def add_menu(self, menu_title):
        """ Add a new menu to list of menus """
        self.menus[menu_title] = []

    def add_button(self, menu_title, button_name, position_rect, action_funct):
        """
        Add a button to a menu group
        :param menu_title:      name of the group to add a button to
        :param button_name:     name of the button to add to the group
        :param position_rect:   position and size rect -> (x, y, width, height)
        :param action_funct:    the function with the button action
        :return:                None
        """
        self.menus[menu_title].append([button_name, position_rect, action_funct])

    def set_current_menu(self, menu_name):
        """set the menu to be displayed"""
        self.current_menu = menu_name

    def get_button(self, button, label, fontface):
        """get the button to be displayed with a label prefixed """
        # reset the button
        # add text to button

        temp_surface = button.copy()
        # Todo add text

        return temp_surface

    def get_header(self, label, fontface):
        """gets the menu header"""
        # Todo add text
        pass

    def draw_buttons(self, surface, mouse_pos, key_pressed):
        """Draws all the buttons and menu header to the surface"""
        for button in self.menus[self.current_menu]:
            #todo display buttons
            pass

    def is_button_pressed(self, mouse_position, mouse_is_pressed):
        """find if any of the buttons on the current menu are being pressed"""
        # todo find if the button is pressed!
        pass

