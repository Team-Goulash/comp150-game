import pygame, random
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

    def vines(self, texture, id):
        draw = False

        x_px_count = 0
        y_px_count = 0

        for x in range(texture.get_width()):
            for y in range(texture.get_height()):
                values = [0, 1]

                if x_px_count == 0:
                    if draw:
                        x_px_count = random.randrange(3, 7)
                    else:
                        x_px_count = random.randrange(20, 30)

                if y_px_count == 0:
                    if draw:
                        y_px_count = random.randrange(5, 25)
                    else:
                        y_px_count = random.randrange(20, 30)

                mud_weights = [0.1, 0.9]
                draw_mud = bool(random.choices(values, mud_weights)[0])

                moss_weights = [0.1, 0.9]
                draw_moss = bool(random.choices(values, moss_weights)[0])

                if draw:
                    if (id == 1 or id == 2) and draw_mud:
                        texture.set_at((x, y), MUD)
                    if id == 2 and draw_moss:
                        texture.set_at((x, y), MOSS)

                y_px_count -= 1
                x_px_count -= 1

                if x_px_count == 0 and y_px_count == 0:
                    draw = not draw

    def generate_material(self, image_id, material_id):
        """
        Generates a procedurally modified texture
        :arg material_id:      specifies the type of material the function will generate
        :arg image_id:    input image the function will modify
        :return: Tile texture with randomly generated features
        """
        base_image = self.tileTypes[image_id]
        pygame.image.save(base_image, "Well Escape tiles/generated texture.png")
        texture = pygame.image.load("Well Escape tiles/generated texture.png")

        if image_id == 1 and material_id > 0:
            self.vines(texture, material_id)

        return texture