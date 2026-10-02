import math
from toolkit.constants import (ABSOLUTE_ZERO,CELS,FAHRENHEIT1,FAHRENHEIT2,LEN,MASS,TEMP)
from toolkit.errors import ConverterError
def find_group(unit: str) -> str:
    unit = unit.lower()
    if unit in LEN:
        return "len"
    if unit in TEMP:
        return "temp"
    if unit in MASS:
        return "mass"
    raise ConverterError(f"Неизвестная единица: {unit}")

def to_kelvin(value: float, unit: str) -> float:
    #Переводит температуру в Кельвины.
    if value < ABSOLUTE_ZERO[unit]:
        raise ConverterError("Температура ниже абсолютного нуля")
    if value == ABSOLUTE_ZERO[unit]:
        return 0.0
    if unit == "c":
        kelvin = value + CELS
    elif unit == "f":
        kelvin = (value - FAHRENHEIT1) * FAHRENHEIT2+ CELS
    else:
        kelvin = value
    return kelvin


def kelvin_to(value: float, unit: str):
   # Переводит температуру из Кельвинов.
    if unit == "c":
        return value - CELS
    if unit == "f":
        return (value - CELS) / FAHRENHEIT2 + FAHRENHEIT1
    return value

def convert(value: float, from_unit: str, to_unit: str) -> float:
    # Переводит значение из одной единицы измерения в другую.
    if not math.isfinite(value):
        raise ConverterError("Неправильное значение")

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    from_group = find_group(from_unit)
    to_group = find_group(to_unit)

    if from_group != to_group:
        raise ConverterError(f"Разные величины: {from_unit} и {to_unit}")
    # температура
    if from_group == "temp":
        kelvin = to_kelvin(value, from_unit)
        return float(kelvin_to(kelvin, to_unit))
    # Длина или масса
    if from_group == "len":
        new_value = value * LEN[from_unit]
        result = new_value / LEN[to_unit]
    else:
        new_value = value * MASS[from_unit]
        result = new_value / MASS[to_unit]

    return float(result)
