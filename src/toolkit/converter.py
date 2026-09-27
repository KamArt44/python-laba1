from toolkit.errors import ToolkitError


length_units = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

mass_units = {
    "g": 0.001,
    "kg": 1.0,
}

temperature_units = {
    "c",
    "f",
    "k",
}


def _find_group(unit: str) -> str:
    """
    Определяет группу единицы измерения.
    """
    unit = unit.lower()

    if unit in length_units:
        return "length"

    if unit in mass_units:
        return "mass"

    if unit in temperature_units:
        return "temperature"

    raise ToolkitError(f"Неизвестная единица: {unit}")


def _temperature_to_kelvin(value: float, unit: str) -> float:
    """
    Переводит температуру в Кельвины.
    """
    if unit == "c":
        kelvin = value + 273.15

    elif unit == "f":
        kelvin = (value - 32) * 5 / 9 + 273.15

    else:
        kelvin = value

    if kelvin < 0:
        raise ToolkitError("Температура ниже абсолютного нуля")

    return kelvin


def _kelvin_to_temperature(value: float, unit: str) -> float:
    """
    Переводит температуру из Кельвинов в нужную единицу.
    """
    if unit == "c":
        return value - 273.15

    if unit == "f":
        return (value - 273.15) * 9 / 5 + 32

    return value


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Переводит значение из одной единицы измерения в другую.
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    from_group = _find_group(from_unit)
    to_group = _find_group(to_unit)

    if from_group != to_group:
        raise ToolkitError(
            f"Несовместимые единицы: {from_unit} и {to_unit}"
        )

    # Температура
    if from_group == "temperature":
        kelvin = _temperature_to_kelvin(value, from_unit)
        return float(_kelvin_to_temperature(kelvin, to_unit))

    # Длина или масса
    if from_group == "length":
        base_value = value * length_units[from_unit]
        result = base_value / length_units[to_unit]

    else:
        base_value = value * mass_units[from_unit]
        result = base_value / mass_units[to_unit]

    return float(result)
