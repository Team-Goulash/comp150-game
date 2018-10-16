import pygame


class UIButtons:
        button_hover = None
        button_normal = None
        button_pressed = None

        screen_pos = (0, 0, 0, 0)
        button_size = (0, 0)

        def __init__(self, button_hover_src, button_normal_src, button_pressed_src, size):
            self.button_size = size
            self.button_hover = pygame.transform.scale(pygame.image.load(button_hover_src), self.button_size)
            self.button_normal = pygame.transform.scale(pygame.image.load(button_normal_src),  self.button_size)
            self.button_pressed = pygame.transform.scale(pygame.image.load(button_pressed_src), self.button_size)

        def is_hover(self, cursor_pos):
            top_left = cursor_pos[0] > self.screen_pos[0] and cursor_pos[1] > self.screen_pos[1]
            bottom_right = cursor_pos[0] < (self.screen_pos[0] + self.button_size[0]) and \
                cursor_pos[1] < (self.screen_pos[1] + self.button_size[1])
            return top_left and bottom_right

        def is_pressed(self, cursor_pos, button_click):
            return self.is_hover and button_click

        def draw_button(self, cursor_pos, button_click):

            if self.is_pressed(cursor_pos, button_click):
                return self.button_pressed
            elif self.is_hover(cursor_pos):
                return self.button_hover
            else:
                return self.button_normal
