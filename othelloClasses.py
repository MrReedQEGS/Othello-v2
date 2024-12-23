class Person:
    def __init__(self,newName):
        self.name = newName
        
    def SayHello(self):
        print("Hello world!  My name is {}.  Pleased to meet you.".format(self.name))
    
