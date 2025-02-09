import xarray as xr
import xesmf as xe

coordinate_names = {
    'latitude': ['lat', 'latitude', 'xlat', 'xlat_u', 'xlat_v'],
    'longitude': ['lon', 'longitude', 'xlon', 'xlong', 'xlong_u', 'xlong_v' 'long'],
    'time': ['time', 'xtime'],
}

def standardise_coords(ds):
    """Standardises coordinate names in a dataset."""
    for coord in ds.coords:
        for key, _ in coordinate_names.items():
            if coord.lower() in coordinate_names[key]:
                ds = ds.rename({coord: key})
    return ds


def interpolate_irregular_to_regular_grid(irregular_data, regular_data, regrid_kwargs={}):
    """Interpolates irregularly spaced data to a regular grid.

    Args:
        irregular_data (xarray.Dataset): Dataset containing irregularly spaced data.
        regular_data (xarray.Dataset): Dataset containing regular grid data.
        regrid_kwargs (dict, optional): Keyword arguments for xe.Regridder. Defaults to {}. 
            Useful kwargs include:
                - method: what interpolation method to use.
                - filename: path to a file with weights, or where to save weights if the file does not exist.
                - reuse_weights: whether to reuse existing weights if they exist.
    Returns:
        xarray.Dataset: Dataset containing irregular data interpolated to a regular grid.
    """

    # Convert coordinates to standard names
    irregular_data = standardise_coords(irregular_data)
    regular_data = standardise_coords(regular_data)

    # Create regular target dataset
    target_ds = xr.Dataset({
    'latitude': regular_data['latitude'],
    'longitude': regular_data['longitude'],
    })

    # Create regridder
    if 'method' not in regrid_kwargs:
        regrid_kwargs['method'] = 'bilinear'
        
    regridder = xe.Regridder(irregular_data, target_ds, **regrid_kwargs)

    # Regrid the data
    regridded_data = regridder(irregular_data)

    return regridded_data

