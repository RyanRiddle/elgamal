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
	


print SS( 101 )

