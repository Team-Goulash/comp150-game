import pygame


class UIButtons:
        button_hover = None
        button_normal = None
        button_pressed = None

        button_size = (0, 0)

        def __init__(self, button_hover_src, button_normal_src, button_pressed_src, size):
            """
            # Driver: Callum; Navigator: Ashley
            # Edited: Ashley
            button sources can be none. this can be useful if you want to set the value to an image that is already
            a surface. Beware if it is none it will cause an error if you try to blit it to screen!
            :param button_hover_src:    File path for hover button (can be none)
            :param button_normal_src:   File path for normal button (can be none)
            :param button_pressed_src:  File path for pressed button (can be none)
            :param size:                The size of the button (width, height)
            """
            self.button_size = size
            if button_hover_src is not None:
                self.button_hover = pygame.transform.scale(pygame.image.load(button_hover_src), self.button_size)
            if button_normal_src is not None:
                self.button_normal = pygame.transform.scale(pygame.image.load(button_normal_src),  self.button_size)
            if button_pressed_src is not None:
                self.button_pressed = pygame.transform.scale(pygame.image.load(button_pressed_src), self.button_size)

        def is_hover(self, cursor_pos, screen_pos):
            top_left = cursor_pos[0] > screen_pos[0] and cursor_pos[1] > screen_pos[1]
            bottom_right = cursor_pos[0] < (screen_pos[0] + self.button_size[0]) and \
                cursor_pos[1] < (screen_pos[1] + self.button_size[1])
            return top_left and bottom_right

        def is_pressed(self, cursor_pos, screen_pos, button_click):
            return self.is_hover(cursor_pos, screen_pos) and button_click

        def draw_button(self, cursor_pos, button_click, screen_pos):

            if self.is_pressed(cursor_pos, screen_pos, button_click):
                return self.button_pressed
            elif self.is_hover(cursor_pos, screen_pos):
                return self.button_hover
            else:
                return self.button_normal


class UISilder(UIButtons):
    slider_bar = None
    silder_width = 100
    slider_pos = (0, 0)
    value = 0; # value = 0 - 1

    def __init__(self,button_hover_src, button_normal_src, button_pressed_src, slider_bar_src, button_size, slider_pos, s_width):
        UIButtons.__init__(self, button_hover_src, button_normal_src, button_pressed_src, button_size)
        self.slider_bar = pygame.image.load(slider_bar_src)
        self.slider_width = s_width
        self.slider_pos = slider_pos

    def draw_slider(self, cursor_pos, button_click, handle_pos, surface):
        """
        draws the slider
        :param cursor_pos: cursor position
        :param button_click: when mouse is clicked
        :param handle_pos: treat as is it is button position
        """
        slider = None

        if handle_pos[0] <= self.slider_pos[0]:
            slider = UIButtons.draw_button(self, cursor_pos, button_click, self.slider_pos)
        elif handle_pos[0] >= self.slider_pos[0] + self.slider_width:
            slider = UIButtons.draw_button(self, cursor_pos, button_click, ((self.slider_pos[0] + self.slider_width), self.slider_pos[1]))
        else:
            slider = UIButtons.draw_button(self, cursor_pos, button_click, handle_pos)


        surface.blit(self.slider_bar, self.slider_pos)
        surface.blit(slider, handle_pos)
