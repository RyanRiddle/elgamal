#Implementation of the ElGamal Cryptosystem
#Author: Ryan Riddle (ryan.riddle@uky.edu)
#Date of Completion: April 20, 2012

#DESCRIPTION AND IMPLEMENTATION
#
#This python program implements the ElGamal cryptosystem.  The program is capable of both
#encrypting and decrypting a message.  At execution the user will be prompted for three things:
#       1) a number n which specifies the length of the prime to be generated
#       2) a number t which specifies the desired confidence that the generated prime
#       is actually prime
#       3) the name of a file that contains the message he wishes to encrypt and decrypt
#
#After the user has provided the necessary information the program will generate a pair
#of keys (K1, K2) used for encryption and decryption.  K1 is the public key and contains
#three integers (p, g, h).
#       p is an n bit prime.  The probability that p is actually prime is 2^-t
#       g is a primitive root mod p
#       h = g^x mod p; x is randomly chosen, 1 <= x < p
#h is computed using fast modular exponentiation, implemented as modexp( base, exp, modulus )
#K2 is the private key and contains three integers (p, g, x) that are described above.
#K1 and K2 are written to files named K1 and K2.
#
#Next the program encodes the bytes of the message into integers z[i] < p.
#The module for this is named encode() and is described further where it is implemented.
#
#After the message has been encoded into integers, the integers are encrypted and written
#to a file, Ciphertext.  The encryption procedure is implemented in encrypt().  It works
#as follows:
#       Each corresponds to a pair (c, d) that is written to Ciphertext.
#       For each integer z[i]:
#               c[i] = g^y (mod p).  d[i] = z[i]h^y (mod p)
#               where y is chosen randomly, 0 <= y < p
#
#The decryption module decrypt() reads each pair of integers from Ciphertext and converts
#them back to encoded integers.  It is implemented as follows:
#       s = c[i]^x (mod p)
#       z[i] = d[i]*s^-1 (mod p)
#
#The decode() module takes the integers produced from the decryption module and separates
#them into the bytes received in the initial message.  These bytes are written to the file
#Plaintext.
#
#HURDLES CLEARED DURING IMPLEMENTATION
#
#modular exponentiation
#The first problem I encountered was in implementing the fast modular exponentiator, modexp().
#At first it did not terminate when given a negative number.  I quickly figured out that when
#performing integer division on negative numbers, the result is rounded down rather than toward
#zero.
#
#finding primitive roots
#Understanding the definition of primitive roots was not enough to find one efficiently.  I had
#search the web to understand how primitive roots can be found.  Wikipedia helped me understand
#I needed to test potential primitive roots multiplicative order.  The algorithm found at
#http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
#is the one I implemented.
#
#finding large prime numbers
#After implementing the Solovay-Strassen primality test I found it was difficult to compute 100
#bit primes even with probability 1/2.  I met with Professor Klapper to discuss this problem and he
#suggested I quit running the program on UK's shared "multilab" and I speed up my Jacobi algorithm
#by using branches to find powers of -1 rather than actually exponentiating them.  After doing this
#I was able to find 500 bit primes in about 15 minutes.
#
#finding prime numbers with confidence > 2
#I found it took a long time to test primes with a large number of bits with confidence greater than
#two.  I went to the web again to read over the description of the Solovay-Strassen primality test
#and realized jacobi(a, n) should be congruent to modexp(a, (n-1)/2, n) mod n.  I had only been checking
#that they were equal.  Before making this change I tried to find a 200 bit prime with confidence 100
#and gave up after an hour and a half.  After this change I was able to succeed after a couple of minutes.
#
#getting encoding and decoding to work
#I knew that encoding and decoding were implemented correctly because I could encode and decode a message
#and get the message I had started with.  But I did not receive the right message when I encrypted and
#decrypted it, despite having checked my encrypt and decrypt modules many times.  I fixed this by raising
#s to p-2 instead of -1 in the decryption function.


import random
import math

#globals
#n-number of bits in prime
#t-confidence p is prime
#message_file - name of file containing message to encrypt and decrypt
n = 0
t = 0
message_file = ""

# computes the greatest common denominator of a and b.  assumes a > b
def gcd( a, b ):
        if b != 0:
                return gcd( b, a % b )
        #a is returned if b == 0
        return a        
        
#computes base^exp mod modulus
def modexp( base, exp, modulus ):
        if exp == 0:
                return 1

        temp = exp
        #if temp is negative, force round toward 0
        if temp < 0:
                temp = math.ceil( temp / 2 )
        else:
        #integer division
                temp = temp // 2 
        
        z = modexp( base, temp, modulus )

        #if exp is even
        if exp % 2 == 0:
                return z*z % modulus
        #if exp is odd
        else:
                return base*z*z % modulus

