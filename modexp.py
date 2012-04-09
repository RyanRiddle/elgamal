import random

def gcd( a, b ):
	if b != 0:
		return gcd( b, a % b )
	return a
	

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

def SS( n ):
	a = random.randint( 1, n-1 )
	print "a is " + str(a)
	if gcd( a, n ) > 1:
		print "gcd"
		return False
	print jacobi(a,n)
	print modexp(a, (n-1)/2, n )
	if jacobi( a, n ) == modexp ( a, (n-1)/2, n ):
		print "jacobi"
		return True
	else:
		print "else"
		return False

def jacobi( a, n ):
	if a == -1:
		return (-1)**((n-1)/2)
	elif a == 1:
		return 1
	elif abs(n) > abs(a):
		z = jacobi( n % a, a )	
	elif a == 2:
		return (-1)**(((n**2)-1)/8)
	elif a % 2 == 1 and gcd( a, n ) == 1:
		if a % 4 == n % 4 == 3:
			z = -1 * jacobi( n, a )
		else:
			z = jacobi( n, a )
	else:
		z = 'fail'
		print z
	return z

def find_primitive_root( p ):
	if p == 2:
		return 1
	p1 = 2
	p2 = p / p1
	
	while( 1 ):
		g = random.randint( 2, p-1 )
		if not modexp( g, (p-1)/p1, p ) == 1:
			if not modexp( g, (p-1)/p2, p ) == 1:
				return g
	
def find_prime( n ):
	while(1):
		p = random.randint( 2, n )
		while( p % 2 == 0 ):
			p = random.randint(2,n)

		while( not SS(p) ):
			p = random.randint( 2, n )
			while( p % 2 == 0 ):
				p = random.randint(2,n)

		p = p * 2 + 1
		if SS(p):
			return p
	


p = find_prime( 101 )
g = find_primitive_root( p )
print '( p = ' + str(p) + ', g = ' + str(g) + ' )'

