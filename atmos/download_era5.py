# This script is intended to download ERA5 data from the Copernicus Climate Change Service (C3S) Climate Data Store (CDS).
# Currently only implemented for downloads of hourly data, grouped by day.

# Before running:
# 1. Install the required packages: `pip install cdsapi`
# 2. Create a CDS API key by signing up at https://cds.climate.copernicus.eu/api-how-to
# 3. Save the API key in a file named `.cdsapirc` in your home directory with the following format:
#    url: https://cds.climate.copernicus.eu/api/v2
#    key: <your_api_key>

# When running:
# 1. Create a yaml configuration file, see `download_era5_config.yaml` for an example.
# 2. Run the script with the following command:
# python download_era5.py -c download_yamls/era5_nz.yaml -s 20200101 -e 20200102 -o /Users/oriordem/datasets/ERA5/

# To do: fix duplication of logging.

import cdsapi
from argparse import ArgumentParser
from pathlib import Path
import yaml
import datetime 
import xarray as xr
import os
import time
import logging

# Set up logging
def setup_logging():
    """
    Set up logging configuration.
    """
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Clear all handlers attached to the 'cdsapi' logger
    cdsapi_logger = logging.getLogger("cdsapi")
    cdsapi_logger.handlers.clear()
    
    # Prevent the cdsapi logger from propagating its logs to the root logger
    cdsapi_logger.propagate = False
    
    logger = logging.getLogger(__name__)
    return logger

def get_commandline_args():
    """
    Parse command line arguments, return parser object.
    """
    parser = ArgumentParser(description="Download ERA5 data from the Copernicus Climate Data Store (CDS).")
    parser.add_argument(
        "-c", "--config", type=str, dest="config", default=None,
        help="Path to the configuration file containing the API key.",
    )
    parser.add_argument(
        "-s", "--start_date", type=str, dest="start_date", default=None,
        help="Start date for the data download in YYYYMMDD format.",
    )
    parser.add_argument(
        "-e", "--end_date", type=str, dest="end_date", default=None,
        help="End date for the data download in YYYYMMDD format.",
    )
    parser.add_argument(
        "-o", "--output", type=str, dest="output", default=None,
        help="Output directory for the downloaded data.",
    )
    parser.add_argument(
        "-p", "--parallel", action='store_true', dest="parallel", default=True,
        help="Use parallel downloading.",
    )
    return parser.parse_args()


def get_pressure_files(_times_dt: list, _cfg: dict):
    """
    Downloads pressure-level files from the ECMWF Climate Data Store (CDS) using the cdsapi.
    :param _times_dt: the list of dates and times to be downloaded.
    :param cfg: the dictionary of configuration settings.
    :return: None
    """
    dates_str = f'{_times_dt.strftime("%Y%m%d")}'
    times = [f'{i:02d}:00' for i in range(0, 24)]
    download_file = Path(_cfg['download_dir']) / 'pressure' / str(_times_dt.year) / str(_times_dt.month).zfill(2) / f'ERA5_{dates_str}_pressure.nc'
    # Create the directory if it doesn't exist
    download_file.parent.mkdir(parents=True, exist_ok=True)

    # Download the data
    c = cdsapi.Client()
    c.retrieve('reanalysis-era5-pressure-levels',
               {
                   'product_type':'reanalysis',
                   'format':'netcdf',
                   'pressure_level': _cfg['pressure_levels'],
                   'date': dates_str.replace('-', '/'),
                   'area':[_cfg['Nort'], _cfg['West'], _cfg['Sout'], _cfg['East']],
                   'time':times,
                   'variable':_cfg['pressure_var'],
               },
               download_file
               )
    
    logger.info(f"Downloaded pressure-level data for {dates_str} to {download_file}")

    # # Wait for the download to finish
    # while not download_file.is_file():
    #     time.sleep(30)

    # # Split files into daily files
    # logger.info(f"Splitting pressure-level data into daily files.")
    # ds = xr.open_dataset(download_file)
    # for day, daily_ds in ds.groupby('time.dt.floor("D")'):
    #     day = day.dt.strftime("%Y%m%d").values
    #     # Create the directory if it doesn't exist
    #     day_dir = Path(_cfg['download_dir']) / 'pressure' / str(day.year) / str(day.month)
    #     day_dir.mkdir(parents=True, exist_ok=True)
    #     # Save the daily file
    #     daily_ds.to_netcdf(f'{day_dir} / ERA5-{day}-pl.nc')
    #     daily_ds.close()
    # logger.info(f"Saved daily pressure-level data to {day_dir} / ERA5-{day}-pl.nc")
    # ds.close()
    # # Remove the original file
    # logger.info(f"Removing original pressure-level file: {download_file}")
    # os.remove(download_file)
    
