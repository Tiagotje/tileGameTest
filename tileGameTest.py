#-------------------------------------------------------------------------------
# Name:        tileGameTest
# Purpose:
#
# Author:      Tiago Scholten
#
# Created:     16/03/2014
# Copyright:   (c) Tiago Scholten 2014
# Licence:     If u touch u die
#-------------------------------------------------------------------------------

# Init stuff
import pygame               #Importeer pygame functies

pygame.init()               #Start pygame
                            #Defineer de kleuren  \/
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

camX = 0
camY = 0

levell = []                 #levellijst is een lege lijst

run = True                  # Of het spel runtss
screenX = 300               # Breedde van Scherm
screenY = 300               # Lengte van Scherm
WinY = -3
WinX = -3
tileX, tileY = 50, 50
PlayerX, PlayerY = 0,0

level = open("level.txt", "r+")                         #Open level.txt als level

class tile(object):
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        if self.t == 3: self.solid = True
        elif self.t == 6: self.solid = True
        else: self.solid = False
    def update(item):
        if item.t == 3:
            pygame.draw.rect(Screen, darkBlue,((item.x-camX)*tileX, (item.y-camY)*tileY, tileX, tileY))
        elif item.t == 0:
            return
        elif item.t == 4:
            item.t = 0
        elif item.t == 5:
            pygame.draw.rect(Screen, red,((item.x-camX)*tileX, (item.y-camY)*tileY, tileX, tileY))
            WinX, WinY = item.x, item.y
            global WinX, WinY
        elif item.t == 6:
            pygame.draw.rect(Screen, (150, 100, 0),((item.x-camX)*tileX, (item.y-camY)*tileY, tileX, tileY))
            item.solid = True
        elif item.t == 7:
            pygame.draw.rect(Screen, (150, 100, 0),((item.x-camX)*tileX, (item.y-camY)*tileY, tileX, tileY-30))
            item.solid = False
        else: print item.t
    def toggle(item):
        if item.t == 6:
            item.t = 7
        elif item.t == 7:
            item.t = 6

rn = -1
for line in level:
    rn += 1
    rowl = line.split(",")
    if rowl[ len(rowl)-1 ][-1] == "\n":
        rowl[ len(rowl)-1 ] = rowl[ len(rowl)-1 ][:-1]
        cn = 0
    for item in range(len(rowl)):
        rowl[item] = tile(cn, rn, int(rowl[item]))
        cn += 1
    levell.append( rowl )

       #Print levellijst ter controle

def giveInfo():
    print "______________________"
    print "CamX: " + str(camX) + "CamY: " + str(camY)
    print "WinX: " + str(WinX) + "WinY: " + str(WinY)
    print "PlayerX: " + str(PlayerX) + "PlayerY: " + str(PlayerY)
    print "Block boven: " + str(levell[PlayerY-1][PlayerX].solid)
    print "Block onder: " + str(levell[PlayerY+1][PlayerX].solid)
    print "Block links: " + str(levell[PlayerY][PlayerX-1].solid)
    print "Block rechts: " + str(levell[PlayerY][PlayerX+1].solid)

logo = pygame.image.load( 'tileLogo.png' )

Screen = pygame.display.set_mode((screenX, screenY))  #Scherm is een nieuw Scherm dat kan worden vergroot & verkleind
pygame.display.set_caption("Tile-Venture")                        #De titel is Tile-Venture
pygame.display.set_icon(logo)

def movePlayer(direction):
    global PlayerX, PlayerY, WinX, WinY
    try:
        if (direction.lower() == "down") and (not levell[PlayerY+1][PlayerX].solid):
            PlayerY = PlayerY + 1
        elif (direction.lower() == "up") and (not levell[PlayerY-1][PlayerX].solid):
            PlayerY -= 1
        elif (direction.lower() == "right") and (not levell[PlayerY][PlayerX+1].solid):
            PlayerX += 1
        elif (direction.lower() == "left") and (not levell[PlayerY][PlayerX-1].solid):
            PlayerX -= 1
        elif( PlayerY == WinY) and (PlayerX == WinX):
            run = False
        return levell
    except:
        return levell


for row in levell:
    for item in row:
        if item.t == 4:
            item.t = 0
            PlayerX = item.x
            PlayerY = item.y



while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                movePlayer("Down")
            if event.key == pygame.K_w:
                movePlayer("Up")
            if event.key == pygame.K_a:
                movePlayer("Left")
            if event.key == pygame.K_d:
                movePlayer("Right")
            if event.key == pygame.K_o:
                giveInfo()
            if event.key == pygame.K_SPACE:
                levell[PlayerY][PlayerX+1].toggle()
                levell[PlayerY+1][PlayerX].toggle()
                levell[PlayerY][PlayerX-1].toggle()
                levell[PlayerY-1][PlayerX].toggle()
        pygame.display.flip()
    #draw a map
    rn = -1
    Screen.fill(black)
    if (PlayerX-4 > camX) and (camX < len(levell[0])-7):
        camX += 3
    if (PlayerX-1 < camX) and (camX > 0):
        camX -= 3
    if (PlayerY-4 > camY) and (camY < len(levell)-7):
        camY += 3
    if (PlayerY-1 < camY) and (camY > 0):
        camY -= 3

    if (PlayerX == WinX) and (PlayerY == WinY):
        run = False


    for row in levell:
        for item in row:
            item.update()
    pygame.draw.rect(Screen, green,((PlayerX-camX)*50, (PlayerY-camY)*50, 50, 50))
    pygame.display.update()



level.close()
pygame.quit()
