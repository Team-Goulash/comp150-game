"""
Driver: ashley sands
"""

import pygame
import library
from animator import Animator
import random
import loadSave
import dungeonGenerator # import get_position_with_offset

class AiAnimation:

    # [room id][path id][path positiom]
    ghost_paths = []
    room_size = []
    ghost_sprite_animations = []  # list of tuples (animator, room_id, path_id, (current position))
    cell_move_timer_lenght = 0.9 # sec
    current_move_time = 0
    first_scene = True

    def reset_animator(self, first_scene):
        self.ghost_paths.clear()
        self.room_size.clear()
        self.ghost_sprite_animations.clear()
        self.current_move_time = 0
        # todo this needs to be set when we go to the next scene
        self.first_scene = first_scene

    def load_paths(self, room_image_src):

        if len(self.room_size) == 0:
            self.room_size.append((7, 9))  # size of start room.

        pixel_img = pygame.image.load(room_image_src)

        start_position = (0, 0)
        # each path
        path = []
        # all paths in room
        paths = []

        while start_position is not None:

            start_position = self.get_start_point(pixel_img, start_position[0], start_position[1])

            if start_position is not None:
                path.append(start_position)
                print("start pos", start_position, "(", room_image_src)
                next_move = start_position
                block_direction = None

                while next_move is not None:
                    next_move, block_direction = self.get_next_point(pixel_img, next_move[0], next_move[1], block_direction)
                    if next_move is not None:
                        path.append(next_move)
                        # print(next_move)
                # prevents single points being entered as paths
                if len(path) > 1:
                    paths.append(path)


            path = []

        self.ghost_paths.append(paths)
        self.room_size.append(pixel_img.get_size())


    def print_data(self):

     # [room id][path id][path positiom]
        for r in range(len(self.ghost_paths)):
            print("room id", r)
            for p in range(len(self.ghost_paths[r])):
                print("path", p)
                print(self.ghost_paths[r][p])


    def get_start_point(self, image, last_x, last_y):

        img_width, img_height = image.get_size()

        for x in range(img_width):
            for y in range(img_height):
                if x < last_x or x == last_x and y <= last_y:
                    continue
                if self.get_color_channel(image, x, y) == 70:
                    return x, y

        return None

    def get_next_point(self, image, last_x, last_y, block_direction):
        """
        Gets the next move
        :param last_x:              last move X position
        :param last_y:              last move Y position
        :param block_direction:     the direction that we came from
        :return:                    (x, y), blocking direction
        """
        # so we need to find next move.
        if block_direction != library.FORWARDS and self.get_color_channel(image, last_x, last_y + 1) == 140:
            return (last_x, last_y + 1), library.BACKWARDS
        elif block_direction != library.BACKWARDS and self.get_color_channel(image, last_x, last_y - 1) == 140:
            return (last_x, last_y - 1), library.FORWARDS
        elif block_direction != library.LEFT and self.get_color_channel(image, last_x + 1, last_y) == 140:
            return (last_x + 1, last_y), library.RIGHT
        elif block_direction != library.RIGHT and self.get_color_channel(image, last_x - 1, last_y) == 140:
            return (last_x - 1, last_y), library.LEFT

        return None, None

    def get_color_channel(self, image, x, y):
        """returns the first color channel (red) gets set to 0 is there is no alpha"""
        color = image.get_at((x, y))
        if color[3] < 75:
            return 0
        else:
            return color[0]

    def apply_position_offset_to_room_path(self, room_offsets_x, room_offsets_y):
        """
        Adds the room position offset to the ai paths
        :param room_offsets_x:      list of room x offsets
        :param room_offsets_y:      list of room y offsets
        :return:                       None
        """

        for room in range(len(room_offsets_x)):
            # take one off room id as we dont include the start room.
            # thee will never be any ai in there
            room_id = room

            if self.first_scene:
                room_id -= 1

            if room_id == -1:
                continue

            paths = self.ghost_paths[room_id]
            print(room_id, paths, self.ghost_paths[-1])

            offset = room_offsets_x[room], room_offsets_y[room]

            for path_id in range(len(paths)):
                for cell_id in range(len(self.ghost_paths[room_id][path_id])):
                    # work out the new position and apply it
                    #new_position_x, new_position_y = offset
                    #print("aaaaa", new_position_y, self.ghost_paths[room_id][path_id][cell_id][1], ((self.ghost_paths[room_id][path_id][cell_id][1]) * library.scaleNum), (((self.ghost_paths[room_id][path_id][cell_id][1]) * library.scaleNum) + new_position_y))
                    # todo find out why the cell id is out by (2, -1)
                    # new_position_x = (offset[0] + self.room_size[room+1][0]) + ((self.ghost_paths[room_id][path_id][cell_id][0] + 3) * library.scaleNum)
                    # new_position_y = (offset[1] + self.room_size[room+1][1]) + ((self.ghost_paths[room_id][path_id][cell_id][1] + 6) * library.scaleNum)
                    new_position_x = offset[0] + (self.ghost_paths[room_id][path_id][cell_id][0] * library.scaleNum)
                    new_position_y = offset[1] + (self.ghost_paths[room_id][path_id][cell_id][1] * library.scaleNum)
                    self.ghost_paths[room_id][path_id][cell_id] = (new_position_x, new_position_y)
                    # set up the ghost animation
                self.add_random_ghost_animation(room_id, path_id, self.ghost_paths[room_id][path_id][0])
                #print(offset)


    def add_random_ghost_animation(self, room_id, path_id, start_position):


        ghost_path = "Well Escape tiles/ghostTiles/"
        ghost_sprite_sheet = random.choice(loadSave.load_files_form_directory(ghost_path, ".png"))
        # Animation_data -> [animator, room_id, path_id, start_cell_id, end_cell_id, forwards, (current position)]
        animation_data = [
            # Todo turn magic numbers in animations into constants
            Animator(ghost_sprite_sheet, library.scaleNum, 3, 7, 0.85),
            room_id,
            path_id,
            0,
            1,
            True,
            start_position
        ]

        self.ghost_sprite_animations.append(animation_data)

    def update_animations(self, delta_time, surface):
        """update the animation and draw the ghost to surface"""

        self.current_move_time += delta_time
        next_id = False

        if self.current_move_time > self.cell_move_timer_lenght:
            self.current_move_time -= self.cell_move_timer_lenght
            next_id = True

        # Todo skip any that are not in view
        for animation in self.ghost_sprite_animations:

            start_position = animation[3]
            end_position = animation[4]
            forwards = animation[5]

            if next_id:
                if forwards and end_position == (len(self.ghost_paths[animation[1]][animation[2]])-1):
                    forwards = False
                    start_position, end_position = self.flip_values(start_position, end_position)
                elif not forwards and end_position == 0:
                    forwards = True
                    start_position, end_position = self.flip_values(start_position, end_position)
                else:
                    if forwards:
                        start_position += 1
                        end_position += 1
                    else:
                        start_position -= 1
                        end_position -= 1

                animation[3] = start_position
                animation[4] = end_position
                animation[5] = forwards

            animation[0].update_time(delta_time)

            animation_percentage = self.current_move_time / self.cell_move_timer_lenght

            current_position = library.lerp_vector2(
                self.ghost_paths[animation[1]][animation[2]][start_position],
                self.ghost_paths[animation[1]][animation[2]][end_position],
                animation_percentage
            )

            surface.blit(animation[0].get_current_sprite(), dungeonGenerator.get_position_with_offset(current_position[0], current_position[1]))

            animation[6] = current_position

    def flip_values(self, value_a, value_b):
        return value_b, value_a

    def ghost_in_position(self, pos_x, pos_y, surface):

        i = 0

        obj_top_left = pos_x, pos_y
        obj_bottom_right = obj_top_left[0] + (library.scaleNum - 20), obj_top_left[1] + (library.scaleNum - 10)


        # todo remove temp shiz!!
        temp_rect = (obj_top_left[0], obj_top_left[1], library.scaleNum-20, library.scaleNum-10)
        pygame.draw.rect(surface, library.RED, temp_rect, 3)

        pos_x += library.scaleNum//2
        pos_y += library.scaleNum//2

        for animation in self.ghost_sprite_animations:

            # get the bounds of the ghost
            ghost_top_left = dungeonGenerator.get_position_with_offset(animation[6][0], animation[6][1])
            ghost_bottom_right = (ghost_top_left[0] + library.scaleNum), (ghost_top_left[1] + library.scaleNum)

            # todo remove temp shiz!!
            temp_rect = (ghost_top_left[0], ghost_top_left[1], library.scaleNum, library.scaleNum)
            pygame.draw.rect(surface, library.RED, temp_rect, 3)

            in_x, in_y = False, False

            i += 1
            '''
            if obj_top_left[0] < ghost_bottom_right[0] and obj_top_left[0] > ghost_top_left[0] and obj_bottom_right[0] > ghost_top_left[0] and obj_bottom_right[1] < ghost_bottom_right[0]:
                print("In Y")
                in_y = True

            if obj_top_left[1] < ghost_bottom_right[1] and obj_top_left[1] > ghost_top_left[1] or obj_bottom_right[1] > ghost_top_left[1] and obj_bottom_right[1] < ghost_bottom_right[1]:
                print("In X")
                in_x = True
            '''

            if pos_x > ghost_top_left[0] and pos_x < ghost_bottom_right[0] and pos_y > ghost_top_left[1] and pos_y < ghost_bottom_right[1]:
                    in_x, in_y = True, True

            if in_x and in_y:
                print("Contact")
                return True

        return False

