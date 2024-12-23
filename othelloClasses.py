class Person:
    def __init__(self,newName):
        self.name = newName
        
    def SayHello(self):
        print("Hello.  My name is {}.".format(self.name))
    
