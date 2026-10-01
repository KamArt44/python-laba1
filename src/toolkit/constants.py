"""Постоянные величины"""

import operator

ALLOWED_CHARACTERS = set("0123456789+-*/(). \t\n\r\v\f")
NUMBER_PATTERN = r"(?:\d+(?:\.\d*)?|\.\d+)"
TOKEN_PATTERN = r"\d[\d.]*|\.[\d.]*|\*\*|[()+\-*/]|\S"

DICT_ACTION = {
    "+": operator.add,
    "-": operator.sub,
    "/": operator.truediv,
    "*": operator.mul,
    "**": operator.pow,
}
DICT_OPERATIONS = {
    "**": 4,
    "u-": 3,
    "u+": 3,
    "*": 2,
    "/": 2,
    "+": 1,
    "-": 1,
}
UNARY_OPERATIONS = {"u-", "u+"}

# Коэффициенты.
LENGTH_UNITS = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
MASS_UNITS = {"g": 0.001, "kg": 1.0}
TEMPERATURE_UNITS = {"c", "f", "k"}

CELSIUS_OFFSET = 273.15
FAHRENHEIT_OFFSET = 32.0
FAHRENHEIT_SCALE = 5 / 9
ABSOLUTE_ZERO = {"c": -273.15, "f": -459.67, "k": 0.0}
