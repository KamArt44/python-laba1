from src.power import power_function


def test_power_positive_exponent() -> None:
    """Проверяет возведение числа в положительную степень."""
    assert power_function(target=2, power=3) == 8
