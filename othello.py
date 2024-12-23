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
import pygame, random, time
from pygame.locals import *
 
##############################################################################
# VARIABLES
##############################################################################
DEBUG_ON = False

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
gameOverImageName = "./images/gameOver.jpg"

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

alwaysShowNextMoves = True
nextMoveColour = (200,200,200)

#Make a blank game grid
gameGrid = [[0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,2,1,0,0,0],
            [0,0,0,1,2,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]]

##############################################################################
# SUB PROGRAMS
##############################################################################
def GetEmptySquares():
    emptySquares = []
    #find everywhere that does not have a piece on it
    for i in range(8):
        for j in range(8):
            if(gameGrid[i][j] == 0):
                emptySquares.append((j,i))

    return emptySquares

def GetCurrentPiece():
    currentPiece = 2
    oppositePiece = 1
    if(turn == COL_BLACK):
        currentPiece = 1
        oppositePiece = 2
    return currentPiece,oppositePiece

def UpdateScores():
    global p1ScoreSurface,p2ScoreSurface,p1Score,p2Score

    p1Score = 0
    p2Score = 0

    for i in range(8):
        for j in range(8):

            if(gameGrid[i][j] == 1):
                p1Score = p1Score + 1
                if(DEBUG_ON):
                    print("p1 point")

            elif(gameGrid[i][j] == 2):
                p2Score = p2Score + 1
                if(DEBUG_ON):
                    print("p2 point")

    p1ScoreSurface = my_font.render(str(p1Score), False, (0, 0, 0))
    p2ScoreSurface = my_font.render(str(p2Score), False, (0, 0, 0))

def LoadImages(running):
    global backImage,turnIndicatorImage,scoreImage,gameOverImage
    try:
        backImage = pygame.image.load(backImageName).convert()
        if(DEBUG_ON):
            print("\"{}\". Loaded successfully.".format(backImageName))
    except:
        print("When loading \"{}\". No image found!!!".format(backImageName))
        print("Quitting PyGame  :(")
        running = False
        return running

    try:
        turnIndicatorImage = pygame.image.load(turnIndicatorImageName).convert()
        if(DEBUG_ON):
            print("\"{}\". Loaded successfully.".format(turnIndicatorImageName))
    except:
        print("When loading \"{}\". No image found!!!".format(turnIndicatorImageName))
        print("Quitting PyGame  :(")
        running = False
        return running

    try:
        scoreImage = pygame.image.load(scoreImageName).convert()
        if(DEBUG_ON):
            print("\"{}\". Loaded successfully.".format(scoreImageName))
    except:
        print("When loading \"{}\". No image found!!!".format(scoreImageName))
        print("Quitting PyGame  :(")
        running = False
        return running

    try:
        gameOverImage = pygame.image.load(gameOverImageName).convert()
        if(DEBUG_ON):
            print("\"{}\". Loaded successfully.".format(gameOverImageName))
    except:
        print("When loading \"{}\". No image found!!!".format(gameOverImageName))
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
        print("Col  =  {}".format(col))
        print("row  =  {}".format(row))

        letters = ["a","b","c","d","e","f","g","h"]
        print("{}{}".format(letters[col],row+1))

    return col,row

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
            elif (thisPiece == 1):
                pieceCol = COL_BLACK
            
            pygame.draw.circle(surface, pieceCol, (A1_location[0] + col*GRID_SIZE_X, A1_location[1] + row*GRID_SIZE_Y), PIECE_SIZE)

