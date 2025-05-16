class Matrix:
    def __init__(self, matrix_data):
        self.row_count = len(matrix_data)
        self.col_count = len(matrix_data[0]) if matrix_data else 0
        if not matrix_data or not all(len(row) == self.col_count for row in matrix_data):
            raise ValueError("Входная сетка должна быть правильной.")
        self.data_grid = [row[:] for row in matrix_data]

    def extract_sequence(self, start_row, start_col):
        if not (0 <= start_row < self.row_count and 0 <= start_col < self.col_count):
            raise ValueError("Начальные индексы выходят за пределы сетки.")
        sequence = []
        current_row = start_row
        current_col = start_col
        for _ in range(self.row_count):
            if not (0 <= current_row < self.row_count and 0 <= current_col < self.col_count):
                raise IndexError("Индексы вышли за пределы при извлечении последовательности.")
            sequence.append(self.data_grid[current_row][current_col])
            current_row = (current_row + 1) % self.row_count
        return sequence

    def store_sequence(self, sequence, start_row, start_col):
        if not sequence or not all(bit in (0, 1) for bit in sequence):
            raise ValueError("Последовательность должна содержать только биты 0 или 1.")
        if len(sequence) != self.row_count:
            raise ValueError("Длина последовательности должна совпадать с количеством строк.")
        if not (0 <= start_row < self.row_count and 0 <= start_col < self.col_count):
            raise ValueError("Начальные индексы выходят за пределы сетки.")
        current_row = start_row
        current_col = start_col
        for bit in sequence:
            if not (0 <= current_row < self.row_count and 0 <= current_col < self.col_count):
                raise IndexError("Индексы вышли за пределы при записи последовательности.")
            self.data_grid[current_row][current_col] = int(bit)
            current_row = (current_row + 1) % self.row_count

    def show_matrix(self):
        for row in self.data_grid:
            print(row)

    def make_f5(self, source_col, target_col):
        if not (0 <= source_col < self.col_count and 0 <= target_col < self.col_count):
            raise ValueError("Индексы столбцов выходят за пределы сетки.")
        source_data = self.extract_sequence(0, source_col)
        self.store_sequence(source_data, target_col, target_col)
        return source_data

    def make_f10(self, source_col, target_col):
        if not (0 <= source_col < self.col_count and 0 <= target_col < self.col_count):
            raise ValueError("Индексы столбцов выходят за пределы сетки.")
        source_data = self.extract_sequence(0, source_col)
        result_data = [1 - bit for bit in source_data]
        self.store_sequence(result_data, target_col, target_col)
        return result_data

    def make_f0(self, target_col):
        if not (0 <= target_col < self.col_count):
            raise ValueError("Индекс целевого столбца выходит за пределы сетки.")
        zero_data = [0] * self.row_count
        self.store_sequence(zero_data, target_col, target_col)
        return zero_data

    def make_f15(self, target_col):
        if not (0 <= target_col < self.col_count):
            raise ValueError("Индекс целевого столбца выходит за пределы сетки.")
        one_data = [1] * self.row_count
        self.store_sequence(one_data, target_col, target_col)
        return one_data

    def compute_binary_sum(self, first_number, second_number):
        current_carry = 0
        length_of_first = len(first_number)
        length_of_second = len(second_number)
        longest_length = max(length_of_first, length_of_second)
        sum_result = [0 for _ in range(longest_length + 1)]

        for position_from_right in range(longest_length):
            reverse_index = -1 - position_from_right

            if position_from_right < length_of_first:
                current_bit_first = first_number[reverse_index]
            else:
                current_bit_first = 0

            if position_from_right < length_of_second:
                current_bit_second = second_number[reverse_index]
            else:
                current_bit_second = 0

            sum_of_bits = current_bit_first + current_bit_second + current_carry
            current_result_bit = sum_of_bits % 2
            sum_result[reverse_index] = current_result_bit
            current_carry = sum_of_bits // 2

        if current_carry == 1:
            sum_result[0] = 1
        if sum_result[0] == 0:
            sum_result = sum_result[1:]

        final_length = min(len(sum_result), 5)
        return sum_result[:final_length]

    def process_fields(self, matching_criterion):
        pattern_length = len(matching_criterion)
        expected_pattern_length = 3
        valid_bits = [0, 1]
        is_pattern_length_correct = pattern_length == expected_pattern_length
        are_bits_valid = True
        for bit in matching_criterion:
            bit_is_valid = bit in valid_bits
            if not bit_is_valid:
                are_bits_valid = False
                break
        if not is_pattern_length_correct or not are_bits_valid:
            raise ValueError("Шаблон должен содержать ровно 3 бита (0 или 1).")

        list_of_updated_records = []

        total_columns = self.col_count
        column_index = 0
        while column_index < total_columns:
            total_rows = self.row_count
            row_shift_index = 0
            while row_shift_index < total_rows:
                starting_row = column_index + row_shift_index
                starting_row = starting_row % total_rows

                extracted_sequence = self.extract_sequence(starting_row, column_index)
                pattern_to_check = []
                pattern_to_check.extend(extracted_sequence[0:3])
                patterns_match = True
                for i in range(expected_pattern_length):
                    if pattern_to_check[i] != matching_criterion[i]:
                        patterns_match = False
                        break

                if patterns_match:
                    first_number_bits = []
                    first_number_bits.extend(extracted_sequence[3:7])
                    second_number_bits = []
                    second_number_bits.extend(extracted_sequence[7:11])

                    sum_of_numbers = self.compute_binary_sum(first_number_bits, second_number_bits)

                    current_sum_length = len(sum_of_numbers)
                    required_sum_length = 5
                    while current_sum_length < required_sum_length:
                        sum_of_numbers.insert(0, 0)
                        current_sum_length = len(sum_of_numbers)

                    new_sequence = []
                    new_sequence.extend(pattern_to_check)
                    new_sequence.extend(first_number_bits)
                    new_sequence.extend(second_number_bits)
                    new_sequence.extend(sum_of_numbers)
                    self.store_sequence(new_sequence, starting_row, column_index)

                    update_info = (column_index, new_sequence)
                    list_of_updated_records.append(update_info)
                    break

                row_shift_index = row_shift_index + 1
            column_index = column_index + 1

        return list_of_updated_records

    def find_match(self, search_pattern):
        if len(search_pattern) != self.row_count:
            raise ValueError("Длина поискового образца должна совпадать с количеством строк.")
        top_score = -1
        best_candidates = []
        for col_idx in range(self.col_count):
            current_word = self.extract_sequence(0, col_idx)
            greater_flags = [0] * len(current_word)
            lesser_flags = [0] * len(current_word)
            match_count = 0
            for i in range(len(current_word)):
                if current_word[i] > search_pattern[i]:
                    greater_flags[i] = 1
                elif current_word[i] < search_pattern[i]:
                    lesser_flags[i] = 1
                if greater_flags[i] == 0 and lesser_flags[i] == 0:
                    match_count += 1
            if match_count > top_score:
                top_score = match_count
                best_candidates = [(col_idx, current_word)]
            elif match_count == top_score:
                best_candidates.append((col_idx, current_word))
        return best_candidates, top_score

