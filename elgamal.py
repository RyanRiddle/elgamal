import random
import math

# computes the greatest common denominator of a and b.  assumes a > b
def gcd( a, b ):
	if b != 0:
		return gcd( b, a % b )
	#returned if b == 0
	return a	
	
#computes base^exp mod modulus
def modexp( base, exp, modulus ):
	if exp == 0:
		return 1

	temp = exp
	temp = temp / 2
	
	z = modexp( base, temp, modulus )

	if exp % 2 == 0:
		return z*z % modulus
	else:
		return base*z*z % modulus

#solovay-strassen primality test.  tests if n is prime
def SS( n ):
	#choose random a between 1 and n-2
	a = random.randint( 1, n-1 )
	
	#if a is not relatively prime to n, n is composite
	if gcd( a, n ) > 1:
		return False
	
	#declares n prime if jacobi(a, n) is congruent to a^((n-1)/2) mod n
	if jacobi( a, n ) == modexp ( a, (n-1)/2, n ):
		return True
	else:
		return False

#computes the jacobi symbol of a, n
def jacobi( a, n ):
	#property 1 of the jacobi symbol
	if a == -1:
		return (-1)**((n-1)/2)
	#if a == 1, jacobi symbol is equal to 1
	elif a == 1:
		return 1
	#property 1 of the jacobi symbol
	#if a = b mod n, jacobi(a, n) = jacobi( b, n )
	elif abs(n) > abs(a):
		z = jacobi( n % a, a )	
	#property 4 of the jacobi symbol
	elif a == 2:
		return (-1)**(((n**2)-1)/8)
	#law of quadratic reciprocity
	#if a is odd and a is coprime to n
	elif a % 2 == 1 and gcd( a, n ) == 1:
		if a % 4 == n % 4 == 3:
			z = -1 * jacobi( n, a )
		else:
			z = jacobi( n, a )
	#i have tried to design the algorithm so any case will
	#be handled by the conditions above and this clause will not be reached
	else:
		z = 'fail'
		print z
	return z

#finds a primitive root for prime p
#this function was implemented from the algorithm described here:
#http://modular.math.washington.edu/edu/2007/spring/ent/ent-html/node31.html
def find_primitive_root( p ):
	if p == 2:
		return 1
	#the prime divisors of p-1 are 2 and (p-1)/2 because
	#p = 2x + 1 where x is a prime
	p1 = 2
	p2 = (p-1) / p1
	
	#test random g's until one is found that is a primitive root mod p
	while( 1 ):
		g = random.randint( 2, p-1 )
		if not modexp( g, (p-1)/p1, p ) == 1:
			if not modexp( g, (p-1)/p2, p ) == 1:
				return g

#find n bit prime
def find_prime( n ):
	#keep testing until one is found
	while(1):
		#generate potential prime randomly
		p = random.randint( 2**(n-1), 2**n )
		#make sure it is odd
		while( p % 2 == 0 ):
			p = random.randint(2**(n-1),2**n)

		#keep doing this if the solovay-strassen test fails
		while( not SS(p) ):
			p = random.randint( 2**(n-1), 2**n )
			while( p % 2 == 0 ):
				p = random.randint(2**(n-1), 2**n)

		#if p is prime compute p = 2*p + 1
		#if p is prime, we have succeeded; else, start over
		p = p * 2 + 1
		if SS(p):
			return p
	
#encodes bytes to integers mod p.  reads bytes from file
def encode( file_name ):
	f = open( 'bytes.txt', 'r' )
	data = f.read(8)
	byte_array = []
	#put data into an array.  each element is a byte
	while( data ):
		byte_array.append( data )
		data = f.read(8)
	f.close()

	#convert each byte to a base 10 integer
	m = []
	for byte in byte_array:
		exp = 0
		num = 0
		for bit in byte:
			#ignore trailing characters
			if bit == '0' or bit == '1':
				num += int(bit)*(2**exp)
			exp += 1
		m.append( num )

	#z is the array of integers mod 504
	z = [0]*math.ceil( len(m) / 63 )
	j = -63
	num = 0
	for i in range( len(m) ):
		if i % 63 == 0:
			j += 63
			num = 0
		z[j/63] += m[i]*(2**(8*(i%63)))


	return z
	
def generate_keys( n ):
	p = find_prime( n )
	g = find_primitive_root( p )
	x = random.randint( 1, p )
	h = modexp( g, x, p )

	keys = [[p, g, h], [p, g, x]]
	return keys

#p = find_prime( 101 )
#g = find_primitive_root( p )
#print '( p = ' + str(p) + ', g = ' + str(g) + ' )'
#z = encode( 'bytes.txt' )
#for i in z:
#	print i
#print generate_keys( 10 )
print find_prime(5 )





