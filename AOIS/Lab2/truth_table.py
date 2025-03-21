def conjuction(elem1, elem2):
    if elem1 == 1 and elem2 == 1:
        return 1
    return 0

def disjunction(elem1, elem2):
    if elem1 == 1 or elem2 == 1:
        return 1
    return 0

def negation(elem1):
    if elem1 == 1:
        return 0
    return 1

def implication(elem1, elem2):
    if elem1 == 1 and elem2 == 0:
        return 0
    return 1

def equivalent(elem1, elem2):
    if elem1 == elem2:
        return 1
    return 0

def priority(op):
        if op == '!':
            return 5
        if op == '&':
            return 4
        if op == '|':
            return 3
        if op == '>':
            return 2
        if op == '~':
            return 1
        return 0

def evaluate_expression(parts, values):
    rpn_result = []
    temp_ops = []
    calc_stack = []

    for part in parts:
        if part.isalpha():
            rpn_result.append(values[part])
        elif part == '(':
            temp_ops.append(part)
        elif part == ')':
            while len(temp_ops) > 0 and temp_ops[-1] != '(':
                rpn_result.append(temp_ops.pop())
            if len(temp_ops) > 0:
                temp_ops.pop()
        elif part in ('!', '&', '|', '~', '>'):
            while len(temp_ops) > 0 and temp_ops[-1] != '(' and priority(temp_ops[-1]) >= priority(part):
                rpn_result.append(temp_ops.pop())
            temp_ops.append(part)

    while temp_ops != []:
        rpn_result.append(temp_ops.pop())

    for thing in rpn_result:
        if isinstance(thing, int):
            calc_stack.append(thing)
        elif thing == '!':
            one = calc_stack.pop()
            calc_stack.append(negation(one))
        else:
            second = calc_stack.pop()
            first = calc_stack.pop()
            if thing == '&':
                calc_stack.append(conjuction(first, second))
            elif thing == '|':
                calc_stack.append(disjunction(first, second))
            elif thing == '>':
                calc_stack.append(implication(first, second))
            elif thing == '~':
                calc_stack.append(equivalent(first, second))

    return calc_stack[0]

def table(expression, var_names):
    table = []
    n = len(var_names)
    total_combinations = 2 ** n
    for i in range(total_combinations):
        binary_values = []
        current_number = i
        for j in range(n - 1, -1, -1):
            power_of_two = 2 ** j
            if current_number >= power_of_two:
                binary_values.append(1)
                current_number -= power_of_two
            else:
                binary_values.append(0)
        variables = {}
        for idx in range(n):
            variables[var_names[idx]] = binary_values[idx]
        result = evaluate_expression(expression, variables)
        table.append((binary_values, result))
    return table

def print_truth_table(table, variable_names, expression):
    print("\nТаблица истинности:")
    print(" ".join(variable_names) + "     " + expression)
    print("-" * (len(variable_names) * 2 + len(expression) + 3))

    for values, result in table:
        print(f"{' '.join(map(str, values))}     {result}")

def binary_to_decimal_without_sign(bin_number: str):
    return binary_to_dec_num(bin_number[1:] if bin_number[0] == '1' else bin_number)

def binary_to_dec_num(binary: str):
        decimal = 0
        length = len(binary)
        for i in range(length):
            if binary[i] == '1':
                decimal += 2 ** (length - i - 1)
        return decimal

def results_to_string(table):
    result_str = ''
    for row in table:
        result = row[1]
        result_str += str(int(result))
    return result_str

def unique_elements(expression):
    set = []
    for char in expression:
        if ('A' <= char <= 'Z') or ('a' <= char <= 'z'):
            if char not in set:
                set.append(char)
    set.sort()
    return set

def numerical_form(table):
    sdnf_nums = []
    sknf_nums = []
    for index, row in enumerate(table):
        values = row[0]
        result = row[1]
        if result == 1:
            sdnf_nums.append(index)
        else:
            sknf_nums.append(index)
    sdnf_str = f"({', '.join(str(i) for i in sdnf_nums)})∨"
    sknf_str = f"({', '.join(str(i) for i in sknf_nums)})∧"
    return sdnf_str, sknf_str


def form_sdnf(truth_table, variable_names):
    if not truth_table or not variable_names:
        raise ValueError("Таблица истинности или список переменных пусты.")
    sdnf_terms = []
    for row in truth_table:
        values = row[0]
        result = row[1]
        if len(values) != len(variable_names):
            raise ValueError("Число значений в строках таблицы не совпадает с числом переменных.")
        if result == 1:
            term_parts = []
            for num, val in zip(variable_names, values):
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

def form_sknf(truth_table, variable_names):
    if not truth_table or not variable_names:
        raise ValueError("Таблица истинности или список переменных пусты.")

    sknf_terms = []
    for row in truth_table:
        values = row[0]
        result = row[1]
        if len(values) != len(variable_names):
            raise ValueError("Число значений в строках таблицы не совпадает с числом переменных.")

        if result == 0:
            term_parts = []
            for var, val in zip(variable_names, values):
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