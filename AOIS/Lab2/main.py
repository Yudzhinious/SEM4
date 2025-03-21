from truth_table import *

def main():
    expression = input("Введите логическое выражение: ")
    var_names = unique_elements(expression)
    truth_table = table(expression, var_names)

    sknf = form_sknf(truth_table, var_names)
    sdnf = form_sdnf(truth_table, var_names)

    sdnf_nums, sknf_nums = numerical_form(truth_table)
    result_str = results_to_string(truth_table)
    decimal_result = binary_to_decimal_without_sign(result_str)

    print_truth_table(truth_table, var_names, expression)

    print("Совершенная дизъюнктивная нормальная форма (СДНФ)", "\n", sdnf)
    print("Совершенная конъюнктивная нормальная форма (СКНФ)", "\n", sknf)

    print("Числовые формы:", "\n", sdnf_nums, "\n", sknf_nums)

    print("Индексная форма", "\n", decimal_result, "-", result_str)


if __name__ == "__main__":
    main()