begin_matrix = [
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

grid = Matrix(begin_matrix)

print("Исходная матрица:")
grid.show_matrix()

print("\nИзвлечение последовательности 0 (начиная с позиции (0,0)):")
seq_0 = grid.extract_sequence(0, 0)
print(f"Последовательность 0: \n{seq_0}")

print("\nИзвлечение последовательности 1 (начиная с позиции (1,1)):")
seq_1 = grid.extract_sequence(1, 1)
print(f"Последовательность 1: \n{seq_1}")

print("\nИзвлечение диагональной последовательности 3 (начиная с позиции (3,0)):")
diag_seq_3 = grid.extract_sequence(3, 0)
print(f"Диагональная последовательность 3: \n{diag_seq_3}")

print("\nПрименение операции копирования (f0) от столбца 0 к 2:")
result_f0 = grid.make_f0(2)
print(f"Результат (столбец 2): \n{result_f0}")
grid.show_matrix()

print("\nПрименение операции копирования (f5) от столбца 1 к 3:")
result_f5 = grid.make_f5(1, 3)
print(f"Результат (столбец 3): \n{result_f5}")
grid.show_matrix()

print("\nПрименение операции инверсии (f10) от столбца 1 к 4:")
result_f10 = grid.make_f10(1, 4)
print(f"Результат (столбец 4): \n{result_f10}")
grid.show_matrix()

print("\nПрименение операции заполнения 1 (f15) к столбцу 5:")
result_f15 = grid.make_f15(5)
print(f"Результат (столбец 5): \n{result_f15}")
grid.show_matrix()

print("\nОбработка полей с фильтром [1, 0, 1]:")
updated_entries = grid.process_fields([1, 0, 1])
print("Обновленные записи (индекс столбца, новое слово):")
for col, word in updated_entries:
    pattern = word[:3]
    part_a = word[3:7]
    part_b = word[7:11]
    sum_part = word[11:]
    print(f"Столбец {col}: P={pattern}, A={part_a}, B={part_b}, S={sum_part}")
grid.show_matrix()

print("\nПоиск лучших совпадений с образцом [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1]:")
top_matches, max_score = grid.find_match([1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1])
print("Лучшие совпадения (индекс столбца, слово):")
for col, word in top_matches:
    print(f"Столбец {col}: {word}")
print(f"Максимальное число совпадений: {max_score}")