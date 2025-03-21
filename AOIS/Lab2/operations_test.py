import unittest
from truth_table import *

class TestLogicalFunctions(unittest.TestCase):

    def test_conjuction(self):
        # Проверка операции конъюнкции (AND)
        self.assertEqual(conjuction(1, 1), 1)
        self.assertEqual(conjuction(1, 0), 0)

    def test_disjunction(self):
        # Проверка операции дизъюнкции (OR)
        self.assertEqual(disjunction(1, 1), 1)
        self.assertEqual(disjunction(1, 0), 1)
    def test_negation(self):
        self.assertEqual(negation(1), 0)
        self.assertEqual(negation(0), 1)

    def test_implication(self):
        self.assertEqual(implication(1, 1), 1)
        self.assertEqual(implication(1, 0), 0)

    def test_equivalent(self):
        self.assertEqual(equivalent(1, 0), 0)
        self.assertEqual(equivalent(0, 1), 0)

    def test_priority(self):
        self.assertEqual(priority('!'), 5)
        self.assertEqual(priority('&'), 4)
        self.assertEqual(priority('|'), 3)
        self.assertEqual(priority('>'), 2)
        self.assertEqual(priority('~'), 1)
        self.assertEqual(priority('x'), 0)

if __name__ == '__main__':
    unittest.main()
