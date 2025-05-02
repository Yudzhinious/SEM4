from calculation_table import CalculationTable
from karno_sdnf_maps import KarnoSDNF
from karno_sknf_maps import KarnoSKNF

LITERALS_ODS3 = ['A', 'B', 'C']
LITERALS_D8421 = ['X1', 'X2', 'X3', 'X4']

def build_truth_table(literals, expression_func):
    table = []
    n = len(literals)
    for i in range(2 ** n):
        values = []
        num = i
        for _ in range(n):
            values.insert(0, num % 2)
            num //= 2
        result = expression_func(values)
        table.append((values, result))
    return table

def get_adder_SDNF():
    def calc_S(values):
        A, B, C = values
        return (A ^ B) ^ C

    def calc_Cout(values):
        A, B, C = values
        return (A & B) | (A & C) | (B & C)

    table_S = build_truth_table(LITERALS_ODS3, calc_S)
    table_Cout = build_truth_table(LITERALS_ODS3, calc_Cout)

    print("Таблица истинности для ОДС-3:")
    print("A B C  S Cout")
    for i in range(len(table_S)):
        values = table_S[i][0]
        S = table_S[i][1]
        Cout = table_Cout[i][1]
        print(f"{values[0]} {values[1]} {values[2]}  {S}  {Cout}")

    karno_S = KarnoSDNF(table_S, LITERALS_ODS3)
    karno_Cout = KarnoSDNF(table_Cout, LITERALS_ODS3)

    SDNF_S = karno_S.karno_1_to_4_sdnf()
    SDNF_Cout = karno_Cout.karno_1_to_4_sdnf()

    calc_table_S = CalculationTable(truth_table=table_S, variable_names=LITERALS_ODS3)
    calc_table_Cout = CalculationTable(truth_table=table_Cout, variable_names=LITERALS_ODS3)

    calc_SDNF_S = calc_table_S.calculate_table_sdnf()
    calc_SDNF_Cout = calc_table_Cout.calculate_table_sdnf()

    print("\nРезультаты минимизации для S:")
    print(f"KarnoSDNF: {SDNF_S}")
    print(f"CalculationTable: {calc_SDNF_S}")
    print("\nРезультаты минимизации для Cout:")
    print(f"KarnoSDNF: {SDNF_Cout}")
    print(f"CalculationTable: {calc_SDNF_Cout}")

    return SDNF_S, SDNF_Cout

def get_D8421_2():
    def get_output(values):
        decimal = values[0] * 8 + values[1] * 4 + values[2] * 2 + values[3] * 1
        if decimal > 9:
            return [-1, -1, -1, -1]
        result = decimal + 2
        out = [0, 0, 0, 0]
        for i in range(3, -1, -1):
            out[i] = result % 2
            result //= 2
        return out

    table = build_truth_table(LITERALS_D8421, get_output)
    print("Таблица истинности для Д8421 в Д8421+2:")
    print("X4 X3 X2 X1  Y4 Y3 Y2 Y1")
    for i in range(len(table)):
        values = table[i][0]
        outputs = table[i][1]
        if outputs[0] == -1:
            print(f"{values[0]} {values[1]} {values[2]} {values[3]}  -  -  -  -")
        else:
            print(f"{values[0]} {values[1]} {values[2]} {values[3]}  {outputs[0]} {outputs[1]} {outputs[2]} {outputs[3]}")

def calc_Y1(values):
        X1, X2, X3, X4 = values
        return X1 | (X2 & X3)

def calc_Y2(values):
        X1, X2, X3, X4 = values
        return ((X2 & (1 - X3)) | ((1 - X2) & X3))

def calc_Y3(values):
        X1, X2, X3, X4 = values
        return (1 - X3)

def calc_Y4(values):
        X1, X2, X3, X4 = values
        return X4

def calculate_Y_functions():


    table_Y1 = build_truth_table(LITERALS_D8421, calc_Y1)
    table_Y2 = build_truth_table(LITERALS_D8421, calc_Y2)
    table_Y3 = build_truth_table(LITERALS_D8421, calc_Y3)
    table_Y4 = build_truth_table(LITERALS_D8421, calc_Y4)

    karno_Y1 = KarnoSDNF(table_Y1, LITERALS_D8421)
    karno_Y2 = KarnoSDNF(table_Y2, LITERALS_D8421)
    karno_Y3 = KarnoSDNF(table_Y3, LITERALS_D8421)
    karno_Y4 = KarnoSDNF(table_Y4, LITERALS_D8421)

    SDNF_Y1 = karno_Y1.karno_1_to_4_sdnf()
    SDNF_Y2 = karno_Y2.karno_1_to_4_sdnf()
    SDNF_Y3 = karno_Y3.karno_1_to_4_sdnf()
    SDNF_Y4 = karno_Y4.karno_1_to_4_sdnf()

    print("\nМинимизированные функции:")
    print(f"Y1 = {SDNF_Y1}")
    print(f"Y2 = {SDNF_Y2}")
    print(f"Y3 = {SDNF_Y3}")
    print(f"Y4 = {SDNF_Y4}")

if __name__ == "__main__":
    SDNF_S, SDNF_Cout = get_adder_SDNF()
    print("\nСДНФ для S: " + SDNF_S)
    print("СДНФ для Cout: " + SDNF_Cout)

    print("\n")
    get_D8421_2()

    calculate_Y_functions()