#solovay-strassen primality test.  tests if num is prime
def SS( num ):
        #ensure confidence of t
        for i in range(t):
                #choose random a between 1 and n-2
                a = random.randint( 1, num-1 )
                
                #if a is not relatively prime to n, n is composite
                if gcd( a, num ) > 1:
                        return False
                
                #declares n prime if jacobi(a, n) is congruent to a^((n-1)/2) mod n
                if not jacobi( a, num ) % num == modexp ( a, (num-1)//2, num ):
                        return False

        #if there have been t iterations without failure, num is believed to be prime
        return True

#computes the jacobi symbol of a, n
def jacobi( a, n ):
        if a == 0:
                if n == 1:
                        return 1
                else:
                        return 0
        #property 1 of the jacobi symbol
        elif a == -1:
                if n % 2 == 0:
                        return 1
                else:
                        return -1
        #if a == 1, jacobi symbol is equal to 1
        elif a == 1:
                return 1
        #property 4 of the jacobi symbol
        elif a == 2:
                if n % 8 == 1 or n % 8 == 7:
                        return 1
                elif n % 8 == 3 or n % 8 == 5:
                        return -1
        #property of the jacobi symbol:
        #if a = b mod n, jacobi(a, n) = jacobi( b, n )
        elif a >= n:
                return jacobi( a%n, n)
        elif a%2 == 0:
                return jacobi(2, n)*jacobi(a//2, n)
        #law of quadratic reciprocity
        #if a is odd and a is coprime to n
        else:
                if a % 4 == 3 and n%4 == 3:
                        return -1 * jacobi( n, a)
                else:
                        return jacobi(n, a )
        

#finds a primitive root for prime p
#this function was implemented from the algorithm described here:
#http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
def find_primitive_root( p ):
        if p == 2:
                return 1
        #the prime divisors of p-1 are 2 and (p-1)/2 because
        #p = 2x + 1 where x is a prime
        p1 = 2
        p2 = (p-1) // p1
        
        #test random g's until one is found that is a primitive root mod p
        while( 1 ):
                g = random.randint( 2, p-1 )
                #g is a primitive root if for all prime factors of p-1, p[i]
                #g^((p-1)/p[i]) (mod p) is not congruent to 1
                if not (modexp( g, (p-1)//p1, p ) == 1):
                        if not modexp( g, (p-1)//p2, p ) == 1:
                                return g

#find n bit prime
def find_prime():
        #keep testing until one is found
        while(1):
                #generate potential prime randomly
                p = random.randint( 2**(n-2), 2**(n-1) )
                #make sure it is odd
                while( p % 2 == 0 ):
                        p = random.randint(2**(n-2),2**(n-1))

                #keep doing this if the solovay-strassen test fails
                while( not SS(p) ):
                        p = random.randint( 2**(n-2), 2**(n-1) )
                        while( p % 2 == 0 ):
                                p = random.randint(2**(n-2), 2**(n-1))

                #if p is prime compute p = 2*p + 1
                #if p is prime, we have succeeded; else, start over
                p = p * 2 + 1
                if SS(p):
                        return p
        
#encodes bytes to integers mod p.  reads bytes from file
def encode():
        f = open( message_file, 'r' )
        #convert to the ascii integer value of the character
        data = ord(f.read(1))
        byte_array = []
        #put data into an array.  each element is a byte
        while( data ):
                byte_array.append( data )
                data = f.read(1)
                #add data to byte array until an empty string is read (EOF)
                if data == '':
                        break
                data = ord(data)                
        f.close()

        #z is the array of integers mod p
        z = []

        #each encoded integer will be a linear combination of k message bytes
        #k must be the number of bits in the prime divided by 8 because each
        #message byte is 8 bits long
        k = n//8

        #j marks the jth encoded integer
        #j will start at 0 but make it -k because j will be incremented during first iteration 
        j = -1 * k
        #num is the summation of the message bytes
        num = 0
        #i iterates through byte array
        for i in range( len(byte_array) ):
                #if i is divisible by k, start a new encoded integer
                if i % k == 0:
                        j += k
                        num = 0
                        z.append(0)
                #add the byte multiplied by 2 raised to a multiple of 8
                z[j//k] += byte_array[i]*(2**(8*(i%k)))

        #example
                #if n = 24, k = n / 8 = 3
                #z[0] = (summation from i = 0 to i = k)m[i]*(2^(8*i))
                #where m[i] is the ith message byte

        #return array of encoded integers
        return z

#decodes integers to the original message bytes
def decode():
        #get encoded integers from file
        f = open( 'Plaintext', 'r' )
        data = f.readline()
        #will contain the integers in the file
        z = []
        #while data is read
        while( data ):
                #if not empty string (EOF), convert the line to an integer, add it to z
                if not data == '':
                        data = int(data)
                        z.append(data)
                #read another line
                data = f.readline()
        f.close()

        #decode
        #bytes array will hold the decoded original message bytes
        bytes_array = []

        #same deal as in the encode function.
        #each encoded integer is a linear combination of k message bytes
        #k must be the number of bits in the prime divided by 8 because each
        #message byte is 8 bits long
        k = n//8

        #num is an integer in list z
        for num in z:
                #get the k message bytes from the integer, i counts from 0 to k-1
                for i in range(k):
                        #temporary integer
                        temp = num
                        #j goes from i+1 to k-1
                        for j in range(i+1, k):
                                #get remainder from dividing integer by 2^(8*j)
                                temp = temp % (2**(8*j))
                        #message byte representing a letter is equal to temp divided by 2^(8*i)
                        letter = temp // (2**(8*i))
                        #add the message byte letter to the byte array
                        bytes_array.append(letter)
                        #subtract the letter multiplied by the power of two from num so
                        #so the next message byte can be found
                        num = num - (letter*(2**(8*i)))

        #example
        #if "You" were encoded.
        #Letter        #ASCII
        #Y              89
        #o              111
        #u              117
        #if the encoded integer is 7696217 and k = 3
        #m[0] = 7696217 % 256 % 65536 / (2^(8*0)) = 89 = 'Y'
        #7696217 - (89 * (2^(8*0))) = 7696128
        #m[1] = 7696128 % 65536 / (2^(8*1)) = 111 = 'o'
        #7696128 - (111 * (2^(8*1))) = 7667712
        #m[2] = 7667712 / (2^(8*2)) = 117 = 'u'
                        
        #write each message byte as a character to file Plaintext
        f = open( 'Plaintext', 'w' )
        #i is a message byte
        for i in bytes_array:
                f.write( chr(i) )
        f.close()
                                

#generates public key K1 (p, g, h) and private key K2 (p, g, x)
#writes K1 to file 'K1' and K2 to file 'K2'
def generate_keys():
        #p is the prime
        #g is the primitve root
        #x is random in (0, p-1) inclusive
        #h = g ^ x mod p
        p = find_prime()
        g = find_primitive_root( p )
        x = random.randint( 1, p )
        h = modexp( g, x, p )

        keys = [[p, g, h], [p, g, x]]
        f = open( 'K1', 'w' )
        for i in keys[0]:
                f.write( str(i) + "\n" )
        f.close
        f = open( 'K2', 'w' )
        for i in keys[1]:
                f.write( str(i) + "\n" )
        f.close()


#sets the globals n, t, and message file from user input
def get_global_params():
        global n
        n = int( input( "Enter a bit length n " ) )
        global t
        t = int (input( "Enter a confidence level t " ) )
        global message_file
        message_file = input("Enter the name of a file containing the message you wish to encrypt ")

        
#encrypts a list of integers z using the public key K1
def encrypt( z ):
        #get p, g, h of K1
        f = open( 'K1', 'r' )
        p = int(f.readline())
        g = int(f.readline())
        h = int(f.readline())
        f.close()

        #encrypt
        #cipher_pairs list will hold pairs (c, d) corresponding to each integer in z
        cipher_pairs = []
        #i is an integer in z
        for i in z:
                #pick random y from (0, p-1) inclusive
                y = random.randint( 0, p )
                #c = g^y mod p
                c = modexp( g, y, p )
                #d = ih^y mod p
                d = (i*modexp( h, y, p)) % p
                #add the pair to the cipher pairs list
                cipher_pairs.append( [c, d] )

        #write the pairs to file 'Cipher'
        f = open( 'Cipher', 'w' )
        #i is a pair
        for i in cipher_pairs:
                f.write( str(i[0]) + ' ' + str(i[1]) + '\n' )
        f.close()       

#performs decryption on the cipher pairs found in Cipher using
#prive key K2 and writes the decrypted values to file Plaintext
def decrypt( ):
        #get p, g, x of K2
        f = open( 'K2', 'r' )
        p = int(f.readline())
        g = int(f.readline())
        x = int(f.readline())
        f.close()

        #decrpyts each pair and adds the decrypted integer to list of plaintext integers
        plaintext = []
        f = open('Cipher', 'r')
        pair = f.readline()
        #continue while lines read are not empty strings (EOF)
        while( not pair == '' ):
                #split the pair on the space
                pair = pair.split( ' ' )
                #c = first number in pair
                c = int(pair[0])
                #d = second number in pair
                d = int(pair[1])

                #s = c^x mod p
                s = modexp( c, x, p )
                #plaintext integer = ds^-1 mod p
                plain = (d*modexp( s, p-2, p)) % p
                #add plain to list of plaintext integers
                plaintext.append( plain )
                #get next pair
                pair = f.readline()
                
        f.close()

        #write all plaintext integers to file Plaintext
        f = open( 'Plaintext', 'w' )
        for i in plaintext:
                f.write( str(i) + "\n" )
        f.close()

#demonstrates the program        
def driver():
        #gets values of n, t, message file from user
        get_global_params()
        print ("generating keys")
        #gets keys and writes them to K1 and K2
        generate_keys()
        #encodes the message bytes of message file to larger integers
        z = encode()
        print ("encrypting")
        #encrypt the encoded integers
        encrypt( z )
        print ("decrypting")
        #decrypt the encrypted integers in Cipher
        decrypt()
        #decode the decrypted, encoded integers
        decode()
        print( 'done' )

#get_global_params()
#z = encode()
#f = open('encoded_text.txt', 'w')
#for i in z:
#        f.write( str(i) + "\n" )
#f.close()
#decode()

driver()
        









