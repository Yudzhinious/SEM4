import unittest
import io
import sys
from unittest.mock import patch
from main import Hash_map

class TestHashMap(unittest.TestCase):
    def setUp(self):
        self._redirect = io.StringIO()
        self._stdout = sys.stdout
        sys.stdout = self._redirect

    def tearDown(self):
        sys.stdout = self._stdout

    def test_init_and_setup(self):
        hash_map = Hash_map()
        self.assertEqual(hash_map.base_capacity, 20)
        self.assertFalse(hash_map.trace_enabled)
        self.assertEqual(hash_map.entry_count, 0)
        self.assertEqual(len(hash_map.storage), 20)
        self.assertEqual(len(hash_map.letter_map), 33)

        hash_map = Hash_map(base_capacity=10, trace_enabled=True)
        self.assertEqual(hash_map.base_capacity, 20)
        self.assertTrue(hash_map.trace_enabled)
        self.assertEqual(hash_map.entry_count, 0)
        self.assertEqual(len(hash_map.storage), 20)
        self.assertEqual(len(hash_map.letter_map), 33)

    def test_make_entry(self):
        hash_map = Hash_map()
        entry = hash_map.make_entry("Test", "Data")
        expected = {
            "label": "Test",
            "info": "Data",
            "code": None,
            "position": None,
            "collision_mark": 0,
            "occupied_mark": 0,
            "terminal_mark": 0,
            "link_mark": 0,
            "delete_mark": 0,
            "next_link": None
        }
        self.assertEqual(entry, expected)

        empty_entry = hash_map.make_entry()
        self.assertEqual(empty_entry["label"], None)
        self.assertEqual(empty_entry["info"], None)

    def test_get_numeric_code(self):
        hash_map = Hash_map()

        self.assertEqual(hash_map.get_numeric_code("А"), 0)
        self.assertEqual(hash_map.get_numeric_code("Я"), 1023)

        self.assertEqual(hash_map.get_numeric_code("АБ"), 0 * 33 + 1)
        self.assertEqual(hash_map.get_numeric_code("ЯЯ"), 32 * 33 - 2)

        self.assertEqual(hash_map.get_numeric_code("Z"), 0)
        self.assertEqual(hash_map.get_numeric_code("AB"), 0)

    def test_calculate_position(self):
        hash_map = Hash_map(base_capacity=20)
        self.assertEqual(hash_map.calculate_position(0), 0)
        self.assertEqual(hash_map.calculate_position(20), 0)
        self.assertEqual(hash_map.calculate_position(21), 1)

    def test_find_slot(self):
        hash_map = Hash_map(trace_enabled=True)

        pos = hash_map.find_slot("Абаев", is_for_addition=True)
        self.assertIsNotNone(pos)
        self.assertLess(pos, hash_map.base_capacity)

        pos = hash_map.find_slot("Абаев", is_for_addition=False)
        self.assertIsNone(pos)

        hash_map.store_item("Абаев", "Сергей")
        pos = hash_map.find_slot("Абаев", is_for_addition=False)
        self.assertIsNotNone(pos)
        self.assertEqual(hash_map.storage[pos]["label"], "Абаев")

    def test_store_item(self):
        hash_map = Hash_map()
        hash_map.store_item("Абаев", "Сергей")
        pos = hash_map.find_slot("Абаев", is_for_addition=False)
        self.assertEqual(hash_map.storage[pos]["label"], "Абаев")
        self.assertEqual(hash_map.storage[pos]["info"], "Сергей")
        self.assertEqual(hash_map.entry_count, 1)

        hash_map.store_item("Бобков", "Тимур" * 3)
        pos = hash_map.find_slot("Бобков", is_for_addition=False)
        self.assertTrue(hash_map.storage[pos]["info"].startswith("ptr_"))

        with self.assertRaises(KeyError):
            hash_map.store_item("Абаев", "Иван")

    def test_retrieve_item(self):
        hash_map = Hash_map()
        hash_map.store_item("Абаев", "Сергей")
        self.assertEqual(hash_map.retrieve_item("Абаев"), "Сергей")
        self.assertIsNone(hash_map.retrieve_item("Неизвестный"))

    def test_remove_item(self):
        hash_map = Hash_map()
        hash_map.store_item("Абаев", "Сергей")
        pos = hash_map.find_slot("Абаев", is_for_addition=False)
        hash_map.remove_item("Абаев")
        self.assertEqual(hash_map.storage[pos]["delete_mark"], 1)
        self.assertEqual(hash_map.entry_count, 0)
        with self.assertRaises(KeyError):
            hash_map.remove_item("Абаев")

    def test_update_item(self):
        hash_map = Hash_map()
        hash_map.store_item("Абаев", "Сергей")
        hash_map.update_item("Абаев", "Иван")
        pos = hash_map.find_slot("Абаев", is_for_addition=False)
        self.assertEqual(hash_map.storage[pos]["info"], "Иван")
        with self.assertRaises(KeyError):
            hash_map.update_item("Неизвестный", "Иван")

    def test_remove_item_simple_case(self):
        hash_map = Hash_map()
        hash_map.store_item("АА", "Data1")
        pos = hash_map.find_slot("АА", is_for_addition=False)
        data = hash_map.storage[pos]
        data["terminal_mark"] = 1
        data["collision_mark"] = 0

        hash_map.remove_item("АА")

        self.assertEqual(data["delete_mark"], 1)
        self.assertEqual(data["occupied_mark"], 0)
        self.assertEqual(hash_map.entry_count, 0)

    def test_remove_item_terminal_chain_case(self):
        hash_map = Hash_map(base_capacity=10)
        hash_map.store_item("АА", "Data1")
        hash_map.store_item("АБ", "Data2")

        pos_aa = hash_map.find_slot("АА", is_for_addition=False)
        pos_ab = hash_map.find_slot("АБ", is_for_addition=False)
        hash_map.storage[pos_aa]["next_link"] = pos_ab
        hash_map.storage[pos_aa]["terminal_mark"] = 0
        hash_map.storage[pos_ab]["terminal_mark"] = 1
        hash_map.storage[pos_ab]["collision_mark"] = 1

        hash_map.remove_item("АБ")

        self.assertEqual(hash_map.storage[pos_ab]["occupied_mark"], 0)
        self.assertEqual(hash_map.storage[pos_aa]["terminal_mark"], 1)
        self.assertIsNone(hash_map.storage[pos_aa]["next_link"])

    def test_remove_item_cascade_copying_case(self):
        hash_map = Hash_map(base_capacity=10)
        hash_map.store_item("АА", "Data1")
        hash_map.store_item("АБ", "Data2")

        pos_aa = hash_map.find_slot("АА", is_for_addition=False)
        pos_ab = hash_map.find_slot("АБ", is_for_addition=False)

        hash_map.storage[pos_aa]["next_link"] = pos_ab
        hash_map.storage[pos_aa]["collision_mark"] = 0
        hash_map.storage[pos_aa]["terminal_mark"] = 0

        hash_map.remove_item("АА")

        data = hash_map.storage[pos_aa]
        self.assertEqual(data["label"], "АБ")
        self.assertEqual(data["info"], "Data2")
        self.assertEqual(hash_map.storage[pos_ab]["occupied_mark"], 0)

    def test_remove_item_deep_chain_collision(self):
        hash_map = Hash_map(base_capacity=10)
        hash_map.store_item("АА", "Data1")
        hash_map.store_item("АБ", "Data2")

        pos1 = hash_map.find_slot("АА", is_for_addition=False)
        pos2 = hash_map.find_slot("АБ", is_for_addition=False)
        hash_map.storage[pos1]["next_link"] = pos2
        hash_map.storage[pos1]["collision_mark"] = 1
        hash_map.storage[pos1]["terminal_mark"] = 0

        hash_map.remove_item("АА")

        self.assertEqual(hash_map.storage[pos1]["label"], "АБ")
        self.assertEqual(hash_map.storage[pos2]["occupied_mark"], 0)

    def test_remove_item_not_found(self):
        hash_map = Hash_map()
        with self.assertRaises(KeyError):
            hash_map.remove_item("Несуществующий")

    def test_remove_item_deleted_already(self):
        hash_map = Hash_map()
        hash_map.store_item("АА", "Data")
        hash_map.remove_item("АА")
        with self.assertRaises(KeyError):
            hash_map.remove_item("АА")

    def test_grow_storage(self):
        hash_map = Hash_map(base_capacity=2)
        hash_map.store_item("Абаев", "Сергей")
        hash_map.store_item("Бобков", "Тимур")
        old_capacity = hash_map.base_capacity
        hash_map.store_item("Видерт", "Евгений")
        self.assertEqual(hash_map.entry_count, 3)

    def test_display_content(self):
        hash_map = Hash_map()
        hash_map.store_item("Абаев", "Сергей")
        captured_output = io.StringIO()
        sys.stdout = captured_output
        hash_map.display_content()
        sys.stdout = self._stdout
        output = captured_output.getvalue()
        self.assertIn("Поз", output)
        self.assertIn("Абаев", output)
        self.assertIn("Сергей", output)

    def test_get_length(self):
        hash_map = Hash_map()
        self.assertEqual(hash_map.get_length(), 0)
        hash_map.store_item("Абаев", "Сергей")
        self.assertEqual(hash_map.get_length(), 1)
        hash_map.remove_item("Абаев")
        self.assertEqual(hash_map.get_length(), 0)

    def test_process_input(self):
        hash_map = Hash_map()
        self.assertEqual(hash_map.process_input("123"), 123)
        self.assertEqual(hash_map.process_input("abc"), "abc")

    def test_collision_handling(self):
        hash_map = Hash_map(base_capacity=2)
        hash_map.store_item("АА", "Data1")
        hash_map.store_item("АБ", "Data2")  # Должно вызвать коллизию
        pos1 = hash_map.find_slot("АА", is_for_addition=False)
        pos2 = hash_map.find_slot("АБ", is_for_addition=False)
        self.assertNotEqual(pos1, pos2)
        self.assertEqual(hash_map.storage[pos1]["collision_mark"], 0)
        self.assertEqual(hash_map.storage[pos2]["collision_mark"], 0)

    @patch('builtins.input', side_effect=['1', 'Иванов', 'Пётр', '2', 'Иванов', '3', 'Иванов', '4', 'Иванов', 'Сергей', '0'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_begin_interactive(self, mock_stdout, mock_input):
        hash_map = Hash_map()
        hash_map.begin()
        output = mock_stdout.getvalue()
        self.assertEqual(hash_map.get_length(), 13)
        self.assertIn("Запись добавлена", output)
        self.assertIn("Результат: Пётр", output)
        self.assertIn("Запись удалена", output)
        self.assertEqual(hash_map.get_length(), 13)

        pos = hash_map.find_slot("Иванов", is_for_addition=False)
        self.assertIn("Программа завершена", output)

    @patch('builtins.input', side_effect=['5', '0'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_begin_invalid_input(self, mock_stdout, mock_input):
        hash_map = Hash_map()
        hash_map.begin()
        output = mock_stdout.getvalue()
        self.assertIn("Неверный ввод, попробуйте снова", output)
        self.assertIn("Программа завершена", output)

    @patch('builtins.input', side_effect=['1', 'Абаев', 'Иван', '0'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_begin_duplicate_key(self, mock_stdout, mock_input):
        hash_map = Hash_map()
        hash_map.begin()
        output = mock_stdout.getvalue()
        self.assertIn("Ключ 'Абаев' уже существует", output)

if __name__ == '__main__':
    unittest.main()