import pygame, random, os, library
from pygame.locals import *
from random import choices


scaleNum = library.scaleNum


class Tiles:
    # load tile images
    floorPath = "Well Escape tiles/FloorTiles/"
    floorPathImages = os.listdir(floorPath)
    floorImages = []
    for img in range(len(floorPathImages)):
        floorImg = pygame.transform.scale(pygame.image.load(floorPath + floorPathImages[img]), (scaleNum, scaleNum))
        floorImages.append(floorImg)

    wallPath = "Well Escape tiles/WallTiles/"
    wallPathImages = os.listdir(wallPath)
    wallImages = []
    for img in range(len(wallPathImages)):
        wallImg = pygame.transform.scale(pygame.image.load(wallPath + wallPathImages[img]), (scaleNum, scaleNum))
        wallImages.append(wallImg)

    doorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/DoorTile.png"), (scaleNum, scaleNum))
    exitDoorImg = pygame.transform.scale(pygame.image.load("Well Escape tiles/ExitDoorTile.png"), (scaleNum, scaleNum))
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
        Generates a mud texture and draws it on the image.

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
                    texture.set_at((x + int(offset * 0.5), y + int(offset * 0.5)), library.MUD)

                timer -= 1      # decrement the timer

                # if timer has finished
                if timer == 0:
                    draw = not draw     # reverse the draw boolean

    @staticmethod
    def moss(texture):
        """
        Generates a moss texture and draws it on the image.

        :param texture: base image
        :return: base image with the moss texture drawn on it
        """

        # initialize variables
        draw = False
        timer = 0
        sub_timer = 0

        # for each pixel position with offset of 6(scrolling horizontally)
        for y in range(texture.get_height() - 6):
            for x in range(texture.get_width() - 6):
                # values that will be chosen randomly
                values = [0, 1]

                # if timer has finished
                if timer == 0:
                    if draw:    # if it's time to draw
                        timer = random.randrange(5, 10)     # set timer
                    else:       # if it's time for a break
                        timer = random.randrange(10, 35)    # set timer

                # if secondary timer has finished
                if sub_timer == 0:
                    if draw:    # if it's time to draw
                        sub_timer = random.randrange(3, 7)      # set secondary timer
                    else:       # if it's time for a break
                        sub_timer = random.randrange(15, 20)    # set secondary timer

                moss_weights = [0.2, 0.4]
                draw_moss = bool(random.choices(values, moss_weights)[0])

                if draw and draw_moss:
                        # draw a moss pixel and center the offset
                        texture.set_at((x + 3, y + 3), library.MOSS)

                timer -= 1      # decrement the timer
                sub_timer -= 1  # decrement the secondary timer

                # if both timers have finished
                if timer == 0 and sub_timer == 0:
                    draw = not draw     # reverse the draw boolean

    # set instance variables
    random_inst = 0
    type_1_inst = []
    type_2_inst = []

    def generate_material(self, image_id, type_id, material_id, inst):
        """
        Generates a procedurally modified texture.

        :arg inst       instance number
        :arg material_id:   specifies the type of material the function will generate
        :arg type_id        specifies the type of image that will be used as a base image
        :arg image_id:      input image the function will modify
        :return: Tile texture with randomly generated features
        """

        # load up the base image
        base_image = self.tileTypes[image_id][type_id]
        # copy the base image
        pygame.image.save(base_image, "Well Escape tiles/copy.png")
        # load up the copy of the base image
        texture = pygame.image.load("Well Escape tiles/copy.png")

        # if the image type is a floor and material type is not in perfect condition
        if image_id == 1 and material_id > 0:
            self.mud(texture)       # generate some mud for the image
            # if the material type is really old
            if material_id == 2:
                self.moss(texture)  # generate some moss for the image
                self.type_2_inst.append(inst)   # add the generated really old material instance number to a list
            else:
                self.type_1_inst.append(inst)   # add the generated dirty material instance number to a list

            # save the generated image to the varieties folder
            name = "Procedural-" + str(image_id) + "_type-" + str(type_id) + \
                   "_mat-" + str(material_id) + "_inst-" + str(inst)
            pygame.image.save(texture, "Well Escape tiles/varieties/" + name + ".png")

        return texture

    def assign_material(self, image_id, type_id, material_id):
        """
        Assigns a randomly chosen variation texture.

        :arg material_id:   specifies the type of material the function will assign
        :arg type_id        specifies the type of image that will be used as a base image
        :arg image_id:      input image the function will modify
        :return: Tile texture with randomly generated features
        """
        # load up the base image
        base_image = self.tileTypes[image_id][type_id]
        # if the image type is a floor and material type is not in perfect condition
        if image_id == 1 and material_id > 0:
            # if the material type is really old
            if material_id == 2:
                # choose a randomly chosen really old texture instance
                self.random_inst = self.type_2_inst[random.randint(0, len(self.type_2_inst)-1)]
            else:
                # choose a randomly chosen dirty texture instance
                self.random_inst = self.type_1_inst[random.randint(0, len(self.type_1_inst)-1)]

            # assign the variation texture
            texture = pygame.image.load("Well Escape tiles/varieties/" +
                                        "Procedural-" + str(image_id) + "_type-" + str(type_id) +
                                        "_mat-" + str(material_id) +
                                        "_inst-" + str(self.random_inst) + ".png")
        else:
            # keep the texture the same
            texture = base_image

        return texture

    @staticmethod
    def get_dungeon_room(first):
        """
        Chooses a pixel map.

        :param first:   specifies if there's a need to generate the starting room
        :return:    a randomly chosen pixel map
        """

        # load up the pixel maps
        pixel_map = "pixelLevels/"
        small_room = pygame.image.load(pixel_map + "smallRoom_000.png")
        hallway = pygame.image.load(pixel_map + "hall_000.png")
        mid_room = pygame.image.load(pixel_map + "MidRoom_000.png")
        rooms = [hallway, small_room, mid_room]
        room_weights = [0.5, 0.75, 0.25]
        if first:
            # load up and choose the starting room pixel map
            current_module = pygame.image.load(pixel_map + "start.png")
        else:
            # choose a random pixel map
            current_module = random.choices(rooms, room_weights)[0]

        return current_module