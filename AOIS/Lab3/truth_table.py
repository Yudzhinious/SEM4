from logical_operations import LogicalOperations

class TruthTable(LogicalOperations):
    def __init__(self, expression: str, var_names: list):
        self.expression = expression
        self.var_names = var_names
        self.table = self.build_truth_table()

    def build_truth_table(self) -> list:
        table = []
        n = len(self.var_names)
        total_combinations = 2 ** n
        for i in range(total_combinations):
            binary_values = []
            current_number = i
            for j in range(n - 1, -1, -1):
                power_of_two = 2 ** j
                binary_values.append(1 if current_number >= power_of_two else 0)
                if current_number >= power_of_two:
                    current_number -= power_of_two
            variables = dict(zip(self.var_names, binary_values))
            result = self.evaluate_expression(self.expression, variables)
            table.append((binary_values, result))
        return table

    def print_truth_table(self):
        print("\nТаблица истинности:")
        print(" ".join(self.var_names) + "     " + ''.join(self.expression))
        print("-" * (len(self.var_names) * 2 + len(self.expression) + 3))
        for values, result in self.table:
            print(f"{' '.join(map(str, values))}     {result}")

    def get_table(self) -> list:
        return self.table