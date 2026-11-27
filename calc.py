from decimal import Decimal, InvalidOperation
from fractions import Fraction
from math import isqrt
from operator import add, sub, mul, truediv
from time import perf_counter


def parse_number(text):
    """Преобразует введённое число в точную дробь."""
    try:
        if "/" in text:
            numerator, denominator = text.split("/", 1)
            return Fraction(int(numerator), int(denominator))
        number = Decimal(text.replace(",", "."))
        if not number.is_finite():
            raise ValueError
        return Fraction(number)
    except (ValueError, InvalidOperation):
        raise ValueError(
            "Введите целое число, дробь вида 3/4 или число вида 0,25."
        ) from None


def exact_nth_root(value, degree):
    """Возвращает целый корень, если он существует, иначе — None."""
    if value < 2 or degree == 1:
        return value

    bits = value.bit_length()
    if degree >= bits:
        return None
    low = 1
    high = 1 << ((bits + degree - 1) // degree)

    while low <= high:
        middle = (low + high) // 2
        powered = middle ** degree

        if powered == value:
            return middle
        if powered < value:
            low = middle + 1
        else:
            high = middle - 1

    return None


def power(base, exponent):
    """Возводит число в целую или дробную степень."""
    p = exponent.numerator
    q = exponent.denominator

    if q == 1:
        return base ** p

    if base < 0 and q % 2 == 0:
        raise ValueError(
            "У отрицательного числа нет действительного корня чётной степени."
        )

    if base == 0:
        if p < 0:
            raise ZeroDivisionError
        return Fraction(0)

    negative = base < 0 and p % 2 != 0
    magnitude = abs(base)
    if p < 0:
        magnitude = Fraction(1) / magnitude
        p = -p

    numerator_root = exact_nth_root(magnitude.numerator, q)
    denominator_root = exact_nth_root(magnitude.denominator, q)

    if numerator_root is not None and denominator_root is not None:
        result = Fraction(numerator_root, denominator_root) ** p
        return -result if negative else result

    result = f"root({q}, {magnitude})"
    if p != 1:
        result = f"{result}^{p}"
    return f"-({result})" if negative else result


def square_root(number):
    """Возвращает квадратный корень как дробь или точную запись."""
    if number < 0:
        raise ValueError(
            "У отрицательного числа нет действительного квадратного корня."
        )

    numerator_root = isqrt(number.numerator)
    denominator_root = isqrt(number.denominator)
    if (
        numerator_root ** 2 == number.numerator
        and denominator_root ** 2 == number.denominator
    ):
        return Fraction(numerator_root, denominator_root)
    return f"√({number})"


# Каждому знаку соответствует функция, которая выполняет операцию.
OPERATIONS = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
    "^": power,
    "**": power,
}


def main():
    print("Примеры: 1/3 + 0,25, 8/27 ^ -2/3, sqrt 9/16")
    print("Ставьте пробелы вокруг знака операции, но не внутри дроби.")
    print("Пустая строка — выход.")

    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            break

        parts = line.split()
        try:
            # Выбираем операцию и разбираем числа до запуска таймера.
            if len(parts) == 2 and parts[0] == "sqrt":
                operation = square_root
                args = (parse_number(parts[1]),)
            elif len(parts) == 3 and parts[1] in OPERATIONS:
                left, sign, right = parts
                operation = OPERATIONS[sign]
                args = (parse_number(left), parse_number(right))
            else:
                raise ValueError(
                    "Введите выражение в формате «2 ^ 3» или «sqrt 9/16»."
                )

            # Замеряем только время выполнения операции.
            start = perf_counter()
            result = operation(*args)
            elapsed_ms = (perf_counter() - start) * 1000

            print(result)
            print(f"Время операции: {elapsed_ms:.6f} мс")
        except ZeroDivisionError:
            print("Ошибка: деление на ноль или нулевой знаменатель.")
        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
