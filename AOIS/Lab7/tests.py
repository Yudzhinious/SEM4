import unittest
from main import *
class TestMatrix(unittest.TestCase):
    def setUp(self):

        self.valid_matrix = [
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1]
        ]
        self.matrix = Matrix(self.valid_matrix)

    def test_init_valid(self):
        self.assertEqual(self.matrix.row_count, 3)
        self.assertEqual(self.matrix.col_count, 5)
        self.assertEqual(self.matrix.data_grid, self.valid_matrix)

    def test_init_invalid_empty(self):

        with self.assertRaises(ValueError):
            Matrix([])

    def test_init_invalid_non_rectangular(self):

        invalid_matrix = [
            [1, 0, 1],
            [0, 1]
        ]
        with self.assertRaises(ValueError):
            Matrix(invalid_matrix)

    def test_extract_sequence_valid(self):

        result = self.matrix.extract_sequence(0, 0)
        expected = [1, 0, 1]
        self.assertEqual(result, expected)

    def test_extract_sequence_out_of_bounds(self):

        with self.assertRaises(ValueError):
            self.matrix.extract_sequence(3, 0)

    def test_store_sequence_valid(self):

        new_sequence = [0, 1, 0]
        self.matrix.store_sequence(new_sequence, 0, 0)
        result = self.matrix.extract_sequence(0, 0)
        self.assertEqual(result, new_sequence)

    def test_store_sequence_invalid_bits(self):

        invalid_sequence = [0, 2, 1]
        with self.assertRaises(ValueError):
            self.matrix.store_sequence(invalid_sequence, 0, 0)

    def test_store_sequence_wrong_length(self):

        wrong_length_sequence = [0, 1]
        with self.assertRaises(ValueError):
            self.matrix.store_sequence(wrong_length_sequence, 0, 0)

    def test_show_matrix(self):

        original_grid = [row[:] for row in self.matrix.data_grid]
        self.matrix.show_matrix()
        self.assertEqual(self.matrix.data_grid, original_grid)

    def test_make_f0_valid(self):
        result = self.matrix.make_f0(1)
        expected = [0, 0, 0]
        self.assertEqual(result, expected)
        self.assertEqual(self.matrix.extract_sequence(0, 1), expected)

    def test_make_f0_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.matrix.make_f0(5)

    def test_make_f5_valid(self):
        source_data = self.matrix.make_f5(0, 1)
        self.assertEqual(source_data, self.matrix.extract_sequence(0, 0))

    def test_make_f5_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.matrix.make_f5(5, 0)

    def test_make_f10_valid(self):
        result = self.matrix.make_f10(0, 1)
        expected = [0, 0, 1]
        self.assertEqual(self.matrix.extract_sequence(0, 1), expected)

    def test_make_f10_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.matrix.make_f10(5, 0)

    def test_make_f15_valid(self):
        result = self.matrix.make_f15(1)
        expected = [1, 1, 1]
        self.assertEqual(result, expected)
        self.assertEqual(self.matrix.extract_sequence(0, 1), expected)

    def test_make_f15_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.matrix.make_f15(5)

    def test_compute_binary_sum(self):
        first = [1, 0, 1]
        second = [0, 1, 1]
        result = self.matrix.compute_binary_sum(first, second)
        expected = [1, 0, 0, 0]
        self.assertEqual(result, expected[:5])


    def test_process_fields_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.matrix.process_fields([1, 2, 1])

    def test_find_match_wrong_length(self):
        with self.assertRaises(ValueError):
            self.matrix.find_match([1, 0])

if __name__ == '__main__':
    unittest.main()