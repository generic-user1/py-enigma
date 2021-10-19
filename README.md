# py-enigma
An Engima machine implemented in pure Python 3

Instantiate the Enigma class to use

Enigma.getDefaultEnigma() creates an instance with reflector B and rotors III, II, and I all in A position
You can set the rotor types manually with
  Enigma.setRightRotor(rotorType)
  Enigma.setMiddleRotor(rotorType)
  Enigma.setLeftRotor(rotorType)
  
The refelector type can be set with Enigma.setReflector(reflectorType)

Rotor positions can be specified using Enigma.setRotorPositions(rotorPositions) 
(takes a 3-tuple of letters)

Ring settings can be specified using Enigma.setRingSettings(ringSettings)
(also takes a 3-tuple of letters)

Plugs can be added to the plugboard with Enigma.plugboard.addPlug(letterA, letterB)
This associates the two letters. You can remove this plug with Enigma.plugboard.removePlug(plugLetter)

Use Enigma.encodeLetter(letter) to encode a single letter

Use Enigma.encodeMessage(message) to encode a string 
(this will convert to lowercase and remove spaces)

Interactive mode coming soon (possibly)
