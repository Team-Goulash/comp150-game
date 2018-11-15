import pygame
from pygame.locals import *
import dungeonGenerator as dunGen
import main
import library
import fuelMeter


class TileStore:
    current_tile_index = 0
    current_tile_pos = [0, 0]
    current_tile_type = 0
    current_tile_material = 0

    current_tile_index2 = 0
    current_tile_pos2 = [0, 0]
    current_tile_type2 = 0
    current_tile_material2 = 0

    current_tile_index3 = 0
    current_tile_pos3 = [0, 0]
    current_tile_type3 = 0
    current_tile_material3 = 0

    current_chest_index = 0
    current_chest_pos = [0, 0]

    previous_inputs = [False, False, False, False]


def find_current_tile(prediction_x, prediction_y):
    """
    Find or predict the tile the player is/will be on.
    :param prediction_x: offset for predicting the next tile on the x axis
    :param prediction_y: offset for predicting the next tile on the y axis
    :return: index of the current tile the player is on
    """

    previous_tile = dunGen.allTilePositions[dunGen.GameStore.current_tile]
    # round the current player position to the position of the nearest tile
    current_tile_x = int(((dunGen.GameStore.player.position[0] +
                           prediction_x)
                          / dunGen.TILE_SIZE)
                         + 0.5) * dunGen.TILE_SIZE
    current_tile_y = int(((dunGen.GameStore.player.position[1] +
                           prediction_y)
                          / dunGen.TILE_SIZE)
                         + 0.85) * dunGen.TILE_SIZE
    tile_pos = [current_tile_x, current_tile_y]

    # if a tile with the calculated position exists
    # and it's not the same as the previous tile
    # set it as the current tile and return the value
    if tile_pos in dunGen.allTilePositions and not tile_pos == previous_tile:
        dunGen.GameStore.current_tile = dunGen.allTilePositions.index(tile_pos)
    return dunGen.GameStore.current_tile


