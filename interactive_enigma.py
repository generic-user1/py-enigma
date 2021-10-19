#!/usr/bin/env python3

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

        #automatically increase box width if message is larger than it
        messageLength = len(self.message)
        if messageLength >= (boxWidth - 4):
            boxWidth = messageLength + 4
            #if box width is an even number, add one to ensure it is odd
            if boxWidth % 2 != 1:
                boxWidth += 1
        
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
    #there may be a more os-independant way of doing this
    @staticmethod
    def getSingleLetter():
        import sys, os

        #use windows library if applicable
        if os.name == "nt":
            import msvcrt
            inputLetter == msvcrt.getch().decode().lower()
            #if input was a 'break' character (CTRL + C), raise a KeyboardInterrupt
            #there may be a better way to do this, but this is simple enough and works
            #on windows systems (unix-like systems raise KeyboardInterrupt upon input)
            if inputLetter == '\x03':
                raise KeyboardInterrupt
            else:
                return inputLetter
        else:
            #use unix terminal control library if not on windows
            import termios

            #get file descriptor for stdin stream
            fileDescriptor = sys.stdin.fileno()

            #save a copy of the stream config so we can reset it later
            oldConfig = termios.tcgetattr(fileDescriptor)
            
            #get a copy of the stream config to modify
            newConfig = termios.tcgetattr(fileDescriptor)
            
            #set the canonical mode flag (ICANON) to false in the new stream config
            #this allows input to be read immediately rather than waiting for ENTER
            #also set the ECHO flag to false 
            #(this prevents auto-printing of the typed char)
            newConfig[3] = newConfig[3] & ~termios.ICANON & ~termios.ECHO


            

            
            try:
                #set new config
                #the TCSANOW option forces this change to happen immediately
                termios.tcsetattr(fileDescriptor, termios.TCSANOW, newConfig)
                
                #read a single character
                charRead = sys.stdin.read(1)
            #before returning (and even if an error occurs),
            #reset the configuration on the stdin stream
            finally:
                #the TCSAFLUSH flag waits to make this change until 
                #after the read character has been transmitted
                #this also 'flushes' any additional characters, if they exist
                termios.tcsetattr(fileDescriptor, termios.TCSAFLUSH, oldConfig)

            #return the single character
            return charRead.lower()

        

    #displays the box representation of the machine
    #and accepts one letter of user input
    #returns None if successful and the offending input if ValueError is thrown
    def acceptInput(self):

        print(self.getBoxStr())
        newLetter = self.getSingleLetter()
        try:
            self.encodeLetter(newLetter)
        except ValueError:
            return newLetter
        else:
            return None
        

    def inputLoop(self):
        
        #initialize offendingValue 
        offendingValue = None

        #accept input forever (until keyboard interrupt)
        while True:
            
            self.clearScreen()
            #if a backspace was typed, remove the last char from the message (and encrypted counterpart)
            #then decrement the rotors
            #\b is used on windows, \x7f is used on unix-like systems
            if (offendingValue == '\b' or offendingValue == '\x7f') and len(self.message) > 0:
                self.message = self.message[:-1]
                self.encodedMessage = self.encodedMessage[:-1]
                self.decrementRotors()
            #show error message if input was invalid
            elif offendingValue != None:
                print(f"Invalid Input: {repr(offendingValue)}")

            #handle KeyboardInterrupt exceptions
            try:
                offendingValue  = self.acceptInput()
            except KeyboardInterrupt:
                print(self.getBoxStr())
                break

    #print the valid rotor types
    @staticmethod
    def printRotorTypes():
        print("Supported Rotor Types:")
        for typeName in map(lambda x: x.name, RotorType):
            print(f" {typeName}")

    #return a set of rotor instances along with their names
    def getRotorsWithNames(self):
        rotors = self.getRotors()

        rotorsWithNames = (
            'Left Rotor', rotors[0],
            'Middle Rotor', rotors[1],
            'Right Rotor', rotors[2]
            )
        return rotorsWithNames

    #prompt user for rotor type input
    def inputRotorTypes(self):

        useDefaultRotorTypes = None
        while useDefaultRotorTypes == None:
            print("Use Default Rotor Types? (y/n): ", end="")
            response = self.getSingleLetter()
            #print response char as getSingleLetter does not echo input
            #this also prints a newline, which is important because the previous line
            #does not end with one
            print(response)
            if response != "y" and response != "n":
                print(f"Invalid Input: {repr(response)}. Please type y or n\n")
            else:
                useDefaultRotorTypes = response == 'y'

        #set default rotor types if user input the letter y
        if useDefaultRotorTypes:
            self.setRightRotor(RotorType.I)
            self.setMiddleRotor(RotorType.II)
            self.setLeftRotor(RotorType.III)
        
        else:
            #otherwise, prompt for a rotorType for each rotor
            rotors = (
                ('Right Rotor', self.setRightRotor),
                ('Middle Rotor', self.setMiddleRotor),
                ('Left Rotor', self.setLeftRotor)
                )
                
            for rotorName, rotorSetMethod in rotors:
                choice = None
                while choice == None:
                    #use the normal input function to allow for multiple characters 
                    response = input(f"Specify Rotor Type for {rotorName} (o for options): ")
                    #print(response)

                    if response == 'o':
                        self.printRotorTypes()
                    else:
                        #try converting input to a rotor type
                        try:
                            selectedRotorType = RotorType[response.upper()]
                        except KeyError:
                            #if a KeyError is raised, input is not a valid rotor type
                            print(f"Invalid Input: {repr(response)}. Please input a valid Rotor Type.")
                            self.printRotorTypes()
                        else:
                            choice = selectedRotorType

                #set selected rotor type
                rotorSetMethod(choice)
                        
                    
    #prompt user to input ring settings
    def inputRingSettings(self):
        
        #ask to use default ringSettings
        useDefaultRingSettings = None
        while useDefaultRingSettings == None:
            print("Use Default Ring Settings? (y/n): ", end="")
            response = self.getSingleLetter()
            #print response char as getSingleLetter does not echo input
            #this also prints a newline, which is important because the previous line
            #does not end with one
            print(response)
            if response != "y" and response != "n":
                print(f"Invalid Input: {repr(response)}. Please type y or n\n")
            else:
                useDefaultRingSettings = response == 'y'
        
        #if default ring settings selected, do not prompt for ring setting input
        #ring settings default to A-01, this is defined within the Rotor class
        if not useDefaultRingSettings:

            #for each rotor, prompt user for a ring setting
            rotors = self.getRotorsWithNames()
            for rotorName, rotorInstance in rotors:
                choice = None
                while choice == None:
                    print(f"Specify ring setting for {rotorName}: ", end="")
                    response = self.getSingleLetter()
                    print(response)
                    
                    #try validating input as a ring setting
                    try:
                        Rotor.validateRingSetting(response)
                    except ValueError:
                        #if a ValueError is raised, response is not a valid ring setting
                        print(f"""Invalid Input: {repr(response)}. 
Please input the ring setting as the letter that aligns with the marked contact on the rotor. 
(single letter, a to z)""")
                    else:
                        choice = response

                #set selected rotor type
                rotorInstance.setRingSetting(choice)

    
    #prompt user to input plug settings
    #TODO: fix repeated code in inputPlugs
    def inputPlugs(self):
        
        while True:

            print("Input a letter to start a plug, or ! to stop adding plugs")
            response = self.getSingleLetter()
            print(response)

            #if response was the quit char, return to exit loop
            if response == '!':
                print(response)
                return
            else:
                
                #validate letter, print message if invalid
                try:
                    Rotor.validateLetter(response)
                except ValueError:
                    print(f"Invalid Input: {repr(response)}")
                else:
                    #if letter is valid, check if it is already present in
                    #the plugs. getLettermap().keys() is used because it returns
                    #every letter that is a member of any plug (unlike getPlugs().keys())
                    pluggedLetters = self.plugboard.getLettermap().keys()
                    
                    if response in pluggedLetters:
                        print(f"{response.upper()} already has a plug in it")

                    else:
                        letterA = response

                        letterB = None
                        #repeat the same process for letterB, but within a loop
                        #so that invalid input doesn't reset, resulting in typing letterA again
                        while letterB == None:
                            
                            print("Input second letter: ", end = "")
                            response = self.getSingleLetter()
                            print(response)

                            try:
                                Rotor.validateLetter(response)
                            except ValueError:
                                print(f"Invalid Input: {repr(response)}")
                            else:
                    
                                pluggedLetters = self.plugboard.getLettermap().keys()
                    
                                if response in pluggedLetters:
                                    print(f"{response.upper()} already has a plug in it")

                                else: 
                                    letterB = response
                        
                        self.plugboard.addPlug(letterA, letterB)
                        print(f'Plugged {letterA} into {letterB}')







            

    

if __name__ == '__main__':

    enigma = InteractiveEnigma().getDefaultEnigma()
    enigma.inputRotorTypes()
    enigma.inputRingSettings()
    enigma.inputPlugs()

    enigma.inputLoop()
