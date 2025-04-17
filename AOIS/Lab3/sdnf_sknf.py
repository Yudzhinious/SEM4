from logical_operations import LogicalOperations

class SDNF_SKNF(LogicalOperations):
    def __init__(self, truth_table=None, variable_names=None, expression=None):
        self.truth_table = truth_table if truth_table is not None else []
        self.variable_names = variable_names if variable_names is not None else []
        self.expression = expression if expression is not None else ""
        self.num_vars = 0
        self.stage = 1
        self.column_width = 1

    def form_sdnf(self):
        if not self.truth_table or not self.variable_names:
            raise ValueError("Таблица истинности или список переменных пусты.")
        sdnf_terms = []
        for row in self.truth_table:
            values = row[0]
            result = row[1]
            if len(values) != len(self.variable_names):
                raise ValueError("Число значений в строках таблицы не совпадает с числом переменных.")
            if result == 1:
                term_parts = []
                for num, val in zip(self.variable_names, values):
                    if val == 1:
                        term_parts.append(num)
                    else:
                        term_parts.append(f'!{num}')
                term = '(' + ' ∧ '.join(term_parts) + ')'
                sdnf_terms.append(term)

        if not sdnf_terms:
            return "Нет выражений для СДНФ"

        sdnf_expression = ' ∨ '.join(sdnf_terms)
        return sdnf_expression

    def form_sknf(self):
        if not self.truth_table or not self.variable_names:
            raise ValueError("Таблица истинности или список переменных пусты.")

        sknf_terms = []
        for row in self.truth_table:
            values = row[0]
            result = row[1]
            if len(values) != len(self.variable_names):
                raise ValueError("Число значений в строках таблицы не совпадает с числом переменных.")

            if result == 0:
                term_parts = []
                for var, val in zip(self.variable_names, values):
                    if val == 0:
                        term_parts.append(var)
                    else:
                        term_parts.append(f'!{var}')
                term = '(' + ' ∨ '.join(term_parts) + ')'
                sknf_terms.append(term)

        if not sknf_terms:
            return "Нет выражений для СКНФ"

        sknf_expression = ' ∧ '.join(sknf_terms)
        return sknf_expression

    def calculate_sdnf(self):
        self.num_vars = 0
        for _ in self.variable_names:
            self.num_vars = self.num_vars + 1

        minterm_list = []
        index = 0
        for entry in self.truth_table:
            if entry[1] == 1:
                minterm_list.append(index)
            index = index + 1

        if len(minterm_list) == 0:
            return "ДНФ отсутствует"

        term_dict = {}
        for m in minterm_list:
            binary = []
            num = m
            for _ in range(self.num_vars):
                bit = str(num % 2)
                binary.insert(0, bit)
                num = num // 2
            while len(binary) < self.num_vars:
                binary.insert(0, "0")
            term_dict[tuple(binary)] = [m]

        print("\nМинимизация СДНФ:")
        print("Начальные минтермы:", list(term_dict.keys()))

        self.stage = 1
        while True:
            new_term_dict = {}
            used_terms = set()
            current_terms = []
            for key in term_dict:
                current_terms.append(key)
            has_changes = False

            for i in range(len(current_terms)):
                for j in range(i + 1, len(current_terms)):
                    term1 = current_terms[i]
                    term2 = current_terms[j]
                    diff_count = 0
                    diff_pos = -1
                    for k in range(self.num_vars):
                        if term1[k] != term2[k]:
                            diff_count = diff_count + 1
                            diff_pos = k
                    if diff_count == 1:
                        new_term = []
                        for k in range(self.num_vars):
                            if k == diff_pos:
                                new_term.append('-')
                            else:
                                new_term.append(term1[k])
                        t1_display = ""
                        for bit in term1:
                            if bit == '0':
                                t1_display = t1_display + '0'
                            elif bit == '1':
                                t1_display = t1_display + '1'
                            else:
                                t1_display = t1_display + 'X'
                        t2_display = ""
                        for bit in term2:
                            if bit == '0':
                                t2_display = t2_display + '0'
                            elif bit == '1':
                                t2_display = t2_display + '1'
                            else:
                                t2_display = t2_display + 'X'
                        result_display = ""
                        for bit in new_term:
                            if bit == '0':
                                result_display = result_display + '0'
                            elif bit == '1':
                                result_display = result_display + '1'
                            else:
                                result_display = result_display + 'X'
                        print(f"({t1_display}) v ({t2_display}) -> ({result_display})")
                        new_term_dict[tuple(new_term)] = term_dict[term1] + term_dict[term2]
                        used_terms.add(term1)
                        used_terms.add(term2)
                        has_changes = True

            for t in term_dict:
                if t not in used_terms:
                    new_term_dict[t] = term_dict[t]

            display_list = []
            for t in new_term_dict:
                term_display = ""
                for bit in t:
                    if bit == '0':
                        term_display = term_display + '0'
                    elif bit == '1':
                        term_display = term_display + '1'
                    else:
                        term_display = term_display + 'X'
                display_list.append(f"({term_display})")
            print(f"Этап {self.stage}: {display_list}")

            if has_changes == False:
                break

            term_dict = new_term_dict
            self.stage = self.stage + 1

        coverage_matrix = {}
        term_index = 0
        for term in term_dict:
            coverage_matrix[term_index] = []
            for _ in range(len(minterm_list)):
                coverage_matrix[term_index].append(False)
            term_index = term_index + 1

        term_index = 0
        for term in term_dict:
            for m_index in range(len(minterm_list)):
                minterm = minterm_list[m_index]
                minterm_binary = []
                num = minterm
                for _ in range(self.num_vars):
                    bit = str(num % 2)
                    minterm_binary.insert(0, bit)
                    num = num // 2
                while len(minterm_binary) < self.num_vars:
                    minterm_binary.insert(0, "0")
                matches = True
                for k in range(self.num_vars):
                    t_bit = term[k]
                    m_bit = minterm_binary[k]
                    if t_bit != '-' and t_bit != m_bit:
                        matches = False
                        break
                if matches:
                    coverage_matrix[term_index][m_index] = True
            term_index = term_index + 1

        selected_terms = []
        covered_minterms = set()
        for col in range(len(minterm_list)):
            covering_terms = []
            for row in range(len(coverage_matrix)):
                if coverage_matrix[row][col] == True:
                    covering_terms.append(row)
            if len(covering_terms) == 1:
                term_idx = covering_terms[0]
                if term_idx not in selected_terms:
                    selected_terms.append(term_idx)
                    for j in range(len(coverage_matrix[term_idx])):
                        if coverage_matrix[term_idx][j] == True:
                            covered_minterms.add(j)

        remaining_minterms = set()
        for i in range(len(minterm_list)):
            if i not in covered_minterms:
                remaining_minterms.add(i)

        while len(remaining_minterms) > 0:
            best_term_idx = -1
            best_coverage = 0
            for row in range(len(coverage_matrix)):
                if row in selected_terms:
                    continue
                coverage_count = 0
                for j in remaining_minterms:
                    if coverage_matrix[row][j] == True:
                        coverage_count = coverage_count + 1
                if coverage_count > best_coverage:
                    best_coverage = coverage_count
                    best_term_idx = row
            if best_term_idx == -1 or best_coverage == 0:
                break
            selected_terms.append(best_term_idx)
            for j in range(len(coverage_matrix[best_term_idx])):
                if coverage_matrix[best_term_idx][j] == True:
                    covered_minterms.add(j)
            remaining_minterms = set()
            for i in range(len(minterm_list)):
                if i not in covered_minterms:
                    remaining_minterms.add(i)

        final_terms = []
        term_list = []
        for key in term_dict:
            term_list.append(key)
        for idx in selected_terms:
            term = term_list[idx]
            term_parts = []
            for i in range(len(term)):
                bit = term[i]
                if bit != '-':
                    if bit == '1':
                        term_parts.append(self.variable_names[i])
                    else:
                        term_parts.append('!' + self.variable_names[i])
            if len(term_parts) > 0:
                if len(term_parts) == 1:
                    final_terms.append(term_parts[0])
                else:
                    final_term = "("
                    for p in range(len(term_parts)):
                        final_term = final_term + term_parts[p]
                        if p < len(term_parts) - 1:
                            final_term = final_term + " ∧ "
                    final_term = final_term + ")"
                    final_terms.append(final_term)

        if len(final_terms) == 0:
            return "0"
        final_expression = ""
        for t in range(len(final_terms)):
            final_expression = final_expression + final_terms[t]
            if t < len(final_terms) - 1:
                final_expression = final_expression + " ∨ "
        return final_expression

    def unique_elements(self):
        elements = []
        for char in self.expression:
            if ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
                if char not in elements:
                    elements.append(char)
        elements.sort()
        return elements

    def numerical_form(self):
        sdnf_nums = []
        sknf_nums = []
        for index, row in enumerate(self.truth_table):
            values = row[0]
            result = row[1]
            if result == 1:
                sdnf_nums.append(index)
            else:
                sknf_nums.append(index)
        sdnf_str = f"({', '.join(str(i) for i in sdnf_nums)})∨"
        sknf_str = f"({', '.join(str(i) for i in sknf_nums)})∧"
        return sdnf_str, sknf_str

    def num_to_bin(self, digit: int, size: int) -> str:
        binary = ""
        current_num = digit
        for _ in range(size):
            remainder = current_num % 2
            binary = str(remainder) + binary
            current_num = current_num // 2
        return binary

    def position_replacement(self, pos1: str, pos2: str) -> int:
        differences = 0
        for i in range(len(pos1)):
            char1 = pos1[i]
            char2 = pos2[i]
            if char1 != char2:
                differences = differences + 1
        return differences

    def is_combinated(self, num1: str, num2: str) -> bool:
        return self.position_replacement(num1, num2) == 1

    def merge(self, str1: str, str2: str) -> str:
        result = ""
        for i in range(len(str1)):
            char1 = str1[i]
            char2 = str2[i]
            if char1 == char2:
                result = result + char1
            else:
                result = result + '-'
        return result

    def calculate_sknf(self):
            self.num_vars = 0
            for _ in self.variable_names:
                self.num_vars = self.num_vars + 1

            maxterm_list = []
            index = 0
            for entry in self.truth_table:
                if entry[1] == 0:
                    maxterm_list.append(index)
                index = index + 1

            if len(maxterm_list) == 0:
                return "КНФ отсутствует"

            term_dict = {}
            for m in maxterm_list:
                binary = []
                num = m
                for _ in range(self.num_vars):
                    bit = str(num % 2)
                    binary.insert(0, bit)
                    num = num // 2
                while len(binary) < self.num_vars:
                    binary.insert(0, "0")
                term_dict[tuple(binary)] = [m]

            print("\nМинимизация СКНФ расчетным методом:")
            print("Начальные макстермы:", list(term_dict.keys()))

            self.stage = 1
            while True:
                new_term_dict = {}
                used_terms = set()
                current_terms = []
                for key in term_dict:
                    current_terms.append(key)
                has_changes = False

                for i in range(len(current_terms)):
                    for j in range(i + 1, len(current_terms)):
                        term1 = current_terms[i]
                        term2 = current_terms[j]
                        diff_count = 0
                        diff_pos = -1
                        for k in range(self.num_vars):
                            if term1[k] != term2[k]:
                                diff_count = diff_count + 1
                                diff_pos = k
                        if diff_count == 1:
                            new_term = []
                            for k in range(self.num_vars):
                                if k == diff_pos:
                                    new_term.append('-')
                                else:
                                    new_term.append(term1[k])
                            t1_display = ""
                            for bit in term1:
                                if bit == '0':
                                    t1_display = t1_display + '0'
                                elif bit == '1':
                                    t1_display = t1_display + '1'
                                else:
                                    t1_display = t1_display + 'X'
                            t2_display = ""
                            for bit in term2:
                                if bit == '0':
                                    t2_display = t2_display + '0'
                                elif bit == '1':
                                    t2_display = t2_display + '1'
                                else:
                                    t2_display = t2_display + 'X'
                            result_display = ""
                            for bit in new_term:
                                if bit == '0':
                                    result_display = result_display + '0'
                                elif bit == '1':
                                    result_display = result_display + '1'
                                else:
                                    result_display = result_display + 'X'
                            print(f"({t1_display}) v ({t2_display}) -> ({result_display})")
                            new_term_dict[tuple(new_term)] = term_dict[term1] + term_dict[term2]
                            used_terms.add(term1)
                            used_terms.add(term2)
                            has_changes = True

                for t in term_dict:
                    if t not in used_terms:
                        new_term_dict[t] = term_dict[t]

                display_list = []
                for t in new_term_dict:
                    term_display = ""
                    for bit in t:
                        if bit == '0':
                            term_display = term_display + '0'
                        elif bit == '1':
                            term_display = term_display + '1'
                        else:
                            term_display = term_display + 'X'
                    display_list.append(f"({term_display})")
                print(f"Этап {self.stage}: {display_list}")

                if has_changes == False:
                    break

                term_dict = new_term_dict
                self.stage = self.stage + 1

            coverage_matrix = {}
            term_index = 0
            for term in term_dict:
                coverage_matrix[term_index] = []
                for _ in range(len(maxterm_list)):
                    coverage_matrix[term_index].append(False)
                term_index = term_index + 1

            term_index = 0
            for term in term_dict:
                for m_index in range(len(maxterm_list)):
                    maxterm = maxterm_list[m_index]
                    maxterm_binary = []
                    num = maxterm
                    for _ in range(self.num_vars):
                        bit = str(num % 2)
                        maxterm_binary.insert(0, bit)
                        num = num // 2
                    while len(maxterm_binary) < self.num_vars:
                        maxterm_binary.insert(0, "0")
                    matches = True
                    for k in range(self.num_vars):
                        t_bit = term[k]
                        m_bit = maxterm_binary[k]
                        if t_bit != '-' and t_bit != m_bit:
                            matches = False
                            break
                    if matches:
                        coverage_matrix[term_index][m_index] = True
                term_index = term_index + 1

            selected_terms = []
            covered_maxterms = set()
            for col in range(len(maxterm_list)):
                covering_terms = []
                for row in range(len(coverage_matrix)):
                    if coverage_matrix[row][col] == True:
                        covering_terms.append(row)
                if len(covering_terms) == 1:
                    term_idx = covering_terms[0]
                    if term_idx not in selected_terms:
                        selected_terms.append(term_idx)
                        for j in range(len(coverage_matrix[term_idx])):
                            if coverage_matrix[term_idx][j] == True:
                                covered_maxterms.add(j)

            remaining_maxterms = set()
            for i in range(len(maxterm_list)):
                if i not in covered_maxterms:
                    remaining_maxterms.add(i)

            while len(remaining_maxterms) > 0:
                best_term_idx = -1
                best_coverage = 0
                for row in range(len(coverage_matrix)):
                    if row in selected_terms:
                        continue
                    coverage_count = 0
                    for j in remaining_maxterms:
                        if coverage_matrix[row][j] == True:
                            coverage_count = coverage_count + 1
                    if coverage_count > best_coverage:
                        best_coverage = coverage_count
                        best_term_idx = row
                if best_term_idx == -1 or best_coverage == 0:
                    break
                selected_terms.append(best_term_idx)
                for j in range(len(coverage_matrix[best_term_idx])):
                    if coverage_matrix[best_term_idx][j] == True:
                        covered_maxterms.add(j)
                remaining_maxterms = set()
                for i in range(len(maxterm_list)):
                    if i not in covered_maxterms:
                        remaining_maxterms.add(i)

            final_terms = []
            term_list = []
            for key in term_dict:
                term_list.append(key)
            for idx in selected_terms:
                term = term_list[idx]
                term_parts = []
                for i in range(len(term)):
                    bit = term[i]
                    if bit != '-':
                        if bit == '0':
                            term_parts.append(self.variable_names[i])
                        else:
                            term_parts.append('!' + self.variable_names[i])
                if len(term_parts) > 0:
                    if len(term_parts) == 1:
                        final_terms.append(term_parts[0])
                    else:
                        final_term = "("
                        for p in range(len(term_parts)):
                            final_term = final_term + term_parts[p]
                            if p < len(term_parts) - 1:
                                final_term = final_term + " ∨ "
                        final_term = final_term + ")"
                        final_terms.append(final_term)

            if len(final_terms) == 0:
                return "1"
            final_expression = ""
            for t in range(len(final_terms)):
                final_expression = final_expression + final_terms[t]
                if t < len(final_terms) - 1:
                    final_expression = final_expression + " ∧ "
            return final_expression


