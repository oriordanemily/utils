import pytest
import xarray as xr
import numpy as np
import xesmf as xe
import pandas as pd
from utils.atmos.netcdf import (standardise_coords, 
                                interpolate_irregular_to_regular_grid)

# Define the test datasets
@pytest.fixture
def irregular_data():
    # Create a small irregular dataset for testing
    data = np.random.rand(1, 4, 5)
    coords = {
        'lat': [0, 1, 2, 3],
        'lon': [0, 1, 2, 3, 4],
        'time': pd.date_range('2023-01-01', periods=1)
    }
    ds = xr.Dataset({'var': (['time', 'lat', 'lon'], data)}, coords=coords)
    return ds

@pytest.fixture
def regular_data():
    # Create a regular grid dataset for testing
    data = np.random.rand(1, 5, 6)
    coords = {
        'latitude': np.linspace(0, 3, 5),
        'longitude': np.linspace(0, 4, 6),
        'time': pd.date_range('2023-01-01', periods=1)
    }
    ds = xr.Dataset({'var': (['time', 'latitude', 'longitude'], data)}, coords=coords)
    return ds

def test_standardise_coords(irregular_data):
    """Test the standardisation of coordinate names."""
    # Check that the coordinates are correctly renamed
    ds = irregular_data
    ds_standardised = standardise_coords(ds)

    # Check if the coordinate names are standardized
    assert 'latitude' in ds_standardised.coords, "latitude not found in coords"
    assert 'longitude' in ds_standardised.coords, "longitude not found in coords"
    assert 'time' in ds_standardised.coords, "time not found in coords"

    # Check if the original coordinate names have been replaced with the standard names
    assert 'lat' not in ds_standardised.coords, "lat found in coords"
    assert 'lon' not in ds_standardised.coords, "lon found in coords"
    assert 'xlat' not in ds_standardised.coords, "xlat found in coords"
    assert 'xlon' not in ds_standardised.coords, "xlon found in coords"

def test_interpolate_irregular_to_regular_grid(irregular_data, regular_data):
    """Test the interpolation of irregular to regular grid."""
    # Call the function to interpolate data
    regridded_data = interpolate_irregular_to_regular_grid(irregular_data, regular_data)

    # Check if the regridded data has the expected shape
    assert regridded_data['var'].values.shape == regular_data['var'].values.shape

    # Check if the coordinates of the output are aligned with the regular grid
    assert np.allclose(regridded_data.coords['latitude'].values, regular_data.coords['latitude'].values)
    assert np.allclose(regridded_data.coords['longitude'].values, regular_data.coords['longitude'].values)

    # Check if the regridded data has the correct variable name
    assert 'var' in regridded_data

    # Test if the regridder method is working properly with bilinear interpolation (default)
    # You can check the values to confirm interpolation, but generally it's harder to validate numerically
    # without specific known data. This test checks the shape and basic functionality.

