elgamal
=======

Overview: elgamal is a python module that lets you encrypt and decrypt text using the ElGamal Cryptosystem.

Intended Use:
This program was created as an exercise in cryptography in one of my classes at the University of Kentucky.
I later turned it into a module.  I do not recommend you use it to protect any sensitive information.

Using elgamal:
Install elgamal by downloading elgamal.py and placing it in your module search path.

If you don't know your module search path, fire up a python console and run

	import sys
	sys.path

To use do

	import elgamal

To generate a public/private key pair do

	elgamal.generate_keys()
	#returns a dictionary {'privateKey': privateKeyObject, 'publicKey': publicKeyObject}
	
To encrypt a message do

	cipher = elgamal.encrypt(publicKey, "This is the message I want to encrypt")
	#returns a string
	
To decrypt the cipher text do

	plaintext = elgamal.decrypt(privateKey, cipher)
	#returns the message passed to elgamal.encrypt()

Compatibility: Python 3.4
