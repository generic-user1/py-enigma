#!/usr/bin/env python3

from os import stat
from enigma import Enigma
from reflector import ReflectorType
from rotor import Rotor, RotorType
from letterswitcher import LetterSwitcher

#a class that provides useful methods for an interactive Enigma machine
class InteractiveEnigma(Enigma):
    
    #override constructor to create instance variables unique to
    #InteractiveEnigma
    def __init__(self):

        #message is what the user has typed in so far
        self.message = ""

        #encodedMessage is what the Enigma has output so far
        self.encodedMessage = ""

        #run the standard Enigma constructor
        super().__init__()

    #override encodeLetter to add letter to both message and plugboard
    def encodeLetter(self, letter):
        
        #validate letter
        Rotor.validateLetter(letter)

        #if letter is valid, add it to the message
        self.message += letter
        
        #encode the letter
        encodedLetter = super().encodeLetter(letter)
        
        #add the encoded letter to the encodedMessage
        self.encodedMessage += encodedLetter

        #return the letter
        return encodedLetter


    #override getDefaultEnigma to use an InteractiveEnigma instance
    #rather than a standard Enigma instance
    @staticmethod
    def getDefaultEnigma(preexistingEnigma = None):
        if preexistingEnigma == None:
            enigma = InteractiveEnigma()
        elif isinstance(preexistingEnigma, InteractiveEnigma):
            enigma = preexistingEnigma
        else:
            raise TypeError("preexistingEnigma must be an instance of InteractiveEnigma")
        return Enigma.getDefaultEnigma(enigma)

    #define a method to clear the screen
    #this *should* work regardless of OS
    @staticmethod
    def clearScreen():
        import os
        #if OS is windows, use the 'cls' command
        if os.name == 'nt':
            os.system('cls')
        
        else:
            #if OS is not windows, it is probably unix-like
            #therefore, use the 'clear' command
            os.system('clear')

        
    
    #returns the rotor positions as a nicely formatted string
    #setting padding will insert spaces to the left of each line
    #to pad the message and visually "push" it to the right
    #borderChar puts a wider horizontal border around the message
    #informed by the padding setting
    def getPrettyRotorPositions(self, padding = 0, borderChar = ""):

        #get the rotor positions as uppercase letters
        leftPos = self.leftRotor.getRotorPosition().upper()
        midPos = self.middleRotor.getRotorPosition().upper()
        rightPos = self.rightRotor.getRotorPosition().upper()

        #determine the padding strings
        if padding <= 0:
            #if padding is 0 (or negative), just set padding to an empty string
            leftPaddingStr = ""
            rightPaddingStr = ""
        else:
            #if border char is not set,
            #set left padding to just spaces and right padding to empty string
            #this is because right padding is not needed when no border is set
            if borderChar == "":
                leftPaddingStr = " " * padding
                rightPaddingStr = ""
            else:
                #if border char is set, both padding strings need to be set
                leftPaddingStr = borderChar + " " * (padding - 1)
                rightPaddingStr = " " * (padding - 1) + borderChar
            
        
            

        #print the rotor positions in a nice format
        rotorPosStr = f"""{leftPaddingStr}###########{rightPaddingStr}
{leftPaddingStr}#{leftPos:^3}{midPos:^3}{rightPos:^3}#{rightPaddingStr}
{leftPaddingStr}###########{rightPaddingStr}"""
        return rotorPosStr

    #prints the rotor positions in a nice format
    def printRotorPositions(self):
        print(self.getPrettyRotorPositions())

    
    #generates a string that displays
    #the current rotor positions, followed by the message
    #so far, followed by the endcoded result
    #all wrapped in a box of some charachter
    def getBoxStr(self, boxWidth = 25, boxChar = "#"):

        
        #find an offset that will center rotorPosStr, knowing it is 11 chars wide
        #the offset to center an item is:
        #  half the width of the container minus half the width of the item
        #we want half the width of 11 (which is a number between 5 and 6)
        #in this case we round down, meaning we use 5
        rotorPosStrOffset = (int(boxWidth/2)) - 5

        #get the rotor position string with the calculated offset and border char
        rotorPosStr = self.getPrettyRotorPositions(rotorPosStrOffset, boxChar)

        #add border chars to message and encodedMessage
        borderedMessage = f'{boxChar}{self.message:^{boxWidth - 2}}{boxChar}'
        borderedEncodedMessage = f'{boxChar}{self.encodedMessage:^{boxWidth - 2}}{boxChar}'
        
        #create a series of lines to visually associate message and encodedMessage
        connectingLines = "|" * len(self.message)
        borderedConnectingLines = f'{boxChar}{connectingLines:^{boxWidth - 2}}{boxChar}'
       
        #create the horizontal border string
        horizontalBorder = boxChar * boxWidth

        #create the vertical border string (for empty rows)
        verticalBorder = f'{boxChar}{boxChar:>{boxWidth - 1}}'

        boxStr = f"""{horizontalBorder}
{rotorPosStr}
{verticalBorder}
{borderedMessage}
{borderedConnectingLines}
{borderedEncodedMessage}
{verticalBorder}
{horizontalBorder}"""
        return boxStr

    #like the builtin input() but doesn't wait for enter; just returns the first char typed
    #thanks, author of
    # https://docs.python.org/2.7/faq/library.html#how-do-i-get-a-single-keypress-at-a-time
    #this is a hack and should be replaced with something better
    #TODO: replace getSingleLetter with a better solution
    @staticmethod
    def getSingleLetter():
        import sys, termios, fcntl, os
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:
            while 1:
                try:
                    c = sys.stdin.read(1)
                    if c != '':
                        return c
                except IOError: 
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

        

    #clears the screen, displays the box representation of the machine,
    #and accepts one letter of user input
    def acceptInput(self):
        
        self.clearScreen()
        print(self.getBoxStr())
        newLetter = self.getSingleLetter()
        self.encodeLetter(newLetter)

    def inputLoop(self):
        while True:
            try:
                self.acceptInput()
            except ValueError:
                print("Invalid Input!")


    

if __name__ == '__main__':

    enigma = InteractiveEnigma().getDefaultEnigma()
    #enigma.plugboard.addPlug('a','f')
    #enigma.plugboard.addPlug('z','q')
    
    enigma.inputLoop()

    #enigma.printMachineState()
    #enigma.encodeMessage("helloworld")
    #print(enigma.getBoxStr())
