#!/usr/bin/env python3
from letterswitcher import LetterSwitcher, LettermapException

class Plugboard(LetterSwitcher):

    #override lettermapIsValid to enforce pairing
    def lettermapIsValid(self, lettermap):
        
        #do all the standard checks first
        isValid = super().lettermapIsValid(lettermap)
        if not isValid:
            return False
        
        #for every key value pair, check if there is a corresponding
        #pair that maps the opposite way
        for key, val in lettermap.items():
            if val not in lettermap.keys():
                return False
            elif lettermap[val] != key:
                return False
        return True

    #override constructor to automatically set to an empty lettermap
    #this allows a plugboard to be used right after instantiation with no further calls
    def __init__(self):
        lettermap = {}
        super().__init__(lettermap)


    #'plug' a letter into another letter; this will swap the 
    #two letters out for each other on both input and output of the enigma
    def addPlug(self, plugA, plugB):

        #validate both inputs as letters
        self.validateLetter(plugA)
        self.validateLetter(plugB)

        #reject plug if there is already a plug in that spot
        if plugA in self.lettermap.keys():
            raise ValueError("Socket {} already has a plug".format(plugA))
        elif plugB in self.lettermap.keys():
            raise ValueError("Socket {} already has a plug".format(plugB))
        
        #create plug by adding two entries to the lettermap,
        #so that each letter is associated both ways
        self.lettermap[plugA] = plugB
        self.lettermap[plugB] = plugA

    #remove a plug that already exists in the lettermap
    #plugLetter can be either of the two letters
    def removePlug(self, pluggedLetter):

        if pluggedLetter not in self.lettermap.keys():
            raise ValueError("Socket {} does not have a plug".format(pluggedLetter))
        
        #get the other letter plugged to this one
        assocLetter = self.lettermap[pluggedLetter]

        #remove both entries related to this plug
        del self.lettermap[pluggedLetter]
        del self.lettermap[assocLetter]

    #method to return all the plugs in this plugboard as a dictionary
    #this is different from getLettermap because it only includes each plug 
    #once (where the lettermap contains mappings for both directions)
    def getPlugs(self):
        
        outputDict = {}

        #iterate through lettermap
        for key, val in self.lettermap.items():
            
            #determine which keys are already in the output
            existingKeys = outputDict.keys()
            
            #if this mapping doesn't exist in the output dictionary
            #(in either direction), add it to the output
            if key not in existingKeys and val not in existingKeys:
                outputDict[key] = val
        
        return outputDict

        

    #override switchLetterReverse to be an alias of switchLetter
    #because of the letter pairing rule; the reverse of a plugboard's 
    #lettermap is just the same lettermap again, so a special method isn't needed
    def switchLetterReverse(self, letter):
        return self.switchLetter(letter)
            
        
if __name__ == '__main__':
    
    #test Plugboard
    
    
    encoder = Plugboard()

    encoder.addPlug("t", "p")
    encoder.addPlug("s",'f')
    encoder.removePlug("p")
    
    msg = 'teststring'
    
    print(msg)
    
    encMsg = encoder.switchSequence(msg)
    
    print(encMsg)
    
    decMsg = encoder.switchSequence(encMsg)
    
    print(decMsg)
