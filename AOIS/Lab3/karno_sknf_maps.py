from logical_operations import *

class KarnoSKNF(LogicalOperations):
    def __init__(self, inputs: list, labels: list):
        super().__init__()
        self.inputs = inputs
        self.labels = labels
        self.var_count = len(labels)
        self.order = [0, 1, 3, 2]

    def karno_sknf(self, verbose=True) -> str:
        if verbose:
            print(f"\nСокращаем СКНФ с помощью карты Карно ({self.var_count} переменных):")

        zeros = []
        if self.var_count == 5:
            grid = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(2)]
            for idx, entry in enumerate(self.inputs):
                q, r, s, t, p = entry[0]
                block = p
                row = self.order.index((q << 1) | r)
                col = self.order.index((s << 1) | t)
                grid[block][row][col] = entry[1]
                if entry[1] == 0:
                    zeros.append((q, r, s, t, p))

            if verbose:
                print("Карта Карно:")
                print("ab\\cde   000  001  011  010   110  111  101  100")
                for row_idx in range(4):
                    row_label = format(self.order[row_idx], '02b')
                    line = f"{row_label}       "
                    block_0 = [str(grid[0][row_idx][c]) for c in range(4)]
                    block_1 = [str(grid[1][row_idx][c]) for c in range(4)]
                    line += "  ".join(f"{val:>3}" for val in block_0)
                    line += "  "
                    line += "  ".join(f"{val:>3}" for val in block_1)
                    print(line)

        else:
            grid = [[[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
            for idx, entry in enumerate(self.inputs):
                q, r, s, t, o, p = entry[0]
                block_o = self.order.index((o << 1) | p)
                row = self.order.index((q << 1) | r)
                col = self.order.index((s << 1) | t)
                grid[block_o][row][col] = entry[1]
                if entry[1] == 0:
                    zeros.append((q, r, s, t, o, p))

            if verbose:
                print("Карта Карно:")
                print("ef ab\\cd   0000  0001  0011  0010   0100  0101  0111  0110   1100  1101  1111  1110   1000  1001  1011  1010")
                for row_idx in range(4):
                    row_label = format(self.order[row_idx], '02b')
                    line = f"  {row_label}       "
                    for block_idx in range(4):
                        block_vals = [str(grid[block_idx][row_idx][c]) for c in range(4)]
                        line += "  ".join(f"{val:>3}" for val in block_vals)
                        line += "  "
                    print(line)

        if not zeros:
            return "1"

        blocks = 2 if self.var_count == 5 else 4
        row_count = 4
        col_count = 4

        found_groups = []
        for block_size in [1, 2, 4][:blocks + 1]:
            for block_start in range(blocks):
                if block_size > 1 and block_start != 0:
                    continue
                for row_size in [1, 2, 4]:
                    for col_size in [1, 2, 4]:
                        for row_start in range(row_count):
                            for col_start in range(col_count):
                                cells = set()
                                has_only_zeros = True
                                for db in range(block_size):
                                    b = (block_start + db) % blocks
                                    for dr in range(row_size):
                                        r = (row_start + dr) % row_count
                                        for dc in range(col_size):
                                            c = (col_start + dc) % col_count
                                            cells.add((b, r, c))
                                            val = grid[b][r][c] if self.var_count == 5 else grid[b][r][c]
                                            if val == 1:
                                                has_only_zeros = False
                                                break
                                        if not has_only_zeros:
                                            break
                                    if not has_only_zeros:
                                        break
                                if has_only_zeros and cells:
                                    mask = ['-' for _ in range(self.var_count)]
                                    cell_data = []
                                    for b, r, c in cells:
                                        qr = self.order[r]
                                        st = self.order[c]
                                        q = (qr >> 1) & 1
                                        r_val = qr & 1
                                        s = (st >> 1) & 1
                                        t = st & 1
                                        if self.var_count == 5:
                                            p = b
                                            cell_data.append([q, r_val, s, t, p])
                                        else:
                                            op = self.order[b]
                                            o = (op >> 1) & 1
                                            p = op & 1
                                            cell_data.append([q, r_val, s, t, o, p])
                                    for var_pos in range(self.var_count):
                                        var_values = set(data[var_pos] for data in cell_data)
                                        if len(var_values) == 1:
                                            mask[var_pos] = str(var_values.pop())
                                    found_groups.append((cells, mask))

        largest_groups = []
        for idx_1, (cells_1, mask_1) in enumerate(found_groups):
            is_biggest = True
            for idx_2, (cells_2, mask_2) in enumerate(found_groups):
                if idx_1 != idx_2 and cells_1.issubset(cells_2) and cells_1 != cells_2:
                    is_biggest = False
                    break
            if is_biggest:
                largest_groups.append((cells_1, mask_1))

        zero_coords = []
        for point in zeros:
            if self.var_count == 5:
                q, r, s, t, p = point
                zero_coords.append((p, self.order.index((q << 1) | r), self.order.index((s << 1) | t)))
            else:
                q, r, s, t, o, p = point
                zero_coords.append(
                    (self.order.index((o << 1) | p), self.order.index((q << 1) | r), self.order.index((s << 1) | t)))

        selected_groups = []
        remaining_zeros = set(range(len(zero_coords)))

        for zero_idx, coord in enumerate(zero_coords):
            matches = []
            for group_idx, (cells, _) in enumerate(largest_groups):
                if coord in cells:
                    matches.append(group_idx)
            if len(matches) == 1:
                group_idx = matches[0]
                if group_idx not in selected_groups:
                    selected_groups.append(group_idx)
                    for z_idx, z_coord in enumerate(zero_coords):
                        if z_coord in largest_groups[group_idx][0]:
                            remaining_zeros.discard(z_idx)

        while remaining_zeros:
            best_group = None
            best_matches = set()
            for group_idx, (cells, _) in enumerate(largest_groups):
                if group_idx in selected_groups:
                    continue
                matches = set()
                for z_idx in remaining_zeros:
                    if zero_coords[z_idx] in cells:
                        matches.add(z_idx)
                if len(matches) > len(best_matches):
                    best_matches = matches
                    best_group = group_idx
            if best_group is None:
                if verbose:
                    print("Не удалось покрыть все нули!")
                break
            selected_groups.append(best_group)
            remaining_zeros -= best_matches

        expression_parts = set()
        for group_idx in selected_groups:
            _, mask = largest_groups[group_idx]
            term_parts = []
            for idx, val in enumerate(mask):
                if val == '0':
                    term_parts.append(self.labels[idx])
                elif val == '1':
                    term_parts.append(f'!{self.labels[idx]}')
            if term_parts:
                if len(term_parts) == 1:
                    expression_parts.add(term_parts[0])
                else:
                    expression_parts.add('(' + ' ∨ '.join(sorted(term_parts)) + ')')

        final_expression = ""
        parts_list = sorted(list(expression_parts))
        if len(parts_list) == 0:
            final_expression = "1"
        else:
            for i in range(len(parts_list)):
                final_expression += parts_list[i]
                if i < len(parts_list) - 1:
                    final_expression += " ∧ "
        return final_expression

    def karno_1_to_4_sknf(self, verbose=True) -> str:
        num_vars = len(self.labels)
        if num_vars not in [1, 2, 3, 4]:
            return "Этот метод работает только для 1–4 переменных."

        if verbose:
            print(f"\nУпрощаем СКНФ через карту Карно ({num_vars} переменных):")
        orders = self.order
        zeros = []
        if num_vars == 1:
            k_map = [0] * 2
            for i, row in enumerate(self.inputs):
                x = row[0][0]
                k_map[x] = row[1]
                if row[1] == 0:
                    zeros.append((x,))

            if verbose:
                print("Карта Карно:")
                print("a    0  1")
                print("     " + "  ".join(f"{k_map[i]:>1}" for i in range(2)))

            if not zeros:
                return "1"

        elif num_vars == 2:
            k_map = [[0] * 2 for _ in range(2)]
            for i, row in enumerate(self.inputs):
                x, y = row[0]
                k_map[x][y] = row[1]
                if row[1] == 0:
                    zeros.append((x, y))

            if verbose:
                print("Карта Карно:")
                print("a\\b   0  1")
                for i in range(2):
                    print(f"{i}     " + "  ".join(f"{k_map[i][j]:>1}" for j in range(2)))

            if not zeros:
                return "1"

        elif num_vars == 3:
            k_map = [[0] * 4 for _ in range(2)]
            for i, row in enumerate(self.inputs):
                x, y, z = row[0]
                row_idx = x
                col_idx = orders.index((y << 1) | z)
                k_map[row_idx][col_idx] = row[1]
                if row[1] == 0:
                    zeros.append((x, y, z))

            if verbose:
                print("Карта Карно:")
                print("a\\bc   00  01  11  10")
                for i in range(2):
                    print(f"{i}     " + "  ".join(f"{k_map[i][j]:>3}" for j in range(4)))

            if not zeros:
                return "1"

        else:
            k_map = [[0] * 4 for _ in range(4)]
            for i, row in enumerate(self.inputs):
                x, y, z, w = row[0]
                row_idx = orders.index((x << 1) | y)
                col_idx = orders.index((z << 1) | w)
                k_map[row_idx][col_idx] = row[1]
                if row[1] == 0:
                    zeros.append((x, y, z, w))

            if verbose:
                print("Карта Карно:")
                print("ab\\cd   00  01  11  10")
                for i in range(4):
                    row_label = format(orders[i], '02b')
                    print(f"{row_label}     " + "  ".join(f"{k_map[i][j]:>3}" for j in range(4)))

            if not zeros:
                return "1"

        if num_vars == 1:
            rows = 1
        elif num_vars == 2 or num_vars == 3:
            rows = 2
        else:
            rows = 4

        if num_vars == 1 or num_vars == 2:
            cols = 2
        else:
            cols = 4

        group_list = []

        if rows <= 2:
            possible_heights = [1, 2]
        else:
            possible_heights = [1, 2, 4]

        if cols == 2:
            possible_widths = [1, 2]
        else:
            possible_widths = [1, 2, 4]

        for height in possible_heights:
            for width in possible_widths:
                for start_row in range(rows):
                    for start_col in range(cols):
                        group_cells = set()
                        all_zeros = True
                        for r in range(height):
                            for c in range(width):
                                row = (start_row + r) % rows
                                col = (start_col + c) % cols
                                group_cells.add((row, col))
                                if k_map[row][col] == 1:
                                    all_zeros = False
                                    break
                            if not all_zeros:
                                break
                        if all_zeros and group_cells:
                            pattern = ['-' for _ in range(num_vars)]
                            cell_values = []
                            for r, c in group_cells:
                                if num_vars == 1:
                                    cell_values.append([c])
                                elif num_vars == 2:
                                    cell_values.append([r, c])
                                elif num_vars == 3:
                                    yz = orders[c]
                                    cell_values.append([r, (yz >> 1) & 1, yz & 1])
                                else:
                                    xy = orders[r]
                                    zw = orders[c]
                                    cell_values.append([(xy >> 1) & 1, xy & 1, (zw >> 1) & 1, zw & 1])
                            for var_idx in range(num_vars):
                                var_vals = {val[var_idx] for val in cell_values}
                                if len(var_vals) == 1:
                                    pattern[var_idx] = str(next(iter(var_vals)))
                            group_list.append((group_cells, pattern))

        best_groups = []
        for i, (cells_1, pat_1) in enumerate(group_list):
            is_largest = True
            for j, (cells_2, pat_2) in enumerate(group_list):
                if i != j and cells_1.issubset(cells_2) and cells_1 != cells_2:
                    is_largest = False
                    break
            if is_largest:
                best_groups.append((cells_1, pat_1))

        zero_positions = []
        for zero in zeros:
            if num_vars == 1:
                zero_positions.append((0, zero[0]))
            elif num_vars == 2:
                zero_positions.append((zero[0], zero[1]))
            elif num_vars == 3:
                zero_positions.append((zero[0], orders.index((zero[1] << 1) | zero[2])))
            else:
                zero_positions.append(
                    (orders.index((zero[0] << 1) | zero[1]), orders.index((zero[2] << 1) | zero[3])))

        chosen_groups = []
        zeros_to_cover = set(range(len(zero_positions)))

        for zero_idx, zero_pos in enumerate(zero_positions):
            covering_groups = []
            for group_idx, (group_cells, _) in enumerate(best_groups):
                if zero_pos in group_cells:
                    covering_groups.append(group_idx)
            if len(covering_groups) == 1:
                group_idx = covering_groups[0]
                if group_idx not in chosen_groups:
                    chosen_groups.append(group_idx)
                    for z_idx, z_pos in enumerate(zero_positions):
                        if z_pos in best_groups[group_idx][0]:
                            zeros_to_cover.discard(z_idx)

        while zeros_to_cover:
            best_group_idx = None
            best_covered = set()
            for group_idx, (group_cells, _) in enumerate(best_groups):
                if group_idx in chosen_groups:
                    continue
                covered = set()
                for z_idx in zeros_to_cover:
                    if zero_positions[z_idx] in group_cells:
                        covered.add(z_idx)
                if len(covered) > len(best_covered):
                    best_covered = covered
                    best_group_idx = group_idx
            if best_group_idx is None:
                if verbose:
                    print("Ошибка: не удалось покрыть все нули.")
                break
            chosen_groups.append(best_group_idx)
            zeros_to_cover -= best_covered

        final_expr = set()
        for group_idx in chosen_groups:
            _, pattern = best_groups[group_idx]
            term = []
            for idx, bit in enumerate(pattern):
                if bit == '0':
                    term.append(self.labels[idx])
                elif bit == '1':
                    term.append(f'!{self.labels[idx]}')
            if term:
                if len(term) == 1:
                    final_expr.add(term[0])
                else:
                    final_expr.add('(' + ' ∨ '.join(sorted(term)) + ')')

        final_expression = ""
        expr_list = sorted(list(final_expr))
        if len(expr_list) == 0:
            final_expression = "1"
        else:
            for i in range(len(expr_list)):
                final_expression += expr_list[i]
                if i < len(expr_list) - 1:
                    final_expression += " ∧ "
        return final_expression
