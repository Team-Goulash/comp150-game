import pygame, random, os
from pygame.locals import *
from random import choices

# assign variables or names to used keys
PAUSE = K_ESCAPE
MOVE = {"left": K_a, "right": K_d, "forwards": K_w, "backwards": K_s}

# directions
LEFT = 0
RIGHT = 1
FORWARDS = 2
BACKWARDS = 3

# boolean values for key pressed states
KEY_PRESSED = {"left": False, "right": False, "forwards": False, "backwards": False}

# set Colors
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MUD = (139, 69, 19)
MOSS = (61, 142, 31)

scaleNum = 90

playerImg = pygame.transform.scale(pygame.image.load("Characters/Player.png"),
                                   (int(scaleNum * 0.75), int(scaleNum * 0.75)))


class Tiles:
    # set images
    doorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/DoorTile.png"), (scaleNum, scaleNum))
    floorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/FloorTile.png"), (scaleNum, scaleNum))
    wallImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/WallTile.png"), (scaleNum, scaleNum))

    # set materials
    FLOOR = 0
    WALL = 1
    DOOR = 2

    # set colors to materials
    tileTypes = {FLOOR: floorImg, WALL: wallImg, DOOR: doorImg}

    @staticmethod
    def mud(texture):
        """
        Generates a mud texture
        :param texture: base image
        :return: base image with the mud texture drawn on it
        """

        # initialize variables
        draw = False
        timer = 0
        offset = 6

        # for each pixel position with offset of 6(scrolling horizontally)
        for y in range(texture.get_height() - offset):
            for x in range(texture.get_width() - offset):
                # values that will be chosen randomly
                values = [0, 1]

                # if timer has finished
                if timer == 0:
                    if draw:    # if it's time to draw
                        timer = random.randrange(10, 15)     # set timer
                    else:       # if it's time for a break
                        timer = random.randrange(20, 60)   # set timer

                mud_weights = [0.5, 0.5]
                draw_mud = bool(random.choices(values, mud_weights)[0])

                if draw and draw_mud:
                    # draw a mud pixel and center the offset
                    texture.set_at((x + int(offset * 0.5), y + int(offset * 0.5)), MUD)

                timer -= 1      # decrement the timer

                # if timer has finished
                if timer == 0:
                    draw = not draw     # reverse the draw boolean

    @staticmethod
    def moss(texture):
        """
        Generates a moss texture
        :param texture: base image
        :return: base image with the moss texture drawn on it
        """

        draw = False
        timer = 0
        sub_timer = 0

        for y in range(texture.get_height() - 6):
            for x in range(texture.get_width() - 6):
                values = [0, 1]

                if timer == 0:
                    if draw:
                        timer = random.randrange(5, 10)
                    else:
                        timer = random.randrange(10, 35)

                if sub_timer == 0:
                    if draw:
                        sub_timer = random.randrange(3, 7)
                    else:
                        sub_timer = random.randrange(15, 20)

                moss_weights = [0.2, 0.4]
                draw_moss = bool(random.choices(values, moss_weights)[0])

                if draw:
                    if draw_moss:
                        texture.set_at((x + 3, y + 3), MOSS)

                timer -= 1
                sub_timer -= 1

                if timer == 0 and sub_timer == 0:
                    draw = not draw

    random_inst = 0
    type_1_inst = []
    type_2_inst = []

    def generate_material(self, image_id, material_id, inst):
        """
        Generates a procedurally modified texture
        :arg inst       instance number
        :arg material_id:   specifies the type of material the function will generate
        :arg image_id:      input image the function will modify
        :return: Tile texture with randomly generated features
        """

        # load up the base image
        base_image = self.tileTypes[image_id]
        # copy the base image
        pygame.image.save(base_image, "Well Escape tiles/copy.png")
        # load up the copy of the base image
        texture = pygame.image.load("Well Escape tiles/copy.png")

        if image_id == 1 and material_id > 0:
            self.mud(texture)  # generate a mud texture and draw it on the image
            if material_id == 2:
                self.moss(texture)     # generate a moss texture and draw it on the image
                self.type_2_inst.append(inst)
            else:
                self.type_1_inst.append(inst)

            name = "Procedural-" + str(image_id) + "_type-" + str(material_id) + "_inst-" + str(inst)
            pygame.image.save(texture, "Well Escape tiles/varieties/" + name + ".png")

        return texture

    def assign_material(self, image_id, material_id):
        """
        assigns a random texture

        :arg material_id:   specifies the type of material the function will assign
        :arg image_id:      input image the function will modify
        :return: Tile texture with randomly generated features
        """
        base_image = self.tileTypes[image_id]
        if image_id == 1 and material_id > 0:
            if material_id == 2:
                self.random_inst = self.type_2_inst[0]
            else:
                self.random_inst = self.type_1_inst[0]

            texture = pygame.image.load("Well Escape tiles/varieties/" +
                                        "Procedural-" + str(image_id) + "_type-" + str(material_id) +
                                        "_inst-" + str(self.random_inst) + ".png")
        else:
            texture = base_image

        return texture