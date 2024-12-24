class Person():
    def __init__(self,newName):
        self.name = newName
    
    def SayHello(self):
        print("Hello my name is {}".format(self.name))

#Keeping track of game time in a separate thread
from threading import Timer,Thread,Event
class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

class MyGameGrid():
    def __init__(self,newRows,newCols,newListOfAllowedCellItems,newPosOfBlankItem):
        self.rows = newRows
        self.cols = newCols
        self.listOfAllowedCellItems = newListOfAllowedCellItems
        self.posOfBlankItem = newPosOfBlankItem

        #now make the blank grid
        blankThing = self.listOfAllowedCellItems[self.posOfBlankItem]
        self.theGrid = []
        for i in range(self.rows):
            newRow = []
            for j in range(self.cols):
                newRow.append(blankThing)
        
            self.theGrid.append(newRow)

    def GetGridItem(self,theCoord):
        #The x and y are coords starting at zero of a position on the game grid that we want
        #
        #  -------------------------
        #  | 0,0 | 1,0 | 2,0 | 3,0 |
        #  -------------------------
        #  | 0,1 | 1,1 | 2,1 | 3,1 |
        #  -------------------------
        #  | 0,2 | 1,2 | 2,2 | 3,2 |
        #  -------------------------
        #
        #  etc.

        #The problem is that the game grid is stored in a list of lists(rows), so:
        #
        # x is col!
        # y is the row!
        #
        # We need to access items using theGrid[y][x]

        x = theCoord[0]
        y = theCoord[1]
        return self.theGrid[y][x]

    def SetGridItem(self,theCoord,newItem):
        x = theCoord[0]
        y = theCoord[1]
        self.theGrid[y][x] = newItem 

    def DebugPrintSelf(self):
        for row in self.theGrid:
            print(row)