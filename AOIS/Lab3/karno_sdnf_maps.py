from logical_operations import LogicalOperations

class KarnoSDNF(LogicalOperations):
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels
        self.var_count = len(labels)
        self.order = [0, 1, 3, 2]

    def make_map_5(self):
        grid = [[[0] * 4 for _ in range(4)] for _ in range(2)]
        ones = []
        for row in self.inputs:
            bit_1, bit_2, bit_3, bit_4, bit_5 = row[0]
            block = bit_5
            row_i = self.order.index((bit_1 << 1) | bit_2)
            col_i = self.order.index((bit_3 << 1) | bit_4)
            grid[block][row_i][col_i] = row[1]
            if row[1] == 1:
                ones.append((bit_1, bit_2, bit_3, bit_4, bit_5))
        return grid, ones

    def make_map_6(self):
        grid = [[[[0] * 4 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        ones = []
        for row in self.inputs:
            bit_1, bit_2, bit_3, bit_4, bit_5, bit_6 = row[0]
            block_i = self.order.index((bit_5 << 1) | bit_6)
            row_i = self.order.index((bit_1 << 1) | bit_2)
            col_i = self.order.index((bit_3 << 1) | bit_4)
            grid[block_i][row_i][col_i] = row[1]
            if row[1] == 1:
                ones.append((bit_1, bit_2, bit_3, bit_4, bit_5, bit_6))
        return grid, ones

    def show_map_5(self, grid):
        print("Карта Карно:")
        print("ab\\cde   000  001  011  010   110  111  101  100")
        for row in range(4):
            label = format(self.order[row], '02b')
            line = f"{label}       "
            part1 = [str(grid[0][row][c]) for c in range(4)]
            part2 = [str(grid[1][row][c]) for c in range(4)]
            line += "  ".join(f"{v:>3}" for v in part1) + "  " + "  ".join(f"{v:>3}" for v in part2)
            print(line)

    def show_map_6(self, grid):
        print("Карта Карно:")
        print("ef ab\\cd   0000  0001  0011  0010   0100  0101  0111  0110   1100  1101  1111  1110   1000  1001  1011  1010")
        for row in range(4):
            label = format(self.order[row], '02b')
            line = f"  {label}       "
            for b in range(4):
                vals = [str(grid[b][row][c]) for c in range(4)]
                line += "  ".join(f"{v:>3}" for v in vals) + "  "
            print(line)

    def get_cells_5_6(self, grid, b_start, b_size, r_start, r_size, c_start, c_size, b_max, r_max, c_max):
        cells = set()
        all_ones = True
        for db in range(b_size):
            block_index = (b_start + db) % b_max
            for dr in range(r_size):
                row_index = (r_start + dr) % r_max
                for dc in range(c_size):
                    column_index = (c_start + dc) % c_max
                    cells.add((block_index, row_index, column_index))
                    if grid[block_index][row_index][column_index] == 0:
                        all_ones = False
                        break
                if not all_ones:
                    break
            if not all_ones:
                break
        return cells, all_ones

    def make_pattern_5_6(self, cells):
        pattern = ['-'] * self.var_count
        values = []
        for block_index, row_index, column_index in cells:
            ab = self.order[row_index]
            cd = self.order[column_index]
            a_val = (ab >> 1) & 1
            b_val = ab & 1
            c_val = (cd >> 1) & 1
            d = cd & 1
            if self.var_count == 5:
                values.append([a_val, b_val, c_val, d, block_index])
            else:
                ef = self.order[block_index]
                e = (ef >> 1) & 1
                f = ef & 1
                values.append([a_val, b_val, c_val, d, e, f])
        for i in range(self.var_count):
            unique_vals = {val[i] for val in values}
            if len(unique_vals) == 1:
                pattern[i] = str(unique_vals.pop())
        return pattern

    def find_groups_5_6(self, grid, b_max):
        groups = []
        for b_size in [1, 2, 4][:b_max + 1]:
            for b_start in range(b_max):
                if b_size > 1 and b_start != 0:
                    continue
                for r_size in [1, 2, 4]:
                    for c_size in [1, 2, 4]:
                        for r_start in range(4):
                            for c_start in range(4):
                                cells, all_ones = self.get_cells_5_6(grid, b_start, b_size, r_start, r_size, c_start, c_size, b_max, 4, 4)
                                if all_ones and cells:
                                    pattern = self.make_pattern_5_6(cells)
                                    groups.append((cells, pattern))
        return groups

    def get_biggest_groups(self, groups):
        biggest = []
        for i, (cells_i, pat_i) in enumerate(groups):
            is_biggest = True
            for j, (cells_j, pat_j) in enumerate(groups):
                if i != j and cells_i <= cells_j and cells_i != cells_j:
                    is_biggest = False
                    break
            if is_biggest:
                biggest.append((cells_i, pat_i))
        return biggest

    def get_ones_pos_5_6(self, ones):
        positions = []
        for p in ones:
            if self.var_count == 5:
                bit_1, bit_2, bit_3, bit_4, bit_5 = p
                positions.append((bit_5, self.order.index((bit_1 << 1) | bit_2), self.order.index((bit_3 << 1) | bit_4)))
            else:
                bit_1, bit_2, bit_3, bit_4, bit_5, f = p
                positions.append((self.order.index((bit_5 << 1) | f), self.order.index((bit_1 << 1) | bit_2), self.order.index((bit_3 << 1) | bit_4)))
        return positions

    def choose_groups(self, big_groups, ones_pos):
        chosen = []
        to_cover = set(range(len(ones_pos)))
        for i, position in enumerate(ones_pos):
            covers = [idx for idx, (cells, _) in enumerate(big_groups) if position in cells]
            if len(covers) == 1:
                idx = covers[0]
                if idx not in chosen:
                    chosen.append(idx)
                    for j, other_pos in enumerate(ones_pos):
                        if other_pos in big_groups[idx][0]:
                            to_cover.discard(j)
        while to_cover:
            best_idx = None
            best_covered = set()
            for idx, (cells, _) in enumerate(big_groups):
                if idx in chosen:
                    continue
                covered = {j for j in to_cover if ones_pos[j] in cells}
                if len(covered) > len(best_covered):
                    best_covered = covered
                    best_idx = idx
            if best_idx is None:
                print("Не удалось покрыть все единицы!")
                break
            chosen.append(best_idx)
            to_cover -= best_covered
        return chosen

    def make_result(self, chosen, big_groups):
        terms = set()
        for idx in chosen:
            pattern = big_groups[idx][1]
            term = []
            for i, value in enumerate(pattern):
                if value == '1':
                    term.append(self.labels[i])
                elif value == '0':
                    term.append(f'!{self.labels[i]}')
            if term:
                term_str = term[0] if len(term) == 1 else '(' + ' ∧ '.join(sorted(term)) + ')'
                terms.add(term_str)
        terms = sorted(terms)
        return "0" if not terms else " ∨ ".join(terms)

    def karno_sdnf(self):
        if self.var_count not in [5, 6]:
            return "Метод работает только с 5 или 6 переменными."
        print(f"\nСокращаем СДНФ с помощью карты Карно ({self.var_count} переменных):")
        if self.var_count == 5:
            grid, ones = self.make_map_5()
            self.show_map_5(grid)
            b_max = 2
        else:
            grid, ones = self.make_map_6()
            self.show_map_6(grid)
            b_max = 4
        if not ones:
            return "0"
        groups = self.find_groups_5_6(grid, b_max)
        big_groups = self.get_biggest_groups(groups)
        ones_pos = self.get_ones_pos_5_6(ones)
        chosen = self.choose_groups(big_groups, ones_pos)
        return self.make_result(chosen, big_groups)

    def make_map_1_to_4(self):
        ones = []
        if self.var_count == 1:
            grid = [0] * 2
            for row in self.inputs:
                bit_1, = row[0]
                grid[bit_1] = row[1]
                if row[1] == 1:
                    ones.append((bit_1,))
        elif self.var_count == 2:
            grid = [[0] * 2 for _ in range(2)]
            for row in self.inputs:
                bit_1, bit_2 = row[0]
                grid[bit_1][bit_2] = row[1]
                if row[1] == 1:
                    ones.append((bit_1, bit_2))
        elif self.var_count == 3:
            grid = [[0] * 4 for _ in range(2)]
            for row in self.inputs:
                bit_1, bit_2, bit_3 = row[0]
                grid[bit_1][self.order.index((bit_2 << 1) | bit_3)] = row[1]
                if row[1] == 1:
                    ones.append((bit_1, bit_2, bit_3))
        else:
            grid = [[0] * 4 for _ in range(4)]
            for row in self.inputs:
                bit_1, bit_2, bit_3, d = row[0]
                grid[self.order.index((bit_1 << 1) | bit_2)][self.order.index((bit_3 << 1) | d)] = row[1]
                if row[1] == 1:
                    ones.append((bit_1, bit_2, bit_3, d))
        return grid, ones

    def show_map_1_to_4(self, grid):
        print("Карта Карно:")
        if self.var_count == 1:
            print("a    0  1")
            print("     " + "  ".join(str(grid[i]) for i in range(2)))
        elif self.var_count == 2:
            print("a\\b   0  1")
            for row in range(2):
                print(f"{row}     " + "  ".join(str(grid[row][c]) for c in range(2)))
        elif self.var_count == 3:
            print("a\\bc   00  01  11  10")
            for row in range(2):
                print(f"{row}     " + "  ".join(f"{grid[row][c]:>3}" for c in range(4)))
        else:
            print("ab\\cd   00  01  11  10")
            for row in range(4):
                label = format(self.order[row], '02b')
                print(f"{label}     " + "  ".join(f"{grid[row][c]:>3}" for c in range(4)))

    def get_cells_1_to_4(self, grid, r_start, r_size, c_start, c_size, r_max, c_max):
        cells = set()
        all_ones = True
        for dr in range(r_size):
            row = (r_start + dr) % r_max
            for dc in range(c_size):
                column = (c_start + dc) % c_max
                cells.add((row, column))
                val = grid[column] if self.var_count == 1 else grid[row][column]
                if val == 0:
                    all_ones = False
                    break
            if not all_ones:
                break
        return cells, all_ones

    def make_pattern_1_to_4(self, cells):
        pattern = ['-'] * self.var_count
        values = []
        for row, column in cells:
            if self.var_count == 1:
                values.append([column])
            elif self.var_count == 2:
                values.append([row, column])
            elif self.var_count == 3:
                bc = self.order[column]
                values.append([row, (bc >> 1) & 1, bc & 1])
            else:
                ab = self.order[row]
                cd = self.order[column]
                values.append([(ab >> 1) & 1, ab & 1, (cd >> 1) & 1, cd & 1])
        for i in range(self.var_count):
            unique_vals = {val[i] for val in values}
            if len(unique_vals) == 1:
                pattern[i] = str(unique_vals.pop())
        return pattern

    def find_groups_1_to_4(self, grid, r_max, c_max):
        groups = []
        row_sizes = [1, 2] if r_max <= 2 else [1, 2, 4]
        col_sizes = [1, 2] if c_max == 2 else [1, 2, 4]
        for r_size in row_sizes:
            for c_size in col_sizes:
                for r_start in range(r_max):
                    for c_start in range(c_max):
                        cells, all_ones = self.get_cells_1_to_4(grid, r_start, r_size, c_start, c_size, r_max, c_max)
                        if all_ones and cells:
                            pattern = self.make_pattern_1_to_4(cells)
                            groups.append((cells, pattern))
        return groups

    def get_ones_pos_1_to_4(self, ones):
        positions = []
        for pos in ones:
            if self.var_count == 1:
                positions.append((0, pos[0]))
            elif self.var_count == 2:
                positions.append((pos[0], pos[1]))
            elif self.var_count == 3:
                positions.append((pos[0], self.order.index((pos[1] << 1) | pos[2])))
            else:
                positions.append((self.order.index((pos[0] << 1) | pos[1]), self.order.index((pos[2] << 1) | pos[3])))
        return positions

    def karno_1_to_4_sdnf(self):
        if self.var_count not in [1, 2, 3, 4]:
            return "Метод работает только с 1, 2, 3 или 4 переменными."
        print(f"\nСокращаем СДНФ с помощью карты Карно ({self.var_count} переменных):")
        grid, ones = self.make_map_1_to_4()
        self.show_map_1_to_4(grid)
        if not ones:
            return "0"
        r_max = 1 if self.var_count == 1 else 2 if self.var_count in [2, 3] else 4
        c_max = 2 if self.var_count in [1, 2] else 4
        groups = self.find_groups_1_to_4(grid, r_max, c_max)
        big_groups = self.get_biggest_groups(groups)
        ones_pos = self.get_ones_pos_1_to_4(ones)
        chosen = self.choose_groups(big_groups, ones_pos)
        return self.make_result(chosen, big_groups)
