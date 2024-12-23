#Attempt 1 at an othello game
#Mr Reed - Dec 2024

from othelloClasses import Person

import pygame, random, time
from pygame.locals import *
 
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

DEBUG_ON = True

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


COL_BLACK = (0,0,0)
COL_WHITE = (255,255,255)
COL_GREY = (150,150,150)
COL_RED = (255,0,0)
BACK_FILL_COLOUR = COL_WHITE
backImageName = "othello blank grid.jpg"

TOP_LEFT = (35,22)
TOP_RIGHT = (452,22)
BOT_LEFT = (35,438)
BOT_RIGHT = (452,438)
GRID_SIZE_X = 52
GRID_SIZE_Y = 52
A1_location = (62,50)  #Used to draw pieces in the correct place!
PIECE_SIZE = 20

running = True

#Testing some code from a different py file...
p1 = Person("Fred")
p1.SayHello()

#Make a blank game grid
gameGrid = [[0,1,0,0,0,0,0,0],
            [0,0,0,0,0,1,1,0],
            [2,0,0,0,0,0,2,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,1,1,0,0,0],
            [0,0,0,2,2,2,1,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]]

#SUB PROGRAMS
def WhatSquareAreWeIn(aPosition):
    #Find out what square somebody clicked on.
    #For example, if we click top left the the answer is row 1 col 1  (aka  "a1")
    currentClickX = aPosition[0]
    currentClickY = aPosition[1]
   
    adjustedX = currentClickX-TOP_LEFT[0]
    col = adjustedX//(GRID_SIZE_X+1)  #The little +1 seems to fix the identifcation of col 6 to 7 which was a bit out?
   

    adjustedY = currentClickY-TOP_LEFT[1]
    row = adjustedY//(GRID_SIZE_Y)
   
    if DEBUG_ON:
        print("Current x = {}\nCurrrent y = {}".format(currentClickX,currentClickY))
        print("Col  =  {}".format(col))
        print("row  =  {}".format(row))

    return row,col

def DrawTheCurrentGameGrid():

    for row in range(8):
        for col in range(8):

            #Get current piece
            thisPiece =  gameGrid[row][col]

            #find out what colour we are drawing
            pieceCol = COL_WHITE
            if(thisPiece == 0):
                continue # its a blank square
            elif (thisPiece == 2):
                pieceCol = COL_BLACK
            
            #pygame.draw.rect(surface, colours[col], pygame.Rect(A1_location[0] + col*GRID_SIZE_X, A1_location[1] + row*GRID_SIZE_Y, 10, 10))
            pygame.draw.circle(surface, pieceCol, (A1_location[0] + col*GRID_SIZE_X, A1_location[1] + row*GRID_SIZE_Y), PIECE_SIZE)


def HandleInput(running):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

        #Toggle grid centre markers?
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

        #Detect a mouse up
        if event.type == pygame.MOUSEBUTTONUP:
            somePos = pygame.mouse.get_pos()
            
            currentClickX = somePos[0]
            currentClickY = somePos[1]

            if(currentClickX < TOP_LEFT[0] or
               currentClickX > TOP_RIGHT[0] or
               currentClickY < TOP_LEFT[1] or
               currentClickY > BOT_RIGHT[1]):
                print("NOT ON THE BOARD")
            else:
                row,col = WhatSquareAreWeIn(somePos)

    return running

#MAIN

#Load the background grid
try:
    backImage = pygame.image.load(backImageName).convert()
except:
    print("When loading \"{}\". No image found!!!".format(backImageName))
    print("Quitting PyGame  :(")
    running = False

#Make some random colours for the square centre markers



while running:

    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (0, 0))

    running = HandleInput(running)
   
    if(running):
        DrawTheCurrentGameGrid()
            
        pygame.display.flip()

pygame.quit()
