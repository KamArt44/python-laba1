import re
import operator
from toolkit.errors import ToolkitError
allowed_characters =   set([str(i) for i in range(10)] + ["*", "-", "+", "/", "(", ")", " ", "."])


dict_action = {
    "+": operator.add,
    "-": operator.sub,
    "/": operator.truediv,
    "*": operator.mul,
    "**": operator.pow,
}

# u- и u+ — это унарный минус и унарный плюс
dict_operations = {
    "**": 4,
    "u-": 3,
    "u+": 3,
    "*": 2,
    "/": 2,
    "+": 1,
    "-": 1,
}

UNARY_OPERATIONS = {"u-", "u+"}


def to_number(s: str):
    if "." in s:
        return float(s)
    return int(s)


def calculate_expression(math_expression : str) -> int|float:
     validation_characters(math_expression)
     tokens =  transformation_math_expression(math_expression)
     validate_tokens(tokens)
     return expression_stack(tokens)


def validation_characters(math_expression: str)-> None:
    for char in math_expression:
        if char not in allowed_characters:
            raise ToolkitError(f"Недопустимый символ: {char}")

def transformation_math_expression(math_expression: str) -> list:
    """
    Разбирает строку с математическим выражением в список токенов.
    Поддерживает унарный минус и унарный плюс.
    """
    expr = math_expression.replace(" ", "")

    # Сначала распознаём числа и операторы
    pattern = r"\d+(?:\.\d+)?|\*\*|[()+\-*/]"
    raw_tokens = re.findall(pattern, expr)

    tokens: list[int | float | str] = []

    for token in raw_tokens:
        # Определяем, является ли + или - унарным оператором
        if token in {"-", "+"} and (
            not tokens
            or tokens[-1] == "("
            or tokens[-1] in dict_operations
        ):
            if token == "-":
                tokens.append("u-")
            else:
                tokens.append("u+")

        # Числа
        elif re.fullmatch(r"\d+(?:\.\d+)?", token):
            tokens.append(to_number(token))

        # Остальные операторы и скобки
        else:
            tokens.append(token)

    return tokens

def validate_tokens(tokens: list) -> None:
    """
    Проверяет корректность последовательности токенов.
    Если выражение некорректное, возбуждает ValueError.
    """
    if not tokens:
        raise ToolkitError("Пустое выражение")

    expect_operand = True
    parentheses_balance = 0

    for token in tokens:
        # Число
        if isinstance(token, (int, float)):
            if not expect_operand:
                raise ToolkitError("Пропущен оператор")

            expect_operand = False

        # Открывающая скобка
        elif token == "(":
            if not expect_operand:
                raise ToolkitError("Пропущен оператор")

            parentheses_balance += 1
            expect_operand = True

        # Закрывающая скобка
        elif token == ")":
            if expect_operand:
                raise ToolkitError("Пропущен операнд")

            parentheses_balance -= 1

            if parentheses_balance < 0:
                raise ToolkitError("Лишняя закрывающая скобка")

            expect_operand = False

        # Унарный оператор
        elif token in {"u-", "u+"}:
            if not expect_operand:
                raise ToolkitError("Лишний унарный оператор")

            expect_operand = True

        # Бинарный оператор
        elif token in {"+", "-", "*", "/"}:
            if expect_operand:
                raise ToolkitError("Пропущен операнд")

            expect_operand = True

        else:
            raise ToolkitError(f"Недопустимый токен: {token}")

    if expect_operand:
        raise ToolkitError("Пропущен операнд")

    if parentheses_balance != 0:
        raise ToolkitError("Непарные скобки")


def apply_top(stack_operands: list, stack_operations: list):
    """
    Применяет верхнюю операцию из стека операций к стеку операндов.
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
        stack_operands.append(dict_action[operation](a, b))


def expression_stack(new_math_expression: list):
    """
    Вычисляет выражение, используя стеки операндов и операций.
    """
    stack_operands = []
    stack_operations = []

    for char in new_math_expression:
        # Если это число
        if isinstance(char, (int, float)):
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
        elif char in dict_operations:
            # Унарные операторы просто кладём в стек
            if char in UNARY_OPERATIONS:
                stack_operations.append(char)

            # Для бинарных операторов учитываем приоритет
            else:
                while (
                    stack_operations
                    and stack_operations[-1] != "("
                    and stack_operations[-1] in dict_operations
                    and dict_operations[char] <= dict_operations[stack_operations[-1]]
                ):
                    apply_top(stack_operands, stack_operations)

                stack_operations.append(char)

    # После разбора выражения применяем оставшиеся операции
    while stack_operations:
        apply_top(stack_operands, stack_operations)

    if stack_operands:
        return stack_operands[0]

    return None
