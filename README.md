# py-enigma
### An Engima machine implemented in pure Python 3

__Instantiate the Enigma class to use__

`Enigma.getDefaultEnigma()` creates an instance with reflector B and rotors III, II, and I

You can set the rotor types manually with:

  - `Enigma.setRightRotor(rotorType)`
  - `Enigma.setMiddleRotor(rotorType)`
  - `Enigma.setLeftRotor(rotorType)`

Rotor types supported are I, II, and III from the Wehrmacht Enigma I as well as IV and V from the M3 Army.
  
The refelector type can be set with `Enigma.setReflector(reflectorType). Wehrmacht refelctors B and C are supported.

Rotors start in A position. Rotor positions can be set using `Enigma.setRotorPositions(rotorPositions)` (takes a 3-tuple of letters).


Ring settings can be specified using `Enigma.setRingSettings(ringSettings)` (also takes a 3-tuple of letters).

Plugs can be added to the plugboard with `Enigma.plugboard.addPlug(letterA, letterB)`. This associates the two letters. You can remove this plug with `Enigma.plugboard.removePlug(plugLetter)`. Either letter of the plug will work.

Use `Enigma.encodeLetter(letter)` to encode a single letter. 

Use `Enigma.encodeMessage(message)` to encode a string (this will convert to lowercase and remove spaces).

#### Limitations
- Does not support more than 3 rotors (fix planned)
- Does not support multi-notched rotors
- Interactive Mode still in progress
