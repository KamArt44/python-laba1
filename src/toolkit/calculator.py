import re

from toolkit.constants import (
    ALLOWED_CHARACTERS,
    DICT_ACTION,
    DICT_OPERATIONS,
    TOKEN_PATTERN,
    UNARY_OPERATIONS,
)
from toolkit.errors import CalculatorError


def to_number(s: str) -> float:
    try:
        return float(s)
    except ValueError:
        raise CalculatorError("Неверное числовое значение") from None


def calculate_expression(math_expression: str) -> float:
    """Главная функция"""
    validation_characters(math_expression)
    tokens = transformation_math_expression(math_expression)
    validate_tokens(tokens)
    return expression_stack(tokens)


def validation_characters(math_expression: str) -> None:
    """Проверяет на символы"""
    for char in math_expression:
        if char not in ALLOWED_CHARACTERS:
            raise CalculatorError(f"Недопустимый символ: {char}")



def transformation_math_expression(math_expression: str) -> list:
    """
    Токенизация
    """

    raw_tokens = re.findall(TOKEN_PATTERN, math_expression)

    tokens: list[ float | str] = []

    for token in raw_tokens:
        # Определяем, является ли + или - унарным оператором
        if token in {"-", "+"} and (
            not tokens or tokens[-1] == "(" or tokens[-1] in DICT_OPERATIONS
        ):
            if token == "-":
                tokens.append("u-")
            else:
                tokens.append("u+")
        # Числа
        elif token[0].isdigit() or token[0] == ".":
            tokens.append(to_number(token))
        # Остальные операторы и скобки
        else:
            tokens.append(token)

    return tokens


def validate_tokens(tokens: list) -> None:
    """
    Валидация
    """
    if not tokens:
        raise CalculatorError("Пустое выражение")

    expect_operand = True
    parentheses_balance = 0
    for token in tokens:
        # Число
        if isinstance(token, float):
            if not expect_operand:
                raise CalculatorError("Пропущен оператор")

            expect_operand = False

        # Открывающая скобка
        elif token == "(":
            if not expect_operand:
                raise CalculatorError("Пропущен оператор")

            parentheses_balance += 1
            expect_operand = True

        # Закрывающая скобка
        elif token == ")":
            if expect_operand:
                raise CalculatorError("Пропущен операнд")

            parentheses_balance -= 1

            if parentheses_balance < 0:
                raise CalculatorError("Лишняя закрывающая скобка")

            expect_operand = False

        # Унарный оператор
        elif token in UNARY_OPERATIONS:
            if not expect_operand:
                raise CalculatorError("Лишний унарный оператор")

            expect_operand = True

        # Бинарный оператор
        elif token in {"+", "-", "*", "/"}:
            if expect_operand:
                raise CalculatorError("Пропущен операнд")

            expect_operand = True

        else:
            raise CalculatorError(f"Недопустимый токен: {token}")

    if expect_operand:
        raise CalculatorError("Пропущен операнд")

    if parentheses_balance != 0:
        raise CalculatorError("Непарные скобки")


def apply_top(stack_operands: list, stack_operations: list) -> None:
    """
    Применение операций из стека
    """
    operation = stack_operations.pop()

    # Унарные операции берут один операнд
    if operation == "u-":
        a = stack_operands.pop()
        stack_operands.append(-a)

    elif operation == "u+":
        a = stack_operands.pop()
        stack_operands.append(+a)

    # Бинарные операции берут два операнда
    else:
        b = stack_operands.pop()
        a = stack_operands.pop()
        if operation == "/" and b == 0:
            raise CalculatorError("Деление на ноль")
        stack_operands.append(DICT_ACTION[operation](a, b))


def expression_stack(new_math_expression: list) ->  float:
    """
    Вычисляет выражение, используя стеки операндов и операций.
    """
    stack_operands = []
    stack_operations = []
    for char in new_math_expression:
        # Если это число
        if isinstance(char,  float):
            stack_operands.append(char)

        # Открывающая скобка
        elif char == "(":
            stack_operations.append(char)

        # Закрывающая скобка
        elif char == ")":
            while stack_operations and stack_operations[-1] != "(":
                apply_top(stack_operands, stack_operations)

            # Убираем открывающую скобку
            if stack_operations and stack_operations[-1] == "(":
                stack_operations.pop()

        # Если это оператор
        elif char in DICT_OPERATIONS:
            # Унарные операторы кладём в стек.
            if char in UNARY_OPERATIONS:
                stack_operations.append(char)

            # Для бинарных операторов учитываем приоритет.
            else:
                while (
                    stack_operations
                    and stack_operations[-1] != "("
                    and stack_operations[-1] in DICT_OPERATIONS
                    and DICT_OPERATIONS[char] <= DICT_OPERATIONS[stack_operations[-1]]
                ):
                    apply_top(stack_operands, stack_operations)

                stack_operations.append(char)
    #  применяем оставшиеся операции
    while stack_operations:
        apply_top(stack_operands, stack_operations)
    if len(stack_operands) != 1:
        raise CalculatorError("Некорректное выражение")
    return stack_operands[0]
