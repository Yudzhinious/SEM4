import unittest
from karno_sdnf_maps import KarnoSDNF
from karno_sknf_maps import KarnoSKNF

class TestKarnoSDNF(unittest.TestCase):
    def test_init(self):
        inputs = [([0, 0, 0, 0, 0], 1), ([1, 1, 1, 1, 1], 0)]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSDNF(inputs, labels)
        self.assertEqual(obj.inputs, inputs)
        self.assertEqual(obj.labels, labels)
        self.assertEqual(obj.var_count, 5)
        self.assertEqual(obj.order, [0, 1, 3, 2])

    def test_karno_sknf_invalid_var_count(self):
        obj = KarnoSKNF([], ['A', 'B', 'C'])
        result = obj.karno_sknf()
        self.assertEqual(result, "Этот метод не поддерживает такое количество переменных.")

    def test_karno_sknf_no_zeros_5_vars(self):
        inputs = [([0, 0, 0, 0, 0], 1), ([1, 1, 1, 1, 1], 1)]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_sknf(verbose=True)
        self.assertEqual(result, "1")

    def test_karno_sknf_single_zero_5_vars(self):
        inputs = [([0, 0, 0, 0, 0], 0), ([1, 1, 1, 1, 1], 1)]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_sknf(verbose=True)
        self.assertEqual(result, "E")

    def test_karno_sknf_merge_5_vars(self):
        inputs = [
            ([0, 0, 0, 0, 0], 0), ([0, 0, 0, 1, 0], 0),
            ([1, 1, 1, 1, 1], 1)  # Для достаточного размера inputs
        ]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_sknf(verbose=True)
        self.assertEqual(result, "E")

    def test_karno_sknf_no_zeros_6_vars(self):
        inputs = [([0, 0, 0, 0, 0, 0], 1), ([1, 1, 1, 1, 1, 1], 1)]
        labels = ['A', 'B', 'C', 'D', 'E', 'F']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_sknf(verbose=True)
        self.assertEqual(result, "1")

    def test_karno_sknf_merge_6_vars(self):
        inputs = [
            ([0, 0, 0, 0, 0, 0], 0), ([0, 0, 0, 0, 0, 1], 0),
            ([1, 1, 1, 1, 1, 1], 1)  # Для достаточного размера
        ]
        labels = ['A', 'B', 'C', 'D', 'E', 'F']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_sknf(verbose=True)
        self.assertEqual(result, "E")

    def test_karno_sknf_uncovered_zeros_5_vars(self):
        inputs = [
            ([0, 0, 0, 0, 0], 0), ([1, 1, 1, 1, 1], 0)
        ]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_sknf(verbose=True)
        self.assertEqual(result, "1")  # Поскольку не покрыты все нули, возвращается "1"

    def test_karno_sknf_verbose_false_5_vars(self):
        inputs = [([0, 0, 0, 0, 0], 0), ([1, 1, 1, 1, 1], 1)]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_sknf(verbose=False)
        self.assertEqual(result, "E")

    def test_karno_1_to_4_sknf_invalid_var_count(self):
        obj = KarnoSKNF([], ['A', 'B', 'C', 'D', 'E'])
        result = obj.karno_1_to_4_sknf()
        self.assertEqual(result, "Этот метод работает только для 1–4 переменных.")

    def test_karno_1_to_4_sknf_no_zeros_1_var(self):
        inputs = [([0], 1), ([1], 1)]
        labels = ['A']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_1_to_4_sknf(verbose=True)
        self.assertEqual(result, "1")

    def test_karno_1_to_4_sknf_no_zeros_2_vars(self):
        inputs = [([0, 0], 1), ([0, 1], 1), ([1, 0], 1), ([1, 1], 1)]
        labels = ['A', 'B']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_1_to_4_sknf(verbose=True)
        self.assertEqual(result, "1")

    def test_karno_1_to_4_sknf_merge_2_vars(self):
        inputs = [([0, 0], 0), ([0, 1], 0), ([1, 0], 1), ([1, 1], 1)]
        labels = ['A', 'B']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_1_to_4_sknf(verbose=True)
        self.assertEqual(result, "A")

    def test_karno_1_to_4_sknf_no_zeros_3_vars(self):
        inputs = [
            ([0, 0, 0], 1), ([0, 0, 1], 1), ([0, 1, 0], 1), ([0, 1, 1], 1),
            ([1, 0, 0], 1), ([1, 0, 1], 1), ([1, 1, 0], 1), ([1, 1, 1], 1)
        ]
        labels = ['A', 'B', 'C']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_1_to_4_sknf(verbose=True)
        self.assertEqual(result, "1")

    def test_karno_1_to_4_sknf_merge_3_vars(self):
        inputs = [
            ([0, 0, 0], 0), ([0, 0, 1], 0), ([0, 1, 0], 1), ([0, 1, 1], 1),
            ([1, 0, 0], 1), ([1, 0, 1], 1), ([1, 1, 0], 1), ([1, 1, 1], 1)
        ]
        labels = ['A', 'B', 'C']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_1_to_4_sknf(verbose=True)
        self.assertEqual(result, "(A ∨ B)")

    def test_karno_1_to_4_sknf_no_zeros_4_vars(self):
        inputs = [
            ([0, 0, 0, 0], 1), ([0, 0, 0, 1], 1), ([0, 0, 1, 0], 1), ([0, 0, 1, 1], 1),
            ([0, 1, 0, 0], 1), ([0, 1, 0, 1], 1), ([0, 1, 1, 0], 1), ([0, 1, 1, 1], 1),
            ([1, 0, 0, 0], 1), ([1, 0, 0, 1], 1), ([1, 0, 1, 0], 1), ([1, 0, 1, 1], 1),
            ([1, 1, 0, 0], 1), ([1, 1, 0, 1], 1), ([1, 1, 1, 0], 1), ([1, 1, 1, 1], 1)
        ]
        labels = ['A', 'B', 'C', 'D']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_1_to_4_sknf(verbose=True)
        self.assertEqual(result, "1")

    def test_karno_1_to_4_sknf_merge_4_vars(self):
        inputs = [
            ([0, 0, 0, 0], 0), ([0, 0, 0, 1], 0), ([0, 0, 1, 0], 1), ([0, 0, 1, 1], 1),
            ([0, 1, 0, 0], 1), ([0, 1, 0, 1], 1), ([0, 1, 1, 0], 1), ([0, 1, 1, 1], 1),
            ([1, 0, 0, 0], 1), ([1, 0, 0, 1], 1), ([1, 0, 1, 0], 1), ([1, 0, 1, 1], 1),
            ([1, 1, 0, 0], 1), ([1, 1, 0, 1], 1), ([1, 1, 1, 0], 1), ([1, 1, 1, 1], 1)
        ]
        labels = ['A', 'B', 'C', 'D']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_1_to_4_sknf(verbose=True)
        self.assertEqual(result, "(A ∨ B ∨ C)")

    def test_karno_1_to_4_sknf_uncovered_zeros_4_vars(self):
        inputs = [
            ([0, 0, 0, 0], 0), ([1, 1, 1, 1], 0)
        ]
        labels = ['A', 'B', 'C', 'D']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_1_to_4_sknf(verbose=True)
        self.assertEqual(result, "1")  # Поскольку не покрыты все нули, возвращается "1"

    def test_karno_1_to_4_sknf_verbose_false_4_vars(self):
        inputs = [
            ([0, 0, 0, 0], 0), ([0, 0, 0, 1], 0), ([0, 0, 1, 0], 1), ([0, 0, 1, 1], 1),
            ([0, 1, 0, 0], 1), ([0, 1, 0, 1], 1), ([0, 1, 1, 0], 1), ([0, 1, 1, 1], 1),
            ([1, 0, 0, 0], 1), ([1, 0, 0, 1], 1), ([1, 0, 1, 0], 1), ([1, 0, 1, 1], 1),
            ([1, 1, 0, 0], 1), ([1, 1, 0, 1], 1), ([1, 1, 1, 0], 1), ([1, 1, 1, 1], 1)
        ]
        labels = ['A', 'B', 'C', 'D']
        obj = KarnoSKNF(inputs, labels)
        result = obj.karno_1_to_4_sknf(verbose=False)
        self.assertEqual(result, "(A ∨ B ∨ C)")


    def test_karno_sdnf_invalid_var_count(self):
        obj = KarnoSDNF([], ['A', 'B', 'C'])
        result = obj.karno_sdnf()
        self.assertEqual(result, "Метод работает только с 5 или 6 переменными.")

    def test_karno_sdnf_no_ones_5_vars(self):
        inputs = [([0, 0, 0, 0, 0], 0), ([1, 1, 1, 1, 1], 0)]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_sdnf()
        self.assertEqual(result, "0")

    def test_karno_sdnf_single_one_5_vars(self):
        inputs = [([0, 0, 0, 0, 0], 1), ([1, 1, 1, 1, 1], 0)]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_sdnf()
        self.assertEqual(result, "(!A ∧ !B ∧ !C ∧ !D ∧ !E)")

    def test_karno_sdnf_merge_5_vars(self):
        inputs = [
            ([0, 0, 0, 0, 0], 1), ([0, 0, 0, 1, 0], 1),
            ([1, 1, 1, 1, 1], 0)  # Для достаточного размера inputs
        ]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_sdnf()
        self.assertEqual(result, "(!A ∧ !B ∧ !C ∧ !E)")

    def test_karno_sdnf_no_ones_6_vars(self):
        inputs = [([0, 0, 0, 0, 0, 0], 0), ([1, 1, 1, 1, 1, 1], 0)]
        labels = ['A', 'B', 'C', 'D', 'E', 'F']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_sdnf()
        self.assertEqual(result, "0")

    def test_karno_sdnf_merge_6_vars(self):
        inputs = [
            ([0, 0, 0, 0, 0, 0], 1), ([0, 0, 0, 0, 0, 1], 1),
            ([1, 1, 1, 1, 1, 1], 0)  # Для достаточного размера
        ]
        labels = ['A', 'B', 'C', 'D', 'E', 'F']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_sdnf()
        self.assertEqual(result, "!E")

    def test_karno_sdnf_uncovered_ones_5_vars(self):
        inputs = [
            ([0, 0, 0, 0, 0], 1), ([1, 1, 1, 1, 1], 1)
        ]
        labels = ['A', 'B', 'C', 'D', 'E']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_sdnf()
        self.assertEqual(result, "(!A ∧ !B ∧ !C ∧ !D ∧ !E) ∨ (A ∧ B ∧ C ∧ D ∧ E)")  # Поскольку не покрыты все единицы, возвращается "0"

    def test_karno_1_to_4_sdnf_invalid_var_count(self):
        obj = KarnoSDNF([], ['A', 'B', 'C', 'D', 'E'])
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "Метод работает только с 1, 2, 3 или 4 переменными.")

    def test_karno_1_to_4_sdnf_no_ones_1_var(self):
        inputs = [([0], 0), ([1], 0)]
        labels = ['A']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "0")

    def test_karno_1_to_4_sdnf_single_one_1_var(self):
        inputs = [([0], 1), ([1], 0)]
        labels = ['A']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "!A")

    def test_karno_1_to_4_sdnf_no_ones_2_vars(self):
        inputs = [([0, 0], 0), ([0, 1], 0), ([1, 0], 0), ([1, 1], 0)]
        labels = ['A', 'B']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "0")

    def test_karno_1_to_4_sdnf_merge_2_vars(self):
        inputs = [([0, 0], 1), ([0, 1], 1), ([1, 0], 0), ([1, 1], 0)]
        labels = ['A', 'B']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "!A")

    def test_karno_1_to_4_sdnf_no_ones_3_vars(self):
        inputs = [
            ([0, 0, 0], 0), ([0, 0, 1], 0), ([0, 1, 0], 0), ([0, 1, 1], 0),
            ([1, 0, 0], 0), ([1, 0, 1], 0), ([1, 1, 0], 0), ([1, 1, 1], 0)
        ]
        labels = ['A', 'B', 'C']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "0")

    def test_karno_1_to_4_sdnf_merge_3_vars(self):
        inputs = [
            ([0, 0, 0], 1), ([0, 0, 1], 1), ([0, 1, 0], 0), ([0, 1, 1], 0),
            ([1, 0, 0], 0), ([1, 0, 1], 0), ([1, 1, 0], 0), ([1, 1, 1], 0)
        ]
        labels = ['A', 'B', 'C']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "(!A ∧ !B)")

    def test_karno_1_to_4_sdnf_no_ones_4_vars(self):
        inputs = [
            ([0, 0, 0, 0], 0), ([0, 0, 0, 1], 0), ([0, 0, 1, 0], 0), ([0, 0, 1, 1], 0),
            ([0, 1, 0, 0], 0), ([0, 1, 0, 1], 0), ([0, 1, 1, 0], 0), ([0, 1, 1, 1], 0),
            ([1, 0, 0, 0], 0), ([1, 0, 0, 1], 0), ([1, 0, 1, 0], 0), ([1, 0, 1, 1], 0),
            ([1, 1, 0, 0], 0), ([1, 1, 0, 1], 0), ([1, 1, 1, 0], 0), ([1, 1, 1, 1], 0)
        ]
        labels = ['A', 'B', 'C', 'D']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "0")

    def test_karno_1_to_4_sdnf_merge_4_vars(self):
        inputs = [
            ([0, 0, 0, 0], 1), ([0, 0, 0, 1], 1), ([0, 0, 1, 0], 0), ([0, 0, 1, 1], 0),
            ([0, 1, 0, 0], 0), ([0, 1, 0, 1], 0), ([0, 1, 1, 0], 0), ([0, 1, 1, 1], 0),
            ([1, 0, 0, 0], 0), ([1, 0, 0, 1], 0), ([1, 0, 1, 0], 0), ([1, 0, 1, 1], 0),
            ([1, 1, 0, 0], 0), ([1, 1, 0, 1], 0), ([1, 1, 1, 0], 0), ([1, 1, 1, 1], 0)
        ]
        labels = ['A', 'B', 'C', 'D']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "(!A ∧ !B ∧ !C)")

    def test_karno_1_to_4_sdnf_uncovered_ones_4_vars(self):
        inputs = [
            ([0, 0, 0, 0], 1), ([1, 1, 1, 1], 1)
        ]
        labels = ['A', 'B', 'C', 'D']
        obj = KarnoSDNF(inputs, labels)
        result = obj.karno_1_to_4_sdnf()
        self.assertEqual(result, "(!A ∧ !B ∧ !C ∧ !D) ∨ (A ∧ B ∧ C ∧ D)")  # Поскольку не покрыты все единицы, возвращается "0"

if __name__ == '__main__':
    unittest.main()