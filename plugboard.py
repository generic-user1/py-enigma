#!/usr/bin/env python3
from letterswitcher import LetterSwitcher, LettermapException

class Plugboard(LetterSwitcher):

    #override lettermapIsValid to enforce pairing
    def lettermapIsValid(self, lettermap):
        
        isValid = super().lettermapIsValid(lettermap)

        if not isValid:
            return False
        else:
            for key, val in lettermap.items():
                if val not in lettermap.keys():
                    return False
                elif lettermap[val] != key:
                    return False
            return True

    #override constructor to automatically set the default lettermap
    #this allows a plugboard to be used right after instantiation with no further calls
    def __init__(self, lettermap = None):
        if lettermap == None:
            lettermap = self.getDefaultLettermap()
        super().__init__(lettermap)


    #TODO: create easy methods for 'plugging' or 'unplugging'
        
if __name__ == '__main__':
    
    #test Plugboard
    
    
    encoder = Plugboard()
    decoder = encoder.getDecoderInstance()
    
    msg = 'teststring'
    
    print(msg)
    
    encMsg = encoder.switchSequence(msg)
    
    print(encMsg)
    
    decMsg = decoder.switchSequence(encMsg)
    
    print(decMsg)
