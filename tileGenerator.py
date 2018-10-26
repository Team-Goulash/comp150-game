"""Driver - Joachim / Navigator - None"""
import pygame
import random
import os
import library

scaleNum = library.scaleNum


class Tiles:
    """A Class which stores all the variables and tile generation functions."""

    # load tile images
    floorPath = "Well Escape tiles/FloorTiles/"
    floorPathImages = os.listdir(floorPath)
    floorImages = []
    for img in range(len(floorPathImages)):
        floorImg = pygame.transform.scale(
            pygame.image.load(floorPath + floorPathImages[img]),
            (scaleNum, scaleNum))

        floorImages.append(floorImg)

    wallPath = "Well Escape tiles/WallTiles/"
    wallPathImages = os.listdir(wallPath)
    wallImages = []

    for img in range(len(wallPathImages)):
        wallImg = pygame.transform.scale(
            pygame.image.load(wallPath + wallPathImages[img]),
            (scaleNum, scaleNum))

        wallImages.append(wallImg)

    doorImg = pygame.transform.scale(
        pygame.image.load("Well Escape tiles/DoorTile.png"),
        (scaleNum, scaleNum))

    exitDoorImg = pygame.transform.scale(
        pygame.image.load("Well Escape tiles/ExitDoorTile.png"),
        (scaleNum, scaleNum))

    interactive = [doorImg, exitDoorImg]

    # set materials
    FLOOR = 0
    WALL = 1
    DOOR = 2

    # set colors to materials
    tileTypes = {FLOOR: floorImages, WALL: wallImages, DOOR: interactive}

    @staticmethod
    def mud(texture):
        """
        Generate a mud texture and draws it on the image.

        :param texture: base image
        :return: base image with the mud texture drawn on it
        """
        draw = False
        timer = 0
        offset = 6

        # for each pixel position with offset of 6(scrolling horizontally)
        for y in range(texture.get_height() - offset):
            for x in range(texture.get_width() - offset):
                if timer == 0:
                    if draw:
                        timer = random.randrange(10, 15)
                    else:
                        timer = random.randrange(20, 60)

                values = [0, 1]
                mud_weights = [0.5, 0.5]
                draw_mud = bool(random.choices(values, mud_weights)[0])

                if draw and draw_mud:
                    # draw a mud pixel and center the offset
                    texture.set_at((x + int(offset * 0.5),
                                    y + int(offset * 0.5)), library.MUD)

                timer -= 1

                if timer == 0:
                    draw = not draw

    @staticmethod
    def moss(texture):
        """
        Generate a moss texture and draws it on the image.

        :param texture: base image
        :return: base image with the moss texture drawn on it
        """
        draw = False
        timer = 0
        sub_timer = 0

        # for each pixel position with offset of 6(scrolling horizontally)
        for y in range(texture.get_height() - 6):
            for x in range(texture.get_width() - 6):

                # if timer has finished
                if timer == 0:
                    if draw:
                        timer = random.randrange(5, 10)
                    else:
                        timer = random.randrange(10, 35)

                values = [0, 1]
                if sub_timer == 0:
                    if draw:
                        sub_timer = random.randrange(3, 7)
                    else:
                        sub_timer = random.randrange(15, 20)

                moss_weights = [0.2, 0.4]
                draw_moss = bool(random.choices(values, moss_weights)[0])

                if draw and draw_moss:
                        # draw a moss pixel and center the offset
                        texture.set_at((x + 3, y + 3), library.MOSS)

                timer -= 1
                sub_timer -= 1

                if timer == 0 and sub_timer == 0:
                    draw = not draw

    random_inst = 0
    type_1_inst = []
    type_2_inst = []

    def generate_material(self, image_id, type_id, material_id, inst):
        """
        Generate a procedurally modified texture.

        :arg inst       instance number
        :arg material_id:   specifies the type of material
         the function will generate
        :arg type_id        specifies the type of image
         that will be used as a base image
        :arg image_id:      input image the function will modify
        :return: Tile texture with randomly generated features
        """
        # load up the base image
        base_image = self.tileTypes[image_id][type_id]
        pygame.image.save(base_image, "Well Escape tiles/copy.png")
        texture = pygame.image.load("Well Escape tiles/copy.png")

        # if the image type is a floor
        # and material type is not in perfect condition
        if image_id == 1 and material_id > 0:
            self.mud(texture)
            # if the material type is really old
            if material_id == 2:
                self.moss(texture)
                # add the generated really old material instance number
                # to a list
                self.type_2_inst.append(inst)
            else:
                # add the generated dirty material instance number to a list
                self.type_1_inst.append(inst)

            # save the generated image to the varieties folder
            name = "Procedural-" + str(image_id) + "_type-" + str(type_id) + \
                   "_mat-" + str(material_id) + "_inst-" + str(inst)
            pygame.image.save(texture,
                              "Well Escape tiles/varieties/" + name + ".png")

        return texture
