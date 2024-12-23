##############################################################################
# DETAILS
#  Attempt 1 at an othello game
#  Mr Reed - Dec 2024
#
#  Sounds 
#  https://pixabay.com/sound-effects/search/clicks/
#
##############################################################################

##############################################################################
# IMPORTS
##############################################################################
from othelloClasses import Person
import pygame, random, time
from pygame.locals import *
 
##############################################################################
# VARIABLES
##############################################################################
DEBUG_ON = True

SCREEN_WIDTH = 560
SCREEN_HEIGHT = 460

# create the display surface object
# of specific dimension.
surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Othello - Mark Reed (c) 2024')

COL_BLACK = (0,0,0)
COL_WHITE = (255,255,255)
COL_GREY = (150,150,150)
COL_RED = (255,0,0)
COL_BLUE = (0,0,255)
COL_DARK_BLUE = (35, 5, 250)
BACK_FILL_COLOUR = COL_WHITE
backImageName = "./images/othello blank grid.jpg"
turnIndicatorImageName = "./images/turnIndicator.jpg"
scoreImageName = "./images/score.jpg"

TOP_LEFT = (35,22)
TOP_RIGHT = (452,22)
BOT_LEFT = (35,438)
BOT_RIGHT = (452,438)
GRID_SIZE_X = 52
GRID_SIZE_Y = 52
A1_location = (62,50)  #Used to draw pieces in the correct place!
PIECE_SIZE = 20

p1Score = 2
p2Score = 2

#sounds
pygame.mixer.init()
clickSound = pygame.mixer.Sound("./sounds/click.mp3")

#fonts
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pygame.font.SysFont('Comic Sans MS', 16)
p1ScoreSurface = my_font.render('2', False, (0, 0, 0))
p2ScoreSurface = my_font.render('2', False, (0, 0, 0))

running = True

turn = COL_BLACK
turnIndicatorYPos = 24

#Testing some code from a different py file...
p1 = Person("Fred")
p1.SayHello()

#Make a blank game grid
gameGrid = [[0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,2,1,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]]

##############################################################################
# SUB PROGRAMS
##############################################################################
def UpdateScores():
    global p1ScoreSurface,p2ScoreSurface,p1Score,p2Score

    p1Score = 0
    p2Score = 0

    for i in range(8):
        for j in range(8):
            if(gameGrid[i][j] == 1):
                p1Score = p1Score + 1
            elif(gameGrid[i][j] == 2):
                p2Score = p2Score + 1

    p1ScoreSurface = my_font.render(str(p1Score), False, (0, 0, 0))
    p2ScoreSurface = my_font.render(str(p2Score), False, (0, 0, 0))

def LoadImages(running):
    global backImage,turnIndicatorImage,scoreImage
    try:
        backImage = pygame.image.load(backImageName).convert()
        print("\"{}\". Loaded successfully.".format(backImageName))
    except:
        print("When loading \"{}\". No image found!!!".format(backImageName))
        print("Quitting PyGame  :(")
        running = False
        return running

    try:
        turnIndicatorImage = pygame.image.load(turnIndicatorImageName).convert()
        print("\"{}\". Loaded successfully.".format(turnIndicatorImageName))
    except:
        print("When loading \"{}\". No image found!!!".format(turnIndicatorImageName))
        print("Quitting PyGame  :(")
        running = False
        return running

    try:
        scoreImage = pygame.image.load(scoreImageName).convert()
        print("\"{}\". Loaded successfully.".format(scoreImageName))
    except:
        print("When loading \"{}\". No image found!!!".format(scoreImageName))
        print("Quitting PyGame  :(")
        running = False
        return running
        

def SwapTurn():
    global turn,turnIndicatorYPos
    if(turn == COL_WHITE):
        turn = COL_BLACK
        turnIndicatorYPos = 24
    else:
        turn = COL_WHITE
        turnIndicatorYPos = 50

def WhatSquareAreWeIn(aPosition):
    #Find out what square somebody clicked on.
    #For example, if we click top left the the answer is row 1 col 1  (aka  "a1")
    currentClickX = aPosition[0]
    currentClickY = aPosition[1]
   
    adjustedX = currentClickX-TOP_LEFT[0]
    col = adjustedX//(GRID_SIZE_X+1) #The +1 in the brackets seems to fix the identifcation of col 6 to 7 which was a bit out?
   

    adjustedY = currentClickY-TOP_LEFT[1]
    row = adjustedY//(GRID_SIZE_Y)
   
    if DEBUG_ON:
        print("Current x = {}\nCurrrent y = {}".format(currentClickX,currentClickY))
        print("Col  =  {}".format(col+1))
        print("row  =  {}".format(row+1))

        letters = ["a","b","c","d","e","f","g","h"]
        print("{}{}".format(letters[col],row))


    return row,col

def DrawTurnMarker():
    pygame.draw.rect(surface, COL_DARK_BLUE, pygame.Rect(487,turnIndicatorYPos, 28, 27),2)
            
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
            
            pygame.draw.circle(surface, pieceCol, (A1_location[0] + col*GRID_SIZE_X, A1_location[1] + row*GRID_SIZE_Y), PIECE_SIZE)
            
def AddPieceToGrid(row,col):

    whatToAdd = 1

    if(turn == COL_BLACK):
        whatToAdd = 2

    #Only allow the move if the square is not full already...
    if(gameGrid[row][col] == 0):
        gameGrid[row][col] = whatToAdd
        pygame.mixer.Sound.play(clickSound)
        pygame.mixer.music.stop()
        SwapTurn()
    else:
        print("Square taken already!!!  Pick again...")

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
                AddPieceToGrid(row,col)
                
    return running

##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages(running)

#game loop
while running:

    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (0, 0))

    surface.blit(turnIndicatorImage, (460, 0))

    surface.blit(scoreImage, (475, 364))

    UpdateScores()

    surface.blit(p1ScoreSurface, (514,390))
    surface.blit(p2ScoreSurface, (514,416))

    DrawTurnMarker()

    running = HandleInput(running)
   
    if(running):
        DrawTheCurrentGameGrid()
        pygame.display.flip()

pygame.quit()
