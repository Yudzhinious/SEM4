import unittest
from truth_table import *

class TestTableFunctions(unittest.TestCase):

    def test_evaluate_expression(self):
        expression = ['A', 'B', '&', 'C', '|']
        values = {'A': 1, 'B': 0, 'C': 1}
        expected_result = 1  # (1 & 0) | 1 = 1
        result = evaluate_expression(expression, values)
        self.assertEqual(result, expected_result)

    def test_table(self):
        expression = ['A', 'B', '&', 'C', '|']
        var_names = ['A', 'B', 'C']
        expected_table = [
            ([0, 0, 0], 0),
            ([0, 0, 1], 0),
            ([0, 1, 0], 0),
            ([0, 1, 1], 1),
            ([1, 0, 0], 1),
            ([1, 0, 1], 1),
            ([1, 1, 0], 1),
            ([1, 1, 1], 1)
        ]
        result_table = table(expression, var_names)
        self.assertEqual(result_table, expected_table)

    def test_binary_to_decimal_without_sign(self):

        bin_number = '110'
        expected_decimal = 2
        result = binary_to_decimal_without_sign(bin_number)
        self.assertEqual(result, expected_decimal)

    def test_binary_to_dec_num(self):
        bin_number = '1101'
        expected_decimal = 13
        result = binary_to_dec_num(bin_number)
        self.assertEqual(result, expected_decimal)

    def test_results_to_string(self):
        table_data = [
            ([0, 0], 0),
            ([0, 1], 1),
            ([1, 0], 1),
            ([1, 1], 0)
        ]
        expected_result = '0110'
        result_str = results_to_string(table_data)
        self.assertEqual(result_str, expected_result)

    def test_unique_elements(self):
        expression = 'A & B | C > D'
        expected_unique_elements = ['A', 'B', 'C', 'D']
        result = unique_elements(expression)
        self.assertEqual(result, expected_unique_elements)

if __name__ == '__main__':
    unittest.main()
