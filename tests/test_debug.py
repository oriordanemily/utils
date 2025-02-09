import pytest
import numpy as np
import os
import matplotlib.pyplot as plt
from utils.python.debug import sns_plot_and_save, hist_plot_and_save, plt_plot_and_save

# Fixture to create temporary test data
@pytest.fixture
def test_data():
    return np.random.rand(10, 10)  # 10x10 random matrix for heatmap and imshow

@pytest.fixture
def test_data_flat():
    return np.random.rand(100)  # 1D random array for histogram

# Fixture to define a temporary file path
@pytest.fixture
def temp_file():
    path = "test_plot.png"
    yield path
    if os.path.exists(path):
        os.remove(path)

# Test sns_plot_and_save
def test_sns_plot_and_save(test_data, temp_file):
    sns_plot_and_save(test_data, path=temp_file)
    assert os.path.exists(temp_file), "Heatmap image was not saved"

# Test hist_plot_and_save
def test_hist_plot_and_save(test_data_flat, temp_file):
    hist_plot_and_save(test_data_flat, path=temp_file)
    assert os.path.exists(temp_file), "Histogram image was not saved"

# Test plt_plot_and_save
def test_plt_plot_and_save(test_data, temp_file):
    plt_plot_and_save(test_data, path=temp_file)
    assert os.path.exists(temp_file), "Imshow image was not saved"

# Remove the temporary file after all tests are done
def test_cleanup(temp_file):
    if os.path.exists(temp_file):
        os.remove(temp_file)
    assert not os.path.exists(temp_file), "Temporary file was not removed"