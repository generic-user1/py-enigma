#!/usr/bin/env python3

#an exception type to raise if a lettermap is invalid
#or if a LetterSwitcher is used without a lettermap
class LettermapException(Exception):
	pass


#class for an enigma element that can switch letters
#this can be subclassed into the plugboard
#as well as the different rotors
class LetterSwitcher():
	from string import ascii_lowercase
	
	alphabet = tuple(ascii_lowercase)
	
	#lettermaps are used to specify the specific letter switching
	#that a given LetterSwitcher should apply
	
	#a lettermap is a dictionary with 0 to 26 (inclusive) entries
	#each key is a lowercase letter (no special chars or space)
	#and each value is another lowercase letter
	
	#no repeats are allowed (in keys this is implicitly enforced,
	# but values are not so we check this manually)
	
	
	#returns a 'default' lettermap that
	#doesn't actually make any switches
	#note that an empty lettermap achieves the same effect
	#this method is to create a lettermap you can edit
	@classmethod
	def getDefaultLettermap(cls):
		
		return {letter: letter for letter in cls.alphabet}
	
	#returns True if the specified lettermap
	#is valid, False otherwise
	@classmethod
	def lettermapIsValid(cls, lettermap):
		
		#if the lettermap is not a dict, return False immediately
		if not isinstance(lettermap, dict):
			return False
		
		#init encounteredValues
		#this will be used to track which letters
		#have been encountered (so we can check for repeats)
		encounteredValues = []
		
		for key, val in lettermap.items():
			
			#if any key is not in the alphabet, return false
			if key not in cls.alphabet:
				return False
			
			#if any value is not in the alphabet, return false
			if val not in cls.alphabet:
				return False
			else:
				#if this value has been encountered before, return false
				if val in encounteredValues:
					return False
				else:
					encounteredValues.append(val)
		
		#if we got to this point, all keys and values must be valid
		#and there are no repeats
		#therefore, this lettermap is valid and we return true
		return True
	
	
	#sets the lettermap var of this instance to the specified lettermap
	#verifies the lettermap before doing so and throws LettermapException if 
	#the provided lettermap is invalid
	#also throws LettermapExeption if a lettermap is already defined
	def setLettermap(self, lettermap):
		
		if self.lettermap != None:
			raise LettermapException('Attempted to set lettermap, but this instance already had a defined lettermap')
		
		if self.lettermapIsValid(lettermap):
			self.lettermap = lettermap
		
		else:
			raise LettermapException("Provided lettermap is invalid: {}".format(repr(lettermap)))


	#init method, required by all classes
	def __init__(self, lettermap = None):
		
		#init lettermap instance variable
		self.lettermap = None
		
		#assign lettermap if one was passed
		if lettermap != None:
			self.setLettermap(lettermap)
	
	#raise a ValueError if letter is not a single, lowercase letter
	@classmethod		
	def validateLetter(self, letter):
		if len(letter) > 1 or letter not in self.alphabet:
			raise ValueError('Letter must be a single, lowercase letter')
	
	
	#takes a given letter and returns its corresponding letter
	#according to the internal lettermap of this LetterSwitcher
	def switchLetter(self, letter):
	
		#raise exception if letter is not a single lowercase letter
		self.validateLetter(letter)
		
		#raise exception if no lettermap is set
		if self.lettermap == None:
			raise LettermapException("Letter switching cannot be performed as there is no lettermap set")
		
		#if the lettermap contains an entry for this letter,
		#return the corresponding letter
		if letter in self.lettermap.keys():
			return self.lettermap[letter]
		
		#otherwise, just return the letter with no change
		else:
			return letter
		
		
	#using switchLetter, takes every letter in a sequence and switches it
	#then returns a string of every switched letter
	def switchSequence(self, letterSequence):
	
		#init switchedSequence
		switchedSequence = ""
		
		for letter in letterSequence:
			switchedSequence += self.switchLetter(letter)
			
		return switchedSequence
		
	
	#returns a copy of the internal lettermap
	def getLettermap(self):
		from copy import copy
		return copy(self.lettermap)
		
	
	#returns a lettermap that performs the exact opposite
	#switches as the current internal lettermap
	#(i.e. a decoder lettermap)
	def getDecoderLettermap(self):
		
		decoderLettermap = {}
		
		for srcLetter, dstLetter in self.lettermap.items():
			decoderLettermap[dstLetter] = srcLetter
		
		return decoderLettermap
		
	
	#returns another instance of LetterSwitcher
	#with an inverted lettermap (decoder lettermap)
	def getDecoderInstance(self):
		
		decoderMap = self.getDecoderLettermap()
		
		return LetterSwitcher(decoderMap)
		
	
	#switch the letter using the decoder version of this lettermap
	#also known as the 'reverse' version of this lettermap
	def switchLetterReverse(self, letter):
		
		#raise exception if letter is not a single lowercase letter
		self.validateLetter(letter)
		
		#raise exception if no lettermap is set
		if self.lettermap == None:
			raise LettermapException("Letter switching cannot be performed as there is no lettermap set")
		
		reversedLettermap = self.getDecoderLettermap()		
				
		#if the lettermap contains an entry for this letter,
		#return the corresponding letter
		if letter in reversedLettermap.keys():
			return reversedLettermap[letter]
		
		#otherwise, just return the letter with no change
		else:
			return letter
		
		
			
if __name__ == '__main__':
	
	#test LetterSwitcher
	
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
		'z': 'j'}
	
	encoder = LetterSwitcher(lettermap)
	
	decoder = encoder.getDecoderInstance()
	
	msg = 'helloworld'
	
	print(msg)
	
	encMsg = encoder.switchSequence(msg)
	
	print(encMsg)
	
	decMsg = decoder.switchSequence(encMsg)
	
	print(decMsg)
	
	
	
	
	
