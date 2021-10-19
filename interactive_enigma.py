#!/usr/bin/env python3

from enigma import Enigma
from reflector import ReflectorType
from rotor import RotorType
from letterswitcher import LetterSwitcher

#a class that provides useful methods for an interactive Enigma machine
class InteractiveEnigma(Enigma):
    
    #override getDefaultEnigma to use an InteractiveEnigma instance
    #rather than a standard Enigma instance
    @classmethod
    def getDefaultEnigma(cls, preexistingEnigma = None):
        if preexistingEnigma == None:
            enigma = InteractiveEnigma()
        elif isinstance(preexistingEnigma, InteractiveEnigma):
            enigma = preexistingEnigma
        else:
            raise TypeError("preexistingEnigma must be an instance of InteractiveEnigma")
        return super().getDefaultEnigma(enigma)

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
                'ringSetting': LetterSwitcher.alphabet[rotor.ringSetting],
                'rotorPosition': rotor.getRotorPosition()
                }
            rotorDicts.append(newRotorDict)

        #assemble rotor
        
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
        
        
        


if __name__ == '__main__':

    enigma = InteractiveEnigma().getDefaultEnigma()
    
    print(enigma.getMachineState())
