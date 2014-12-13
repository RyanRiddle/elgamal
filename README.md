elgamal
=======

Overview: elgamal is a python module that lets you encrypt and decrypt text using the ElGamal Cryptosystem.

Intended Use:
This program was created as an exercise in cryptography in one of my classes at the University of Kentucky.
I later turned it into a module.  I do not recommend you use it to protect any sensitive information.

Using elgamal:
Install elgamal by download elgamal.py and placing it in your module search path.

If you don't know your module search path, fire up a python console and run

	import sys
	sys.path

To use do

	import elgamal

The three functions you need to use elgamal are
	1) elgamal.generate_keys()
	2) elgamal.encrypt()
	3) elgamal.decrypt()

elgamal.generate_keys() returns a dictionary containing a public key and a private key.
By default generate_keys() generates keys using 256 bit primes with a certainty level of 32.
Certainity level 32 means the probability that there is a 1-(2^-32) chance that the primes
are actually prime.  You can adjust these values.  For example, elgamal.generate_keys(1024, 10)
would generate keys using 1024 bit primes with 1-(2^-10) probability that they are primes.

Warning: generating large primes is slow.  On my machine it took ~3 minutes to generate a 512 bit prime.

elgamal.encrypt() takes two arguments, the public key and a text string.  It returns cipher text.

elgamal.decrypt() takes two arguments, the private key and the cipher text.  It returns the plaintext.

Compatibility: Python 3.4

Issues:  It seems that encrypting strings with more than 32 characters is not working.  It was working
before i converted this project to a library, so I'm sure it's a small mistake that I can fix quickly.
