import pytest

from toolkit.calculator import calculate_expression
from toolkit.errors import CalculatorError


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ("2 + 3 * 4", 14),
        ("(2 + 3) * 4", 20),
        ("10 - 3 - 2", 5),
        ("12 / 3 / 2", 2),
        ("2 * -3", -6),
        ("+2 + -3", -1),
        ("-(2 + 3)", -5),
        (".5 + 1.25", 1.75),
        (" 2\t+\n3 ", 5),
    ],
)
def test_valid_expression(expression: str, expected: float) -> None:
    """Проверяет арифметику, приоритеты, скобки и унарные знаки."""
    assert calculate_expression(expression) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("expression", "message"),
    [
        ("", "Пустое выражение"),
        ("   ", "Пустое выражение"),
        ("2 + a", "Недопустимый символ"),
        ("2 +", "Пропущен операнд"),
        ("2 * / 3", "Пропущен операнд"),
        ("1 / 0", "Деление на ноль"),
        ("1 / (2 - 2)", "Деление на ноль"),
        ("1 2", "Пропущен оператор"),
        ("1..2", "Неверное числовое значение"),
        (".", "Неверное числовое значение"),
        ("(2 + 3", "Непарные скобки"),
        ("2 + 3)", "Лишняя закрывающая скобка"),
    ],
)
def test_invalid_expression(expression: str, message: str) -> None:
    """Проверяет, что неверное выражение вызывает CalculatorError."""
    with pytest.raises(CalculatorError, match=message):
        calculate_expression(expression)
