import pygame
from pygame.locals import *
import dungeonGenerator as dunGen
import main
import library


def find_current_tile(prediction_x, prediction_y):
    """
    Find or predict the tile the player is/will be on.
    :param prediction_x: offset for predicting the next tile on the x axis
    :param prediction_y: offset for predicting the next tile on the y axis
    :return: index of the current tile the player is on
    """

    previous_tile = dunGen.allTilePositions[dunGen.GameStore.current_tile]
    # round the current player position to the position of the nearest tile
    current_tile_x = int(((dunGen.GameStore.playerX +
                           prediction_x)
                          / dunGen.TILE_SIZE)
                         + 0.5) * dunGen.TILE_SIZE
    current_tile_y = int(((dunGen.GameStore.playerY +
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
    current_tile_index = find_current_tile(0, 0)
    current_tile_pos = dunGen.allTilePositions[current_tile_index]
    current_tile_type = dunGen.allTiles[current_tile_index]
    current_tile_material = dunGen.allTileMaterials[current_tile_index]

    # find values of the predicted tile that the player might land on
    current_tile_index2 = find_current_tile(dunGen.GameStore.prediction_X,
                                            dunGen.GameStore.prediction_Y)
    current_tile_pos2 = dunGen.allTilePositions[current_tile_index2]
    current_tile_type2 = dunGen.allTiles[current_tile_index2]

    # find values of the second predicted tile that the player might land on
    current_tile_index3 = find_current_tile(dunGen.GameStore.
                                            secondary_prediction_X,
                                            dunGen.GameStore.
                                            secondary_prediction_Y)
    current_tile_pos3 = dunGen.allTilePositions[current_tile_index3]
    current_tile_type3 = dunGen.allTiles[current_tile_index3]

    # if the is a floor or a door
    if current_tile_type2 == 0 or current_tile_type2 > 1:
        # save the current position of the player
        dunGen.GameStore.previousPlayerY = dunGen.GameStore.playerY
        dunGen.GameStore.previousPlayerX = dunGen.GameStore.playerX
        # save the current predicted tile
        dunGen.GameStore.last_tile = current_tile_index2
        # create a rect for the current tile
        current_tile_rect = Rect(dunGen.GameStore.x + current_tile_pos[0]
                                 - dunGen.GameStore.offsetX,
                                 dunGen.GameStore.y
                                 + current_tile_pos[1]
                                 - dunGen.GameStore.offsetY,
                                 dunGen.TILE_SIZE, dunGen.TILE_SIZE)
        # create a rect for the predicted tile
        current_tile_rect2 = Rect(dunGen.GameStore.x + current_tile_pos2[0]
                                  - dunGen.GameStore.offsetX,
                                  dunGen.GameStore.y
                                  + current_tile_pos2[1]
                                  - dunGen.GameStore.offsetY,
                                  dunGen.TILE_SIZE, dunGen.TILE_SIZE)
        # create a rect for the secondary predicted tile
        current_tile_rect3 = Rect(dunGen.GameStore.x + current_tile_pos3[0]
                                  - dunGen.GameStore.offsetX,
                                  dunGen.GameStore.y
                                  + current_tile_pos3[1]
                                  - dunGen.GameStore.offsetY,
                                  dunGen.TILE_SIZE, dunGen.TILE_SIZE)

        # if the current tile is an exit door, block the bottom
        # and let the player press space to restart
        if current_tile_type == 2:
            if current_tile_material == 1:
                if library.KEY_PRESSED["space"]:
                    main.start()
                if current_tile_pos[1] < dunGen.GameStore.playerY:
                    dunGen.GameStore.bottom_col = True
                else:
                    dunGen.GameStore.bottom_col = False

        if current_tile_type == 3:
            if current_tile_material == 0:
                if library.KEY_PRESSED["space"]:
                    return

        pygame.draw.rect(main.screen, Color("red"), current_tile_rect3, 3)
        pygame.draw.rect(main.screen, Color("orange"), current_tile_rect2, 3)
        pygame.draw.rect(main.screen, Color("green"), current_tile_rect, 3)

    # if the secondary predicted tile is a wall tile
    if current_tile_type3 == 1:
        # add all the true collision values to a list
        true_collisions = []
        for i in range(len(dunGen.GameStore.collisions)):
            if dunGen.GameStore.collisions[i]:
                true_collisions.append(dunGen.GameStore.collisions[i])

        print(dunGen.GameStore.collisions)
        # if there are no true collisions yet, save the player position
        if len(true_collisions) < 1:
            dunGen.GameStore.previousPlayerX = dunGen.GameStore.playerX
            dunGen.GameStore.previousPlayerY = dunGen.GameStore.playerY

        # find which direction the predicted tile is from the current tile
        # and set booleans which block the movement in corresponding directions
        difference = dunGen.GameStore.last_tile - current_tile_index2
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
        if not current_tile_type2 == 2:
            dunGen.GameStore.bottom_col = False
        dunGen.GameStore.left_col = False
        dunGen.GameStore.right_col = False
