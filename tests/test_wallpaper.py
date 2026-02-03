# tests/test_wallpaper.py

import numpy as np
import pytest
from unittest.mock import patch

from isohypseswallpaper.wallpaper import generate_wallpaper


@pytest.fixture
def dummy_dem():
    dem = np.linspace(0, 100, 100).reshape(10, 10)
    return dem


@patch("isohypseswallpaper.wallpaper.metadata.write_metadata")
@patch("isohypseswallpaper.wallpaper.plt.savefig")
def test_generate_wallpaper_basic(mock_savefig, mock_write_metadata, dummy_dem):
    dem = dummy_dem
    output_path = "dummy_output.png"

    generate_wallpaper(
        dem_array=dem,
        lat=42.0,
        lon=12.0,
        zoom_level=12,
        width=200,
        height=100,
        contour_interval=10,
        contour_color="white",
        background_color="#111111",
        output_path=output_path,
    )

    mock_savefig.assert_called_once()
    mock_write_metadata.assert_called_once()


@patch("isohypseswallpaper.wallpaper.metadata.write_metadata")
@patch("isohypseswallpaper.wallpaper.plt.savefig")
def test_generate_wallpaper_no_contours(mock_savefig, mock_write_metadata, dummy_dem):
    dem = dummy_dem
    output_path = "dummy_output.png"

    generate_wallpaper(
        dem_array=dem,
        lat=42.0,
        lon=12.0,
        zoom_level=12,
        width=100,
        height=100,
        contour_interval=None,
        contour_color="white",
        background_color="#222222",
        output_path=output_path,
    )

    mock_savefig.assert_called_once()
    mock_write_metadata.assert_called_once()
