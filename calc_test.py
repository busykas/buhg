import unittest
from fractions import Fraction

from calculator import power, square_root


class TestPower(unittest.TestCase):
    def test_exact_fraction_results(self):
        cases = [
            (Fraction(2, 3), Fraction(3), Fraction(8, 27)),
            (Fraction(4, 9), Fraction(1, 2), Fraction(2, 3)),
            (Fraction(8, 27), Fraction(-2, 3), Fraction(9, 4)),
            (Fraction(-8, 27), Fraction(1, 3), Fraction(-2, 3)),
            (Fraction(-8, 27), Fraction(2, 3), Fraction(4, 9)),
            (Fraction(0), Fraction(1, 3), Fraction(0)),
        ]

        for base, exponent, expected in cases:
            with self.subTest(base=base, exponent=exponent):
                result = power(base, exponent)
                self.assertIsInstance(result, Fraction)
                self.assertEqual(result, expected)

    def test_irrational_result_has_exact_notation(self):
        # Кубический корень из 2 должен выводиться без округления.
        self.assertEqual(power(Fraction(2), Fraction(1, 3)), "root(3, 2)")

    def test_even_root_of_negative_base(self):
        with self.assertRaises(ValueError):
            power(Fraction(-4, 9), Fraction(1, 2))

    def test_zero_to_negative_fractional_power(self):
        with self.assertRaises(ZeroDivisionError):
            power(Fraction(0), Fraction(-1, 2))


class TestSquareRoot(unittest.TestCase):
    def test_exact_fraction_results(self):
        cases = [
            (Fraction(9, 16), Fraction(3, 4)),
            (Fraction(25), Fraction(5)),
            (Fraction(0), Fraction(0)),
        ]

        for number, expected in cases:
            with self.subTest(number=number):
                result = square_root(number)
                self.assertIsInstance(result, Fraction)
                self.assertEqual(result, expected)

    def test_irrational_result_has_exact_notation(self):
        self.assertEqual(square_root(Fraction(2)), "√(2)")

    def test_negative_number(self):
        with self.assertRaises(ValueError):
            square_root(Fraction(-1))


if __name__ == "__main__":
    unittest.main()
