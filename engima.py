#!/usr/bin/env python3

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
        self.rightmostRotor = None
        self.middleRotor = None
        self.leftmostRotor = None

        self.reflector = None

        #the plugboard can be initialized with a default plugboard
        #as plugboard configuration can be changed during the machine's operation
        #(i.e. Plugboard supports changing its lettermap after it is initially set)
        self.plugboard = Plugboard()

    #define methods for setting up each configurable piece of the machine
    def setRightRotor(self, rotorType):
        self.rightmostRotor = Rotor(rotorType)

    def setMiddleRotor(self, rotorType):
        self.middleRotor = Rotor(rotorType)

    def setLeftRotor(self, rotorType):
        self.leftmostRotor = Rotor(rotorType)

    def setReflector(self, reflectorType):
        self.reflector = Reflector(reflectorType)

    #raise an EnigmaException if this Engima instance
    #does not yet have all of its rotors and reflector set 
    def validateEnigmaSetup(self):
        if self.reflector == None:
            raise EnigmaException("Enigma cannot be used before reflector is set using Engigma.setReflector(reflectorType)")
        else:
            missingRotor = None
            if self.rightmostRotor == None:
                missingRotor = 'Rightmost Rotor'
                method = 'setRightRotor'
            elif self.middleRotor == None:
                missingRotor = 'Middle Rotor'
                method = 'setMiddleRotor'
            elif self.leftmostRotor == None:
                missingRotor = 'Leftmost Rotor'
                method = 'setLeftRotor'

            if missingRotor != None:
                raise EnigmaException("Enigma cannot be used before {} is set using Enigma.{}(rotorType)".format(missingRotor, method))

    #define a method that returns a pre-configured Enigma (mostly for testing purposes)
    @staticmethod
    def getDefaultEnigma():
        enigma = Enigma()
        enigma.setReflector(ReflectorType.B)
        enigma.setRightRotor(RotorType.I)
        enigma.setMiddleRotor(RotorType.II)
        enigma.setLeftRotor(RotorType.III)
        return enigma

    
    #takes a letter as input, runs it through the Enigma process, and returns the result
    #increments rotors as needed
    def encodeLetter(self, letter):

        #validate the letter before doing anything else
        self.validateLetter(letter)

        #run the letter through the plugboard
        plugboardedLetter = self.plugboard.switchLetter(letter)

        #run the letter through each rotor
        #TODO: finish encodeLetter
        raise NotImplementedError("Encode Letter is unfinished at this time")

    

    

if __name__ == "__main__":
    
    enigma = Enigma.getDefaultEnigma()



    

