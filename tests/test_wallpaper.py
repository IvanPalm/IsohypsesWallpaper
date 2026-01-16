import numpy as np
import pytest
from unittest.mock import patch

from isohypseswallpaper.wallpaper import generate_wallpaper


@pytest.fixture
def dummy_dem():
    """Create a small dummy DEM array for testing."""
    dem = np.linspace(0, 100, 100).reshape(10, 10)  # 10x10 DEM
    dem_meta = {}  # Metadata not used in this test
    return dem, dem_meta


@patch("matplotlib.pyplot.savefig")
def test_generate_wallpaper_basic(mock_savefig, dummy_dem):
    """Test that generate_wallpaper runs with hillshade and contours."""
    dem, dem_meta = dummy_dem
    output_path = "dummy_output.png"
    width_px, height_px = 200, 100

    generate_wallpaper(
        dem=dem,
        dem_meta=dem_meta,
        output_path=output_path,
        width_px=width_px,
        height_px=height_px,
        background_color="#111111",
        contour_color="white",
        contour_interval=10,
    )

    # Check savefig was called once
    mock_savefig.assert_called_once()
    args, kwargs = mock_savefig.call_args
    assert args[0] == output_path


@patch("matplotlib.pyplot.savefig")
def test_generate_wallpaper_no_contours(mock_savefig, dummy_dem):
    """Test that wallpaper generates correctly without contours."""
    dem, dem_meta = dummy_dem
    output_path = "dummy_output.png"

    generate_wallpaper(
        dem=dem,
        dem_meta=dem_meta,
        output_path=output_path,
        width_px=100,
        height_px=100,
        background_color="#222222",
        contour_color="white",
        contour_interval=None,  # No contours
    )

    mock_savefig.assert_called_once()
