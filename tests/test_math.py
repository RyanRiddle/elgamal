import unittest
import elgamal


class GreatestCommonDivisorTests(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(elgamal.gcd(0, 0), 0)

    def test_any_number_and__one_returns_one(self):
        self.assertEqual(elgamal.gcd(1, 1), 1)
        self.assertEqual(elgamal.gcd(2, 1), 1)
        self.assertEqual(elgamal.gcd(3, 1), 1)

    def test_primes_are_divided_by_one(self):
        self.assertEqual(elgamal.gcd(3, 2), 1)
        self.assertEqual(elgamal.gcd(5, 3), 1)
        self.assertEqual(elgamal.gcd(7, 3), 1)
        self.assertEqual(elgamal.gcd(11, 7), 1)
        self.assertEqual(elgamal.gcd(13, 5), 1)
        self.assertEqual(elgamal.gcd(17, 2), 1)

    def test_coprimes_are_divided_by_one(self):
        self.assertEqual(elgamal.gcd(9, 8), 1)

    def test_not_coprime(self):
        self.assertNotEqual(elgamal.gcd(10, 20), 1)


if __name__ == '__main__':
    unittest.main()
