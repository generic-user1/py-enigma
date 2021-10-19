#!/usr/bin/env python3

from letterswitcher import LetterSwitcher
from enum import Enum

#define an enumeration for the different types of Reflector 
#that are currently supported 
#TODO: support thin reflectors
class ReflectorType(Enum):
    B = 0
    C = 1


#class for an Enigma reflector
#reflectors are used to 'reflect' the signal
#back through the rotors and towards the output display of the machine
#they do not rotate, and map letters in pairs (so if A maps to F, then F must map to A)
#fun fact: this letter pairing is what's responsible for no letter ever mapping to itself
#and this weakness is a large part of how Turing's team broke Enigma during the war
class Reflector(LetterSwitcher):

    #define lettermaps for the various supported reflector types
    #these are accessed by index - which index points to which
    #lettermap/reflector type is defined in the ReflectorType enum
    _reflectorLettermaps = (
        {'a': 'y', 'b': 'r', 'c': 'u', 'd': 'h', 'e': 'q', 'f': 's', 'g': 'l', 'h': 'd', 'i': 'p', 'j': 'x', 'k': 'n', 'l': 'g', 'm': 'o', 'n': 'k', 'o': 'm', 'p': 'i', 'q': 'e', 'r': 'b', 's': 'f', 't': 'z', 'u': 'c', 'v': 'w', 'w': 'v', 'x': 'j', 'y': 'a', 'z': 't'},
        {'a': 'f', 'b': 'v', 'c': 'p', 'd': 'j', 'e': 'i', 'f': 'a', 'g': 'o', 'h': 'y', 'i': 'e', 'j': 'd', 'k': 'r', 'l': 'z', 'm': 'x', 'n': 'w', 'o': 'g', 'p': 'c', 'q': 't', 'r': 'k', 's': 'u', 't': 'q', 'u': 's', 'v': 'b', 'w': 'n', 'x': 'm', 'y': 'h', 'z': 'l'}
        )

    #validate a given ReflectorType and return it as an integer
    #raise an exception (ValueError) if input is invalid
    @staticmethod
    def validateReflectorType(reflectorType):
        if isinstance(reflectorType, ReflectorType):
            return reflectorType.value
        else:
            if not (isinstance(reflectorType, int) 
                and reflectorType >= 0
                and reflectorType <= 1):
                raise ValueError("reflectorType must be of type ReflectorType or an integer from 0 to 1")
            else:
                return reflectorType

    
    #return the lettermap for a specified ReflectorType
    @classmethod
    def getReflectorLettermap(cls, reflectorType):

        #get reflector type as an int (and validate)
        reflectorType = cls.validateReflectorType(reflectorType)

        return cls._reflectorLettermaps[reflectorType]

    #override constructor to require a reflectorType and automatically
    #set the correct lettermap
    def __init__(self, reflectorType):
        
        #keep track of the reflector type
        #this is done so creation of identical reflectors is easy
        self.reflectorType = self.validateReflectorType(reflectorType)

        lettermap = self.getReflectorLettermap(reflectorType)

        super().__init__(lettermap)

    
    #override methods related to the 'decoder' lettermap (a.k.a. reverse lettermap)
    #this is done because, for reflectors (which always swap letters in pairs),
    #the reverse of their lettermap is just the same lettermap
    
    def getDecoderLettermap(self):
        return self.getLettermap()

    def getDecoderInstance(self):
        return Reflector(self.reflectorType)

    def switchLetterReverse(self, letter):
        return self.switchLetter(letter)


if __name__ == '__main__':

    #test Reflector

    encoder = Reflector(ReflectorType.B)

    print(encoder.switchLetter('a'))
    print(encoder.switchLetter('y'))