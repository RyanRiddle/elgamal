elgamal
=======

Overview: Python implementation of the El Gamal crypto system.  Encrypts a given message and then decrypts it.
Works with Python 3.2.3.  It may work with other versions too, but I have not tested it.

Intended Use:
This program was created as an exercise in cryptography in one of my classes at the University of Kentucky.
It demonstrates the El Gamal Cryptosystem.  I do not recommend you use it to protect any sensitive information.

Instructions for Use:
Create a text file with the message you want to encrypt/decrypt.  You will be asked for the file name at runtime.
Run elgamal.py.  It will ask you to enter a key length.  Enter the number of bits you want to use for the key.  
Then it will ask you for a confidence level t.  Enter a number here.  The confidence level means that the numbers
the algorithm uses are 1-(2^-t) percent certain to be primes.  If you enter 250 for the number of bits and 32 for
t, the keys will be generated very quickly.  If you enter 500 for the number of bits and 32 for t, it will take about
3 minutes (on my machine) to generate the keys.  You can enter whatever numbers you like; those are just some benchmakrs.

Finally, it will ask you for the name of the file that contains the information you want to encrypt.  Enter the file name.
It will generate two key files K1 and K2 used for encrypting and decrypting the message.  Upon completing encryption,
it will create a file called "Cipher", containing the cipher-text.  Upon completing decryption, it will create a file
called "Plaintext", containing the plain-text.  

When I ran the program I encrypted/decrypted the following text.
"You can trust some of the people all of the time.  You can trust all the people some of the time.  But you can't trust
all of the people all of the time."
