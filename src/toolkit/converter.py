import math

from toolkit.constants import (ABSOLUTE_ZERO,CELSIUS,FAHRENHEIT1,FAHRENHEIT2,LENGTH,MASS,TEMPERATURE)
from toolkit.errors import ConverterError
def find_group(unit: str) -> str:
    unit = unit.lower()
    if unit in LENGTH:
        return "length"
    if unit in MASS:
        return "mass"
    if unit in TEMPERATURE:
        return "temperature"
    raise ConverterError(f"Неизвестная единица: {unit}")

def temperature_to_kelvin(value: float, unit: str) -> float:
    #Переводит температуру в Кельвины.
    if value < ABSOLUTE_ZERO[unit]:
        raise ConverterError("Температура ниже абсолютного нуля")
    if value == ABSOLUTE_ZERO[unit]:
        return 0.0
    if unit == "c":
        kelvin = value + CELSIUS
    elif unit == "f":
        kelvin = (value - FAHRENHEIT1) * FAHRENHEIT2+ CELSIUS
    else:
        kelvin = value
    return kelvin


def kelvin_to_temperature(value: float, unit: str) -> float:
   # Переводит температуру из Кельвинов.
    if unit == "c":
        return value - CELSIUS
    if unit == "f":
        return (value - CELSIUS) / FAHRENHEIT2 + FAHRENHEIT1
    return value

def convert(value: float, from_unit: str, to_unit: str) -> float:
    # Переводит значение из одной единицы измерения в другую.
    if not math.isfinite(value):
        raise ConverterError("Неверное числовое значение")

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    from_group = find_group(from_unit)
    to_group = find_group(to_unit)

    if from_group != to_group:
        raise ConverterError(f"Несовместимые единицы: {from_unit} и {to_unit}")
    # температура
    if from_group == "temperature":
        kelvin = temperature_to_kelvin(value, from_unit)
        return float(kelvin_to_temperature(kelvin, to_unit))
    # Длина или масса
    if from_group == "length":
        new_value = value * LENGTH[from_unit]
        result = new_value / LENGTH[to_unit]
    else:
        new_value = value * MASS[from_unit]
        result = new_value / MASS[to_unit]

    return float(result)
