import pytest
from atmos.convert_units import (
    kelvin_to_celsius,
    celsius_to_kelvin,
    kelvin_to_fahrenheit,
    fahrenheit_to_kelvin,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius
)

# Test kelvin_to_celsius
def test_kelvin_to_celsius():
    assert kelvin_to_celsius(273.15) == 0
    assert kelvin_to_celsius(0) == -273.15
    assert kelvin_to_celsius(373.15) == 100

# Test celsius_to_kelvin
def test_celsius_to_kelvin():
    assert celsius_to_kelvin(0) == 273.15
    assert celsius_to_kelvin(-273.15) == 0
    assert celsius_to_kelvin(100) == 373.15

# Test kelvin_to_fahrenheit
def test_kelvin_to_fahrenheit():
    assert kelvin_to_fahrenheit(273.15) == 32
    assert kelvin_to_fahrenheit(0) == -459.67
    assert kelvin_to_fahrenheit(373.15) == 212

# Test fahrenheit_to_kelvin
def test_fahrenheit_to_kelvin():
    assert fahrenheit_to_kelvin(32) == pytest.approx(273.15, rel=1e-5)
    assert fahrenheit_to_kelvin(-459.67) == pytest.approx(0, rel=1e-5)
    assert fahrenheit_to_kelvin(212) == pytest.approx(373.15, rel=1e-5)

# Test celsius_to_fahrenheit
def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(-40) == -40  # Edge case
    assert celsius_to_fahrenheit(100) == 212

# Test fahrenheit_to_celsius
def test_fahrenheit_to_celsius():
    assert fahrenheit_to_celsius(32) == 0
    assert fahrenheit_to_celsius(-40) == -40  # Edge case
    assert fahrenheit_to_celsius(212) == 100

# Parameterized tests to reduce redundancy
@pytest.mark.parametrize("kelvin, celsius", [
    (273.15, 0),
    (0, -273.15),
    (373.15, 100),
])
def test_kelvin_celsius_conversion(kelvin, celsius):
    assert kelvin_to_celsius(kelvin) == celsius
    assert celsius_to_kelvin(celsius) == kelvin

@pytest.mark.parametrize("kelvin, fahrenheit", [
    (273.15, 32),
    (0, -459.67),
    (373.15, 212),
])
def test_kelvin_fahrenheit_conversion(kelvin, fahrenheit):
    assert kelvin_to_fahrenheit(kelvin) == pytest.approx(fahrenheit, rel=1e-5)
    assert fahrenheit_to_kelvin(fahrenheit) == pytest.approx(kelvin, rel=1e-5)
