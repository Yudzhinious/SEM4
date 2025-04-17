from truth_table import TruthTable
from sdnf_sknf import SDNF_SKNF
from karno_sknf_maps import KarnoSKNF
from karno_sdnf_maps import KarnoSDNF
from calculation_table import CalculationTable


def main():
    expression = input("Введите логическое выражение: ").replace(" ", "")
    var_names = TruthTable.unique_elements(expression)
    parts = list(expression)

    truth_table_obj = TruthTable(parts, var_names)
    truth_table = truth_table_obj.get_table()

    sdnf_sknf_obj = SDNF_SKNF(truth_table, var_names)
    sknf = sdnf_sknf_obj.form_sknf()
    sdnf = sdnf_sknf_obj.form_sdnf()
    sdnf_nums, sknf_nums = TruthTable.numerical_form(truth_table)
    result_str = TruthTable.results_to_string(truth_table)
    decimal_result = TruthTable.bin_to_dec(result_str)

    truth_table_obj.print_truth_table()
    print("\nСовершенная дизъюнктивная нормальная форма (СДНФ):")
    print(sdnf)
    print("\nСовершенная конъюнктивная нормальная форма (СКНФ):")
    print(sknf)
    print("\nЧисловые формы:")
    print("СДНФ:", sdnf_nums)
    print("СКНФ:", sknf_nums)
    print("\nИндексная форма:")
    print(f"{decimal_result} - {result_str}")

    print("\nВыберите метод минимизации:")
    print("1. Расчетный метод для СДНФ")
    print("2. Расчетный метод для СКНФ")
    print("3. Расчетно-табличный метод для СДНФ")
    print("4. Расчетно-табличный метод для СКНФ")
    print("5. Табличный метод для СДНФ")
    print("6. Табличный метод для СКНФ")

    choice = input("Введите номер метода (1-6): ")

    if choice == "1":
        min_sdnf = sdnf_sknf_obj.calculate_sdnf()
        print("Результат:", min_sdnf)
    elif choice == "2":
        min_sknf = sdnf_sknf_obj.calculate_sknf()
        print("Результат:", min_sknf)
    elif choice == "3":
        calc_table = CalculationTable(truth_table, var_names)
        min_sdnf = calc_table.calculate_table_sdnf()
        print("Результат:", min_sdnf)
    elif choice == "4":
        calc_table = CalculationTable(truth_table, var_names)
        min_sknf = calc_table.calculate_table_sknf()
        print("Результат:", min_sknf)
    elif choice == "5":
        karno_sdnf = KarnoSDNF(truth_table, var_names)
        min_sdnf = karno_sdnf.karno_sdnf() if len(var_names) >= 5 else karno_sdnf.karno_1_to_4_sdnf()
        print("Результат:", min_sdnf)
    elif choice == "6":
        karno_sknf = KarnoSKNF(truth_table, var_names)
        min_sknf = karno_sknf.karno_sknf() if len(var_names) >= 5 else karno_sknf.karno_1_to_4_sknf()
        print("Результат:", min_sknf)
    else:
        print("Ошибка")


if __name__ == "__main__":
    main()