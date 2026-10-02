#Постоянные величины

import operator

ALLOWED_CHARACTERS = set("0123456789+-*/(). ")
TOKEN_PATTERN = r"\d[\d.]*|\.[\d.]*|[()+\-*/]|\S"

DICT_ACTION = { "+": operator.add, "-": operator.sub, "/": operator.truediv, "*": operator.mul}
DICT_OPERATIONS = {"u-": 3, "u+": 3, "*": 2, "/": 2, "+": 1, "-": 1}
UNARY_OPERATIONS = {"u-", "u+"}

LENGTH = {"mm": 0.001, "cm": 0.01, "m": 1.0, "km": 1000.0}
MASS = {"g": 0.001, "kg": 1.0}
TEMPERATURE = {"c", "f", "k"}
CELSIUS = 273.15
FAHRENHEIT1 = 32.0
FAHRENHEIT2 = 5 / 9
ABSOLUTE_ZERO = {"c": -273.15, "f": -459.67, "k": 0.0}
