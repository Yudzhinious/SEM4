from logical_operations import *

class KarnoSKNF(LogicalOperations):
    def __init__(self, inputs, labels):
        super().__init__()
        self.inputs = inputs
        self.labels = labels
        self.var_count = len(labels)
        self.order = [0, 1, 3, 2]

    def make_map_5(self):
        karnaugh_map = [[[0] * 4 for _ in range(4)] for _ in range(2)]
        zero_positions = []
        for row in self.inputs:
            bit_1, bit_2, bit_3, bit_4, bit_5 = row[0]
            block_index = bit_5
            row_index = self.order.index((bit_1 << 1) | bit_2)
            col_index = self.order.index((bit_3 << 1) | bit_4)
            karnaugh_map[block_index][row_index][col_index] = row[1]
            if row[1] == 0:
                zero_positions.append((bit_1, bit_2, bit_3, bit_4, bit_5))
        return karnaugh_map, zero_positions

    def make_map_6(self):
        karnaugh_map = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        zero_positions = []
        for row in self.inputs:
            bit_1, bit_2, bit_3, bit_4, bit_5, bit_6 = row[0]
            block_index = self.order.index((bit_5 << 1) | bit_6)
            row_index = self.order.index((bit_1 << 1) | bit_2)
            col_index = self.order.index((bit_3 << 1) | bit_4)
            karnaugh_map[block_index][row_index][col_index] = row[1]
            if row[1] == 0:
                zero_positions.append((bit_1, bit_2, bit_3, bit_4, bit_5, bit_6))
        return karnaugh_map, zero_positions

    def show_map_5(self, karnaugh_map):
        print("Карта Карно:")
        print("ab\\cde   000  001  011  010   110  111  101  100")
        for row in range(4):
            label = format(self.order[row], '02b')
            line = f"{label}       "
            part1 = [str(karnaugh_map[0][row][c]) for c in range(4)]
            part2 = [str(karnaugh_map[1][row][c]) for c in range(4)]
            line += "  ".join(f"{v:>3}" for v in part1) + "  " + "  ".join(f"{v:>3}" for v in part2)
            print(line)

    def show_map_6(self, karnaugh_map):
        print("Карта Карно:")
        print("ef ab\\cd   0000  0001  0011  0010   0100  0101  0111  0110   1100  1101  1111  1110   1000  1001  1011  1010")
        for row in range(4):
            label = format(self.order[row], '02b')
            line = f"  {label}       "
            for b in range(4):
                vals = [str(karnaugh_map[b][row][c]) for c in range(4)]
                line += "  ".join(f"{v:>3}" for v in vals) + "  "
            print(line)

    def get_cells_5_6(self, karnaugh_map, block_start, block_size, row_start, row_size, col_start, col_size, max_blocks, max_rows, max_cols):
        covered_cells = set()
        all_zeros_flag = True
        for db in range(block_size):
            block_index = (block_start + db) % max_blocks
            for dr in range(row_size):
                    covered_cells.add((block_index, row_index, col_index))
                    if karnaugh_map[block_index][row_index][col_index] == 1:
                        all_zeros_flag = False
                        break
                if not all_zeros_flag:
                    break
            if not all_zeros_flag:
                break
        return covered_cells, all_zeros_flag

    def make_pattern_5_6(self, covered_cells):
        maxterm_pattern = ['-'] * self.var_count
        values = []
        for block_index, row_index, col_index in covered_cells:
            ab = self.order[row_index]
            cd = self.order[col_index]
            bit_1 = (ab >> 1) & 1
            bit_2 = ab & 1
            bit_3 = (cd >> 1) & 1
            bit_4 = cd & 1
            if self.var_count == 5:
                bit_5 = block_index
                values.append([bit_1, bit_2, bit_3, bit_4, bit_5])
            else:
                ef = self.order[block_index]
                bit_5 = (ef >> 1) & 1
                bit_6 = ef & 1
                values.append([bit_1, bit_2, bit_3, bit_4, bit_5, bit_6])
        for i in range(self.var_count):
            unique_vals = {val[i] for val in values}
            if len(unique_vals) == 1:
                maxterm_pattern[i] = str(unique_vals.pop())
        return maxterm_pattern

    def find_groups_5_6(self, karnaugh_map, max_blocks):
        groups = []
        for block_size in [1, 2, 4][:max_blocks + 1]:
            for block_start in range(max_blocks):
                if block_size > 1 and block_start != 0:
                    continue
                for row_size in [1, 2, 4]:
                    for col_size in [1, 2, 4]:
                                covered_cells, all_zeros_flag = self.get_cells_5_6(karnaugh_map, block_start, block_size, row_start, row_size, col_start, col_size, max_blocks, 4, 4)
                                if all_zeros_flag and covered_cells:
                                    maxterm_pattern = self.make_pattern_5_6(covered_cells)
                                    groups.append((covered_cells, maxterm_pattern))
        return groups

    def get_biggest_groups(self, groups):
        largest_groups = []
        for i, (covered_cells_i, maxterm_pattern_i) in enumerate(groups):
            is_biggest = True
            for j, (covered_cells_j, maxterm_pattern_j) in enumerate(groups):
                if i != j and covered_cells_i <= covered_cells_j and covered_cells_i != covered_cells_j:
                    is_biggest = False
                    break
            if is_biggest:
                largest_groups.append((covered_cells_i, maxterm_pattern_i))
        return largest_groups

    def get_zeros_pos_5_6(self, zero_positions):
        positions = []
        for p in zero_positions:
            if self.var_count == 5:
                bit_1, bit_2, bit_3, bit_4, bit_5 = p
                positions.append((bit_5, self.order.index((bit_1 << 1) | bit_2), self.order.index((bit_3 << 1) | bit_4)))
            else:
                bit_1, bit_2, bit_3, bit_4, bit_5, bit_6 = p
                positions.append((self.order.index((bit_5 << 1) | bit_6), self.order.index((bit_1 << 1) | bit_2), self.order.index((bit_3 << 1) | bit_4)))
        return positions

    def choose_groups(self, largest_groups, zeros_pos, verbose):
        selected_groups = []
        to_cover = set(range(len(zeros_pos)))
        for i, pos in enumerate(zeros_pos):
            covers = [idx for idx, (covered_cells, _) in enumerate(largest_groups) if pos in covered_cells]
            if len(covers) == 1:
                idx = covers[0]
                if idx not in selected_groups:
                    selected_groups.append(idx)
                    for j, other_pos in enumerate(zeros_pos):
                        if other_pos in largest_groups[idx][0]:
                            to_cover.discard(j)
        while to_cover:
            best_idx = None
            best_covered = set()
            for idx, (covered_cells, _) in enumerate(largest_groups):
                if idx in selected_groups:
                    continue
                covered = {j for j in to_cover if zeros_pos[j] in covered_cells}
                if len(covered) > len(best_covered):
                    best_covered = covered
                    best_idx = idx
            if best_idx is None:
                if verbose:
                    print("Не удалось покрыть все нули!")
                break
            selected_groups.append(best_idx)
            to_cover -= best_covered
        return selected_groups

    def make_result(self, selected_groups, largest_groups):
        maxterms = set()
        for idx in selected_groups:
            maxterm_pattern = largest_groups[idx][1]
            term = []
            for i, val in enumerate(maxterm_pattern):
                if val == '0':
                    term.append(self.labels[i])
                elif val == '1':
                    term.append(f'!{self.labels[i]}')
            if term:
                term_str = term[0] if len(term) == 1 else '(' + ' ∨ '.join(sorted(term)) + ')'
                maxterms.add(term_str)
        maxterms = sorted(maxterms)
        result = "1" if not maxterms else " ∧ ".join(maxterms)
        return result

    def karno_sknf(self, verbose=True):
        if self.var_count not in [5, 6]:
            return "Этот метод не поддерживает такое количество переменных."
        if verbose:
            print(f"\nСокращаем СКНФ с помощью карты Карно ({self.var_count} переменных):")
        if self.var_count == 5:
            karnaugh_map, zero_positions = self.make_map_5()
            if verbose:
                self.show_map_5(karnaugh_map)
            max_blocks = 2
        else:
            karnaugh_map, zero_positions = self.make_map_6()
            if verbose:
                self.show_map_6(karnaugh_map)
            max_blocks = 4
        if not zero_positions:
            return "1"
        groups = self.find_groups_5_6(karnaugh_map, max_blocks)
        largest_groups = self.get_biggest_groups(groups)
        zeros_pos = self.get_zeros_pos_5_6(zero_positions)
        selected_groups = self.choose_groups(largest_groups, zeros_pos, verbose)
        return self.make_result(selected_groups, largest_groups)

    def make_map_1_to_4(self):
        zero_positions = []
        if self.var_count == 1:
            karnaugh_map = [0] * 2
            for row in self.inputs:
                bit_1, = row[0]
                karnaugh_map[bit_1] = row[1]
                if row[1] == 0:
                    zero_positions.append((bit_1,))
        elif self.var_count == 2:
            karnaugh_map = [[0] * 2 for _ in range(2)]
            for row in self.inputs:
                bit_1, bit_2 = row[0]
                karnaugh_map[bit_1][bit_2] = row[1]
                if row[1] == 0:
                    zero_positions.append((bit_1, bit_2))
        elif self.var_count == 3:
            karnaugh_map = [[0] * 4 for _ in range(2)]
            for row in self.inputs:
                bit_1, bit_2, bit_3 = row[0]
                karnaugh_map[bit_1][self.order.index((bit_2 << 1) | bit_3)] = row[1]
                if row[1] == 0:
                    zero_positions.append((bit_1, bit_2, bit_3))
        else:
            karnaugh_map = [[0] * 4 for _ in range(4)]
            for row in self.inputs:
                bit_1, bit_2, bit_3, bit_4 = row[0]
                karnaugh_map[self.order.index((bit_1 << 1) | bit_2)][self.order.index((bit_3 << 1) | bit_4)] = row[1]
                if row[1] == 0:
                    zero_positions.append((bit_1, bit_2, bit_3, bit_4))
        return karnaugh_map, zero_positions

    def show_map_1_to_4(self, karnaugh_map):
        print("Карта Карно:")
        if self.var_count == 1:
            print("a    0  1")
            print("     " + "  ".join(str(karnaugh_map[i]) for i in range(2)))
        elif self.var_count == 2:
            print("a\\b   0  1")
            for row in range(2):
                print(f"{row}     " + "  ".join(str(karnaugh_map[row][c]) for c in range(2)))
        elif self.var_count == 3:
            print("a\\bc   00  01  11  10")
            for row in range(2):
                print(f"{row}     " + "  ".join(f"{karnaugh_map[row][c]:>3}" for c in range(4)))
        else:
            print("ab\\cd   00  01  11  10")
            for row in range(4):
                label = format(self.order[row], '02b')
                print(f"{label}     " + "  ".join(f"{karnaugh_map[row][c]:>3}" for c in range(4)))

    def get_cells_1_to_4(self, karnaugh_map, row_start, row_size, col_start, col_size, max_rows, max_cols):
        covered_cells = set()
        all_zeros_flag = True
        for dr in range(row_size):
            row_index = (row_start + dr) % max_rows
            for dc in range(col_size):
                col_index = (col_start + dc) % max_cols
                covered_cells.add((row_index, col_index))
                val = karnaugh_map[col_index] if self.var_count == 1 else karnaugh_map[row_index][col_index]
                if val == 1:
                    all_zeros_flag = False
                    break
            if not all_zeros_flag:
                break
        return covered_cells, all_zeros_flag

    def make_pattern_1_to_4(self, covered_cells):
        maxterm_pattern = ['-'] * self.var_count
        values = []
        for row_index, col_index in covered_cells:
            if self.var_count == 1:
                values.append([col_index])
            elif self.var_count == 2:
                values.append([row_index, col_index])
            elif self.var_count == 3:
                bc = self.order[col_index]
                values.append([row_index, (bc >> 1) & 1, bc & 1])
            else:
                ab = self.order[row_index]
                cd = self.order[col_index]
                values.append([(ab >> 1) & 1, ab & 1, (cd >> 1) & 1, cd & 1])
        for i in range(self.var_count):
            unique_vals = {val[i] for val in values}
            if len(unique_vals) == 1:
                maxterm_pattern[i] = str(unique_vals.pop())
        return maxterm_pattern

    def find_groups_1_to_4(self, karnaugh_map, max_rows, max_cols):
        groups = []
        row_sizes = [1, 2] if max_rows <= 2 else [1, 2, 4]
        col_sizes = [1, 2] if max_cols == 2 else [1, 2, 4]
        for row_size in row_sizes:
            for col_size in col_sizes:
                        covered_cells, all_zeros_flag = self.get_cells_1_to_4(karnaugh_map, row_start, row_size, col_start, col_size, max_rows, max_cols)
                        if all_zeros_flag and covered_cells:
                            maxterm_pattern = self.make_pattern_1_to_4(covered_cells)
                            groups.append((covered_cells, maxterm_pattern))
        return groups

    def get_zeros_pos_1_to_4(self, zero_positions):
        positions = []
        for p in zero_positions:
            if self.var_count == 1:
                positions.append((0, p[0]))
            elif self.var_count == 2:
                positions.append((p[0], p[1]))
            elif self.var_count == 3:
                positions.append((p[0], self.order.index((p[1] << 1) | p[2])))
            else:
                positions.append((self.order.index((p[0] << 1) | p[1]), self.order.index((p[2] << 1) | p[3])))
        return positions

    def karno_1_to_4_sknf(self, verbose=True):
        if self.var_count not in [1, 2, 3, 4]:
            return "Этот метод работает только для 1–4 переменных."
        if verbose:
            print(f"\nУпрощаем СКНФ через карту Карно ({self.var_count} переменных):")
        karnaugh_map, zero_positions = self.make_map_1_to_4()
        if verbose:
            self.show_map_1_to_4(karnaugh_map)
        if not zero_positions:
            return "1"
        max_rows = 1 if self.var_count == 1 else 2 if self.var_count in [2, 3] else 4
        max_cols = 2 if self.var_count in [1, 2] else 4
        groups = self.find_groups_1_to_4(karnaugh_map, max_rows, max_cols)
        largest_groups = self.get_biggest_groups(groups)
        zeros_pos = self.get_zeros_pos_1_to_4(zero_positions)
        selected_groups = self.choose_groups(largest_groups, zeros_pos, verbose)
        return self.make_result(selected_groups, largest_groups)
