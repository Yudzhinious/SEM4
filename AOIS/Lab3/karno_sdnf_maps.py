from logical_operations import LogicalOperations

class KarnoSDNF(LogicalOperations):
    def __init__(self, inputs: list, labels: list):
        self.inputs = inputs
        self.labels = labels
        self.var_count = len(labels)
        self.order = [0, 1, 3, 2]

    def karno_sdnf(self) -> str:
        if self.var_count not in [5, 6]:
            return "Метод работает только с 5 или 6 переменными."

        print(f"\nСокращаем СДНФ с помощью карты Карно ({self.var_count} переменных):")
        zeros = []
        if self.var_count == 5:
            map_grid = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(2)]
            for idx, row in enumerate(self.inputs):
                a, b, c, d, e = row[0]
                block = e
                row_idx = self.order.index((a << 1) | b)
                col_idx = self.order.index((c << 1) | d)
                map_grid[block][row_idx][col_idx] = row[1]
                if row[1] == 1:
                    zeros.append((a, b, c, d, e))

            print("Карта Карно:")
            print("ab\\cde   000  001  011  010   110  111  101  100")
            for r in range(4):
                row_label = format(self.order[r], '02b')
                line = f"{row_label}       "
                block_0 = [str(map_grid[0][r][c]) for c in range(4)]
                block_1 = [str(map_grid[1][r][c]) for c in range(4)]
                line += "  ".join(f"{val:>3}" for val in block_0)
                line += "  "
                line += "  ".join(f"{val:>3}" for val in block_1)
                print(line)

        else:
            map_grid = [[[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
            for idx, row in enumerate(self.inputs):
                a, b, c, d, e, f = row[0]
                block_idx = self.order.index((e << 1) | f)
                row_idx = self.order.index((a << 1) | b)
                col_idx = self.order.index((c << 1) | d)
                map_grid[block_idx][row_idx][col_idx] = row[1]
                if row[1] == 1:
                    zeros.append((a, b, c, d, e, f))

            print("Карта Карно:")
            print("ef ab\\cd   0000  0001  0011  0010   0100  0101  0111  0110   1100  1101  1111  1110   1000  1001  1011  1010")
            for r in range(4):
                row_label = format(self.order[r], '02b')
                line = f"  {row_label}       "
                for b in range(4):
                    block_vals = [str(map_grid[b][r][c]) for c in range(4)]
                    line += "  ".join(f"{val:>3}" for val in block_vals)
                    line += "  "
                print(line)

        if not zeros:
            return "0"

        block_count = 2 if self.var_count == 5 else 4
        row_count = 4
        col_count = 4

        rectangles = []
        for block_size in [1, 2, 4][:block_count + 1]:
            for block_start in range(block_count):
                if block_size > 1 and block_start != 0:
                    continue
                for row_size in [1, 2, 4]:
                    for col_size in [1, 2, 4]:
                        for row_start in range(row_count):
                            for col_start in range(col_count):
                                cells = set()
                                all_ones = True
                                for db in range(block_size):
                                    b = (block_start + db) % block_count
                                    for dr in range(row_size):
                                        r = (row_start + dr) % row_count
                                        for dc in range(col_size):
                                            c = (col_start + dc) % col_count
                                            cells.add((b, r, c))
                                            val = map_grid[b][r][c]
                                            if val == 0:
                                                all_ones = False
                                                break
                                        if not all_ones:
                                            break
                                    if not all_ones:
                                        break
                                if all_ones and cells:
                                    pattern = ['-' for _ in range(self.var_count)]
                                    cell_values = []
                                    for b, r, c in cells:
                                        ab = self.order[r]
                                        cd = self.order[c]
                                        a = (ab >> 1) & 1
                                        b_val = ab & 1
                                        c_val = (cd >> 1) & 1
                                        d = cd & 1
                                        if self.var_count == 5:
                                            e = b
                                            cell_values.append([a, b_val, c_val, d, e])
                                        else:
                                            ef = self.order[b]
                                            e = (ef >> 1) & 1
                                            f = ef & 1
                                            cell_values.append([a, b_val, c_val, d, e, f])
                                    for pos in range(self.var_count):
                                        values = set(val[pos] for val in cell_values)
                                        if len(values) == 1:
                                            pattern[pos] = str(values.pop())
                                    rectangles.append((cells, pattern))

        max_rectangles = []
        for i, (cells_i, pat_i) in enumerate(rectangles):
            is_max = True
            for j, (cells_j, pat_j) in enumerate(rectangles):
                if i != j and cells_i.issubset(cells_j) and cells_i != cells_j:
                    is_max = False
                    break
            if is_max:
                max_rectangles.append((cells_i, pat_i))

        one_coords = []
        for point in zeros:
            if self.var_count == 5:
                a, b, c, d, e = point
                one_coords.append((e, self.order.index((a << 1) | b), self.order.index((c << 1) | d)))
            else:
                a, b, c, d, e, f = point
                one_coords.append((self.order.index((e << 1) | f), self.order.index((a << 1) | b), self.order.index((c << 1) | d)))

        picked_rectangles = []
        ones_to_cover = set(range(len(one_coords)))

        for one_idx, coord in enumerate(one_coords):
            covering = [rect_idx for rect_idx, (cells, _) in enumerate(max_rectangles) if coord in cells]
            if len(covering) == 1:
                rect_idx = covering[0]
                if rect_idx not in picked_rectangles:
                    picked_rectangles.append(rect_idx)
                    for o_idx, o_coord in enumerate(one_coords):
                        if o_coord in max_rectangles[rect_idx][0]:
                            ones_to_cover.discard(o_idx)

        while ones_to_cover:
            best_rect = None
            best_covered = set()
            for rect_idx, (cells, _) in enumerate(max_rectangles):
                if rect_idx in picked_rectangles:
                    continue
                covered = {o_idx for o_idx in ones_to_cover if one_coords[o_idx] in cells}
                if len(covered) > len(best_covered):
                    best_covered = covered
                    best_rect = rect_idx
            if best_rect is None:
                print("Не удалось покрыть все единицы!")
                break
            picked_rectangles.append(best_rect)
            ones_to_cover -= best_covered

        terms = set()
        for rect_idx in picked_rectangles:
            _, pattern = max_rectangles[rect_idx]
            term = []
            for idx, val in enumerate(pattern):
                if val == '1':
                    term.append(self.labels[idx])
                elif val == '0':
                    term.append(f'!{self.labels[idx]}')
            if term:
                terms.add(term[0] if len(term) == 1 else '(' + ' ∧ '.join(sorted(term)) + ')')

        terms_list = sorted(terms)
        return "0" if not terms_list else " ∨ ".join(terms_list)

    def karno_1_to_4_sdnf(self) -> str:
        if self.var_count not in [1, 2, 3, 4]:
            return "Метод работает только с 1, 2, 3 или 4 переменными."

        print(f"\nСокращаем СДНФ с помощью карты Карно ({self.var_count} переменных):")
        ones = []
        if self.var_count == 1:
            map_grid = [0] * 2
            for idx, row in enumerate(self.inputs):
                a, = row[0]
                map_grid[a] = row[1]
                if row[1] == 1:
                    ones.append((a,))

            print("Карта Карно:")
            print("a    0  1")
            print("     " + "  ".join(f"{map_grid[i]:>1}" for i in range(2)))

        elif self.var_count == 2:
            map_grid = [[0] * 2 for _ in range(2)]
            for idx, row in enumerate(self.inputs):
                a, b = row[0]
                map_grid[a][b] = row[1]
                if row[1] == 1:
                    ones.append((a, b))

            print("Карта Карно:")
            print("a\\b   0  1")
            for r in range(2):
                print(f"{r}     " + "  ".join(f"{map_grid[r][c]:>1}" for c in range(2)))

        elif self.var_count == 3:
            map_grid = [[0] * 4 for _ in range(2)]
            for idx, row in enumerate(self.inputs):
                a, b, c = row[0]
                row_idx = a
                col_idx = self.order.index((b << 1) | c)
                map_grid[row_idx][col_idx] = row[1]
                if row[1] == 1:
                    ones.append((a, b, c))

            print("Карта Карно:")
            print("a\\bc   00  01  11  10")
            for r in range(2):
                print(f"{r}     " + "  ".join(f"{map_grid[r][c]:>3}" for c in range(4)))

        else:
            map_grid = [[0] * 4 for _ in range(4)]
            for idx, row in enumerate(self.inputs):
                a, b, c, d = row[0]
                row_idx = self.order.index((a << 1) | b)
                col_idx = self.order.index((c << 1) | d)
                map_grid[row_idx][col_idx] = row[1]
                if row[1] == 1:
                    ones.append((a, b, c, d))

            print("Карта Карно:")
            print("ab\\cd   00  01  11  10")
            for r in range(4):
                row_label = format(self.order[r], '02b')
                print(f"{row_label}     " + "  ".join(f"{map_grid[r][c]:>3}" for c in range(4)))

        if not ones:
            return "0"

        row_count = 1 if self.var_count == 1 else 2 if self.var_count in [2, 3] else 4
        col_count = 2 if self.var_count in [1, 2] else 4

        rectangles = []
        possible_rows = [1, 2] if row_count <= 2 else [1, 2, 4]
        possible_cols = [1, 2] if col_count == 2 else [1, 2, 4]

        for row_size in possible_rows:
            for col_size in possible_cols:
                for row_start in range(row_count):
                    for col_start in range(col_count):
                        cells = set()
                        all_ones = True
                        for dr in range(row_size):
                            r = (row_start + dr) % row_count
                            for dc in range(col_size):
                                c = (col_start + dc) % col_count
                                cells.add((r, c))
                                val = map_grid[c] if self.var_count == 1 else map_grid[r][c]
                                if val == 0:
                                    all_ones = False
                                    break
                            if not all_ones:
                                break
                        if all_ones and cells:
                            pattern = ['-' for _ in range(self.var_count)]
                            cell_values = []
                            for r, c in cells:
                                if self.var_count == 1:
                                    cell_values.append([c])
                                elif self.var_count == 2:
                                    cell_values.append([r, c])
                                elif self.var_count == 3:
                                    bc = self.order[c]
                                    cell_values.append([r, (bc >> 1) & 1, bc & 1])
                                else:
                                    ab = self.order[r]
                                    cd = self.order[c]
                                    cell_values.append([(ab >> 1) & 1, ab & 1, (cd >> 1) & 1, cd & 1])
                            for pos in range(self.var_count):
                                values = set(val[pos] for val in cell_values)
                                if len(values) == 1:
                                    pattern[pos] = str(values.pop())
                            rectangles.append((cells, pattern))

        max_rectangles = []
        for i, (cells_i, pat_i) in enumerate(rectangles):
            is_max = True
            for j, (cells_j, pat_j) in enumerate(rectangles):
                if i != j and cells_i.issubset(cells_j) and cells_i != cells_j:
                    is_max = False
                    break
            if is_max:
                max_rectangles.append((cells_i, pat_i))

        one_coords = []
        for point in ones:
            if self.var_count == 1:
                one_coords.append((0, point[0]))
            elif self.var_count == 2:
                one_coords.append((point[0], point[1]))
            elif self.var_count == 3:
                one_coords.append((point[0], self.order.index((point[1] << 1) | point[2])))
            else:
                one_coords.append((self.order.index((point[0] << 1) | point[1]), self.order.index((point[2] << 1) | point[3])))

        picked_rectangles = []
        ones_to_cover = set(range(len(one_coords)))

        for one_idx, coord in enumerate(one_coords):
            covering = [rect_idx for rect_idx, (cells, _) in enumerate(max_rectangles) if coord in cells]
            if len(covering) == 1:
                rect_idx = covering[0]
                if rect_idx not in picked_rectangles:
                    picked_rectangles.append(rect_idx)
                    for o_idx, o_coord in enumerate(one_coords):
                        if o_coord in max_rectangles[rect_idx][0]:
                            ones_to_cover.discard(o_idx)

        while ones_to_cover:
            best_rect = None
            best_covered = set()
            for rect_idx, (cells, _) in enumerate(max_rectangles):
                if rect_idx in picked_rectangles:
                    continue
                covered = {o_idx for o_idx in ones_to_cover if one_coords[o_idx] in cells}
                if len(covered) > len(best_covered):
                    best_covered = covered
                    best_rect = rect_idx
            if best_rect is None:
                print("Не удалось покрыть все единицы!")
                break
            picked_rectangles.append(best_rect)
            ones_to_cover -= best_covered

        terms = set()
        for rect_idx in picked_rectangles:
            _, pattern = max_rectangles[rect_idx]
            term = []
            for idx, val in enumerate(pattern):
                if val == '1':
                    term.append(self.labels[idx])
                elif val == '0':
                    term.append(f'!{self.labels[idx]}')
            if term:
                terms.add(term[0] if len(term) == 1 else '(' + ' ∧ '.join(sorted(term)) + ')')

        terms_list = sorted(terms)
        return "0" if not terms_list else " ∨ ".join(terms_list)