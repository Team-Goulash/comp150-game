import UI


class UiMenu:

    current_menu = None
    menus = {}

    def add_menu(self, menu_title):
        new_menu_item = {menu_title: []}
        self.menus += new_menu_item
        pass

    def add_button(self, menu_title, button_name, position_rect, action_funct):
        self.menus[menu_title].append([button_name, position_rect, action_funct])
        pass

    def set_current_menu(self, menu_name):
        self.current_menu = menu_name

    def get_button(self):
        # reset the button
        # add text to button
        pass

    def get_header(self):
        # get and return the menu header
        pass

    def draw_buttons(self, surface, mouse_pos, key_pressed):

        for button in self.menus[self.current_menu]:
            screen.blit(main_menu_buttons["new game"].draw_button(pygame.mouse.get_pos(), library.KEY_PRESSED["mouse"],
                                                                  (460, 168)),(460, 168))
            pass


    def is_button_pressed(self):
        pass

