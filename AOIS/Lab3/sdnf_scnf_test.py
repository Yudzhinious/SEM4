import unittest
from sdnf_sknf import SDNF_SKNF
import unittest
import io
from unittest.mock import patch



class TestSDNFSKNF(unittest.TestCase):
    def test_init_default(self):
        obj = SDNF_SKNF()
        self.assertEqual(obj.truth_table, [])
        self.assertEqual(obj.variable_names, [])
        self.assertEqual(obj.expression, "")
        self.assertEqual(obj.num_vars, 0)
        self.assertEqual(obj.stage, 1)
        self.assertEqual(obj.column_width, 1)

    def test_init_with_values(self):
        truth_table = [([1, 0], 1), ([0, 1], 0)]
        variable_names = ['A', 'B']
        expression = "A ∧ !B"
        obj = SDNF_SKNF(truth_table, variable_names, expression)
        self.assertEqual(obj.truth_table, truth_table)
        self.assertEqual(obj.variable_names, variable_names)
        self.assertEqual(obj.expression, expression)
        self.assertEqual(obj.num_vars, 0)
        self.assertEqual(obj.stage, 1)
        self.assertEqual(obj.column_width, 1)

    def test_form_sdnf_empty_table(self):
        obj = SDNF_SKNF()
        with self.assertRaises(ValueError) as context:
            obj.form_sdnf()
        self.assertEqual(str(context.exception), "Таблица истинности или список переменных пусты.")

    def test_form_sdnf_empty_variables(self):
        obj = SDNF_SKNF(truth_table=[([1, 0], 1)])
        with self.assertRaises(ValueError) as context:
            obj.form_sdnf()
        self.assertEqual(str(context.exception), "Таблица истинности или список переменных пусты.")

    def test_form_sdnf_invalid_row_length(self):
        obj = SDNF_SKNF(truth_table=[([1], 1)], variable_names=['A', 'B'])
        with self.assertRaises(ValueError) as context:
            obj.form_sdnf()
        self.assertEqual(str(context.exception), "Число значений в строках таблицы не совпадает с числом переменных.")

    def test_form_sdnf_no_ones(self):
        obj = SDNF_SKNF(truth_table=[([0, 0], 0), ([0, 1], 0)], variable_names=['A', 'B'])
        result = obj.form_sdnf()
        self.assertEqual(result, "Нет выражений для СДНФ")

    def test_form_sdnf_valid(self):
        obj = SDNF_SKNF(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)],
            variable_names=['A', 'B']
        )
        result = obj.form_sdnf()
        self.assertEqual(result, "(!A ∧ B) ∨ (A ∧ !B)")

    def test_form_sknf_empty_table(self):
        obj = SDNF_SKNF()
        with self.assertRaises(ValueError) as context:
            obj.form_sknf()
        self.assertEqual(str(context.exception), "Таблица истинности или список переменных пусты.")

    def test_form_sknf_empty_variables(self):
        obj = SDNF_SKNF(truth_table=[([1, 0], 0)])
        with self.assertRaises(ValueError) as context:
            obj.form_sknf()
        self.assertEqual(str(context.exception), "Таблица истинности или список переменных пусты.")

    def test_form_sknf_invalid_row_length(self):
        obj = SDNF_SKNF(truth_table=[([1], 0)], variable_names=['A', 'B'])
        with self.assertRaises(ValueError) as context:
            obj.form_sknf()
        self.assertEqual(str(context.exception), "Число значений в строках таблицы не совпадает с числом переменных.")

    def test_form_sknf_no_zeros(self):
        obj = SDNF_SKNF(truth_table=[([0, 0], 1), ([0, 1], 1)], variable_names=['A', 'B'])
        result = obj.form_sknf()
        self.assertEqual(result, "Нет выражений для СКНФ")

    def test_form_sknf_valid(self):
        obj = SDNF_SKNF(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)],
            variable_names=['A', 'B']
        )
        result = obj.form_sknf()
        self.assertEqual(result, "(A ∨ B) ∧ (!A ∨ !B)")

    def test_calculate_sdnf_no_variables(self):
        obj = SDNF_SKNF(truth_table=[([0], 0)], variable_names=[])
        result = obj.calculate_sdnf()
        self.assertEqual(result, "ДНФ отсутствует")

    def test_calculate_sdnf_no_ones(self):
        obj = SDNF_SKNF(truth_table=[([0, 0], 0), ([0, 1], 0)], variable_names=['A', 'B'])
        result = obj.calculate_sdnf()
        self.assertEqual(result, "ДНФ отсутствует")

    def test_calculate_sdnf_single_term(self):
        obj = SDNF_SKNF(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 0), ([1, 1], 0)],
            variable_names=['A', 'B']
        )
        result = obj.calculate_sdnf()
        self.assertEqual(result, "(!A ∧ B)")

    def test_calculate_sdnf_multiple_terms(self):
        obj = SDNF_SKNF(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)],
            variable_names=['A', 'B']
        )
        result = obj.calculate_sdnf()
        self.assertEqual(result, "(!A ∧ B) ∨ (A ∧ !B)")

    def test_calculate_sdnf_merge_terms(self):
        obj = SDNF_SKNF(
            truth_table=[([0, 0, 0], 0), ([0, 0, 1], 1), ([0, 1, 0], 1), ([0, 1, 1], 0)],
            variable_names=['A', 'B', 'C']
        )
        result = obj.calculate_sdnf()
        self.assertEqual(result, "(!A ∧ !B ∧ C) ∨ (!A ∧ B ∧ !C)")

    def test_calculate_sknf_no_variables(self):
        obj = SDNF_SKNF(truth_table=[([0], 1)], variable_names=[])
        result = obj.calculate_sknf()
        self.assertEqual(result, "КНФ отсутствует")

    def test_calculate_sknf_no_zeros(self):
        obj = SDNF_SKNF(truth_table=[([0, 0], 1), ([0, 1], 1)], variable_names=['A', 'B'])
        result = obj.calculate_sknf()
        self.assertEqual(result, "КНФ отсутствует")

    def test_calculate_sknf_single_term(self):
        obj = SDNF_SKNF(
            truth_table=[([0, 0], 1), ([0, 1], 0), ([1, 0], 1), ([1, 1], 1)],
            variable_names=['A', 'B']
        )
        result = obj.calculate_sknf()
        self.assertEqual(result, "(A ∨ !B)")

    def test_calculate_sknf_multiple_terms(self):
        obj = SDNF_SKNF(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)],
            variable_names=['A', 'B']
        )
        result = obj.calculate_sknf()
        self.assertEqual(result, "(A ∨ B) ∧ (!A ∨ !B)")

    def test_calculate_sknf_merge_terms(self):
        obj = SDNF_SKNF(
            truth_table=[([0, 0, 0], 0), ([0, 0, 1], 1), ([0, 1, 0], 1), ([0, 1, 1], 0)],
            variable_names=['A', 'B', 'C']
        )
        result = obj.calculate_sknf()
        self.assertEqual(result, "(A ∨ B ∨ C) ∧ (A ∨ !B ∨ !C)")

    def test_unique_elements_empty_expression(self):
        obj = SDNF_SKNF(expression="")
        result = obj.unique_elements()
        self.assertEqual(result, [])

    def test_unique_elements_no_letters(self):
        obj = SDNF_SKNF(expression="123!@#")
        result = obj.unique_elements()
        self.assertEqual(result, [])

    def test_unique_elements_mixed_case(self):
        obj = SDNF_SKNF(expression="A ∧ !b ∨ C")
        result = obj.unique_elements()
        self.assertEqual(result, ['A', 'C', 'b'])

    def test_unique_elements_duplicates(self):
        obj = SDNF_SKNF(expression="A ∧ A ∨ B ∧ B")
        result = obj.unique_elements()
        self.assertEqual(result, ['A', 'B'])

    def test_numerical_form_empty_table(self):
        obj = SDNF_SKNF()
        sdnf_str, sknf_str = obj.numerical_form()
        self.assertEqual(sdnf_str, "()∨")
        self.assertEqual(sknf_str, "()∧")

    def test_numerical_form_valid(self):
        obj = SDNF_SKNF(
            truth_table=[([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]
        )
        sdnf_str, sknf_str = obj.numerical_form()
        self.assertEqual(sdnf_str, "(1, 2)∨")
        self.assertEqual(sknf_str, "(0, 3)∧")

    def test_num_to_bin(self):
        obj = SDNF_SKNF()
        self.assertEqual(obj.num_to_bin(5, 3), "101")
        self.assertEqual(obj.num_to_bin(2, 4), "0010")
        self.assertEqual(obj.num_to_bin(0, 2), "00")

    def test_position_replacement(self):
        obj = SDNF_SKNF()
        self.assertEqual(obj.position_replacement("101", "100"), 1)
        self.assertEqual(obj.position_replacement("101", "010"), 3)
        self.assertEqual(obj.position_replacement("111", "111"), 0)

    def test_is_combinated(self):
        obj = SDNF_SKNF()
        self.assertTrue(obj.is_combinated("101", "100"))
        self.assertFalse(obj.is_combinated("101", "010"))
        self.assertFalse(obj.is_combinated("111", "111"))

    def test_merge(self):
        obj = SDNF_SKNF()
        self.assertEqual(obj.merge("101", "100"), "10-")
        self.assertEqual(obj.merge("111", "111"), "111")
        self.assertEqual(obj.merge("101", "011"), "--1")

if __name__ == '__main__':
    unittest.main()