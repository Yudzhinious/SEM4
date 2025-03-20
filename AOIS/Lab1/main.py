from laba import Digit

def main():
    choice = Digit()
    print("Сложение:")
    print("Ввод числа №1")
    num1 = int(input())
    print("Число введено:", num1)
    print("Прямой код: [", choice.convert_to_binary_number(num1), "]", sep='')
    print("Обратный код: [", choice.convert_to_reverse_binary(num1), "]", sep='')
    print("Дополнительный код: [", choice.convert_to_additional_binary(num1), "]", sep='')
    print("Ввод числа №2")
    num2 = int(input())
    print("Число введено:", num2)
    print("Прямой код: [", choice.convert_to_binary_number(num2), "]", sep='')
    print("Обратный код: [", choice.convert_to_reverse_binary(num2), "]", sep='')
    print("Дополнительный код: [", choice.convert_to_additional_binary(num2), "]", sep='')

    result = choice.additional_summa(num1, num2)
    print("Результат:", choice.convert_to_dec(result))
    print("Прямой код: [", choice.convert_to_binary_number(choice.convert_to_dec(result)), "]", sep='')
    print("Обратный код: [", choice.convert_to_reverse_binary(choice.convert_to_dec(result)), "]", sep='')
    print("Дополнительный код: [", choice.convert_to_additional_binary(choice.convert_to_dec(result)), "]", sep='')

    print("Вычитание:")
    result = choice.additional_subtract(num1, num2)
    print("Результат:", choice.convert_to_dec(result))
    print("Прямой код: [", choice.convert_to_binary_number(choice.convert_to_dec(result)), "]", sep='')
    print("Обратный код: [", choice.convert_to_reverse_binary(choice.convert_to_dec(result)), "]", sep='')
    print("Дополнительный код: [", choice.convert_to_additional_binary(choice.convert_to_dec(result)), "]", sep='')

    print("Умножение:")
    print(choice.direct_code_multiplication(num1, num2))

    print("Деление:")
    result = choice.divide_bin(num1, num2)
    print(result)

    for _ in range(6):
     print("Сложение чисел с плавающей точкой:")
     print("Ввод числа №1")
     float1 = choice.convert_float_to_bin(float(input()))
     print("Ввод числа №2")
     float2 = choice.convert_float_to_bin(float(input()))
     choice.display_ieee(float1)
     choice.display_ieee(float2)
     result = choice.float_summa(choice.convert_bin_to_float(float1), choice.convert_bin_to_float(float2))
     print("Результат:", result)

if __name__ == '__main__':
    main()