def detect_collision():
    """Check for collision between the player and the wall tiles."""

    dunGen.GameStore.collisions = [dunGen.GameStore.top_col,
                                   dunGen.GameStore.bottom_col,
                                   dunGen.GameStore.left_col,
                                   dunGen.GameStore.right_col]

    # find values of the tile the player is currently on
    TileStore.current_tile_index = find_current_tile(0, 0)
    TileStore.current_tile_pos = dunGen.allTilePositions[
        TileStore.current_tile_index]
    TileStore.current_tile_type = dunGen.allTiles[
        TileStore.current_tile_index]
    TileStore.current_tile_material = dunGen.allTileMaterials[
        TileStore.current_tile_index]

    # find values of the predicted tile that the player might land on
    TileStore.current_tile_index2 = find_current_tile(
        dunGen.GameStore.prediction_X, dunGen.GameStore.prediction_Y)
    TileStore.current_tile_pos2 = dunGen.allTilePositions[
        TileStore.current_tile_index2]
    TileStore.current_tile_type2 = dunGen.allTiles[
        TileStore.current_tile_index2]
    TileStore.current_tile_material2 = dunGen.allTileMaterials[
        TileStore.current_tile_index2]

    # find values of the second predicted tile that the player might land on
    TileStore.current_tile_index3 = find_current_tile(dunGen.GameStore.
                                                      secondary_prediction_X,
                                                      dunGen.GameStore.
                                                      secondary_prediction_Y)
    TileStore.current_tile_pos3 = dunGen.allTilePositions[
        TileStore.current_tile_index3]
    TileStore.current_tile_type3 = dunGen.allTiles[
        TileStore.current_tile_index3]
    TileStore.current_tile_material3 = dunGen.allTileMaterials[
        TileStore.current_tile_index3]

    if TileStore.current_tile_pos in dunGen.GameStore.chests:
        TileStore.current_chest_index = dunGen.GameStore.chests.index(
            TileStore.current_tile_pos)
        TileStore.current_chest_pos = dunGen.GameStore.chests[
            TileStore.current_chest_index]
    else:
        TileStore.current_chest_index = -1

    # if the secondary predicted tile is a floor or a door
    if (TileStore.current_tile_type2 == 0
        or TileStore.current_tile_type2 > 1) and \
            not (TileStore.current_tile_type2 == 2
                 and TileStore.current_tile_material2 == 0) and\
            not TileStore.current_tile_type == 1:

        # save the current movement inputs
        if library.KEY_PRESSED["forwards"]:
            TileStore.previous_inputs[0] = True
            TileStore.previous_inputs[1] = False
        elif library.KEY_PRESSED["backwards"]:
            TileStore.previous_inputs[1] = True
            TileStore.previous_inputs[0] = False
        else:
            TileStore.previous_inputs[0] = False
            TileStore.previous_inputs[1] = False

        if library.KEY_PRESSED["left"]:
            TileStore.previous_inputs[2] = True
            TileStore.previous_inputs[3] = False
        elif library.KEY_PRESSED["right"]:
            TileStore.previous_inputs[3] = True
            TileStore.previous_inputs[2] = False
        else:
            TileStore.previous_inputs[2] = False
            TileStore.previous_inputs[3] = False

        # save the current predicted tile
        dunGen.GameStore.last_tile = TileStore.current_tile_index2

        # if the current tile is an exit door, block the bottom
        # and let the player press space to restart
        if TileStore.current_tile_type == 2 \
                and TileStore.current_tile_material == 1:
                if library.KEY_PRESSED["space"]:
                    dunGen.reset()
                if TileStore.current_tile_pos[1] < dunGen.GameStore.player.position[1]:
                    dunGen.GameStore.bottom_col = True
                else:
                    dunGen.GameStore.bottom_col = False

        if TileStore.current_chest_index > -1:
            if library.KEY_PRESSED["space"]:
                dunGen.GameStore.add_fuel = True
                dunGen.GameStore.chests.pop(TileStore.current_chest_index)

    # if the secondary predicted tile is a wall tile
    if TileStore.current_tile_type3 == 1 or TileStore.current_tile_type2 == 1 \
            or TileStore.current_tile_type == 1 \
            or (TileStore.current_tile_type3 == 2
                and TileStore.current_tile_material3 == 0):

        # add all the true collision values to a list
        true_collisions = []
        for i in range(len(dunGen.GameStore.collisions)):
            if dunGen.GameStore.collisions[i]:
                true_collisions.append(dunGen.GameStore.collisions[i])

        # block the movement in corresponding directions
        # depending on the current and predicted tiles' types
        if TileStore.current_tile_type == 1 and \
                not TileStore.current_tile_type3 == 0:
            if TileStore.previous_inputs[0]:
                dunGen.GameStore.top_col = True
            if TileStore.previous_inputs[1]:
                dunGen.GameStore.bottom_col = True
            if TileStore.previous_inputs[2]:
                dunGen.GameStore.left_col = True
            if TileStore.previous_inputs[3]:
                dunGen.GameStore.right_col = True
        else:
            difference = dunGen.GameStore.last_tile \
                         - TileStore.current_tile_index2
            if difference > 1:
                dunGen.GameStore.top_col = True
                if len(true_collisions) < 1:
                    dunGen.GameStore.secondary_prediction_X = 0
            if difference < -1:
                dunGen.GameStore.bottom_col = True
                if len(true_collisions) < 1:
                    dunGen.GameStore.secondary_prediction_X = 0
            if difference == 1:
                dunGen.GameStore.left_col = True
                if len(true_collisions) < 1:
                    dunGen.GameStore.secondary_prediction_Y = 0
            if difference == -1:
                dunGen.GameStore.right_col = True
                if len(true_collisions) < 1:
                    dunGen.GameStore.secondary_prediction_Y = 0
    else:
        # disable collisions
        dunGen.GameStore.top_col = False
        if not TileStore.current_tile_type2 == 2:
            dunGen.GameStore.bottom_col = False
        dunGen.GameStore.left_col = False
        dunGen.GameStore.right_col = False


def draw_collision():
    # create a rect for the current tile
    current_tile_rect = Rect(dunGen.GameStore.x
                             + TileStore.current_tile_pos[0]
                             - dunGen.GameStore.offsetX,
                             dunGen.GameStore.y
                             + TileStore.current_tile_pos[1]
                             - dunGen.GameStore.offsetY,
                             dunGen.TILE_SIZE, dunGen.TILE_SIZE)
    # create a rect for the predicted tile
    current_tile_rect2 = Rect(dunGen.GameStore.x
                              + TileStore.current_tile_pos2[0]
                              - dunGen.GameStore.offsetX,
                              dunGen.GameStore.y
                              + TileStore.current_tile_pos2[1]
                              - dunGen.GameStore.offsetY,
                              dunGen.TILE_SIZE, dunGen.TILE_SIZE)
    # create a rect for the secondary predicted tile
    current_tile_rect3 = Rect(dunGen.GameStore.x
                              + TileStore.current_tile_pos3[0]
                              - dunGen.GameStore.offsetX,
                              dunGen.GameStore.y
                              + TileStore.current_tile_pos3[1]
                              - dunGen.GameStore.offsetY,
                              dunGen.TILE_SIZE, dunGen.TILE_SIZE)

    pygame.draw.rect(main.screen, Color("red"), current_tile_rect3, 3)
    pygame.draw.rect(main.screen, Color("orange"), current_tile_rect2, 3)
    pygame.draw.rect(main.screen, Color("green"), current_tile_rect, 3)
