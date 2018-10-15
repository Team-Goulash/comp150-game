import pygame, main

change = False                      # variable that activates lightning sequence

currentposx = main.GameStore.playerX
currentposy = main.GameStore.playerY
currentTilex = 0
currentTiley = 0
currentTile = (currentTilex, currentTiley)        #tile that character is on
previousTile = (currentTilex + 1 , currentTiley + 1)   #tile that character was last frame

xtilelength = 10
ytilelength = 3

def check:
    while True:
        for i in main.MAP_WIDTH:
            r = i * 90
            t = currentposx - r
            if t < 0:
                currentTilex = i
                break

        for i in main.MAP_HEIGHT:
            r = i * 90
            t = currentposx - r
            if t < 0:
                currentTiley = i
                break
    if currentTile != previousTile:
        change = True
        previousTile = currentTile





"""if change:                          #start the lightning sequence
    xarray = [xtile - 3, xtile - 2, xtile + 2, xtile + 3]
    yarray = [ytile - 3, ytile - 2, ytile + 2, ytile + 3]
    for x in xarray:
        for y in yarray:
            tile = (x,y)
            line = pygame.draw.line(DISPLAYSURF, (255,0,0), (playersPosition), tilesPoisition)
            if line.collidelist #if there is wall value
                tile #texture change to black
                """
