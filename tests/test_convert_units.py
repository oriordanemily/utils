import pytest
from utils.atmos.convert_units import (
    kelvin_to_celsius,
    celsius_to_kelvin,
    kelvin_to_fahrenheit,
    fahrenheit_to_kelvin,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius
)

# Test kelvin_to_celsius
def test_kelvin_to_celsius():
    assert kelvin_to_celsius(273.15) == pytest.approx(0, rel=1e-5)
    assert kelvin_to_celsius(0) == pytest.approx(-273.15, rel=1e-5)
    assert kelvin_to_celsius(373.15) == pytest.approx(100, rel=1e-5)

# Test celsius_to_kelvin
def test_celsius_to_kelvin():
    assert celsius_to_kelvin(0) == pytest.approx(273.15, rel=1e-5)
    assert celsius_to_kelvin(-273.15) == pytest.approx(0, rel=1e-5)
    assert celsius_to_kelvin(100) == pytest.approx(373.15, rel=1e-5)

# Test kelvin_to_fahrenheit
def test_kelvin_to_fahrenheit():
    assert kelvin_to_fahrenheit(273.15) == pytest.approx(32, rel=1e-5)
    assert kelvin_to_fahrenheit(0) == pytest.approx(-459.67, rel=1e-5)
    assert kelvin_to_fahrenheit(373.15) == pytest.approx(212, rel=1e-5)

# Test fahrenheit_to_kelvin
def test_fahrenheit_to_kelvin():
    assert fahrenheit_to_kelvin(32) == pytest.approx(273.15, rel=1e-5)
    assert fahrenheit_to_kelvin(-459.67) == pytest.approx(0, rel=1e-5)
    assert fahrenheit_to_kelvin(212) == pytest.approx(373.15, rel=1e-5)

# Test celsius_to_fahrenheit
def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == pytest.approx(32, rel=1e-5)
    assert celsius_to_fahrenheit(-40) == pytest.approx(-40, rel=1e-5)  # Edge case
    assert celsius_to_fahrenheit(100) == pytest.approx(212, rel=1e-5)

# Test fahrenheit_to_celsius
def test_fahrenheit_to_celsius():
    assert fahrenheit_to_celsius(32) == pytest.approx(0, rel=1e-5)
    assert fahrenheit_to_celsius(-40) == pytest.approx(-40, rel=1e-5) # Edge case
    assert fahrenheit_to_celsius(212) == pytest.approx(100, rel=1e-5)

# Parameterized tests to reduce redundancy
@pytest.mark.parametrize("kelvin, celsius", [
    (273.15, 0),
    (0, -273.15),
    (373.15, 100),
])
def test_kelvin_celsius_conversion(kelvin, celsius):
    assert kelvin_to_celsius(kelvin) == pytest.approx(celsius, rel=1e-5)
    assert celsius_to_kelvin(celsius) == pytest.approx(kelvin, rel=1e-5)

@pytest.mark.parametrize("kelvin, fahrenheit", [
    (273.15, 32),
    (0, -459.67),
    (373.15, 212),
])
def test_kelvin_fahrenheit_conversion(kelvin, fahrenheit):
    assert kelvin_to_fahrenheit(kelvin) == pytest.approx(fahrenheit, rel=1e-5)
    assert fahrenheit_to_kelvin(fahrenheit) == pytest.approx(kelvin, rel=1e-5)
