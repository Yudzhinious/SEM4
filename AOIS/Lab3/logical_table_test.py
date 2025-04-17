import unittest
from logical_operations import LogicalOperations

class TestLogicalOperations(unittest.TestCase):
    def test_conjunction(self):
        self.assertEqual(LogicalOperations.conjunction(1, 1), 1)
        self.assertEqual(LogicalOperations.conjunction(1, 0), 0)
        self.assertEqual(LogicalOperations.conjunction(0, 1), 0)
        self.assertEqual(LogicalOperations.conjunction(0, 0), 0)

    def test_disjunction(self):
        self.assertEqual(LogicalOperations.disjunction(1, 1), 1)
        self.assertEqual(LogicalOperations.disjunction(1, 0), 1)
        self.assertEqual(LogicalOperations.disjunction(0, 1), 1)
        self.assertEqual(LogicalOperations.disjunction(0, 0), 0)

    def test_negation(self):
        self.assertEqual(LogicalOperations.negation(1), 0)
        self.assertEqual(LogicalOperations.negation(0), 1)

    def test_implication(self):
        self.assertEqual(LogicalOperations.implication(1, 1), 1)
        self.assertEqual(LogicalOperations.implication(1, 0), 0)
        self.assertEqual(LogicalOperations.implication(0, 1), 1)
        self.assertEqual(LogicalOperations.implication(0, 0), 1)

    def test_equivalence(self):
        self.assertEqual(LogicalOperations.equivalence(1, 1), 1)
        self.assertEqual(LogicalOperations.equivalence(0, 0), 1)
        self.assertEqual(LogicalOperations.equivalence(1, 0), 0)
        self.assertEqual(LogicalOperations.equivalence(0, 1), 0)

    def test_priority(self):
        self.assertEqual(LogicalOperations.priority('!'), 5)
        self.assertEqual(LogicalOperations.priority('&'), 4)
        self.assertEqual(LogicalOperations.priority('|'), 3)
        self.assertEqual(LogicalOperations.priority('>'), 2)
        self.assertEqual(LogicalOperations.priority('~'), 1)
        self.assertEqual(LogicalOperations.priority('x'), 0)

    def test_evaluate_expression_simple(self):
        parts = ['A', 'B', '&']
        values = {'A': 1, 'B': 1}
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 1)
        values = {'A': 1, 'B': 0}
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 0)

    def test_evaluate_expression_negation(self):
        parts = ['A', '!']
        values = {'A': 1}
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 0)
        values = {'A': 0}
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 1)

    def test_evaluate_expression_complex(self):
        parts = ['A', 'B', '|', 'C', '&']
        values = {'A': 1, 'B': 0, 'C': 1}
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 1)
        values = {'A': 0, 'B': 0, 'C': 0}
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 0)

    def test_evaluate_expression_parentheses(self):
        parts = ['A', 'B', '&', 'C', '|']
        values = {'A': 1, 'B': 1, 'C': 0}
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 1)
        parts = ['(', 'A', 'B', '&', ')', 'C', '|']
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 1)

    def test_evaluate_expression_all_operators(self):
        parts = ['A', 'B', '>', 'C', '!', '~']
        values = {'A': 1, 'B': 0, 'C': 1}
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 1)
        values = {'A': 0, 'B': 1, 'C': 1}
        self.assertEqual(LogicalOperations.evaluate_expression(parts, values), 1)

    def test_bin_to_dec(self):
        self.assertEqual(LogicalOperations.bin_to_dec("101"), 5)
        self.assertEqual(LogicalOperations.bin_to_dec("0"), 0)
        self.assertEqual(LogicalOperations.bin_to_dec(""), 0)

    def test_binary_to_dec_num(self):
        self.assertEqual(LogicalOperations.binary_to_dec_num("101"), 5)
        self.assertEqual(LogicalOperations.binary_to_dec_num("0"), 0)
        self.assertEqual(LogicalOperations.binary_to_dec_num(""), 0)
        self.assertEqual(LogicalOperations.binary_to_dec_num("1111"), 15)

    def test_results_to_string(self):
        table = [([0, 0], 0), ([0, 1], 1), ([1, 0], 0), ([1, 1], 1)]
        self.assertEqual(LogicalOperations.results_to_string(table), "0101")
        table = [([0], 1), ([1], 0)]
        self.assertEqual(LogicalOperations.results_to_string(table), "10")

    def test_unique_elements(self):
        self.assertEqual(LogicalOperations.unique_elements("A & B | C"), ['A', 'B', 'C'])
        self.assertEqual(LogicalOperations.unique_elements("A & A | B"), ['A', 'B'])
        self.assertEqual(LogicalOperations.unique_elements("! & |"), [])
        self.assertEqual(LogicalOperations.unique_elements("aBc"), ['B', 'a', 'c'])

    def test_numerical_form(self):
        table = [([0, 0], 0), ([0, 1], 1), ([1, 0], 0), ([1, 1], 1)]
        sdnf, sknf = LogicalOperations.numerical_form(table)
        self.assertEqual(sdnf, "(1, 3)∨")
        self.assertEqual(sknf, "(0, 2)∧")
        table = [([0], 1), ([1], 0)]
        sdnf, sknf = LogicalOperations.numerical_form(table)
        self.assertEqual(sdnf, "(0)∨")
        self.assertEqual(sknf, "(1)∧")

    def test_num_to_bin(self):
        self.assertEqual(LogicalOperations.num_to_bin(5, 3), "101")
        self.assertEqual(LogicalOperations.num_to_bin(0, 2), "00")
        self.assertEqual(LogicalOperations.num_to_bin(3, 4), "0011")

    def test_position_replacement(self):
        self.assertEqual(LogicalOperations.position_replacement("101", "100"), 1)
        self.assertEqual(LogicalOperations.position_replacement("101", "001"), 1)
        self.assertEqual(LogicalOperations.position_replacement("111", "111"), 0)
        self.assertEqual(LogicalOperations.position_replacement("", ""), 0)

    def test_is_combinated(self):
        self.assertTrue(LogicalOperations.is_combinated("101", "100"))
        self.assertFalse(LogicalOperations.is_combinated("111", "111"))
        self.assertFalse(LogicalOperations.is_combinated("", ""))

    def test_merge(self):
        self.assertEqual(LogicalOperations.merge("101", "100"), "10-")
        self.assertEqual(LogicalOperations.merge("111", "111"), "111")
        self.assertEqual(LogicalOperations.merge("001", "101"), "-01")
        self.assertEqual(LogicalOperations.merge("", ""), "")

if __name__ == '__main__':
    unittest.main()