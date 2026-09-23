from src.converter import meters_to_centimeters



def test_meters_to_centimeters() -> None:
    assert meters_to_centimeters(1.0) == 100.0
