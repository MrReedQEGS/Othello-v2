class Person:
    def __init__(self,newName):
        self.name = newName
        
    def SayHello(self):
        print("Hello world!".format(self.name))
    