def CheckVerticalUp(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for vert run UP
    numInRun = 0
    for i in range(row-1,-1,-1):
        if(gameGrid[i][col] == 0):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(gameGrid[i][col] == oppositePiece):
            numInRun = numInRun + 1
        if(gameGrid[i][col] == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(row-1,row-1-numInRun,-1):
                gameGrid[i][col] = currentPiece
    
        if(DEBUG_ON):
            print("Vertical UP move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckVerticalDown(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for vert run DOWN
    numInRun = 0
    for i in range(row+1,8):
        if(gameGrid[i][col] == 0):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(gameGrid[i][col] == oppositePiece):
            numInRun = numInRun + 1
        if(gameGrid[i][col] == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(row+1,row+1+numInRun):
                gameGrid[i][col] = currentPiece
        
        if(DEBUG_ON):
            print("Vertical down move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckHorizontalRight(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for horizontal run ->
    numInRun = 0
    for i in range(col+1,8):
        if(gameGrid[row][i] == 0):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(gameGrid[row][i] == oppositePiece):
            numInRun = numInRun + 1
        if(gameGrid[row][i] == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(col+1,col+1+numInRun):
                gameGrid[row][i] = currentPiece
    
        if(DEBUG_ON):
            print("Horizontal right move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckHorizontalLeft(currentPiece,oppositePiece,row,col,applyTheMove=True):
    runFound = True
    #look for horizontal run <-
    numInRun = 0
    for i in range(col-1,-1,-1):
        if(gameGrid[row][i] == 0):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(gameGrid[row][i] == oppositePiece):
            numInRun = numInRun + 1
        if(gameGrid[row][i] == currentPiece):
            break  # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(col-1,col-1-numInRun,-1):
                gameGrid[row][i] = currentPiece
   
        if(DEBUG_ON):
            print("Horizontal left move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def CheckDiagonalDownRight(currentPiece,oppositePiece,row,col,applyTheMove = True):
    runFound = True
    #look for diagonal run DOWN RIGHT
    numInRun = 0
    rowNeedTo7 = 7 - row
    colNeededTo7 = 7 - col
    numOfLoops = min(rowNeedTo7,colNeededTo7)

    for i in range(1,numOfLoops):

        #print("checking",rowNeedTo7,colNeededTo7,numOfLoops,row+i,col+i)

        if(gameGrid[row + i][col + i] == 0):
            numInRun = 0  # if we get to a blank square then it cannot be run
            break
        if(gameGrid[row + i][col + i] == oppositePiece):
            numInRun = numInRun + 1
        if(gameGrid[row + i][col + i] == currentPiece):
            break # end of possible run
    else:
        numInRun = 0 # if we did not break then it isn't a run!

    if(numInRun == 0):
        runFound = False
    else:
        #Flip the run all over
        if(applyTheMove):
            for i in range(row+1,row+1+numInRun):
                for j in range(col+1,col+1+numInRun):
                    gameGrid[i][j] = currentPiece
        
        if(DEBUG_ON):
            print("diagonal right down move allowed? " + str(runFound))
            print("Run found : {} ".format(numInRun))

    return runFound

def MoveAllowed(somecol, somerow, applyTheMove):
    #Not all moves are valid!!
    #1 - Cannot move outside the grid
    #2 - Cannot add where a piece already is
    #3 - It must be a legal move that causes pieces to flip
    #      B W W W W b <--- HERE IS ALLOWED
    #
    #     resulting in this...
    #      B B B B B b <-- The grid after the "flipping"

    atLeastOneRunWasFound = False

    #who is playing this move?
    currentPiece, oppositePiece = GetCurrentPiece()

    if(gameGrid[somerow][somecol] == 1 or gameGrid[somerow][somecol] == 2):
        atLeastOneRunWasFound = False
        return atLeastOneRunWasFound  # piece is here...  DO NOT ALLOW
    else:
        runFound = CheckHorizontalRight(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True
        
        runFound = CheckHorizontalLeft(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True

        runFound = CheckVerticalDown(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True
       
        runFound = CheckVerticalUp(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True

        runFound = CheckDiagonalDownRight(currentPiece, oppositePiece, somerow, somecol, applyTheMove)
        if(runFound):
            atLeastOneRunWasFound = True

    return atLeastOneRunWasFound

def ShowNextMoves(gameOver):

    if(gameOver):
        return

    emptySquares = GetEmptySquares()
    
    atLeastOneMove = False

    for square in emptySquares:
        if(MoveAllowed(square[0],square[1],False)):
            if(alwaysShowNextMoves):
                atLeastOneMove = True
                pygame.draw.rect(surface, nextMoveColour, pygame.Rect(37+square[0]*GRID_SIZE_X,24+square[1]*GRID_SIZE_Y, GRID_SIZE_X, GRID_SIZE_Y),6)

    if(alwaysShowNextMoves and not atLeastOneMove):
        print("NO MORE MOVES...GAME OVER!!!")
        return False
    else:
        return True

def AddPieceToGrid(col,row):

    currentPiece,oppositePiece = GetCurrentPiece()

    #Only allow the move if the square is not full already...
    if(MoveAllowed(col,row,True)):
        gameGrid[row][col] = currentPiece
        pygame.mixer.Sound.play(clickSound)
        pygame.mixer.music.stop()
        SwapTurn()
        UpdateScores()
  
def HandleInput(running,gameOver):

    global alwaysShowNextMoves

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if(not gameOver):    
            #Toggle grid centre markers?
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    alwaysShowNextMoves = not alwaysShowNextMoves

            #Detect a mouse up
            if event.type == pygame.MOUSEBUTTONUP:

                somePos = pygame.mouse.get_pos()
                
                currentClickX = somePos[0]
                currentClickY = somePos[1]

                if(currentClickX < TOP_LEFT[0] or
                currentClickX > TOP_RIGHT[0] or
                currentClickY < TOP_LEFT[1] or
                currentClickY > BOT_RIGHT[1]):
                    if(DEBUG_ON):
                        print("NOT ON THE BOARD")
                    else:
                        pass
                else:
                    col,row = WhatSquareAreWeIn(somePos)
                    AddPieceToGrid(col,row)
                
    return running

##############################################################################
# MAIN
##############################################################################
pygame.init()

LoadImages(running)

gameOver = False

#game loop
while running:
    # Fill the scree with white color - "blank it"
    surface.fill(BACK_FILL_COLOUR)

    # Using blit to copy the background grid onto the blank screen
    surface.blit(backImage, (0, 0))

    surface.blit(turnIndicatorImage, (460, 0))

    surface.blit(scoreImage, (475, 364))

    surface.blit(p1ScoreSurface, (514,390))
    surface.blit(p2ScoreSurface, (514,416))

    DrawTurnMarker()

    if ShowNextMoves(gameOver) == False:
        gameOver = True
        #game over happened!!!

    running = HandleInput(running,gameOver)
   
    if(running):
        DrawTheCurrentGameGrid()

        if(gameOver):
            surface.blit(gameOverImage, (92, 144))
        
        pygame.display.flip()

pygame.quit()
