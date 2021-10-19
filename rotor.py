#!/usr/bin/env python3

from letterswitcher import LetterSwitcher, LettermapException

from enum import Enum

#define an enumeration for the 
#different types of rotors supported
#TODO: support more rotors
class RotorType(Enum):
    I = 0
    II = 1
    III = 2
    IV = 3
    V = 4

#class for an engima rotor
#details on the workings of the real-life enigma rotors can be found at
# http://users.telenet.be/d.rijmenants/en/enigmatech.htm
#if you are curious
class Rotor(LetterSwitcher):
    
    #define letter maps for different rotor types
    #rotorLetterMaps is accessed by index,
    #you can see which index translates to which
    #rotor type using the RotorType enum
    __rotorLetterMaps = (
            {'a': 'e', 'b': 'k', 'c': 'm', 'd': 'f', 'e': 'l', 'f': 'g', 'g': 'd', 'h': 'q', 'i': 'v', 'j': 'z', 'k': 'n', 'l': 't', 'm': 'o', 'n': 'w', 'o': 'y', 'p': 'h', 'q': 'x', 'r': 'u', 's': 's', 't': 'p', 'u': 'a', 'v': 'i', 'w': 'b', 'x': 'r', 'y': 'c', 'z': 'j'},
            {'a': 'a', 'b': 'j', 'c': 'd', 'd': 'k', 'e': 's', 'f': 'i', 'g': 'r', 'h': 'u', 'i': 'x', 'j': 'b', 'k': 'l', 'l': 'h', 'm': 'w', 'n': 't', 'o': 'm', 'p': 'c', 'q': 'q', 'r': 'g', 's': 'z', 't': 'n', 'u': 'p', 'v': 'y', 'w': 'f', 'x': 'v', 'y': 'o', 'z': 'e'},
            {'a': 'b', 'b': 'd', 'c': 'f', 'd': 'h', 'e': 'j', 'f': 'l', 'g': 'c', 'h': 'p', 'i': 'r', 'j': 't', 'k': 'x', 'l': 'v', 'm': 'z', 'n': 'n', 'o': 'y', 'p': 'e', 'q': 'i', 'r': 'w', 's': 'g', 't': 'a', 'u': 'k', 'v': 'm', 'w': 'u', 'x': 's', 'y': 'q', 'z': 'o'},
            {'a': 'e', 'b': 's', 'c': 'o', 'd': 'v', 'e': 'p', 'f': 'z', 'g': 'j', 'h': 'a', 'i': 'y', 'j': 'q', 'k': 'u', 'l': 'i', 'm': 'r', 'n': 'h', 'o': 'x', 'p': 'l', 'q': 'n', 'r': 'f', 's': 't', 't': 'g', 'u': 'k', 'v': 'd', 'w': 'c', 'x': 'm', 'y': 'w', 'z': 'b'},
            {'a': 'v', 'b': 'z', 'c': 'b', 'd': 'r', 'e': 'g', 'f': 'i', 'g': 't', 'h': 'y', 'i': 'u', 'j': 'p', 'k': 's', 'l': 'd', 'm': 'n', 'n': 'h', 'o': 'l', 'p': 'x', 'q': 'a', 'r': 'w', 's': 'm', 't': 'j', 'u': 'q', 'v': 'o', 'w': 'f', 'x': 'e', 'y': 'c', 'z': 'k'}
        )
        
    
        
    #define the rotor notch positions for each rotor
    #each of these is defined as the index of the letter 
    #that displays in the window when the notch is 
    #lined up to rotate the next rotor with the next keypress
    #(note: this is not actually where the physical notch is on a real Engima rotor
    # storing notch positions this way is just easier to implement
    # however, the output for a given rotor configuration should still be the same)
    __rotorNotchPositions = (
        16,
        4,
        21,
        9,
        25
        )
        
    #validate a rotorType and return it as an integer
    #raise an exception if input is invalid
    @staticmethod
    def validateRotorType(rotorType):
        if isinstance(rotorType, RotorType):
            rotorType = rotorType.value
        else:
            if not (isinstance(rotorType, int) 
                and rotorType <= 4 
                and rotorType >= 0):
                
                #raise an exception if rotor type is out of bounds
                raise ValueError("rotorType must be of type RotorType or an integer from 0 to 4")
        return rotorType
    
        
    #returns the pre-defined rotor lettermaps for the different supported rotors
    @classmethod
    def getRotorLettermap(cls, rotorType):
    
        #get rotor type as an integer (and validate)
        rotorType = cls.validateRotorType(rotorType)
        
        return cls.__rotorLetterMaps[rotorType]
    
                
    #returns the pre-defined rotor notch positions for the
    #different supported rotors
    @classmethod
    def getRotorNotchPos(cls, rotorType):
    
        #get rotor type as an integer (and validate)
        rotorType = cls.validateRotorType(rotorType)
        
        return cls.__rotorNotchPositions[rotorType]
                    
    
    #lettermaps for rotors must contain exactly 26 entries,
    #one for each letter
    @classmethod
    def lettermapIsValid(cls, lettermap):
        if len(lettermap) != 26:
            return False
        else:
            #the remaining checks can be fulfilled by the
            #validator from LetterSwitcher
            return super().lettermapIsValid(lettermap)
            
    
    def __init__(self, rotorType):

        #useful for debugging
        self.rotorType = rotorType
        
        #set the lettermap var to be passed to the
        #super constructor method
        #calling getRotorLettermap will throw a ValueError
        #if rotorType is invalid
        lettermap = self.getRotorLettermap(rotorType)
        
        #set the notch position of this rotor to the predefined notch position 
        #for this particular rotor type
        self.notchPosition = self.getRotorNotchPos(rotorType)
        #note: notch position being stored as a single value disallows
        #the use of rotors with multiple notches
        #multi-notched rotors were created, but are not supported at this time
        #TODO: support multi-notched rotors

        
        #used to keep track of the rotor's rotation,
        #rotorPosition maps 0 - 25 to the letters a to z
        #that you would see through the viewing window on an actual Enigma
        self.rotorPosition = 0
        #this will be used as an offset to access the lettermap

        #initialize ring setting (sometimes called ringstellung)
        #this affects the 
        self.ringSetting = 0
        
        #run super constructor (this sets the lettermap)
        super().__init__(lettermap)


    #given a letter, uses the rotorPosition instance var
    #to return which letter the specified 
    #letter will enter the 'rotor' (lettermap) as
    def getRotatedLetter(self, letter):
        
        #raise exception if letter is not valid
        self.validateLetter(letter)
        
        
        indexInAlphabet = self.alphabet.index(letter)
        
        #'rotate' by rotorPosition by adding it to the 
        #letter index and modulo the result by 26
        #to guarentee a value between 0 and 25
        rotatedIndex = (indexInAlphabet + self.rotorPosition) % 26
        
        return self.alphabet[rotatedIndex]
        
    #rotate the output of this rotor using rotorPosition
    #this is done to account for the entire rotor rotating
    #getRotatedLetter is used to account for the rotation of input,
    #whereas this is used to account for the rotation of output
    def _getOutputLetter(self, letter):
        
        letterIndex = self.alphabet.index(letter)
        outputIndex = (letterIndex - (self.rotorPosition + self.ringSetting)) % 26
        return self.alphabet[outputIndex]
        
    
    #increment rotorPosition
    #keeps it within the range 0 - 25 inclusive
    #this is technically unneeded as getRotatedLetter uses a modulo
    #but I figured it would make a bit more sense
    def incrementRotor(self):
        
        self.rotorPosition += 1
        #Normally I would use >= 26, but doing it this way
        #ensures that if someone manually sets the rotor position to something
        #outside this range, the rotor will continue incrementing as normal instead of
        #mysteriously "incrementing" from 252 to 0
        if self.rotorPosition == 26:
            self.rotorPosition = 0
    
    #returns the letter you would see through the viewer
    #if you looked at this current position
    #that is, the rotor's position (accounting for ring setting)
    def getRotorPosition(self):
        letterIndex = (self.rotorPosition + self.ringSetting) % 26
        return self.alphabet[letterIndex]

    #validates a ring setting input and returns it as an integer
    #raises a ValueError if input is invalid
    @classmethod
    def validateRingSetting(cls, ringSetting):
        
        #if ring setting is an integer, verify it is within bounds (0-25)
        #and then return it
        if isinstance(ringSetting, int) and ringSetting >= 0 and ringSetting <= 25:
            return ringSetting
        #if ring setting is a string, verify it is a single letter, then convert it to
        #an integer and return the result
        elif isinstance(ringSetting, str) and len(ringSetting) == 1 and ringSetting in cls.alphabet:
            return cls.alphabet.index(ringSetting)
        else:
            raise ValueError("Ring setting must be a single lowercase letter or integer from 0 to 25 (inclusive)")

    #alias of validateRingSetting
    #these inputs are validated using the same procedure;
    #this method exists in case that ever changes in the future
    @classmethod
    def validateRotorPosition(cls, rotorPosition):
        try:
            return cls.validateRingSetting(rotorPosition)
        except ValueError:
            #use a custom error message if invalid
            raise ValueError("Rotor position must be a single lowercase letter or integer from 0 to 25 inclusive")
        

    #sets the rotor's rotation such that the specified letter appears in the window
    #better than setting rotorPosition directly because it accounts for ring setting
    def setRotorPosition(self, rotorPosition):
       
        #validate rotorPosition and get it as an integer
        rotorPositionIndex = self.validateRotorPosition(rotorPosition)

        self.rotorPosition = (rotorPositionIndex - self.ringSetting) % 26

    #set the ring setting to the specified value
    #raises a ValueError if the input is invalid
    #also adjusts the rotor position to keep the window letter constant
    def setRingSetting(self, ringSetting):
        #note rotor position
        rotorPos = self.rotorPosition
        #set the ring setting after validating it
        self.ringSetting = self.validateRingSetting(ringSetting)
        #set the rotor position such that the window letter is kept the same
        #this is because on real enigma machines, the rotor's position was set based on the
        #window letter, not the actual rotation of the rotor
        self.setRotorPosition(rotorPos)
    
    #returns true if the notch is in position
    #to increment the next rotor (the rotor to the left) on this rotor's next turn
    #the notch is attached to the alphabet ring and thus the ring setting influences
    #its position
    def notchInPosition(self):
        return (self.rotorPosition + self.ringSetting) % 26 == self.notchPosition
    
    #applies ring setting to a letter
    #given the letter coming out of the rotor's internal wiring,
    #returns the letter of the output pin accounting for shifting due to ring setting
    def applyRing(self, letter):
        
        #convert the letter to an integer
        letterIndex = self.alphabet.index(letter)

        #apply the ring setting
        letterIndex = (letterIndex + self.ringSetting) % 26

        #return the resulting letter
        return self.alphabet[letterIndex]

    
    #override switchLetter to include rotation
    def switchLetter(self, letter):
        
        #apply rotation to input
        letter = self.getRotatedLetter(letter)
        
        #swap letter according to internal wiring
        letter = super().switchLetter(letter)
        
        #apply ring setting rotation to output
        letter = self.applyRing(letter)

        #apply full rotor rotation to output and return
        return self._getOutputLetter(letter)

    #override switchLetterReverse to include rotation
    #this is important as signals travel through all 3 rotors forward AND back
    #on each keypress
    def switchLetterReverse(self, letter):

        
        letter = self.getRotatedLetter(letter)

        letter = super().switchLetterReverse(letter)

        letter = self._getOutputLetter(letter)

        letter = self.applyRing(letter)

        return letter
        
        
    
    #disable the switchSeqence method for rotors, 
    # as it shouldn't be used due to an inability
    # to check when the next rotor should turn
    #TODO: fix Rotor.switchSequence so that it can be used
    def switchSequence(self):
        raise NotImplementedError("Rotor.switchSequence is not implemented")
    

if __name__ == '__main__':

    #test Rotor
    
    encode = Rotor(RotorType.I)
    
    print('switchLetter (expected e):',encode.switchLetter('a'))
    print('switchLetterReverse (expected a):',encode.switchLetterReverse('e'))

    encode.setRingSetting(1)
    encode.setRotorPosition('a')
    print("setting ring to B-02")
    print("setting rotor to A")
    
    switchedLetter = encode.switchLetter('a')
    print('switch letter (expected k):', switchedLetter)
    
    switchedLetter = encode.switchLetterReverse('k')
    print('switch letter reverse (expected a):', switchedLetter)

    encode.setRingSetting(5)
    encode.setRotorPosition('y')
    print("setting ring to F-06")
    print("setting rotor to Y")
    
    switchedLetter = encode.switchLetter('a')
    print('switch letter (expected w):', switchedLetter)
    
    switchedLetter = encode.switchLetterReverse('w')
    print('switch letter reverse (expected a):', switchedLetter)
    