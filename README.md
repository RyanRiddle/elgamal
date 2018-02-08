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
	
By default generate_keys() generates a key of 256 bits with probability 0.9999999997671694
(1-(2^-32)) that your key is prime.  You can alter the bitness of your keys and the certainty
that your key is prime by passing arguments n and t like this.

	elgamal.generate_keys(n, t)
	
where n is the number of bits you want your key to have and t means the probability that the
key is prime is 1-(2^-t).
	
To encrypt a message do

	cipher = elgamal.encrypt(publicKey, "This is the message I want to encrypt")
	#returns a string
	
To decrypt the cipher text do

	plaintext = elgamal.decrypt(privateKey, cipher)
	#returns the message passed to elgamal.encrypt()

Compatibility: Python 3.4.  Does not work in python 2.7!

License: MIT

Like this module?  Tell me what you like about it here https://goo.gl/forms/nA8gBcjPiwAoWzg32
