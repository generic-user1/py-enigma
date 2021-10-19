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

    #define a method that returns a pre-configured Enigma (mostly for testing purposes)
    @staticmethod
    def getDefaultEnigma():
        enigma = Enigma()
        enigma.setReflector(ReflectorType.B)
        enigma.setRightRotor(RotorType.I)
        enigma.setMiddleRotor(RotorType.II)
        enigma.setLeftRotor(RotorType.III)
        return enigma

    #increments the rotors 
    #uses appropriate rules for each rotor 
    #(details within method definition)
    def incrementRotors(self):
        
        #determine if the middle rotor should increment
        #due to the right rotor's position
        middleRotates = self.leftRotor.notchInPosition()
        
        
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
        
    #return the current rotor positions as a 3-tuple
    #(left, middle, right)
    def getWindowLetters(self):
        return (
            self.leftRotor.getWindowLetter(),
            self.middleRotor.getWindowLetter(),
            self.rightRotor.getWindowLetter()
            )

    #reset rotors to AAA position
    def resetRotors(self):
        self.leftRotor.rotorPosition = 0
        self.middleRotor.rotorPosition = 0
        self.rightRotor.rotorPosition = 0
    
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
    

    

if __name__ == "__main__":
    
    enigma = Enigma.getDefaultEnigma()
    
    #test Enigma
    msg = 'hello world'
    print(msg)

    #encode a message
    encMsg = enigma.encodeMessage(msg)
    print(encMsg)
    #expected output for default enigma: mfnczbbfzm

    #decode that message by resetting the machine and using it as a decoder
    enigma.resetRotors()
    decMsg = enigma.encodeMessage(encMsg)
    print(decMsg)
    #expected output: helloworld



    

