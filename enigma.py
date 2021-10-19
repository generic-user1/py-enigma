#!/usr/bin/env python3

from typing import Type
from rotor import Rotor, RotorType
from reflector import Reflector, ReflectorType
from plugboard import Plugboard



#define an exception type to be thrown when 
#attempting to use an Enigma that has not been
#fully set up (i.e. is missing rotors or a reflector)
class EnigmaException(Exception):
    pass


#a class that simulates an Enigma machine
#currently supports 3-rotor configurations, though machines
#did exist that supported 4 rotors (possibly more, I need to do more research on this topic)
#TODO: support more than 3 rotors
class Enigma():

    def __init__(self):

        #init instance variables (rotors, reflector, and plugboard)

        #each rotor is stored in its own variable
        #this will have to be changed for 4-rotor (or more)
        #configurations
        self.rightRotor = None
        self.middleRotor = None
        self.leftRotor = None

        self.reflector = None

        #the plugboard can be initialized with a default plugboard
        #as plugboard configuration can be changed during the machine's operation
        #(i.e. Plugboard supports changing its lettermap after it is initially set)
        self.plugboard = Plugboard()

    #define methods for setting up each configurable piece of the machine
    def setRightRotor(self, rotorType):
        self.rightRotor = Rotor(rotorType)

    def setMiddleRotor(self, rotorType):
        self.middleRotor = Rotor(rotorType)

    def setLeftRotor(self, rotorType):
        self.leftRotor = Rotor(rotorType)

    def setReflector(self, reflectorType):
        self.reflector = Reflector(reflectorType)

    #method to return all rotor instances in a tuple
    #(leftRotor, middleRotor, rightRotor)
    #this is to save work later if more than three rotors are supported
    #in the future
    def getRotors(self):
        return (
            self.leftRotor,
            self.middleRotor,
            self.rightRotor
        )

    #raise an EnigmaException if this Engima instance
    #does not yet have all of its rotors and reflector set 
    def validateEnigmaSetup(self):
        if self.reflector == None:
            raise EnigmaException("Enigma cannot be used before reflector is set using Engigma.setReflector(reflectorType)")
        else:
            missingRotor = None
            if self.rightRotor == None:
                missingRotor = 'Right Rotor'
                method = 'setRightRotor'
            elif self.middleRotor == None:
                missingRotor = 'Middle Rotor'
                method = 'setMiddleRotor'
            elif self.leftRotor == None:
                missingRotor = 'Left Rotor'
                method = 'setLeftRotor'

            if missingRotor != None:
                raise EnigmaException("Enigma cannot be used before {} is set using Enigma.{}(rotorType)".format(missingRotor, method))

    #set all three rotor positions
    #accepts a 3-tuple of either single lowercase letters or integers from 0 to 25
    #tuple should be in the structure (left, middle, right)
    def setRotorPositions(self, rotorPositions):
        
        #validate that rotorPositions is a 3 tuple
        if (not isinstance(rotorPositions, tuple)) or len(rotorPositions) != 3:
            raise ValueError('Rotor positions must be a 3-tuple of the form (left, middle, right)')
        
        #set the rotor positions
        #setRotorPosition will raise a ValueError if the input is invalid
        self.leftRotor.setRotorPosition(rotorPositions[0])
        self.middleRotor.setRotorPosition(rotorPositions[1])
        self.rightRotor.setRotorPosition(rotorPositions[2])

    #returns the rotors' current positions as a 3 tuple
    #(left, middle, right)
    def getRotorPositions(self):
        rotorInstances = self.getRotors()
        rotorPositions = [rotor.getRotorPosition() for rotor in rotorInstances]
        return tuple(rotorPositions)

    #set all three ring settings
    #uses the same format as setRotorPositions
    def setRingSettings(self, ringSettings):
        
        #get rotor instances
        rotorInstances = self.getRotors()

        #validate that ringSettings is a 3 tuple
        if (not isinstance(ringSettings, tuple)) or len(ringSettings) != len(rotorInstances):
            raise ValueError('Ring settings must be a 3-tuple of the form (left, middle, right)')

        #set the ring settings
        #setRingSetting will raise a ValueError if the input is invalid
        for ringSetting, rotor in zip(ringSettings, rotorInstances):
            rotor.setRingSetting(ringSetting)

    #define a method that returns a pre-configured Enigma (mostly for testing purposes)
    #supports modifying a pre-existing Enigma instance as well as creating a new instance
    @staticmethod
    def getDefaultEnigma(preexistingEnigma = None):
        if preexistingEnigma == None:
            enigma = Enigma()
        elif isinstance(preexistingEnigma, Enigma):
            enigma = preexistingEnigma
        else:
            raise TypeError("preexistingEnigma must be an Enigma instance")
        enigma.setReflector(ReflectorType.B)
        enigma.setRightRotor(RotorType.I)
        enigma.setMiddleRotor(RotorType.II)
        enigma.setLeftRotor(RotorType.III)
        return enigma

    #define a method that returns an Enigma that is pre-configured to test double-step
    @staticmethod
    def getDoubleStepEnigma(preexistingEnigma = None):
        enigma = Enigma.getDefaultEnigma(preexistingEnigma)
        enigma.setRotorPositions(('k','d','o'))
        return enigma


    #increments the rotors 
    #uses appropriate rules for each rotor 
    #(details within method definition)
    def incrementRotors(self):
        
        #determine if the middle rotor should increment
        #due to the right rotor's position
        middleRotates = self.rightRotor.notchInPosition()
        
        
        #increment the right rotor,
        #as the right rotor rotates with every keypress
        self.rightRotor.incrementRotor()
        
        #determine if the left rotor should increment
        #due to the middle rotor's position
        leftRotates = self.middleRotor.notchInPosition()
        
        #note: due to the ratchet/pawl system used in the Engima,
        #there is a quirk of the rotation of the middle rotor:
        #it will rotate BOTH when the right rotor's notch is in position,
        #AND when its own notch is in position; this is called "double step",
        #so called because the middle rotor will rotate on two keypresses in a row
        
        #this behavior is simulated by rotating the middle rotor either if 
        #the left rotor's notch is in position, or if its own notch is in position
        if leftRotates:
            #the left rotor only rotates if the middle rotor's notch is in position
            self.leftRotor.incrementRotor()
            self.middleRotor.incrementRotor()
        elif middleRotates:
            self.middleRotor.incrementRotor()


    #decrements the rotors
    #uses the same rules as incrementRotors, but in reverse
    def decrementRotors(self):

        middleRotated = self.rightRotor.notchInReversePosition()

        self.rightRotor.decementRotor()

        leftRotated = self.middleRotor.notchInReversePosition()

        if leftRotated:
            self.leftRotor.decementRotor()
            self.middleRotor.decementRotor()
        elif middleRotated:
            self.middleRotor.decementRotor()   
    
    #takes a letter as input, runs it through the Enigma process, and returns the result
    #increments rotors as needed
    def encodeLetter(self, letter):

        #validate the letter before doing anything else
        Rotor.validateLetter(letter)

        #increment the rotors
        self.incrementRotors()

        #run the letter through the plugboard
        letter = self.plugboard.switchLetter(letter)

        #run the letter through each rotor from right to left
        letter = self.rightRotor.switchLetter(letter)
        letter = self.middleRotor.switchLetter(letter)
        letter = self.leftRotor.switchLetter(letter)
        
        #run the letter through the reflector
        letter = self.reflector.switchLetter(letter)
        
        #run the letter back through the rotors,
        #this time from left to right
        letter = self.leftRotor.switchLetterReverse(letter)
        letter = self.middleRotor.switchLetterReverse(letter)
        letter = self.rightRotor.switchLetterReverse(letter)
        
        #run the letter back through the plugboard
        letter = self.plugboard.switchLetter(letter)
        
        

        #return the letter
        return letter

    #reset rotors to AAA position
    def resetRotors(self):
        self.leftRotor.setRotorPosition('a')
        self.middleRotor.setRotorPosition('a')
        self.rightRotor.setRotorPosition('a')
    
    #encodes a message (must be string or other iterable of single charachters)
    #removes spaces and converts to lowercase automatically
    #due to the design of the Enigma (both real and by extention this simulation), 
    #this method can be used both to encode a message AND decode a message, assuming
    #the configurations of the encoder and decoder machines are identical
    def encodeMessage(self, message):
        
        encodedMessage = ""
        
        for letter in message:
            #skip spaces
            if letter == ' ':
                continue
            
            encodedLetter = self.encodeLetter(letter.lower())
            encodedMessage += encodedLetter

        return encodedMessage

    
    #define a method that will return the machine's state as a dictionary
    #this includes the reflector type, rotor types, 
    #rotor positions, ring settings, and plugboard settings
    def getMachineState(self):
        
        #gather information about the machine's state
        
        #get reflector type
        reflectorType = ReflectorType(self.reflector.reflectorType)
        
        #get all three rotors
        rotors = self.getRotors()

        #for each rotor, get its rotorType, ring setting, and rotor position
        rotorDicts = []
        for rotor in rotors:
            newRotorDict = {
                'rotorType': RotorType(rotor.rotorType),
                'ringSetting': Rotor.alphabet[rotor.ringSetting],
                'rotorPosition': rotor.getRotorPosition()
                }
            rotorDicts.append(newRotorDict)
        
        #get all the plugs in the plugboard
        plugs = self.plugboard.getPlugs()

        #assemble dictionary for output
        outputDict = {
            'reflectorType': reflectorType,
            'plugs': plugs,
            'leftRotor':rotorDicts[0],
            'middleRotor':rotorDicts[1],
            'rightRotor':rotorDicts[2]
            }
        return outputDict

    #given a ring setting as a letter or integer,
    #return the (what I assume to be) official name of that setting
    @staticmethod
    def getRingSettingName(ringSetting):
        
        #validate the input and get it as an integer, if it wasn't already
        ringSettingInt = Rotor.validateRingSetting(ringSetting)

        #translate that integer to a letter
        ringSettingLetter = Rotor.alphabet[ringSettingInt].upper()

        #add 1 to the ring setting integer (so setting A outputs as A-01 rather than A-00)
        ringSettingInt += 1

        #fill in format string and return
        return f'{ringSettingLetter}-{ringSettingInt:02d}'

    #get the machine's state, then print it in a human-readable format
    def printMachineState(self):

        #get the machine's state
        state = self.getMachineState()

        #print the reflector/rotor types 
        reflectorType = state['reflectorType']
        leftRotorType = state['leftRotor']['rotorType']
        midRotorType = state['middleRotor']['rotorType']
        rightRotorType = state['rightRotor']['rotorType']

        rotorConfigStr = f"""REFLECTOR       LEFT ROTOR      MID ROTOR       RIGHT ROTOR
{reflectorType.name:16}{leftRotorType.name:16}{midRotorType.name:16}{rightRotorType.name:16}
"""
        print(rotorConfigStr)

        #print the ring setting of each ring
        leftRingSetting = self.getRingSettingName(state['leftRotor']['ringSetting'])
        midRingSetting = self.getRingSettingName(state['middleRotor']['ringSetting'])
        rightRingSetting = self.getRingSettingName(state['rightRotor']['ringSetting'])

        ringSettingStr = f"""RING SETTINGS:
                {leftRingSetting:16}{midRingSetting:16}{rightRingSetting:16}
"""
        print(ringSettingStr)

        #print the rotor positions
        leftRotorPosition = (state['leftRotor']['rotorPosition']).upper()
        midRotorPosition = (state['middleRotor']['rotorPosition']).upper()
        rightRotorPosition = (state['rightRotor']['rotorPosition']).upper()
        
        rotorPosStr = f"""ROTOR POSITIONS:
                {leftRotorPosition:16}{midRotorPosition:16}{rightRotorPosition:16}
"""
        print(rotorPosStr)

        #print plugs, if there are any
        if len(state['plugs']):
            print("PLUGS:")
            for letterA, letterB in state['plugs'].items():
                print(f"{letterA.upper():} plugged to {letterB.upper():}")
        else:
            print("NO PLUGS")
        #print empty line to visually seperate the printed state from
        #whatever is printed next
        print("")
    

    

if __name__ == "__main__":
    
    #test Enigma

    enigma = Enigma.getDoubleStepEnigma()

    enigma.plugboard.addPlug("h","z")
    
    rotorPos = enigma.getRotorPositions()

    enigma.setRingSettings(('a','a','z'))

    enigma.printMachineState()

    msg = 'hello world'
    print(msg)

    #encode a message
    encMsg = enigma.encodeMessage(msg)
    print(encMsg)
    #expected output for a 'double step test' enigma (rotor positions K D O)
    #where ring setting on right rotor is 25 (Z-26)
    #and plugboard has H plugged to Z:
    #dqhheprgzu

    #decode that message by resetting the machine and using it as a decoder
    enigma.setRotorPositions(rotorPos)
    decMsg = enigma.encodeMessage(encMsg)
    print(decMsg)
    #expected output: helloworld
