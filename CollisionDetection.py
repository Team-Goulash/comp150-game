import pygame
from pygame.locals import *
import dungeonGenerator as dunGen
import main


def find_current_tile():
    previous_tile = dunGen.allTilePositions[dunGen.GameStore.current_tile]

    current_tile_x = int(((dunGen.GameStore.playerX +
                           dunGen.GameStore.prediction_X)
                          / dunGen.TILE_SIZE)
                         + 0.5) * dunGen.TILE_SIZE
    current_tile_y = int(((dunGen.GameStore.playerY +
                           dunGen.GameStore.prediction_Y)
                          / dunGen.TILE_SIZE)
                         + 0.85) * dunGen.TILE_SIZE

    tile_pos = [current_tile_x, current_tile_y]

    if tile_pos in dunGen.allTilePositions and not tile_pos == previous_tile:
        dunGen.GameStore.current_tile = dunGen.allTilePositions.index(tile_pos)
        print(dunGen.GameStore.current_tile)
        print(dunGen.allTiles[dunGen.GameStore.current_tile])
    return dunGen.GameStore.current_tile


def detect_collision():
    """Draw the colliders on the player and wall tiles."""
    current_tile_index = find_current_tile()
    current_tile_pos = dunGen.allTilePositions[current_tile_index]
    current_tile_type = dunGen.allTiles[dunGen.GameStore.current_tile]
    if current_tile_type == 0:
        dunGen.GameStore.last_tile = current_tile_index
        current_tile_rect = Rect(dunGen.GameStore.x + current_tile_pos[0]
                                 - dunGen.GameStore.offsetX,
                                 dunGen.GameStore.y
                                 + current_tile_pos[1]
                                 - dunGen.GameStore.offsetY,
                                 dunGen.TILE_SIZE, dunGen.TILE_SIZE)

        pygame.draw.rect(main.screen, Color("red"), current_tile_rect, 1)
    else:
        difference = dunGen.GameStore.last_tile - current_tile_index
        if difference > 1:
            dunGen.GameStore.top_col = True
        if difference < -1:
            dunGen.GameStore.bottom_col = True
        if difference == 1:
            dunGen.GameStore.left_col = True
        if difference == -1:
            dunGen.GameStore.right_col = True
