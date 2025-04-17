import unittest
import io
from unittest.mock import patch
from calculation_table import CalculationTable

class TestCalculationTable(unittest.TestCase):
    def test_init_default(self):
        obj = CalculationTable()
        self.assertEqual(obj.truth_table, [])
        self.assertEqual(obj.variable_names, [])
        self.assertEqual(obj.expression, "")
        self.assertEqual(obj.max_vars, 5)
        self.assertEqual(obj.stage, 1)
        self.assertEqual(obj.column_width, 1)
        self.assertEqual(obj.num_vars, 0)

    def test_init_with_values(self):
        truth_table = [([1, 0], 1), ([0, 1], 0)]
        variable_names = ['A', 'B']
        expression = "A ∧ !B"
        max_vars = 3
        obj = CalculationTable(truth_table, variable_names, expression, max_vars)
        self.assertEqual(obj.truth_table, truth_table)
        self.assertEqual(obj.variable_names, variable_names)
        self.assertEqual(obj.expression, expression)
        self.assertEqual(obj.max_vars, max_vars)
        self.assertEqual(obj.stage, 1)
        self.assertEqual(obj.column_width, 1)
        self.assertEqual(obj.num_vars, 0)

    def test_calculate_table_sdnf_empty_table(self):
        obj = CalculationTable()
        result = obj.calculate_table_sdnf()
        self.assertEqual(result, "Нет СДНФ")

    def test_calculate_table_sdnf_no_minterms(self):
        obj = CalculationTable(truth_table=[([0, 0], 0), ([0, 1], 0)], variable_names=['A', 'B'])
        result = obj.calculate_table_sdnf()
        self.assertEqual(result, "Нет СДНФ")

    def test_calculate_table_sdnf_single_minterm(self):
        obj = CalculationTable(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 0), ([1, 1], 0)],
            variable_names=['A', 'B']
        )
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            result = obj.calculate_table_sdnf()
        self.assertEqual(result, "(!A ∧ B)")
        output = captured_output.getvalue()

    def test_calculate_table_sdnf_merge_terms(self):
        obj = CalculationTable(
            truth_table=[([0, 0, 0], 0), ([0, 0, 1], 1), ([0, 1, 0], 1), ([0, 1, 1], 0)],
            variable_names=['A', 'B', 'C']
        )
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            result = obj.calculate_table_sdnf()
        self.assertEqual(result, "(!A ∧ !B ∧ C) v (!A ∧ B ∧ !C)")
        output = captured_output.getvalue()

    def test_calculate_table_sdnf_multiple_minterms(self):
        obj = CalculationTable(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)],
            variable_names=['A', 'B']
        )
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            result = obj.calculate_table_sdnf()
        self.assertEqual(result, "(!A ∧ B) v (A ∧ !B)")
        output = captured_output.getvalue()

    def test_calculate_table_sknf_empty_table(self):
        obj = CalculationTable()
        result = obj.calculate_table_sknf()
        self.assertEqual(result, "Нет СКНФ")

    def test_calculate_table_sknf_too_many_variables(self):
        obj = CalculationTable(
            truth_table=[([0, 0, 0, 0, 0, 0], 0)],
            variable_names=['A', 'B', 'C', 'D', 'E', 'F']
        )
        with self.assertRaises(ValueError) as context:
            obj.calculate_table_sknf()
        self.assertEqual(str(context.exception), "Метод поддерживает до 5 переменных.")

    def test_calculate_table_sknf_no_maxterms(self):
        obj = CalculationTable(
            truth_table=[([0, 0], 1), ([0, 1], 1)],
            variable_names=['A', 'B']
        )
        result = obj.calculate_table_sknf()
        self.assertEqual(result, "Нет СКНФ")

    def test_calculate_table_sknf_single_maxterm(self):
        obj = CalculationTable(
            truth_table=[([0, 0], 1), ([0, 1], 0), ([1, 0], 1), ([1, 1], 1)],
            variable_names=['A', 'B']
        )
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            result = obj.calculate_table_sknf()
        self.assertEqual(result, "(A ∨ !B)")

    def test_calculate_table_sknf_merge_terms(self):
        obj = CalculationTable(
            truth_table=[([0, 0, 0], 0), ([0, 0, 1], 1), ([0, 1, 0], 1), ([0, 1, 1], 0)],
            variable_names=['A', 'B', 'C']
        )
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            result = obj.calculate_table_sknf()
        self.assertEqual(result, "(A ∨ B ∨ C) ∧ (A ∨ !B ∨ !C)")
        output = captured_output.getvalue()

    def test_calculate_table_sknf_multiple_maxterms(self):
        obj = CalculationTable(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)],
            variable_names=['A', 'B']
        )
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            result = obj.calculate_table_sknf()
        self.assertEqual(result, "(A ∨ B) ∧ (!A ∨ !B)")
        output = captured_output.getvalue()

    def test_calculate_table_sdnf_no_coverage(self):
        obj = CalculationTable(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 0), ([1, 1], 0)],
            variable_names=['A', 'B']
        )
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            result = obj.calculate_table_sdnf(verbose=False)
        self.assertEqual(result, "(!A ∧ B)")

    def test_calculate_table_sknf_no_coverage(self):
        obj = CalculationTable(
            truth_table=[([0, 0], 1), ([0, 1], 0), ([1, 0], 1), ([1, 1], 1)],
            variable_names=['A', 'B']
        )
        captured_output = io.StringIO()
        with patch('sys.stdout', captured_output):
            result = obj.calculate_table_sknf(verbose=False)
        self.assertEqual(result, "(A ∨ !B)")

if __name__ == '__main__':
    unittest.main()