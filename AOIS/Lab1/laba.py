class Digit:
    def __init__(self):
        self.TOTAL_BITS = 32
        self.MAX_BITS = 31
        self.EXPONENT_BITS = 127
        self.MANTISSA_BITS = 23
        self.NUM_0, self.NUM_1, self.NUM_9, self.NUM_32 = 0, 1, 9, 32
        self.IEEE = '01111111'

    def positive_bin(self, dec_num):
        number = int(dec_num)
        binary = ''
        while number > 0:
            binary = str(number % 2) + binary
            number //= 2
        while len(binary) < self.MAX_BITS:
            binary = '0' + binary
        return '0' + binary

    def negative_bin(self, dec_num):
        abs_number = abs(dec_num)
        binary = self.positive_bin(abs_number)[1:]
        return '1' + binary.zfill(self.MAX_BITS)

    def preadditional_summa(self, bin_string):
        bin_list = list(bin_string)
        transfer = 1
        for i in range(len(bin_list) - 1, -1, -1):
            if transfer == 0:
                break
            if bin_list[i] == '0':
                bin_list[i] = '1'
                transfer = 0
            else:
                bin_list[i] = '0'
        if transfer:
            bin_list.insert(0, '1')
        return ''.join(bin_list)

    def binary_to_dec_num(self, binary: str) -> int:
        decimal = 0
        length = len(binary)
        for i in range(length):
            if binary[i] == '1':
                decimal += 2 ** (length - i - 1)
        return decimal

    def convert_to_dec(self, binary_number: str) -> int:
        if binary_number[0] == '1':
            for b in binary_number[1:]:
                if b == '0':
                    inverted += '1'
                else:
                    inverted += '0'
            return -self.binary_to_dec_num(inverted) - 1
        return self.binary_to_dec_num(binary_number)

    def convert_to_binary_number(self, dec_num):
        if dec_num >= 0:
            return self.positive_bin(dec_num)
        return self.negative_bin(dec_num)

    def direct_summa(self, num1, num2):
        bin1 = self.convert_to_binary_number(num1).zfill(self.TOTAL_BITS)
        bin2 = self.convert_to_binary_number(num2).zfill(self.TOTAL_BITS)
        result = []
        carry = 0
        for i in range(self.MAX_BITS, -1, -1):
            sum_bit = int(bin1[i]) + int(bin2[i]) + carry
            result.append(str(sum_bit % 2))
            carry = sum_bit // 2
        result = ''.join(reversed(result))
        return result[-self.TOTAL_BITS:]

    def convert_to_reverse_binary(self, dec_num):
        if dec_num >= 0:
            return self.positive_bin(dec_num)
        positive = self.positive_bin(abs(dec_num))
        inverted = ''.join('1' if b == '0' else '0' for b in positive[1:])
        return '1' + inverted

    def convert_to_additional_binary(self, dec_num):
        if dec_num > 0:
            return self.convert_to_reverse_binary(dec_num)
        else:
            binary_number = self.convert_to_reverse_binary(dec_num)
            binary_number = self.preadditional_summa(binary_number)
            return binary_number

    def additional_summa(self, num1, num2):
        bin1 = self.convert_to_additional_binary(num1).zfill(self.TOTAL_BITS)
        bin2 = self.convert_to_additional_binary(num2).zfill(self.TOTAL_BITS)

        bring = 0
        result = []
        for i in range(self.MAX_BITS, -1, -1):
            total = int(bin1[i]) + int(bin2[i]) + bring
            result.append(str(total % 2))
            bring = total // 2

        result = ''.join(reversed(result))
        return result[-self.TOTAL_BITS:]

    def additional_subtract(self, number1, number2):
        bin1 = self.convert_to_additional_binary(number1).zfill(self.TOTAL_BITS)
        bin2 = self.convert_to_additional_binary(-number2).zfill(self.TOTAL_BITS)
        carry = 0
        result = []
        for i in range(self.MAX_BITS, -1, -1):
            total = int(bin1[i]) + int(bin2[i]) + carry
            result.append(str(total % 2))
            carry = total // 2
        result = ''.join(reversed(result))
        return result[-self.TOTAL_BITS:]

    def direct_code_to_int(self, bin_str: str) -> int:
        sign = -1 if bin_str[0] == '1' else 1
        magnitude = int(bin_str[1:], 2)
        return sign * magnitude

    def direct_code_multiplication(self, num1, num2):
        if (num1 < 0 and num2 > 0) or (num1 > 0 and num2 < 0):
            result_sign = 1
        else:
            result_sign = 0

        abs_num1 = abs(num1)
        abs_num2 = abs(num2)

        bin_num1 = self.positive_bin(abs_num1).zfill(self.TOTAL_BITS)[1:]
        bin_num2 = self.positive_bin(abs_num2).zfill(self.TOTAL_BITS)[1:]

        product = [0] * (self.TOTAL_BITS * 2)

        for i in range(len(bin_num2) - 1, -1, -1):
            if bin_num2[i] == '1':
                carry = 0
                for j in range(len(bin_num1) - 1, -1, -1):
                    idx = i + j + 1
                    total = int(bin_num1[j]) + product[idx] + carry
                    product[idx] = total % 2
                    carry = total // 2
                product[i] += carry

        product_str = ''.join(str(bit) for bit in product)[-self.TOTAL_BITS:]

        if product_str.endswith('00'):
            product_str = product_str[:-2]

        result_bin = str(result_sign) + product_str
        result_dec = self.direct_code_to_int(result_bin)
        return f"Результат в прямом коде: [{result_bin}]  Десятичный результат: {result_dec}"

    def float_to_binary_fraction(self, fraction: float) -> str:
        binary_fraction = ""
        while fraction != 0 and len(binary_fraction) < self.TOTAL_BITS:
            fraction *= 2
            if fraction >= 1:
                binary_fraction += '1'
                fraction -= 1
            else:
                binary_fraction += '0'
        return binary_fraction

    def display_ieee(self, ieee_binary_str):
        sign_bit = ieee_binary_str[0]
        mantissa_bits, exponent_bits = '', ''
        for i in range(1, 9):
            exponent_bits += ieee_binary_str[i]
        for i in range(9, 32):
            mantissa_bits += ieee_binary_str[i]
        print(f"IEEE-754: [{sign_bit} {exponent_bits} {mantissa_bits}]")

    def convert_float_to_bin(self, float_number: float) -> str:
        if float_number == 0.0:
            return '0' * self.TOTAL_BITS

        sign_bit = '0' if float_number >= 0 else '1'
        float_number = abs(float_number)

        exponent_counter = 0
        normalized_float = float_number

        if normalized_float >= 1.0:
            while normalized_float >= 2.0:
                normalized_float /= 2.0
                exponent_counter += 1
        else:
            while normalized_float < 1.0:
                normalized_float *= 2.0
                exponent_counter -= 1

        biased_exponent = exponent_counter + self.EXPONENT_BITS

        exponent_binary_string = ''
        temp_exponent = biased_exponent
        for _ in range(8):
            exponent_binary_string = str(temp_exponent % 2) + exponent_binary_string
            temp_exponent //= 2

        normalized_float -= 1.0
        mantissa_bits = ''
        for _ in range(self.MANTISSA_BITS):
            normalized_float *= 2
            if normalized_float >= 1.0:
                mantissa_bits += '1'
                normalized_float -= 1.0
            else:
                mantissa_bits += '0'

        final_binary_string = sign_bit + exponent_binary_string + mantissa_bits
        return final_binary_string

    def convert_bin_to_float(self, binary_str) -> float:
        sign_char = int(binary_str[0])
        sign = -1 if sign_char else 1

        exponent_bits = ''
        for i in range(1, 9):
            exponent_bits += binary_str[i]
        exponent_value = int(exponent_bits, 2) - self.EXPONENT_BITS

        mantissa_value = 1.0
        for idx in range(9, len(binary_str)):
            if binary_str[idx] == '1':
                mantissa_value += 2 ** -(idx - 8)

        float_result = sign * mantissa_value * (2 ** exponent_value)
        return float_result

    def float_summa(self, float_num1, float_num2):
        FULL_MANTISSA = self.MANTISSA_BITS + 1

        bin_num1 = self.convert_float_to_bin(float_num1)
        bin_num2 = self.convert_float_to_bin(float_num2)

        sign1, exp_bits1, mantissa1 = bin_num1[0], bin_num1[1:9], '1' + bin_num1[9:]
        sign2, exp_bits2, mantissa2 = bin_num2[0], bin_num2[1:9], '1' + bin_num2[9:]

        exp_val1 = int(exp_bits1, 2) - self.EXPONENT_BITS
        exp_val2 = int(exp_bits2, 2) - self.EXPONENT_BITS

        if exp_val1 > exp_val2:
            shift = exp_val1 - exp_val2
            mantissa2 = ('0' * shift) + mantissa2[:-shift]
            exp_val2 = exp_val1
        elif exp_val2 > exp_val1:
            shift = exp_val2 - exp_val1
            mantissa1 = ('0' * shift) + mantissa1[:-shift]
            exp_val1 = exp_val2

        mantissa_val1 = int(mantissa1, 2)
        mantissa_val2 = int(mantissa2, 2)

        if sign1 == sign2:
            mantissa_sum = mantissa_val1 + mantissa_val2
            res_sign = sign1
        else:
            if mantissa_val1 >= mantissa_val2:
                mantissa_sum = mantissa_val1 - mantissa_val2
                res_sign = sign1
            else:
                mantissa_sum = mantissa_val2 - mantissa_val1
                res_sign = sign2

        if mantissa_sum == 0:
            return 0.0

        while mantissa_sum >= (1 << FULL_MANTISSA):
            mantissa_sum >>= 1
            exp_val1 += 1

        while mantissa_sum < (1 << self.MANTISSA_BITS):
            mantissa_sum <<= 1
            exp_val1 -= 1

        final_exp = exp_val1 + self.EXPONENT_BITS
        exp_bits = f"{final_exp:08b}"
        mantissa_bits = f"{mantissa_sum:0{FULL_MANTISSA}b}"[1:]

        result_bin = res_sign + exp_bits + mantissa_bits
        return self.convert_bin_to_float(result_bin)


    def divide_bin(self, dividend_dec, divisor_dec):

        if divisor_dec == 0:
            raise ValueError("Делить на ноль нельзя.")
        if (dividend_dec < 0) and (divisor_dec >= 0):
            result_sign_bit = '1'
        elif (dividend_dec >= 0) and (divisor_dec < 0):
            result_sign_bit = '1'
        else:
            result_sign_bit = '0'

        dividend_abs = abs(dividend_dec)
        divisor_abs = abs(divisor_dec)

        dividend_bin = bin(dividend_abs)[2:]
        divisor_bin = bin(divisor_abs)[2:]
        quotient_bin = ''
        current_remainder = ''

        for bit in dividend_bin:
            current_remainder += bit
            current_remainder = current_remainder.lstrip('0') or '0'
            if len(current_remainder) > len(divisor_bin) or (
                    len(current_remainder) == len(divisor_bin) and int(current_remainder, 2) >= int(divisor_bin, 2)
            ):
                current_remainder = bin(int(current_remainder, 2) - int(divisor_bin, 2))[2:]
                quotient_bin += '1'
            else:
                quotient_bin += '0'

        quotient_bin = quotient_bin.lstrip('0') or '0'

        fractional_part_bin = ''
        for _ in range(self.MANTISSA_BITS - 10):
            current_remainder += '0'
            current_remainder = current_remainder.lstrip('0') or '0'
            if len(current_remainder) > len(divisor_bin) or (
                    len(current_remainder) == len(divisor_bin) and int(current_remainder, 2) >= int(divisor_bin, 2)
            ):
                current_remainder = bin(int(current_remainder, 2) - int(divisor_bin, 2))[2:]
                fractional_part_bin += '1'
            else:
                fractional_part_bin += '0'
            if current_remainder == '0':
                break

        if quotient_bin != '0' :
            quotient_decimal = int(quotient_bin, 2)
        else :
            quotient_decimal = 0

        fractional_decimal = 0

        for i, bit in enumerate(fractional_part_bin):
            if bit == '1':
                fractional_decimal += 1 / (2 ** (i + 1))

        decimal_result = quotient_decimal + fractional_decimal
        if result_sign_bit == '1':
            decimal_result = -decimal_result

        decimal_result = round(decimal_result, 5)

        binary_result_str = f"{result_sign_bit} {quotient_bin}.{fractional_part_bin}"
        return f"Результат в прямом коде: [{binary_result_str}]  Десятичный результат: {decimal_result}"


