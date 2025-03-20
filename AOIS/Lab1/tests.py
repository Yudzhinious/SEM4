import unittest
from laba import *

class TestMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.method = Digit()
    def test_direct_code_multiplication_positive(self):
        result = self.method.direct_code_multiplication(3, 4)
        self.assertIn("Результат в прямом коде: [0000000000000000000000000001100]  Десятичный результат: 12", result)

    def test_binary_to_dec_num(self):
        binary_str = "1011"
        expected_result = 11
        self.assertEqual(self.method.binary_to_dec_num(binary_str), expected_result)

    def test_additional_subtract(self):
        number1 = 11
        number2 = 5
        expected_result = "00000000000000000000000000000110"
        self.assertEqual(self.method.additional_subtract(number1, number2), expected_result)

    def test_direct_code_multiplication_negative_positive(self):
        result = self.method.direct_code_multiplication(-5, 3)
        self.assertIn("Результат в прямом коде: [1000000000000000000000000001111]  Десятичный результат: -15", result)

    def test_direct_code_multiplication_positive_negative(self):
        result = self.method.direct_code_multiplication(6, -2)
        self.assertIn("Результат в прямом коде: [1000000000000000000000000001100]  Десятичный результат: -12", result)

    def test_direct_sum_of_binary_numbers(self):
        self.assertEqual(self.method.direct_summa(11, 25), "00000000000000000000000000100100")
        self.assertEqual(self.method.direct_summa(11, -25), "10000000000000000000000000100100")

    def test_convert_to_reverse_binary(self):
        self.assertEqual(self.method.convert_to_reverse_binary(11), "00000000000000000000000000001011")
        self.assertEqual(self.method.convert_to_reverse_binary(-11), "11111111111111111111111111110100")

    def test_convert_to_additional_binary(self):
        self.assertEqual(self.method.convert_to_additional_binary(11), "00000000000000000000000000001011")
        self.assertEqual(self.method.convert_to_additional_binary(-11), "11111111111111111111111111110101")

    def test_sum_of_additional_binary(self):
        self.assertEqual(self.method.additional_summa(11, 25), "00000000000000000000000000100100")
        self.assertEqual(self.method.additional_summa(11, -25), "11111111111111111111111111110010")

    def test_float_to_binary_fraction(self):
        self.assertEqual(self.method.float_to_binary_fraction(0.5), "1")
        self.assertEqual(self.method.float_to_binary_fraction(0.25), "01")

    def test_float_to_binary(self):
        self.assertEqual(self.method.convert_float_to_bin(11.5), "01000001001110000000000000000000")
        self.assertEqual(self.method.convert_float_to_bin(-11.5), "11000001001110000000000000000000")

    def test_divide_binary(self):
        result1 = self.method.divide_bin(11, 25)
        self.assertFalse(result1.startswith('0'))

        result2 = self.method.divide_bin(-11, 25)
        self.assertFalse(result2.startswith('0'))

        with self.assertRaises(ValueError):
            self.method.divide_bin(11, 0)

    def test_convert_float_to_binary(self):
        self.assertEqual(self.method.convert_float_to_bin(3.5), "01000000011000000000000000000000")
        self.assertEqual(self.method.convert_float_to_bin(4.6), "01000000100100110011001100110011")
    def test_float_sum(self):
        self.assertEqual(self.method.float_summa(3.4, 2.5), 5.899999618530273)

    def display_ieee(self, param):
        pass


if __name__ == '__main__':
    unittest.main()