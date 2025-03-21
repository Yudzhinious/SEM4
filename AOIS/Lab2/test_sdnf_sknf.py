import unittest
from truth_table import *
class TestPerfectNormalForm(unittest.TestCase):

    def test_numerical_form(self):
        table = [
            (['0', '0'], 1),
            (['0', '1'], 0),
            (['1', '0'], 1),
            (['1', '1'], 0),
        ]
        expected_sdnf = "(0, 2)∨"
        expected_sknf = "(1, 3)∧"
        sdnf, sknf = numerical_form(table)
        self.assertEqual(sdnf, expected_sdnf)
        self.assertEqual(sknf, expected_sknf)

    def test_form_sdnf(self):
        truth_table = [
            (['0', '0'], 1),
            (['0', '1'], 0),
            (['1', '0'], 1),
            (['1', '1'], 0),
        ]
        variable_names = ['x', 'y']
        expected_sdnf = "(!x ∧ !y) ∨ (!x ∧ !y)"
        sdnf = form_sdnf(truth_table, variable_names)
        self.assertEqual(sdnf, expected_sdnf)

    def test_form_sknf(self):
        truth_table = [
            (['0', '0'], 1),
            (['0', '1'], 1),
            (['1', '0'], 1),
            (['1', '1'], 0),
        ]
        variable_names = ['x', 'y']
        expected_sknf = "(!x ∨ !y)"
        sknf = form_sknf(truth_table, variable_names)
        self.assertEqual(sknf, expected_sknf)

    def test_empty_truth_table(self):
        with self.assertRaises(ValueError):
            form_sdnf([], ['x', 'y'])

        with self.assertRaises(ValueError):
            form_sknf([], ['x', 'y'])

    def test_mismatched_values_and_variables(self):
        truth_table = [
            (['0', '0', '0'], 1),
            (['1', '1', '0'], 0),
        ]
        variable_names = ['x', 'y']

        with self.assertRaises(ValueError):
            form_sdnf(truth_table, variable_names)

        with self.assertRaises(ValueError):
            form_sknf(truth_table, variable_names)

if __name__ == '__main__':
    unittest.main()