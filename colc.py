import math
import re


class DecimalCalculator:
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
            'десятых': 10, 'сотых': 100, 'тысячных': 1000
        }

    def text_to_number(self, text):
        """Преобразует текстовое представление числа в числовое"""
        if text == 'ноль':
            return 0.0

        parts = text.split(' и ')
        integer_part = parts[0]
        decimal_part = parts[1] if len(parts) > 1 else None

        # Обрабатываем целую часть
        integer_value = self._parse_integer_part(integer_part)

        # Обрабатываем дробную часть
        decimal_value = 0.0
        if decimal_part:
            decimal_value = self._parse_decimal_part(decimal_part)

        return integer_value + decimal_value

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

        result += current
        return result

    def _parse_decimal_part(self, text):
        """Парсит дробную часть числа"""
        words = text.split()
        numerator = 0
        denominator = 1

        # Ищем числитель и знаменатель
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

        return numerator / denominator

    def number_to_text(self, number):
        """Преобразует число в текстовое представление"""
        if number == 0:
            return "ноль"

        # Округляем до тысячных
        number = round(number, 3)

        integer_part = int(number)
        decimal_part = round(number - integer_part, 3)

        integer_text = self._integer_to_text(integer_part)

        if decimal_part == 0:
            return integer_text
        else:
            decimal_text = self._decimal_to_text(decimal_part)
            return f"{integer_text} и {decimal_text}"

    def _integer_to_text(self, number):
        """Преобразует целое число в текст"""
        if number == 0:
            return "ноль"

        result = []

        # Обрабатываем сотни
        hundreds = number // 100
        if hundreds > 0:
            for key, value in self.hundreds.items():
                if value == hundreds * 100:
                    result.append(key)
                    break

        # Обрабатываем десятки и единицы
        remainder = number % 100
        if remainder > 0:
            if remainder in self.units:
                result.append(self._get_unit_key(remainder))
            else:
                tens_part = (remainder // 10) * 10
                units_part = remainder % 10

                for key, value in self.tens.items():
                    if value == tens_part:
                        result.append(key)
                        break

                if units_part > 0:
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
        # Определяем точность
        if decimal == 0:
            return ""

        # Умножаем на 1000 и округляем до целого
        decimal_rounded = round(decimal, 3)
        numerator = int(round(decimal_rounded * 1000))

        # Определяем знаменатель и сокращаем если нужно
        if numerator % 10 == 0:
            denominator = 100
            numerator = numerator // 10
        elif numerator % 100 == 0:
            denominator = 10
            numerator = numerator // 100
        else:
            denominator = 1000

        # Получаем текстовое представление числителя
        numerator_text = self._integer_to_text(numerator)

        # Получаем текстовое представление знаменателя
        denominator_text = self._get_denominator_text(denominator)

        return f"{numerator_text} {denominator_text}"

    def _get_denominator_text(self, denominator):
        """Возвращает текстовое представление знаменателя"""
        denominators = {
            10: 'десятых',
            100: 'сотых',
            1000: 'тысячных'
        }
        return denominators[denominator]

    def calculate(self, expression):
        """Выполняет вычисление по текстовому выражению"""
        # Нормализуем выражение
        expression = expression.lower().replace('на', '').strip()

        # Определяем операцию
        if 'разделить' in expression:
            parts = expression.split('разделить')
            operation = '/'
        elif 'остаток' in expression:
            parts = expression.split('остаток')
            operation = '%'
        else:
            raise ValueError("Неизвестная операция")

        if len(parts) != 2:
            raise ValueError("Некорректное выражение")

        # Парсим операнды
        left_operand = self.text_to_number(parts[0].strip())
        right_operand = self.text_to_number(parts[1].strip())

        # Выполняем операцию
        if operation == '/':
            if right_operand == 0:
                raise ValueError("Деление на ноль")
            result = left_operand / right_operand
        else:  # '%'
            result = left_operand % right_operand

        # Преобразуем результат в текст
        return self.number_to_text(result)


def calc(expression):
    """Основная функция калькулятора"""
    calculator = DecimalCalculator()
    return calculator.calculate(expression)



print("Напишите выражение для вычисления")

result = calc(input())
print('ответ:', result)

''''
Примеры:
десять и пять десятых разделить на два
сто и двадцать пять тысячных разделить на пять
семь и три сотых разделить на три
пятьдесят разделить на четыре
десять и три десятых разделить на три и одна десятая
'''