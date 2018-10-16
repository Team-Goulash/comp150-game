import main
import pygame
import sys


class var():
    light = 100
    change = False                      '''variable that activates lightning sequence'''
    currentposx = main.GameStore.playerX    #characters position
    currentposy = main.GameStore.playerY    #characters position
    ctx = 4                        #x tile that character is on
    cty = 4                        #y tile that character is on
    previoustilex = 0                       #x tile that character was on 1 frame ago
    previoustiley = 0                       #y tile that character was on 1 frame ago
    xtilelength = 10           #finds amount of tiles in width
    ytilelength = 10           #finds amount of tiles in height
    tile = []
    tiles = []
    xarray = []
    yarray = []


for y in range(var.ytilelength):
    var.tile = []
    for x in range(var.xtilelength):
        item = 1
        var.tile.append(item)
    var.tiles.append(var.tile)
print(var.tiles)


def check():
        for i in main.MAP_WIDTH:
            r = i * 90
            t = var.currentposx - r
            if t < 0:
                var.ctx = i - 1
                if var.ctx is not var.previoustilex:
                    aply()
                break

        for i in main.MAP_HEIGHT:
            r = i * 90
            t = var.currentposx - r
            if t < 0:
                var.cty = i - 1
                if var.cty is not var.previoustiley:
                    aply()
                break


def aply():
    var.previoustilex = var.ctx
    var.previoustiley = var.cty
    if var.light > 66:
        var.xarray = [var.ctx - 3, var.ctx - 2, var.ctx - 1, var.ctx, var.ctx + 1, var.ctx + 2, var.ctx + 3]
        var.yarray = [var.cty - 3, var.cty - 2, var.cty - 1, var.cty, var.cty + 1, var.cty + 2, var.cty + 3]
    elif var.light > 33:
        var.xarray = [var.ctx - 2, var.ctx - 1, var.ctx, var.ctx + 1, var.ctx + 2, ]
        var.yarray = [var.cty - 2, var.cty - 1, var.cty, var.cty + 1, var.cty + 2, ]
    else:
        var.xarray = [var.ctx - 1, var.ctx, var.ctx + 1]
        var.yarray = [var.cty - 1, var.cty, var.cty + 1]

    for y in range(var.ytilelength):
        for x in range(var.xtilelength):
            var.tile[x] = 0
        var.tiles[y] = var.tile
    print(var.tiles)

    for x in range(var.xtilelength):
        for y in range(var.ytilelength):

            if y in var.yarray and x in var.xarray:
                var.tiles[y][x] = 1
            else:
                var.tiles[y][x] = 0

            #line = pygame.draw.line(main.screen, (255, 0, 0), (currentposx, currentposy), tilesPoisition)

            #for x in line.collidelist:
                #if x = wall
                #tile texture = its texture
            #destroy line
    print(var.tiles)

aply()