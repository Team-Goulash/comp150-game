import main, pygame, sys


class var():
    light = 100
    change = False                      #variable that activates lightning sequence
    currentposx = main.GameStore.playerX    #characters position
    currentposy = main.GameStore.playerY    #characters position
    ctx = 1                      #x tile that character is on
    cty = 1                        #y tile that character is on
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
        var.xarray = [var.ctx - 2, var.ctx - 1, var.ctx, var.ctx + 1, var.ctx + 2]
        var.yarray = [var.cty - 2, var.cty - 1, var.cty, var.cty + 1, var.cty + 2]
    else:
        var.xarray = [var.ctx - 1, var.ctx, var.ctx + 1]
        var.yarray = [var.cty - 1, var.cty, var.cty + 1]

    print(var.xarray)
    print(var.yarray)
    for yx in range(var.ytilelength):
        for xy in range(var.xtilelength):
            var.tile[xy] = 0
        var.tiles[yx] = var.tile
    print(var.tiles)

    temp_tiles = []

    for yy in range(var.ytilelength):
        temp_light = []
        for xx in range(var.xtilelength):

            print(xx, ":", yy, "::", 1 - ((xx / var.xtilelength) + (yy / var.ytilelength) / 2))
            if xx + 1 in var.xarray and yy + 1 in var.yarray:
                temp_light.append(1)


            else:
                temp_light.append(0)

        temp_tiles.append(temp_light)
        #    """#line = pygame.draw.line(main.screen, (255, 0, 0), (currentposx, currentposy), tilesPoisition)
        #
        #   #for x in line.collidelist:
        #       #if x = wall
        #       #tile texture = its texture
        #   #destroy line"""
    var.tiles = temp_tiles
    print(var.tiles)


aply()
