#!/usr/bin/env python3
from letterswitcher import LetterSwitcher, LettermapException

class Plugboard(LetterSwitcher):

	#allow for re-assigning lettermap after assignment
	def setLettermap(self, lettermap):
		
		if not self.lettermapIsValid(lettermap):
			raise LettermapException("Provided lettermap is invalid: {}".format(repr(lettermap)))
		else:
			self.lettermap = lettermap

	#override constructor to automatically set the default lettermap
	#this allows a plugboard to be used right after instantiation with no further calls
	def __init__(self):
		lettermap = self.getDefaultLettermap()
		super().__init__(lettermap)


	#TODO: create easy methods for 'plugging' or 'unplugging'
		
if __name__ == '__main__':
	
	#test Plugboard
	
	lettermap = {
		'a': 'n', 
		'b': 'h', 
		'c': 'a', 
		'd': 'l', 
		'e': 'g', 
		'f': 'p', 
		'g': 'u', 
		'h': 'z', 
		'i': 'q', 
		'j': 'i', 
		'k': 'v', 
		'l': 'r', 
		'm': 's', 
		'n': 'd', 
		'o': 'e', 
		'p': 't', 
		'q': 'x', 
		'r': 'y', 
		's': 'w', 
		't': 'o', 
		'u': 'b', 
		'v': 'm', 
		'w': 'c', 
		'x': 'k', 
		'y': 'f', 
		'z': 'j'
	}
		
	
	encoder = Plugboard(Plugboard.getDefaultLettermap())
	encoder.setLettermap(lettermap)
	decoder = encoder.getDecoderInstance()
	
	msg = 'teststring'
	
	print(msg)
	
	encMsg = encoder.switchSequence(msg)
	
	print(encMsg)
	
	decMsg = decoder.switchSequence(encMsg)
	
	print(decMsg)
