import re
from decimal import Decimal, getcontext
from fractions import Fraction


class AdvancedDecimalCalculator:
    def __init__(self):
        # Словари для числительных
        self.units = {
            'ноль': 0, 'один': 1, 'одна': 1, 'два': 2, 'две': 2, 'три': 3,
            'четыре': 4, 'пять': 5, 'шесть': 6, 'семь': 7, 'восемь': 8,
            'девять': 9, 'десять': 10, 'одиннадцать': 11, 'двенадцать': 12,
            'тринадцать': 13, 'четырнадцать': 14, 'пятнадцать': 15,
            'шестнадцать': 16, 'семнадцать': 17, 'восемнадцать': 18,
            'девятнадцать': 19
        }

        self.tens = {
            'двадцать': 20, 'тридцать': 30, 'сорок': 40, 'пятьдесят': 50,
            'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят': 80,
            'девяносто': 90
        }

        self.hundreds = {
            'сто': 100, 'двести': 200, 'триста': 300, 'четыреста': 400,
            'пятьсот': 500, 'шестьсот': 600, 'семьсот': 700,
            'восемьсот': 800, 'девятьсот': 900
        }

        self.fractions = {
            'десятых': 10, 'сотых': 100, 'тысячных': 1000,
            'десятитысячных': 10000, 'стотысячных': 100000,
            'миллионных': 1000000
        }

        self.operations = {
            'плюс': '+', 'прибавить': '+', 'сложить': '+',
            'минус': '-', 'вычесть': '-', 'отнять': '-',
            'умножить': '*', 'умножить на': '*', 'произведение': '*',
            'разделить': '/', 'делить': '/', 'деление': '/',
            'остаток': '%', 'остаток от деления': '%', 'модуль': '%'
        }

        # Устанавливаем высокую точность
        getcontext().prec = 20

    def text_to_number(self, text):
        """Преобразует текстовое представление числа в числовое"""
        text = text.strip()
        if text == 'ноль':
            return Decimal('0')

        # Проверяем на отрицательное число
        is_negative = False
        if text.startswith('минус '):
            is_negative = True
            text = text[6:]

        parts = text.split(' и ')
        integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else None

        # Обрабатываем целую часть
        integer_value = self._parse_integer_part(integer_part)

        # Обрабатываем дробную часть
        decimal_value = Decimal('0')
        if decimal_part:
            decimal_value = self._parse_decimal_part(decimal_part)

        result = Decimal(str(integer_value)) + decimal_value
        return -result if is_negative else result

    def _parse_integer_part(self, text):
        """Парсит целую часть числа"""
        words = text.split()
        result = 0
        current = 0

        for word in words:
            if word in self.units:
                current += self.units[word]
            elif word in self.tens:
                current += self.tens[word]
            elif word in self.hundreds:
                current += self.hundreds[word]
            elif word == 'тысяча':
                current *= 1000
                result += current
                current = 0
            elif word == 'миллион':
                current *= 1000000
                result += current
                current = 0

        result += current
        return result

    def _parse_decimal_part(self, text):
        """Парсит дробную часть числа до миллионных"""
        words = text.split()
        numerator = 0
        denominator = 1

        current_num = 0
        for word in words:
            if word in self.units:
                current_num += self.units[word]
            elif word in self.tens:
                current_num += self.tens[word]
            elif word in self.hundreds:
                current_num += self.hundreds[word]
            elif word in self.fractions:
                numerator = current_num
                denominator = self.fractions[word]
                break

        return Decimal(str(numerator)) / Decimal(str(denominator))

    def _find_repeating_decimal(self, decimal_str, max_period_length=4):
        """Находит периодическую часть в десятичной дроби"""
        if not decimal_str or decimal_str == '0':
            return None, None

        # Убираем незначащие нули в конце
        decimal_str = decimal_str.rstrip('0')
        if not decimal_str:
            return None, None

        # Ищем период разной длины
        for period_len in range(1, max_period_length + 1):
            for start in range(len(decimal_str) - period_len * 2 + 1):
                period = decimal_str[start:start + period_len]

                # Проверяем, повторяется ли период
                is_repeating = True
                for i in range(1, 3):  # Проверяем минимум 3 повторения
                    next_start = start + period_len * i
                    next_end = next_start + period_len
                    if next_end > len(decimal_str):
                        is_repeating = False
                        break
                    if decimal_str[next_start:next_end] != period:
                        is_repeating = False
                        break

                if is_repeating and period != '0' * len(period):
                    return start, period

        return None, None

    def number_to_text(self, number):
        """Преобразует число в текстовое представление с учетом периодичности"""
        number = Decimal(str(number))

        if number == 0:
            return "ноль"

        # Обработка отрицательных чисел
        is_negative = number < 0
        if is_negative:
            number = -number

        integer_part = int(number)
        decimal_part = number - Decimal(integer_part)

        # Преобразуем дробную часть в строку с высокой точностью
        decimal_str = format(decimal_part, '.20f').split('.')[1].rstrip('0')

        # Проверяем на периодичность
        period_start, period = self._find_repeating_decimal(decimal_str)

        integer_text = self._integer_to_text(integer_part)

        if decimal_str and decimal_str != '0':
            if period:
                # Периодическая дробь
                non_periodic = decimal_str[:period_start]
                periodic_text = self._decimal_to_text_periodic(non_periodic, period)
                result = f"{integer_text} и {periodic_text}"
            else:
                # Обычная дробь (округляем до миллионных)
                rounded_decimal = decimal_part.quantize(Decimal('0.000001'))
                if rounded_decimal > 0:
                    decimal_text = self._decimal_to_text(rounded_decimal)
                    result = f"{integer_text} и {decimal_text}"
                else:
                    result = integer_text
        else:
            result = integer_text

        return f"минус {result}" if is_negative else result

    def _decimal_to_text_periodic(self, non_periodic, period):
        """Формирует текст для периодической дроби"""
        non_periodic_text = ""
        if non_periodic and non_periodic != '0':
            non_periodic_num = int(non_periodic)
            non_periodic_text = self._integer_to_text(non_periodic_num)

        period_num = int(period)
        period_text = self._integer_to_text(period_num)

        # Определяем разрядность непериодической части
        non_periodic_digits = len(non_periodic)
        period_digits = len(period)

        denominator_non_periodic = self._get_fraction_name(10 ** non_periodic_digits)
        denominator_periodic = self._get_fraction_name(10 ** (non_periodic_digits + period_digits))

        if non_periodic_text:
            return f"{non_periodic_text} {denominator_non_periodic} и {period_text} {denominator_periodic} в периоде"
        else:
            return f"{period_text} {denominator_periodic} в периоде"

    def _integer_to_text(self, number):
        """Преобразует целое число в текст"""
        if number == 0:
            return "ноль"

        result = []

        # Миллионы
        millions = number // 1000000
        if millions > 0:
            result.append(self._number_to_text_simple(millions))
            result.append('миллион' + self._get_plural_suffix(millions))
            number %= 1000000

        # Тысячи
        thousands = number // 1000
        if thousands > 0:
            result.append(self._number_to_text_simple(thousands, True))
            result.append('тысяча' + self._get_plural_suffix(thousands, True))
            number %= 1000

        # Сотни, десятки, единицы
        if number > 0:
            result.append(self._number_to_text_simple(number))

        return ' '.join(result)

    def _number_to_text_simple(self, number, for_thousands=False):
        """Преобразует числа до 999 в текст"""
        if number == 0:
            return ""

        result = []

        # Сотни
        hundreds = number // 100
        if hundreds > 0:
            for key, value in self.hundreds.items():
                if value == hundreds * 100:
                    result.append(key)
                    break

        # Десятки и единицы
        remainder = number % 100
        if remainder > 0:
            if remainder in self.units:
                if for_thousands and remainder in [1, 2]:
                    result.append('одна' if remainder == 1 else 'две')
                else:
                    result.append(self._get_unit_key(remainder))
            else:
                tens_part = (remainder // 10) * 10
                units_part = remainder % 10

                for key, value in self.tens.items():
                    if value == tens_part:
                        result.append(key)
                        break

                if units_part > 0:
                    if for_thousands and units_part in [1, 2]:
                        result.append('одна' if units_part == 1 else 'две')
                    else:
                        result.append(self._get_unit_key(units_part))

        return ' '.join(result)

    def _get_unit_key(self, number):
        """Возвращает правильную форму числительного"""
        forms = {
            1: 'один', 2: 'два', 3: 'три', 4: 'четыре',
            5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь',
            9: 'девять', 10: 'десять', 11: 'одиннадцать',
            12: 'двенадцать', 13: 'тринадцать', 14: 'четырнадцать',
            15: 'пятнадцать', 16: 'шестнадцать', 17: 'семнадцать',
            18: 'восемнадцать', 19: 'девятнадцать'
        }
        return forms[number]

    def _decimal_to_text(self, decimal):
        """Преобразует дробную часть в текст"""
        # Преобразуем в дробь с знаменателем до миллионных
        decimal_str = format(decimal, '.6f').split('.')[1].rstrip('0')
        if not decimal_str:
            return ""

        numerator = int(decimal_str)
        denominator = 10 ** len(decimal_str)

        # Сокращаем дробь если возможно
        from math import gcd
        divisor = gcd(numerator, denominator)
        numerator //= divisor
        denominator //= divisor

        numerator_text = self._integer_to_text(numerator)
        denominator_text = self._get_fraction_name(denominator)

        return f"{numerator_text} {denominator_text}"

    def _get_fraction_name(self, denominator):
        """Возвращает название дробной части"""
        names = {
            10: 'десятых',
            100: 'сотых',
            1000: 'тысячных',
            10000: 'десятитысячных',
            100000: 'стотысячных',
            1000000: 'миллионных'
        }
        return names.get(denominator, '')

    def _get_plural_suffix(self, number, for_thousands=False):
        """Возвращает правильное окончание для тысяч/миллионов"""
        if for_thousands:
            if number % 10 == 1 and number % 100 != 11:
                return ""
            elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
                return "и"
            else:
                return ""
        else:
            if number % 10 == 1 and number % 100 != 11:
                return ""
            elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
                return "а"
            else:
                return "ов"

    def parse_expression(self, expression):
        """Парсит математическое выражение с произвольным количеством операций"""
        expression = expression.lower()

        # Заменяем текстовые операции на символы
        for text_op, symbol in sorted(self.operations.items(), key=lambda x: -len(x[0])):
            expression = expression.replace(text_op, f" {symbol} ")

        # Разбиваем на токены
        tokens = re.findall(r'[-+]?\d*\.?\d+|[+\-*/%()]|[а-я]+', expression)
        tokens = [token.strip() for token in tokens if token.strip()]

        # Преобразуем числовые токены
        parsed_tokens = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in ['+', '-', '*', '/', '%', '(', ')']:
                parsed_tokens.append(token)
                i += 1
            else:
                # Собираем числовое выражение до следующего оператора
                number_parts = []
                while i < len(tokens) and tokens[i] not in ['+', '-', '*', '/', '%', '(', ')']:
                    number_parts.append(tokens[i])
                    i += 1
                number_text = ' '.join(number_parts)
                try:
                    number = self.text_to_number(number_text)
                    parsed_tokens.append(number)
                except:
                    raise ValueError(f"Не могу распознать число: {number_text}")

        return parsed_tokens

    def evaluate_expression(self, tokens):
        """Вычисляет значение выражения с учетом приоритета операций"""

        def apply_operator(operators, values):
            operator = operators.pop()
            right = values.pop()
            left = values.pop()
            if operator == '+':
                values.append(left + right)
            elif operator == '-':
                values.append(left - right)
            elif operator == '*':
                values.append(left * right)
            elif operator == '/':
                if right == 0:
                    raise ValueError("Деление на ноль")
                values.append(left / right)
            elif operator == '%':
                values.append(left % right)

        def precedence(op):
            if op in ['+', '-']:
                return 1
            if op in ['*', '/', '%']:
                return 2
            return 0

        values = []
        operators = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if isinstance(token, Decimal):
                values.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operators, values)
                operators.pop()  # Убираем '('
            else:
                while (operators and operators[-1] != '(' and
                       precedence(operators[-1]) >= precedence(token)):
                    apply_operator(operators, values)
                operators.append(token)

            i += 1

        while operators:
            apply_operator(operators, values)

        return values[0] if values else Decimal('0')

    def calculate(self, expression):
        """Вычисляет текстовое математическое выражение"""
        try:
            tokens = self.parse_expression(expression)
            result = self.evaluate_expression(tokens)
            return self.number_to_text(result)
        except Exception as e:
            return f"Ошибка: {str(e)}"


def calc(expression):
    calculator = AdvancedDecimalCalculator()
    return calculator.calculate(expression)

print("Напишите выражение для вычисления")

result = calc(input())
print('ответ:', result)

