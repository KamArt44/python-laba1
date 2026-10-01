import math

from toolkit.constants import (
    ABSOLUTE_ZERO,
    CELSIUS_OFFSET,
    FAHRENHEIT_OFFSET,
    FAHRENHEIT_SCALE,
    LENGTH_UNITS,
    MASS_UNITS,
    TEMPERATURE_UNITS,
)
from toolkit.errors import ConverterError


def _find_group(unit: str) -> str:
    """
    Определяет группу единицы измерения.
    """
    unit = unit.lower()

    if unit in LENGTH_UNITS:
        return "length"

    if unit in MASS_UNITS:
        return "mass"

    if unit in TEMPERATURE_UNITS:
        return "temperature"

    raise ConverterError(f"Неизвестная единица: {unit}")


def _temperature_to_kelvin(value: float, unit: str) -> float:
    """
    Переводит температуру в Кельвины.
    """
    if value < ABSOLUTE_ZERO[unit]:
        raise ConverterError("Температура ниже абсолютного нуля")
    # Точное граничное значение не должно пострадать от округления float.
    if value == ABSOLUTE_ZERO[unit]:
        return 0.0

    if unit == "c":
        kelvin = value + CELSIUS_OFFSET

    elif unit == "f":
        kelvin = (value - FAHRENHEIT_OFFSET) * FAHRENHEIT_SCALE + CELSIUS_OFFSET

    else:
        kelvin = value

    return kelvin


def _kelvin_to_temperature(value: float, unit: str) -> float:
    """
    Переводит температуру из Кельвинов в нужную единицу.
    """
    if unit == "c":
        return value - CELSIUS_OFFSET

    if unit == "f":
        return (value - CELSIUS_OFFSET) / FAHRENHEIT_SCALE + FAHRENHEIT_OFFSET

    return value


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Переводит значение из одной единицы измерения в другую.
    """
    try:
        value = float(value)
    except (TypeError, ValueError, OverflowError) as error:
        raise ConverterError("Неверное числовое значение") from error
    if not math.isfinite(value):
        raise ConverterError("Неверное числовое значение")

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    from_group = _find_group(from_unit)
    to_group = _find_group(to_unit)

    if from_group != to_group:
        raise ConverterError(f"Несовместимые единицы: {from_unit} и {to_unit}")

    # Температура
    if from_group == "temperature":
        kelvin = _temperature_to_kelvin(value, from_unit)
        return float(_kelvin_to_temperature(kelvin, to_unit))

    # Длина или масса
    if from_group == "length":
        base_value = value * LENGTH_UNITS[from_unit]
        result = base_value / LENGTH_UNITS[to_unit]

    else:
        base_value = value * MASS_UNITS[from_unit]
        result = base_value / MASS_UNITS[to_unit]

    return float(result)
