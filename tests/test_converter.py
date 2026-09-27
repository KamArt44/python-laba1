import pytest

from toolkit.converter import convert
from toolkit.errors import ToolkitError
def test_meters_to_centimeters() -> None:
    assert convert(1, "m", "cm") == 100.0

def test_kilometers_to_meters() -> None:
    assert convert(2.5, "km", "m") == 2500.0

def test_grams_to_kilograms() -> None:
    assert convert(500, "g", "kg") == 0.5


def test_kilograms_to_grams() -> None:
    assert convert(2, "kg", "g") == 2000.0


def test_millimeters_to_meters() -> None:
    assert convert(1000, "mm", "m") == 1.0


def test_case_insensitive_units() -> None:
    assert convert(2, "M", "CM") == 200.0


def test_celsius_to_kelvin() -> None:
    assert convert(0, "c", "k") == pytest.approx(273.15)


def test_kelvin_to_celsius() -> None:
    assert convert(273.15, "k", "c") == pytest.approx(0.0)


def test_fahrenheit_to_celsius() -> None:
    assert convert(32, "f", "c") == pytest.approx(0.0)


def test_same_unit() -> None:
    assert convert(25, "cm", "cm") == 25.0


# ---------- Негативные тесты ----------


def test_unknown_source_unit() -> None:
    with pytest.raises(ToolkitError):
        convert(1, "abc", "m")


def test_unknown_target_unit() -> None:
    with pytest.raises(ToolkitError):
        convert(1, "m", "abc")


def test_incompatible_units() -> None:
    with pytest.raises(ToolkitError):
        convert(1, "m", "kg")


def test_temperature_below_absolute_zero_celsius() -> None:
    with pytest.raises(ToolkitError):
        convert(-300, "c", "k")

def test_temperature_below_absolute_zero_kelvin() -> None:
    with pytest.raises(ToolkitError):
        convert(-1, "k", "c")
