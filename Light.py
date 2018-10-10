import pygame

x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  #tile mep
y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print ("Input X 0-9")               #3 debug lines
xtile = input(int)
ytile = input(int)

change = False                      # variable that activates lightning sequence

currentTile = [xtile, ytile]        #tile that character is on
previousTile = [xtile + 1, ytile]   #tile that character was last frame

if currentTile != previousTile:     #checks whether you have moved onto another tile
    change = True
    print("happened 1")

if change:                          #start the lightning sequence
    xarray = [xtile - 3, xtile - 2, xtile + 2, xtile + 3]
    yarray = [ytile - 3, ytile - 2, ytile + 2, ytile + 3]
    for x in xarray:
        for y in yarray:
            
            pygame.rect.collidelist
