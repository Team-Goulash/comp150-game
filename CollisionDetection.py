import pygame
from pygame.locals import *
import dungeonGenerator as dunGen
import main
import library


def find_current_tile(prediction_x, prediction_y):
    previous_tile = dunGen.allTilePositions[dunGen.GameStore.current_tile]

    current_tile_x = int(((dunGen.GameStore.playerX +
                           prediction_x)
                          / dunGen.TILE_SIZE)
                         + 0.5) * dunGen.TILE_SIZE
    current_tile_y = int(((dunGen.GameStore.playerY +
                           prediction_y)
                          / dunGen.TILE_SIZE)
                         + 0.85) * dunGen.TILE_SIZE

    tile_pos = [current_tile_x, current_tile_y]

    if tile_pos in dunGen.allTilePositions and not tile_pos == previous_tile:
        dunGen.GameStore.current_tile = dunGen.allTilePositions.index(tile_pos)
    return dunGen.GameStore.current_tile


def detect_collision():
    """Draw the colliders on the player and wall tiles."""
    current_tile_index = find_current_tile(0, 0)
    current_tile_pos = dunGen.allTilePositions[current_tile_index]
    current_tile_type = dunGen.allTiles[current_tile_index]

    current_tile_index2 = find_current_tile(dunGen.GameStore.prediction_X,
                                            dunGen.GameStore.prediction_Y)
    current_tile_pos2 = dunGen.allTilePositions[current_tile_index2]
    current_tile_type2 = dunGen.allTiles[current_tile_index2]

    current_tile_index3 = find_current_tile(dunGen.GameStore.
                                            secondary_prediction_X,
                                            dunGen.GameStore.
                                            secondary_prediction_Y)
    current_tile_pos3 = dunGen.allTilePositions[current_tile_index3]
    current_tile_type3 = dunGen.allTiles[current_tile_index3]

    if current_tile_type2 == 0 or current_tile_type2 > 1:
        dunGen.GameStore.last_tile = current_tile_index2
        current_tile_rect = Rect(dunGen.GameStore.x + current_tile_pos[0]
                                 - dunGen.GameStore.offsetX,
                                 dunGen.GameStore.y
                                 + current_tile_pos[1]
                                 - dunGen.GameStore.offsetY,
                                 dunGen.TILE_SIZE, dunGen.TILE_SIZE)

        current_tile_rect2 = Rect(dunGen.GameStore.x + current_tile_pos2[0]
                                 - dunGen.GameStore.offsetX,
                                 dunGen.GameStore.y
                                 + current_tile_pos2[1]
                                 - dunGen.GameStore.offsetY,
                                 dunGen.TILE_SIZE, dunGen.TILE_SIZE)

        current_tile_rect3 = Rect(dunGen.GameStore.x + current_tile_pos3[0]
                                  - dunGen.GameStore.offsetX,
                                  dunGen.GameStore.y
                                  + current_tile_pos3[1]
                                  - dunGen.GameStore.offsetY,
                                  dunGen.TILE_SIZE, dunGen.TILE_SIZE)

        pygame.draw.rect(main.screen, Color("red"), current_tile_rect3, 1)
        pygame.draw.rect(main.screen, Color("orange"), current_tile_rect2, 1)
        pygame.draw.rect(main.screen, Color("green"), current_tile_rect, 1)

    if current_tile_type3 == 1:
        difference = dunGen.GameStore.last_tile - current_tile_index2
        if difference > 1:
            dunGen.GameStore.top_col = True
        if difference < -1:
            dunGen.GameStore.bottom_col = True
        if difference == 1:
            dunGen.GameStore.left_col = True
        if difference == -1:
            dunGen.GameStore.right_col = True
    else:
        dunGen.GameStore.top_col = False
        dunGen.GameStore.bottom_col = False
        dunGen.GameStore.left_col = False
        dunGen.GameStore.right_col = False