def get_surface_files(_times_dt, _cfg):
    """
    Downloads surface-level files from the ECMWF Climate Data Store(CDS) using the cdsapi.
    : param _times_dt: the list of dates and times to be downloaded.
    : param cfg: the dictionary of configuration settings.
    : return: None
    """
    dates_str = f'{_times_dt.strftime("%Y%m%d")}'
    times = [f'{i:02d}:00' for i in range(0, 24)]
    download_file = Path(_cfg['download_dir']) / 'surface' / str(_times_dt.year) / str(_times_dt.month).zfill(2) / f'ERA5_{dates_str}_surface.nc'
    # Create the directory if it doesn't exist
    download_file.parent.mkdir(parents=True, exist_ok=True)

    # Download the data
    c = cdsapi.Client()
    c.retrieve('reanalysis-era5-single-levels',
               {
                   'product_type': 'reanalysis',
                   'format': 'netcdf',
                   'variable': _cfg['surface_var'],
                   'date': dates_str.replace('-', '/'),
                   'area': [_cfg['Nort'], _cfg['West'], _cfg['Sout'], _cfg['East']],
                   'time': times
               },
               download_file)
    logger.info(f"Downloaded surface-level data for {dates_str} to {download_file}")

    # Wait for the download to finish
    # while not download_file.is_file():
    #     time.sleep(30)

    # # Split files into daily files
    # logger.info(f"Splitting surface-level data into daily files.")
    # ds = xr.open_dataset(download_file)
    # for day, daily_ds in ds.groupby('time.dt.floor("D")'):
    #     day = day.dt.strftime("%Y%m%d").values
    #     # Create the directory if it doesn't exist
    #     day_dir = Path(_cfg['download_dir']) / 'surface' / str(day.year) / str(day.month)
    #     day_dir.mkdir(parents=True, exist_ok=True)
    #     # Save the daily file
    #     daily_ds.to_netcdf(f'{day_dir} / ERA5-{day}-sl.nc')
    #     daily_ds.close()
    # logger.info(f"Saved daily surface-level data to {day_dir} / ERA5-{day}-sl.nc")
    # ds.close()

    # # Remove the original file
    # logger.info(f"Removing original surface-level file {download_file}")
    # os.remove(download_file)



if __name__ == "__main__":
    # Set up logging
    logger = setup_logging()
    logger.info("Starting the ERA5 data download script.")

    # Get command line arguments
    args = get_commandline_args()
    config_path = Path(args.config)
    if not config_path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Load configuration file
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)

    # Create output directory if it doesn't exist
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Set the configuration settings
    cfg['download_dir'] = output_dir
    cfg['start_date'] = args.start_date
    cfg['end_date'] = args.end_date

    # Sort out the start and end times.
    times_dt = []
    start_dt = datetime.datetime.strptime(args.start_date, '%Y%m%d')
    end_dt = datetime.datetime.strptime(args.end_date, '%Y%m%d')
    assert end_dt >= start_dt, 'The end time needs to be after start time'
    new_dt = start_dt
    while new_dt <= end_dt:
        times_dt.append(new_dt)
        new_dt += datetime.timedelta(days=1)

    if not args.parallel:
        for day in times_dt:        
            logger.info(f"Downloading data for {day.strftime('%Y-%m-%d')}")

            # Download pressure-level files
            logger.info("Downloading pressure-level files.")
            get_pressure_files(day, cfg)

            # Download surface-level files
            logger.info("Downloading surface-level files.")
            get_surface_files(day, cfg)
    
    else:
        # Parallel downloads
        import concurrent.futures
        from tqdm import tqdm
        
        # Create a list of all tasks (each day produces 2 tasks)
        all_tasks = []
        for day in times_dt:
            all_tasks.append((get_pressure_files, day, cfg))
            all_tasks.append((get_surface_files, day, cfg))

        # Define your batch size (number of concurrent requests)
        batch_size = 10

        with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
            # Process tasks in batches
            for i in range(0, len(all_tasks), batch_size):
                batch = all_tasks[i : i + batch_size]
                futures = [
                    executor.submit(task, day, cfg)
                    for task, day, cfg in batch
                ]
                # Use tqdm to monitor progress of the current batch
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"Error downloading data: {e}")
    logger.info("All downloads completed.")

